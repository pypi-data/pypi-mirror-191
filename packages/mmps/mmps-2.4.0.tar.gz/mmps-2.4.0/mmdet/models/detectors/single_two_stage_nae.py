import pdb
import warnings

import torch
import torch.nn as nn
import numpy as np
from collections import defaultdict

import torch.nn.functional as F
# from mmdet.core import bbox2result, bbox2roi, build_assigner, build_sampler
from ..builder import DETECTORS, build_backbone, build_head, build_neck
from .base import BaseDetector
from mmdet.core import bbox2result_reid


@DETECTORS.register_module()
class SingleTwoStageDetectorNAE(BaseDetector):
    """Base class for two-stage detectors.

    Two-stage detectors typically consisting of a region proposal network and a
    task-specific regression head.
    """

    def __init__(self,
                 backbone,
                 rpn_head,
                 roi_head,
                 train_cfg,
                 test_cfg,
                 neck=None,
                 pretrained=None):
        super(SingleTwoStageDetectorNAE, self).__init__()

        # pdb.set_trace()
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
        # pdb.set_trace()
        super(SingleTwoStageDetectorNAE, self).init_weights(pretrained)
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
            # pdb.set_trace()
            self.roi_head.init_weights(pretrained)
        # self.bbox_head.init_weights()

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

    def forward_train(self,
                      img,
                      img_metas,
                      gt_bboxes,
                      gt_labels,
                      gt_ids,
                      gt_bboxes_ignore=None,
                      gt_masks=None,
                      proposals=None,
                      **kwargs):
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
        ###### !!!!NAE mode: can train
        # 1. person search and
        # 2.detection only (because pid=-1 when detecion dataset,
        # and pid=pid-1=-2 in oim_loss, background pid=-1, valid index:inds = roi_label >= -1 and ignore -1)
        # ==>oim_loss=0.

        # pdb.set_trace()
        xb = self.extract_feat(img)
        #print("here", xb.shape)
        # bs = xb[0].shape[0]
        losses = dict()


        # RPN forward and loss
        if self.with_rpn:
            rpn_outs = self.rpn_head(xb)
            rpn_loss_inputs = rpn_outs + (gt_bboxes, img_metas)
            #rpn_losses ['loss_rpn_cls', 'loss_rpn_bbox']
            rpn_losses = self.rpn_head.loss(*rpn_loss_inputs, gt_bboxes_ignore=gt_bboxes_ignore)
            losses.update(rpn_losses)

            proposal_cfg = self.train_cfg.get("rpn_proposal", self.test_cfg.rpn)
            proposal_list = self.rpn_head.get_bboxes(*rpn_outs, img_metas, cfg=proposal_cfg)
        else:
            proposal_list = proposals


        # pdb.set_trace()
        #roi_losses (['loss_bbox', 'loss_cls', 'loss_oim'])
        roi_losses, feats_pids_roi = self.roi_head.forward_train(xb, img_metas, proposal_list,
                                                 gt_bboxes, gt_labels, gt_ids,
                                                 gt_bboxes_ignore, gt_masks,
                                                 **kwargs)
        losses.update(roi_losses)
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
        # use_rpn: use proporals that generated from nae branch, not Alignps branch
        # use_rpn: only return features, not (det_box,score,feat)
        # pdb.set_trace()
        if query_mode:
            use_rpn = False
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
        if query_mode:
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

