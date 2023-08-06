import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import ConvModule, xavier_init
from mmcv.ops import DeformConv2dPack

from mmdet.core import auto_fp16, bbox2roi
from ..builder import NECKS, build_roi_extractor


@NECKS.register_module()
class FPNLconv3_Attribute(nn.Module):
    r"""Feature Pyramid Network.

    This is an implementation of paper `Feature Pyramid Networks for Object
    Detection <https://arxiv.org/abs/1612.03144>`_.

    Args:
        in_channels (List[int]): Number of input channels per scale.
        out_channels (int): Number of output channels (used at each scale)
        num_outs (int): Number of output scales.
        start_level (int): Index of the start input backbone level used to
            build the feature pyramid. Default: 0.
        end_level (int): Index of the end input backbone level (exclusive) to
            build the feature pyramid. Default: -1, which means the last level.
        add_extra_convs (bool | str): If bool, it decides whether to add conv
            layers on top of the original feature maps. Default to False.
            If True, its actual mode is specified by `extra_convs_on_inputs`.
            If str, it specifies the source feature map of the extra convs.
            Only the following options are allowed

            - 'on_input': Last feat map of neck inputs (i.e. backbone feature).
            - 'on_lateral':  Last feature map after lateral convs.
            - 'on_output': The last output feature map after fpn convs.
        extra_convs_on_inputs (bool, deprecated): Whether to apply extra convs
            on the original feature from the backbone. If True,
            it is equivalent to `add_extra_convs='on_input'`. If False, it is
            equivalent to set `add_extra_convs='on_output'`. Default to True.
        relu_before_extra_convs (bool): Whether to apply relu before the extra
            conv. Default: False.
        no_norm_on_lateral (bool): Whether to apply norm on lateral.
            Default: False.
        conv_cfg (dict): Config dict for convolution layer. Default: None.
        norm_cfg (dict): Config dict for normalization layer. Default: None.
        act_cfg (str): Config dict for activation layer in ConvModule.
            Default: None.
        upsample_cfg (dict): Config dict for interpolate layer.
            Default: `dict(mode='nearest')`

    Example:
        >>> import torch
        >>> in_channels = [2, 3, 5, 7]
        >>> scales = [340, 170, 84, 43]
        >>> inputs = [torch.rand(1, c, s, s)
        ...           for c, s in zip(in_channels, scales)]
        >>> self = FPN(in_channels, 11, len(in_channels)).eval()
        >>> outputs = self.forward(inputs)
        >>> for i in range(len(outputs)):
        ...     print(f'outputs[{i}].shape = {outputs[i].shape}')
        outputs[0].shape = torch.Size([1, 11, 340, 340])
        outputs[1].shape = torch.Size([1, 11, 170, 170])
        outputs[2].shape = torch.Size([1, 11, 84, 84])
        outputs[3].shape = torch.Size([1, 11, 43, 43])
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 num_outs,###
                 strides,###
                 start_level=0,
                 end_level=-1,
                 add_extra_convs=False,
                 roi_align_outsize=32,###
                 max_labeled_person_num=32,  ###
                 extra_convs_on_inputs=True,
                 relu_before_extra_convs=False,
                 no_norm_on_lateral=False,
                 conv_cfg=None,
                 norm_cfg=None,
                 act_cfg=None,
                 upsample_cfg=dict(mode='nearest')):
        super(FPNLconv3_Attribute, self).__init__()
        assert isinstance(in_channels, list)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_ins = len(in_channels)
        self.num_outs = num_outs
        self.roi_align_outsize = roi_align_outsize
        self.max_labeled_person_num = max_labeled_person_num
        self.relu_before_extra_convs = relu_before_extra_convs
        self.no_norm_on_lateral = no_norm_on_lateral
        self.fp16_enabled = False
        self.upsample_cfg = upsample_cfg.copy()

        if end_level == -1:
            self.backbone_end_level = self.num_ins  # 4
            assert num_outs >= self.num_ins - start_level
        else:
            # if end_level < inputs, no extra level is allowed
            self.backbone_end_level = end_level
            assert end_level <= len(in_channels)
            assert num_outs == end_level - start_level
        self.start_level = start_level
        self.end_level = end_level
        self.add_extra_convs = add_extra_convs
        assert isinstance(add_extra_convs, (str, bool))
        if isinstance(add_extra_convs, str):
            # Extra_convs_source choices: 'on_input', 'on_lateral', 'on_output'
            assert add_extra_convs in ('on_input', 'on_lateral', 'on_output')
        elif add_extra_convs:  # True
            if extra_convs_on_inputs:
                # For compatibility with previous release
                # TODO: deprecate `extra_convs_on_inputs`
                self.add_extra_convs = 'on_input'
            else:
                self.add_extra_convs = 'on_output'

        # roi_outchannels = sum(self.in_channels[self.start_level:])
        bbox_roi_extractor1 = dict(
            type="GenericRoIExtractor",
            roi_layer=dict(type="RoIAlign", output_size=[32,16], sample_num=0),
            # roi_layer=dict(type="RoIAlign", output_size=32, sample_num=0),
            out_channels=512,
            aggregation='concat',
            featmap_strides=[8],
        )
        self.bbox_roi_extractor1 = build_roi_extractor(bbox_roi_extractor1)
        bbox_roi_extractor2 = dict(
            type="GenericRoIExtractor",
            roi_layer=dict(type="RoIAlign", output_size=[16, 8], sample_num=0),
            # roi_layer=dict(type="RoIAlign", output_size=16, sample_num=0),
            out_channels=1024,
            aggregation='concat',
            featmap_strides=[16],
        )
        self.bbox_roi_extractor2 = build_roi_extractor(bbox_roi_extractor2)
        bbox_roi_extractor3 = dict(
            type="GenericRoIExtractor",
            roi_layer=dict(type="RoIAlign", output_size=[8, 4], sample_num=0),
            # roi_layer=dict(type="RoIAlign", output_size=8, sample_num=0),
            out_channels=2048,
            aggregation='concat',
            featmap_strides=[32],
        )
        self.bbox_roi_extractor3 = build_roi_extractor(bbox_roi_extractor3)
        self.lateral_convs = nn.ModuleList()


        for i in range(self.start_level, self.backbone_end_level):  # 1,2,3
            '''
            l_conv = ConvModule(
                in_channels[i],
                out_channels,
                3,
                padding=1,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg if not self.no_norm_on_lateral else None,
                act_cfg=act_cfg,
                inplace=False)
            '''
            l_conv = ConvModule(
                in_channels[i],
                out_channels,
                1,
                padding=0,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg if not self.no_norm_on_lateral else None,
                act_cfg=act_cfg,
                inplace=False)
            self.lateral_convs.append(l_conv)

        # add extra conv layers (e.g., RetinaNet)
        extra_levels = num_outs - self.backbone_end_level + self.start_level
        if self.add_extra_convs and extra_levels >= 1:
            for i in range(extra_levels):  # 2
                if i == 0 and self.add_extra_convs == 'on_input':
                    in_channels = self.in_channels[self.backbone_end_level - 1]
                else:
                    in_channels = out_channels
                extra_fpn_conv = ConvModule(
                    in_channels,
                    out_channels,
                    3,
                    stride=2,
                    padding=1,
                    conv_cfg=conv_cfg,
                    norm_cfg=norm_cfg,
                    act_cfg=act_cfg,
                    inplace=False)
                self.fpn_convs.append(extra_fpn_conv)

    # default init_weights for conv(msra) and norm in ConvModule
    def init_weights(self):
        """Initialize the weights of FPN module."""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                xavier_init(m, distribution='uniform')
        if self.bbox_roi_extractor:
            self.bbox_roi_extractor.init_weights()

    @auto_fp16()
    def forward(self, inputs, gt_bboxes=None, gt_attrs=None, gt_ids=None):
        """Forward function."""
        # pdb.set_trace()
        assert len(inputs) == len(self.in_channels)

        #get bbox features
        gt_bboxes_ = []
        gt_attrs_ = []
        gt_ids_ = []
        num = 0
        flag = False
        for gt_ids_per_img in gt_ids:
            num += (gt_ids_per_img != -1).sum()
        if num > self.max_labeled_person_num:
            flag = True
        for img_id, gt_ids_per_img in enumerate(gt_ids):
            # pdb.set_trace()

            gt_bbox = gt_bboxes[img_id]
            gt_attr = gt_attrs[img_id]
            assert len(gt_ids_per_img) == len(gt_bbox) == len(gt_attr)
            index = gt_ids_per_img != -1  # not use unlabeled data
            thresh = self.max_labeled_person_num // len(gt_attrs)
            if flag and len(index) > thresh:
                index[thresh:] = False
            gt_bbox = gt_bbox[index]
            gt_attr = gt_attr[index]
            gt_bboxes_.append(gt_bbox)
            gt_attrs_.append(gt_attr)
            gt_ids_.append(gt_ids_per_img[index])

        rois = bbox2roi(gt_bboxes_)
        # bbox_feats = self.bbox_roi_extractor(inputs[self.start_level:], rois) #[bbox_num,3584,14,14]

        #拆成每个level的feature
        # start = 0
        # bbox_feats_lvl = []
        # for channel in self.in_channels[self.start_level:]:
        #     bbox_feats_lvl.append(bbox_feats[:, start:start + channel,:,:].contiguous())
        #     start = start + channel

        bbox_feats_lvl = []
        bbox_feats_1 = self.bbox_roi_extractor1([inputs[self.start_level]], rois)  # [bbox_num,512,32,16]
        bbox_feats_2 = self.bbox_roi_extractor2([inputs[self.start_level+1]], rois)  # [bbox_num,1024,16,8]
        bbox_feats_3 = self.bbox_roi_extractor3([inputs[self.start_level+2]], rois)  # [bbox_num,2048,8,4]
        bbox_feats_lvl.append(bbox_feats_1)
        bbox_feats_lvl.append(bbox_feats_2)
        bbox_feats_lvl.append(bbox_feats_3)

        # bbox_feats1 = F.adaptive_max_pool2d(bbox_feats, 1)

        # build laterals
        laterals = [
            # lateral_conv(inputs[i + self.start_level])
            lateral_conv(bbox_feats_lvl[i])
            for i, lateral_conv in enumerate(self.lateral_convs)
        ]

        # build top-down path
        used_backbone_levels = len(laterals)
        for i in range(used_backbone_levels - 1, 0, -1):
            # In some cases, fixing `scale factor` (e.g. 2) is preferred, but
            #  it cannot co-exist with `size` in `F.interpolate`.
            if 'scale_factor' in self.upsample_cfg:
                #laterals[i - 1] += F.interpolate(laterals[i],
                #                                 **self.upsample_cfg)
                laterals[i - 1] = torch.cat((laterals[i - 1], F.interpolate(laterals[i], **self.upsample_cfg)), 1)
            else:
                prev_shape = laterals[i - 1].shape[2:]
                #laterals[i - 1] += F.interpolate(
                #    laterals[i], size=prev_shape, **self.upsample_cfg)
                laterals[i - 1] = torch.cat((laterals[i - 1], F.interpolate(laterals[i], size=prev_shape, **self.upsample_cfg)), 1)

        # build outputs
        # part 1: from original levels

        outs = laterals
        # part 2: add extra levels
        if self.num_outs > len(outs):
            # use max pool to get more levels on top of outputs
            # (e.g., Faster R-CNN, Mask R-CNN)
            if not self.add_extra_convs:
                for i in range(self.num_outs - used_backbone_levels):
                    outs.append(F.max_pool2d(outs[-1], 1, stride=2))
            # add conv layers on top of original feature maps (RetinaNet)
            else:
                if self.add_extra_convs == 'on_input':
                    extra_source = inputs[self.backbone_end_level - 1]
                elif self.add_extra_convs == 'on_lateral':
                    extra_source = laterals[-1]
                elif self.add_extra_convs == 'on_output':
                    extra_source = outs[-1]
                else:
                    raise NotImplementedError
                outs.append(self.fpn_convs[used_backbone_levels](extra_source))
                for i in range(used_backbone_levels + 1, self.num_outs):
                    if self.relu_before_extra_convs:
                        outs.append(self.fpn_convs[i](F.relu(outs[-1])))
                    else:
                        outs.append(self.fpn_convs[i](outs[-1]))
        if outs[0].isnan().nonzero().shape[0] != 0:
            pdb.set_trace()

        outs.append(bbox_feats_lvl[2])
        #outs len=4,前3个shape=[bbox_num, 256*3,32,16],[bbox_num, 256*2,16,8],[bbox_num, 256*1,8,4],
        # 第4个是[bbox_num, 2048,8,4]

        return tuple(outs), gt_attrs_, gt_ids_
