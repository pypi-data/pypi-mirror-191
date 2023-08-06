import pdb
import warnings
import math
import torch
import random
import torch.nn as nn
import numpy as np
from collections import defaultdict

from mmcv.runner import auto_fp16
import torch.nn.functional as F
# from mmdet.core import bbox2result, bbox2roi, build_assigner, build_sampler
from ..builder import DETECTORS, build_backbone, build_head, build_neck
from .base_contrast import BaseContrastDetector
from mmdet.core import bbox2result_reid, bbox2roi
from mmdet.utils.smic import check_isnan_or_isinf

@DETECTORS.register_module()
class SingleTwoStageDetectorNAEContrast(BaseContrastDetector):
    """Base class for two-stage detectors.

    Two-stage detectors typically consisting of a region proposal network and a
    task-specific regression head.
    """

    def __init__(self,
                 backbone,
                 rpn_head,
                 roi_head,
                 predictor_head,
                 train_cfg,
                 test_cfg,
                 neck=None,
                 contrast_mode='gt_bbox',#['gt_bbox','bbox_pred','feat_map_point']
                 detection_data_randomerasing=dict(
                     probability=0,
                     sl=0.02, # Minimum proportion of erased area
                     sh=0.3, #Maximum proportion of erased area
                     r1=0.3, # Minimum aspect ratio of erased area.
                     min_bbox_area=0,
                     max_bboxes_num=100,
                     bbox_probability=1,
                     fill_value=0
                 ),
                 pretrained=None,
                 check_have_two_type_data=True):
        super(SingleTwoStageDetectorNAEContrast, self).__init__()
        self.contrast_mode =contrast_mode
        self.detection_data_randomerasing = detection_data_randomerasing
        self.check_have_two_type_data=check_have_two_type_data

        self.backbone = build_backbone(backbone)

        if neck is not None:
            self.neck = build_neck(neck)

        if rpn_head is not None:
            rpn_train_cfg = train_cfg.rpn if train_cfg is not None else None
            rpn_head_ = rpn_head.copy()
            rpn_head_.update(train_cfg=rpn_train_cfg, test_cfg=test_cfg.rpn)
            self.rpn_head = build_head(rpn_head_)

        if roi_head is not None:
            # update train and test cfg here for now
            # TODO: refactor assigner & sampler
            rcnn_train_cfg = train_cfg.rcnn if train_cfg is not None else None
            roi_head.update(train_cfg=rcnn_train_cfg)
            roi_head.update(test_cfg=test_cfg.rcnn)
            # roi_head.pretrained = pretrained
            self.roi_head = build_head(roi_head)

        # if bbox_head is not None:
        #     bbox_head.update(train_cfg=train_cfg)
        #     bbox_head.update(test_cfg=test_cfg)
        #     self.bbox_head = build_head(bbox_head)

        assert predictor_head is not None
        self.predictor_head = build_head(predictor_head)

        self.train_cfg = train_cfg
        self.test_cfg = test_cfg

        self.init_weights(pretrained=pretrained)


    @property
    def with_rpn(self):
        """bool: whether the detector has RPN"""
        return hasattr(self, 'rpn_head') and self.rpn_head is not None

    @property
    def with_roi_head(self):
        """bool: whether the detector has a RoI head"""
        return hasattr(self, 'roi_head') and self.roi_head is not None

    def init_weights(self, pretrained=None):
        """Initialize the weights in detector.

        Args:
            pretrained (str, optional): Path to pre-trained weights.
                Defaults to None.
        """
        super(SingleTwoStageDetectorNAEContrast, self).init_weights(pretrained)
        # pdb.set_trace()
        self.backbone.init_weights(pretrained=pretrained)
        if self.with_neck:
            if isinstance(self.neck, nn.Sequential):
                for m in self.neck:
                    m.init_weights()
            else:
                self.neck.init_weights()
        if self.with_rpn:
            self.rpn_head.init_weights()
        if self.with_roi_head:
            self.roi_head.init_weights(pretrained)
        # pdb.set_trace()
        # self.bbox_head.init_weights()
        self.predictor_head.init_weights()

    def extract_feat(self, img):
        """Directly extract features from the backbone+neck."""
        x = self.backbone(img)
        if self.with_neck:
            x = self.neck(x)
        return x

    def forward_dummy(self, img):
        """Used for computing network flops.

        See `mmdetection/tools/analysis_tools/get_flops.py`
        """
        outs = ()
        # backbone
        x = self.extract_feat(img)
        # rpn
        if self.with_rpn:
            rpn_outs = self.rpn_head(x)
            outs = outs + (rpn_outs,)
        proposals = torch.randn(1000, 4).to(img.device)
        # roi_head
        roi_outs = self.roi_head.forward_dummy(x, proposals)
        outs = outs + (roi_outs,)
        return outs

    @auto_fp16(apply_to=('img',))
    def encoder(self,
               img,
               img_metas,
               gt_bboxes,
               gt_labels,
               gt_ids,
               gt_bboxes_ignore=None,
               gt_masks=None,
               proposals=None,
               **kwargs):
        if check_isnan_or_isinf(img):
            pdb.set_trace()

        xb = self.extract_feat(img)
        # print("=====here", xb.shape)
        # print("===={}".format(img_metas))
        # pdb.set_trace()
        img_types=[]
        # pdb.set_trace()
        for img_meta in img_metas:
            img_types.append(img_meta['data_type'])
        # 当既有reid又有det时，打开下面的作为检查

        if self.check_have_two_type_data:
            condition='re_id' in img_types and 'detection' in img_types
            if not condition:
                print(img_metas)
                pdb.set_trace()
                assert 'there are only {} images!!!'.format(img_types[0])
        if xb[0].isnan().nonzero().shape[0] != 0 or img.isnan().nonzero().shape[0] != 0:
            pdb.set_trace()

        bs = xb[0].shape[0]
        losses = dict()

        reid_data_id = []
        det_data_id = []
        for ind, img_meta in enumerate(img_metas):
            data_type = img_meta['data_type']
            if data_type == 're_id':
                reid_data_id.append(ind)
            else:
                det_data_id.append(ind)

            # pdb.set_trace()
            # img_name=img_meta['ori_filename'].replace('/','_')
            # import cv2
            # import os.path as osp
            # # pdb.set_trace()
            # # [103.530, 116.280, 123.675]
            # probe_img = img[ind].permute([1, 2, 0]).cpu().numpy()  # c,h,w->h,w,c
            # probe_img[:,:,0]+=103.530
            # probe_img[:, :, 1] += 116.280
            # probe_img[:, :, 2] += 123.675
            # probe_img = cv2.UMat(probe_img).get()
            # # pdb.set_trace()
            # gt_bb= gt_bboxes[ind].cpu().numpy()
            # for bb in gt_bb:
            #     bboxes = list(map(int,bb))
            #
            #     cv2.rectangle(probe_img, (bboxes[0], bboxes[1]), (bboxes[2], bboxes[3]),
            #                   color=(255, 0, 0),
            #                   thickness=2)
            # # pdb.set_trace()
            # cv2.imwrite(osp.join('/tianyanling',img_name), probe_img)



        # pdb.set_trace()
        # RPN forward and loss
        roi_losses_det = None
        feats_pids_roi=None
        return_rois=None
        xb_det=None
        if self.with_rpn and len(det_data_id) > 0:
            # pdb.set_trace()
            # rpn_outs = self.rpn_head(xb)
            xb_det = (xb[0][det_data_id],)  # tensor
            rpn_outs = self.rpn_head(xb_det)

            gt_bboxes_det = [gt_bboxes[ind] for ind in det_data_id]  # list
            img_metas_det = [img_metas[ind] for ind in det_data_id]  # list
            gt_labels_det = [gt_labels[ind] for ind in det_data_id]  # list
            gt_ids_det = [gt_ids[ind] for ind in det_data_id]  # list
            # rpn_loss_inputs = rpn_outs + (gt_bboxes, img_metas)
            rpn_loss_inputs = rpn_outs + (gt_bboxes_det, img_metas_det)
            gt_bboxes_ignore_det = [gt_bboxes_ignore[ind] for ind in det_data_id]  # list
            # rpn_losses ['loss_rpn_cls', 'loss_rpn_bbox']
            rpn_losses = self.rpn_head.loss(*rpn_loss_inputs, gt_bboxes_ignore=gt_bboxes_ignore_det)
            losses.update(rpn_losses)

            proposal_cfg = self.train_cfg.get("rpn_proposal", self.test_cfg.rpn)
            proposal_list_det = self.rpn_head.get_bboxes(*rpn_outs, img_metas_det, cfg=proposal_cfg)

            roi_losses_det, bbox_pred = self.roi_head.forward_train(xb_det, img_metas_det, proposal_list_det,
                                                                     gt_bboxes_det, gt_labels_det, gt_ids_det,
                                                                     gt_bboxes_ignore_det, gt_masks,
                                                                     **kwargs)
            if self.contrast_mode == 'gt_bbox':
                # fetch features with gt_bboxes to do contrastive learning
                return_rois = gt_bboxes_det
            elif self.contrast_mode == 'bbox_pred':
                return_rois = bbox_pred
            else:
                return_rois = None

        # else:
        #     proposal_list = proposals
        # pdb.set_trace()
        roi_losses_reid = None
        if len(reid_data_id) > 0:  # mask sure proposal_list is wrt ori images???
            xb_reid = (xb[0][reid_data_id],)
            gt_bboxes_reid = [gt_bboxes[ind] for ind in reid_data_id]  # list
            img_metas_reid = [img_metas[ind] for ind in reid_data_id]  # list
            gt_labels_reid = [gt_labels[ind] for ind in reid_data_id]  # list
            gt_ids_reid = [gt_ids[ind] for ind in reid_data_id]  # list
            gt_bboxes_ignore_reid = [gt_bboxes_ignore[ind] for ind in reid_data_id]  # list
            proposal_list_reid = [gt_bbox for i, gt_bbox in enumerate(gt_bboxes) if i in reid_data_id]
            # roi_losses_reid, _ = self.roi_head.forward_train(xb_reid, img_metas_reid, proposal_list_reid,
            #                                                          gt_bboxes_reid, gt_labels_reid, gt_ids_reid,
            #                                                          gt_bboxes_ignore_reid, gt_masks,
            #                                                          **kwargs)
            rois = bbox2roi(gt_bboxes_reid)
            bbox_results = self.roi_head._bbox_forward(xb_reid, rois)
            roi_losses_reid = self.roi_head.bbox_head.loss(None, None, bbox_results["feature"], None,
                                                           torch.cat(gt_ids_reid),
                                                           None, None, None, None)


        
        if roi_losses_reid is not None:
            losses['loss_oim'] = roi_losses_reid['loss_oim']
            # losses['loss_cls'] = roi_losses_det['loss_cls']
            # losses['loss_bbox'] = roi_losses_det['loss_bbox']

            if math.isnan(roi_losses_reid['loss_oim']):
                pdb.set_trace()
        if roi_losses_det is not None:
            losses['loss_cls'] = roi_losses_det['loss_cls']
            losses['loss_bbox'] = roi_losses_det['loss_bbox']

            if math.isnan(roi_losses_det['loss_cls']):
                pdb.set_trace()

        if check_isnan_or_isinf(losses):
            pdb.set_trace()
        # loss_names=['loss_oim','loss_rpn_cls','loss_rpn_bbox','loss_cls','loss_bbox']
        # # print(losses)
        # for name in loss_names:
        #     # if name in ['loss_rpn_cls','loss_rpn_bbox']:
        #     if name not in losses.keys():
        #         if name in ['loss_rpn_cls','loss_rpn_bbox']:
        #             losses[name] = [torch.zeros([],device=img.device)]
        #         else:
        #             losses[name] = torch.zeros([], device=img.device)


        # print("losses={}".format(losses))
        # pdb.set_trace()
        detection_data_randomerasing_condition = self.detection_data_randomerasing['probability'] >= random.uniform(0,
                                                                                                                    1) \
                                                 and len(return_rois) < self.detection_data_randomerasing[
                                                     'max_bboxes_num']
        xb_det_feat = xb_det
        if return_rois is not None and xb_det is not None:

            if detection_data_randomerasing_condition:
                stride=16###
                sl = self.detection_data_randomerasing['sl']
                sh = self.detection_data_randomerasing['sh']
                r1 = self.detection_data_randomerasing['r1']
                # pdb.set_trace()
                det_features_list = []
                for index, det_img_ori in enumerate(xb_det[0]): #xb_det[0] [2, 1024, 94, 92]
                    det_img=det_img_ori.clone()
                    for roi in return_rois[index]/stride:
                        bbox_h = roi[3] - roi[1]
                        bbox_w = roi[2] - roi[0]
                        area = bbox_h * bbox_w
                        if area < self.detection_data_randomerasing['min_bbox_area']:
                            continue
                        if random.uniform(0, 1) > self.detection_data_randomerasing['bbox_probability']:
                            continue
                        target_area = random.uniform(sl, sh) * area
                        aspect_ratio = random.uniform(r1, 1 / r1)

                        h = int(round(math.sqrt(target_area * aspect_ratio)))
                        w = int(round(math.sqrt(target_area / aspect_ratio)))

                        if w < bbox_w and h < bbox_h:
                            y1 = random.randint(0, int(bbox_h - h))
                            x1 = random.randint(0, int(bbox_w - w))
                            x1 = x1 + int(roi[0])
                            y1 = y1 + int(roi[1])
                            det_img[:,y1: y1 + h, x1: x1 + w]= 0
                    det_features_list.append(det_img)

                xb_det_feat = (torch.stack(det_features_list),)#tuple must have ,

        # pdb.set_trace()
        return return_rois, losses, xb_det_feat


    # def forward_train(self,
    #                   img,
    #                   img_metas,
    #                   gt_bboxes,
    #                   gt_labels,
    #                   gt_ids,
    #                   gt_bboxes_ignore=None,
    #                   gt_masks=None,
    #                   proposals=None,
    #                   **kwargs):
    def forward_train(self, data):
        """
        Args:
            img (Tensor): of shape (N, C, H, W) encoding input images.
                Typically these should be mean centered and std scaled.

            img_metas (list[dict]): list of image info dict where each dict
                has: 'img_shape', 'scale_factor', 'flip', and may also contain
                'filename', 'ori_shape', 'pad_shape', and 'img_norm_cfg'.
                For details on the values of these keys see
                `mmdet/datasets/pipelines/formatting.py:Collect`.

            gt_bboxes (list[Tensor]): Ground truth bboxes for each image with
                shape (num_gts, 4) in [tl_x, tl_y, br_x, br_y] format.

            gt_labels (list[Tensor]): class indices corresponding to each box

            gt_bboxes_ignore (None | list[Tensor]): specify which bounding
                boxes can be ignored when computing the loss.

            gt_masks (None | Tensor) : true segmentation masks for each box
                used if the architecture supports a segmentation task.

            proposals : override rpn proposals with custom proposals. Use when
                `with_rpn` is False.

        Returns:
            dict[str, Tensor]: a dictionary of loss components
        """
        ######!!!!NAE mode: can train
        # 1. person search and
        # 2. reid only and
        # 3. detection only (because pid=-1 when detecion dataset,
        # and pid=pid-1=-2 in oim_loss, background pid=-1, valid index:inds = roi_label >= -1 and ignore -1)
        # ==>oim_loss=0. However, test is not rewriten. So do not use this model when detection task only.

        assert len(data)==2
        data1, data2 = data[0], data[1]

        losses = dict()
        rois_1, loss_1, xb_det1 = self.encoder(**data1)  # NxC
        rois_2, loss_2, xb_det2 = self.encoder(**data2)  # NxC
        # pdb.set_trace()
        losses_1 =dict()
        for key, val in loss_1.items():
            k= key + '_1'
            losses_1[k]=val
        losses.update(losses_1)
        losses.update(loss_2)

        # pdb.set_trace()
        # losses.update(single_losses)
        # for key, val in single_losses.items():
        #     if key in losses:
        #         # pdb.set_trace()
        #         #print("losses", key, losses[key], losses[key].shape)
        #         #print("val", val, val.shape)
        #         losses[key] += val
        #     else:
        #         losses[key] = val
        if rois_1 is not None and rois_2 is not None:
            # pdb.set_trace()
            if self.contrast_mode == 'gt_bbox':
                # fetch features with gt_bboxes to do contrastive learning
                rois = bbox2roi(rois_1)
                if check_isnan_or_isinf(xb_det1):
                    print("!!!!!!xb_det1")
                if check_isnan_or_isinf(rois):
                    print("!!!!!!rois")
                bbox_results = self.roi_head._bbox_forward(xb_det1, rois)
                z1 = bbox_results['feature']
                rois_2 = bbox2roi(rois_2)
                if check_isnan_or_isinf(xb_det2):
                    print("!!!!!!xb_det2")
                if check_isnan_or_isinf(rois_2):
                    print("!!!!!!rois_2")
                bbox_results_2 = self.roi_head._bbox_forward(xb_det2, rois_2)
                z2 = bbox_results_2['feature']
            elif self.contrast_mode == 'bbox_pred':
                z1, z2 = None, None
            else:
                z1, z2 = None, None
            # pdb.set_trace()
        # if z1 is not None and z2 is not None:
        #     print(z1)
        #     print(z2)
            loss_contrast = 0.5 * (self.predictor_head(z1, z2)['loss'] + self.predictor_head(z2, z1)['loss'])
            losses['contrast'] = loss_contrast
        else:
            assert 'Input of loss_constrast z1,z2 is None!!!'
        #     losses['contrast'] = torch.zeros([], device=data1['img'].device)
        # pdb.set_trace()
        # print('final_losses={}'.format(losses))
        return losses

    def simple_test(self, img, img_metas,
                    gt_bboxes=None,
                    gt_labels=None,
                    gt_ids=None,
                    gt_bboxes_ignore=None,
                    gt_masks=None,
                    proposals=None,
                    rescale=False,
                    query_mode=False,
                    **kwargs):
        """Test without augmentation."""
        assert self.with_bbox, 'Bbox head must be implemented.'

        xb = self.extract_feat(img)

        proposal_list = self.rpn_head.simple_test_rpn(xb, img_metas)
        use_rpn = True

        reid_mode=False
        if img_metas[0]['data_type'] == 're_id':
            reid_mode=True
            # pass

        # use_rpn: use proporals that generated from nae branch, not Alignps branch
        # use_rpn: only return features, not (det_box,score,feat)
        if query_mode or reid_mode:
            use_rpn = False
            # pdb.set_trace()
            proposal_list = [gt_bboxes[0]] #x1,y1,x2,y2 proposal is in original image???

        #(tl_x, tl_y, br_x, br_y, score)
        bbox_results_b = self.roi_head.simple_test(
            xb, proposal_list, img_metas, rescale=rescale,
            use_rpn=use_rpn)


        # if query_mode:#if bbox_results_b (n,260),260=4+256 4means gt_bboxes that is after augmentation, which is different from inference in test_results.py
        #     bboxes = gt_bboxes[0].cpu().numpy()
        #     reid_feats = bbox_results_b.cpu().numpy()
        #     # pdb.set_trace()
        #     bbox_results_b = np.concatenate((bboxes, reid_feats), axis=1)
        if query_mode or reid_mode:
            bbox_results_b = bbox_results_b.cpu().numpy()

        return bbox_results_b

    def aug_test(self, imgs, img_metas, rescale=False):
        """Test with augmentations.

        If rescale is False, then returned bboxes and masks will fit the scale
        of imgs[0].
        """
        # recompute feats to save memory
        x = self.extract_feats(imgs)
        proposal_list = self.rpn_head.aug_test_rpn(x, img_metas)
        return self.roi_head.aug_test(
            x, proposal_list, img_metas, rescale=rescale)

