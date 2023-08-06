from mmdet.core import bbox2result, bbox2roi, bbox2result_reid
from mmdet.models.builder import HEADS
from mmdet.models.roi_heads.standard_roi_head import StandardRoIHead

import torch
from torch import nn
import torch.nn.functional as F
import pdb

@HEADS.register_module()
class PersonSearchRoIHead2Input1NAE(StandardRoIHead):
    def __init__(self, **kwargs):
        super(PersonSearchRoIHead2Input1NAE,self).__init__(**kwargs)
        # pdb.set_trace()
        if self.training and kwargs['train_cfg'] is not None:
            self.add_gt_as_propsals_config=kwargs['train_cfg']['sampler']['add_gt_as_proposals']


    def forward_train(
        self,
        x,
        img_metas,
        proposal_list,
        gt_bboxes,
        gt_labels,
        gt_pids,
        gt_bboxes_ignore=None,
        gt_masks=None,
        da_alignment=False,
        gt_domains=None
    ):
        # assign gts and sample proposals
        if self.with_bbox or self.with_mask:
            num_imgs = len(img_metas)
            if gt_bboxes_ignore is None:
                gt_bboxes_ignore = [None for _ in range(num_imgs)]
            sampling_results = []
            # pdb.set_trace()
            self.bbox_sampler.add_gt_as_proposals=self.add_gt_as_propsals_config
            if da_alignment:
                self.bbox_sampler.add_gt_as_proposals=False

            for i in range(num_imgs):
                assign_result = self.bbox_assigner.assign(
                    proposal_list[i], gt_bboxes[i], gt_bboxes_ignore[i], gt_labels[i]
                )
                sampling_result = self.bbox_sampler.sample(
                    assign_result,
                    proposal_list[i],
                    gt_bboxes[i],
                    gt_labels[i],
                    feats=[lvl_feat[i][None] for lvl_feat in x],
                )
                sampling_results.append(sampling_result)

        if x[0].isnan().nonzero().shape[0] != 0:
            pdb.set_trace()
        losses = dict()
        feats_pids = dict()
        # bbox head forward and loss
        if self.with_bbox:
            bbox_results = self._bbox_forward_train(
                x, sampling_results, gt_bboxes, gt_labels, gt_pids, img_metas,
                gt_domains=gt_domains
            )
            losses.update(bbox_results["loss_bbox"])
            feats_pids['bbox_feats'] = bbox_results["feature"]#reid feature 256d
            feats_pids['gt_pids'] = bbox_results["gt_pids"]
            feats_pids['bbox_pred'] = bbox_results["bbox_pred"]#[256,4]
            feats_pids['bbox_feats_2048'] = bbox_results["bbox_feats"]  # bbox feature 2048d(after res5)
            feats_pids['ins_domains'] = bbox_results["ins_domains"]

        # mask head forward and loss
        if self.with_mask:
            mask_results = self._mask_forward_train(
                x, sampling_results, bbox_results["bbox_feats"], gt_masks, img_metas
            )
            # TODO: Support empty tensor input. #2280
            if mask_results["loss_mask"] is not None:
                losses.update(mask_results["loss_mask"])

        return losses, feats_pids
        # return losses, feats_pids, bbox_results['bbox_pred']#做contrastive learning, if self.contrast_mode == 'bbox_pred'

    def _bbox_forward(self, x, rois,gt_domains=None):
        # TODO: a more flexible way to decide which feature maps to use
        # pdb.set_trace()
        bbox_feats = self.bbox_roi_extractor(x[: self.bbox_roi_extractor.num_inputs], rois)
        bbox_feats1 = F.adaptive_max_pool2d(bbox_feats, 1)# res4 1024
        if self.with_shared_head:
            bbox_feats = self.shared_head(bbox_feats)
            bbox_feats = F.adaptive_max_pool2d(bbox_feats, 1)#res5 2048
        cls_score, bbox_pred, feature = self.bbox_head(bbox_feats1, bbox_feats)
        # pdb.set_trace()
        domians_ind = rois[:, 0]
        instance_domains = torch.rand_like(domians_ind)
        if gt_domains is not None:
            # n=len(gt_domains)
            # pdb.set_trace()
            for i, gt_domain in enumerate(gt_domains):
                instance_domains[domians_ind==i]=gt_domain.type_as(instance_domains)
        bbox_results = dict(
            cls_score=cls_score,#[256], 256 means n
            bbox_pred=bbox_pred, #[256, 4]
            feature=feature, #[256, 256]
            bbox_feats=bbox_feats, #[256, 2048, 1, 1]
            ins_domains=instance_domains
        )
        if cls_score.isnan().nonzero().shape[0] != 0 or torch.isinf(cls_score).any():
            pdb.set_trace()
        return bbox_results

    def _bbox_forward_train(self, x, sampling_results, gt_bboxes, gt_labels, gt_pids, img_metas,gt_domains=None):
        # pdb.set_trace()
        # print([res.bboxes for res in sampling_results])
        # pdb.set_trace()
        rois = bbox2roi([res.bboxes for res in sampling_results])#[batch_ind, x1, y1, x2, y2]
        bbox_results = self._bbox_forward(x, rois,gt_domains=gt_domains)
        # if len(rois)%128 !=0:
        #     pdb.set_trace()

        bbox_targets = self.bbox_head.get_targets(
            sampling_results, gt_bboxes, gt_labels, gt_pids, self.train_cfg
        )
        loss_bbox = self.bbox_head.loss(
            bbox_results["cls_score"],
            bbox_results["bbox_pred"],
            bbox_results["feature"],
            rois,
            *bbox_targets
        )

        bbox_results.update(loss_bbox=loss_bbox)
        bbox_results.update(gt_pids=bbox_targets[0])
        return bbox_results

    def simple_test_bboxes(
        self, x, img_metas, proposals, rcnn_test_cfg, rescale=False, use_rpn=True
    ):
        """Test only det bboxes without augmentation."""
        # pdb.set_trace()
        #rois [batch_ind,x1,y1,x2,y2]
        rois = bbox2roi(proposals)#proposals len=1, proposals[0].shape=300,5
        bbox_results = self._bbox_forward(x, rois)
        # pdb.set_trace()
        if not use_rpn:
            return None, None, bbox_results["feature"]
        img_shape = img_metas[0]["img_shape"]
        scale_factor = img_metas[0]["scale_factor"]
        det_bboxes, det_labels, det_features = self.bbox_head.get_bboxes(
            rois,
            bbox_results["cls_score"],
            bbox_results["bbox_pred"],
            bbox_results["feature"],
            img_shape,
            scale_factor,
            rescale=rescale,
            cfg=rcnn_test_cfg,
        )
        # pdb.set_trace()
        return det_bboxes, det_labels, det_features

    def simple_test(self, x, proposal_list, img_metas, proposals=None, rescale=False, use_rpn=True):
        """Test without augmentation."""
        assert self.with_bbox, "Bbox head must be implemented."

        det_bboxes, det_labels, det_features = self.simple_test_bboxes(
            x, img_metas, proposal_list, self.test_cfg, rescale=rescale, use_rpn=use_rpn
        )
        if det_bboxes is None:#and query_mode=True == use_rpn=False
            return det_features #means embeddings=reid feature
            # return None, det_features
        #bbox_results = bbox2result(det_bboxes, det_labels, self.bbox_head.num_classes)
        bbox_results = bbox2result_reid(det_bboxes, det_labels, det_features, self.bbox_head.num_classes)


        # pdb.set_trace()
        # bbox_results1 = [
        #    bbox2result_reid(det_bboxes[i], det_labels[i], det_features[i],
        #                self.bbox_head.num_classes)
        #    for i in range(len(det_bboxes))
        # ]
        # pdb.set_trace()
        if not self.with_mask:
            return bbox_results
        else:
            segm_results = self.simple_test_mask(
                x, img_metas, det_bboxes, det_labels, rescale=rescale
            )
            return bbox_results, segm_results
