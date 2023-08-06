import pdb
import warnings

import torch
import torch.nn as nn
from mmcv.runner import auto_fp16

from mmdet.utils.smic import check_isnan_or_isinf
from mmdet.core import bbox2result_reid
from .base import BaseDetector
from . import BaseContrastDetector
from ..builder import DETECTORS, build_backbone, build_head, build_neck


@DETECTORS.register_module()
class SingleStageReidDetectorContrast(BaseContrastDetector):
    """Base class for single-stage detectors.

    Single-stage detectors directly and densely predict bounding boxes on the
    output features of the backbone+neck.
    """

    def __init__(self,
                 backbone,
                 predictor_head,
                 neck=None,
                 bbox_head=None,
                 contrast_mode='gt_bbox',  # ['gt_bbox','bbox_pred','feat_map_point']
                 detection_data_randomerasing=dict(
                     probability=0,
                     sl=0.02,  # Minimum proportion of erased area
                     sh=0.3,  # Maximum proportion of erased area
                     r1=0.3,  # Minimum aspect ratio of erased area.
                     min_bbox_area=0,
                     max_bboxes_num=100,
                     bbox_probability=1,
                     fill_value=0
                 ),
                 train_cfg=None,
                 test_cfg=None,
                 pretrained=None):
        super(SingleStageReidDetectorContrast, self).__init__(
        )
        self.contrast_mode = contrast_mode
        self.detection_data_randomerasing = detection_data_randomerasing

        self.backbone = build_backbone(backbone)
        if neck is not None:
            self.neck = build_neck(neck)
        bbox_head.update(train_cfg=train_cfg)
        bbox_head.update(test_cfg=test_cfg)
        self.bbox_head = build_head(bbox_head)
        self.train_cfg = train_cfg
        self.test_cfg = test_cfg
        self.init_weights(pretrained=pretrained)
        assert predictor_head is not None
        self.predictor_head = build_head(predictor_head)

    def init_weights(self, pretrained=None):
        """Initialize the weights in detector.

        Args:
            pretrained (str, optional): Path to pre-trained weights.
                Defaults to None.
        """
        super(SingleStageReidDetectorContrast, self).init_weights(pretrained)
        self.backbone.init_weights(pretrained=pretrained)
        if self.with_neck:
            if isinstance(self.neck, nn.Sequential):
                for m in self.neck:
                    m.init_weights()
            else:
                self.neck.init_weights()
        self.bbox_head.init_weights()

    def extract_feat(self, img):
        """Directly extract features from the backbone+neck."""
        x = self.backbone(img)
        if self.with_neck:
            x = self.neck(x)
        return x

    def forward_dummy(self, img):
        """Used for computing network flops.

        See `mmdetection/tools/get_flops.py`
        """
        x = self.extract_feat(img)
        outs = self.bbox_head(x)
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
        x = self.extract_feat(img)  # type=tuple, len(x)=5 means lvl x[0].shape=[2, 256, 188, 184]
        # pdb.set_trace()
        img_types = []
        for img_meta in img_metas:
            img_types.append(img_meta['data_type'])
        # 当既有reid又有det时，打开下面的作为检查
        dist = True
        # dist = False
        condition = 're_id' in img_types and 'detection' in img_types or not dist
        if not condition:
            print(img_metas)
            pdb.set_trace()
            assert 'there are only {} images!!!'.format(img_types[0])

        losses = dict()

        reid_data_id = []
        det_data_id = []
        for ind, img_meta in enumerate(img_metas):
            data_type = img_meta['data_type']
            if data_type == 're_id':
                reid_data_id.append(ind)
            else:
                det_data_id.append(ind)

        return_rois = None
        det_data_losses = None
        x_data_det = None
        if len(det_data_id) > 0:
            x_data_det = tuple([x_feat[det_data_id] for x_feat in x])
            gt_bboxes_det = [gt_bboxes[ind] for ind in det_data_id]  # list
            img_metas_det = [img_metas[ind] for ind in det_data_id]  # list
            gt_labels_det = [gt_labels[ind] for ind in det_data_id]  # list
            gt_ids_det = [gt_ids[ind] for ind in det_data_id]  # list
            gt_bboxes_ignore_det = [gt_bboxes_ignore[ind] for ind in det_data_id]  # list
            det_data_losses = self.bbox_head.forward_train(x_data_det, img_metas_det,
                                                           gt_bboxes_det,
                                                           gt_labels_det, gt_ids_det,
                                                           gt_bboxes_ignore_det)
            # losses.update(det_data_losses)
            if self.contrast_mode == 'gt_bbox':
                # fetch features with gt_bboxes to do contrastive learning
                return_rois = gt_bboxes_det
            elif self.contrast_mode == 'bbox_pred':
                return_rois = None
            else:
                return_rois = None

        reid_data_losses = None
        if len(reid_data_id) > 0:
            x_data_reid = tuple([x_feat[reid_data_id] for x_feat in x])
            gt_bboxes_reid = [gt_bboxes[ind] for ind in reid_data_id]  # list
            img_metas_reid = [img_metas[ind] for ind in reid_data_id]  # list
            gt_labels_reid = [gt_labels[ind] for ind in reid_data_id]  # list
            gt_ids_reid = [gt_ids[ind] for ind in reid_data_id]  # list
            gt_bboxes_ignore_reid = [gt_bboxes_ignore[ind] for ind in reid_data_id]  # list
            reid_data_losses = self.bbox_head.forward_train(x_data_reid, img_metas_reid,
                                                            gt_bboxes_reid,
                                                            gt_labels_reid, gt_ids_reid,
                                                            gt_bboxes_ignore_reid)
        # ['loss_cls', 'loss_bbox', 'loss_centerness', 'loss_oim', 'loss_tri']
        if reid_data_losses is not None:
            # pdb.set_trace()
            reid_losses = ['loss_oim', 'loss_tri']
            for key in reid_data_losses.keys():
                if key in reid_losses:
                    losses[key] = reid_data_losses[key]

        if det_data_losses is not None:
            # pdb.set_trace()
            det_losses = ['loss_cls', 'loss_bbox', 'loss_centerness']
            for key in det_data_losses.keys():
                if key in det_losses:
                    losses[key] = det_data_losses[key]

        # losses = self.bbox_head.forward_train(x, img_metas, gt_bboxes,
        #                                       gt_labels, gt_ids, gt_bboxes_ignore)

        return return_rois, losses, x_data_det

    # def forward_train(self,
    #                   img,
    #                   img_metas,
    #                   gt_bboxes,
    #                   gt_labels,
    #                   gt_ids,
    #                   gt_bboxes_ignore=None):
    def forward_train(self, data):

        assert len(data) == 2
        data1, data2 = data[0], data[1]

        losses = dict()
        rois_1, loss_1, xb_det1 = self.encoder(**data1)  # NxC
        rois_2, loss_2, xb_det2 = self.encoder(**data2)  # NxC
        # pdb.set_trace()
        losses_1 = dict()
        for key, val in loss_1.items():
            k = key + '_1'
            losses_1[k] = val
        losses.update(losses_1)
        losses.update(loss_2)

        if rois_1 is not None and rois_2 is not None:
            # pdb.set_trace()
            if self.contrast_mode == 'gt_bbox':
                z1 = self.bbox_head.get_center_feature_p3(xb_det1, rois_1)
                z2 = self.bbox_head.get_center_feature_p3(xb_det2, rois_2)
            elif self.contrast_mode == 'bbox_pred':
                z1, z2 = None, None
            else:
                z1, z2 = None, None
            loss_contrast = 0.5 * (self.predictor_head(z1, z2)['loss'] + self.predictor_head(z2, z1)['loss'])
            losses['contrast'] = loss_contrast
        else:
            assert 'Input of loss_constrast z1,z2 is None!!!'

        return losses

    def simple_test(self, img, img_metas, proposals=None, rescale=False):
        """Test function without test time augmentation.

        Args:
            imgs (list[torch.Tensor]): List of multiple images
            img_metas (list[dict]): List of image information.
            rescale (bool, optional): Whether to rescale the results.
                Defaults to False.

        Returns:
            list[list[np.ndarray]]: BBox results of each image and classes.
                The outer list corresponds to each image. The inner list
                corresponds to each class.
        """
        x = self.extract_feat(img)
        outs = self.bbox_head(x, proposals)

        # print(type(img_metas), img_metas)
        bbox_list = self.bbox_head.get_bboxes(
            *outs, img_metas, rescale=rescale)
        # skip post-processing when exporting to ONNX
        if torch.onnx.is_in_onnx_export():
            return bbox_list

        bbox_results = [
            bbox2result_reid(det_bboxes, det_labels, reid_feats, self.bbox_head.num_classes)
            for det_bboxes, det_labels, reid_feats in bbox_list
        ]
        return bbox_results

    def aug_test(self, imgs, img_metas, rescale=False):
        """Test function with test time augmentation."""
        raise NotImplementedError
