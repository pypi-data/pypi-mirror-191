import pdb

import torch.nn as nn
from mmcv.cnn import constant_init, kaiming_init
from mmcv.runner import load_checkpoint

from mmdet.core import auto_fp16
from mmdet.models.backbones import ShuffleNetV1
from mmdet.models.builder import SHARED_HEADS
from mmdet.models.utils import ShuffleLayer as _ShuffleLayer
from mmdet.utils import get_root_logger
from mmdet.models.utils import make_divisible

@SHARED_HEADS.register_module()
class ShuffleLayer(nn.Module):

    def __init__(self,
                 # in_channels,
                 out_channels,
                 groups=3,
                 stage=3,
                 first_block=False,
                 widen_factor=1.0,
                 conv_cfg=None,
                 norm_cfg=dict(type='BN'),
                 with_cp=False):
        super(ShuffleLayer, self).__init__()
        self.norm_cfg = norm_cfg
        self.stage = stage
        self.fp16_enabled = False
        stage_blocks = ShuffleNetV1.stage_blocks
        num_blocks = stage_blocks[stage]

        self.block, channels = ShuffleNetV1.arch_settings[groups]
        channels = [make_divisible(ch * widen_factor, 8) for ch in channels]

        self.in_channels = int(24 * widen_factor)

        if stage==0:
            in_channels=self.in_channels
        else:
            in_channels=channels[stage-1]

        assert out_channels == channels[stage]

        shuffle_layer = _ShuffleLayer(
            self.block,
            in_channels,
            out_channels,
            num_blocks,
            first_block=first_block,
            conv_cfg=conv_cfg,
            groups=groups,
            with_cp=with_cp,
            norm_cfg=self.norm_cfg,
            act_cfg=dict(type='ReLU'),
        )
        temp=nn.ModuleList()
        for i in range(stage):
            temp.append(nn.ModuleList())
        temp.append(shuffle_layer)
        self.add_module(f'layers', temp)

    def init_weights(self, pretrained=None):
        """Initialize the weights in the module.

        Args:
            pretrained (str, optional): Path to pre-trained weights.
                Defaults to None.
        """
        if isinstance(pretrained, str):
            # pdb.set_trace()
            logger = get_root_logger()
            load_checkpoint(self, pretrained, strict=False, logger=logger)
            # pdb.set_trace()
        elif pretrained is None:
            for m in self.modules():
                if isinstance(m, nn.Conv2d):
                    kaiming_init(m)
                elif isinstance(m, nn.BatchNorm2d):
                    constant_init(m, 1)
        else:
            raise TypeError('pretrained must be a str or None')

    @auto_fp16()
    def forward(self, x):
        # res_layer = getattr(self, f'layer{self.stage}')
        res_layer = getattr(self, f'layers')
        # pdb.set_trace()
        out = res_layer[self.stage](x)
        return out

    def train(self, mode=True):
        super(ShuffleLayer, self).train(mode)
        # if self.norm_eval:
        #     for m in self.modules():
        #         if isinstance(m, nn.BatchNorm2d):
        #             m.eval()
