from mmcv.cnn import build_conv_layer, build_norm_layer
from torch import nn as nn


class ShuffleLayer(nn.Sequential):
    """Stack ShuffleUnit blocks to make a layer.

    Args:
        block (nn.Module): block used to build ResLayer.
        out_channels (int): out_channels of the block.
        num_blocks (int): Number of blocks.
        first_block (bool): Whether is the first ShuffleUnit of a
            sequential ShuffleUnits. Default: False, which means using
            the grouped 1x1 convolution.
    """

    def __init__(self,
                 block,
                 in_channels,
                 out_channels,
                 num_blocks,
                 first_block=False,
                 conv_cfg=None,
                 groups=3,
                 norm_cfg=dict(type='BN'),
                 act_cfg=dict(type='ReLU'),
                 with_cp=False,
                 **kwargs):
        self.in_channels=in_channels
        layers = []
        for i in range(num_blocks):
            first_block = first_block if i == 0 else False
            combine_mode = 'concat' if i == 0 else 'add'
            layers.append(
                block(
                    self.in_channels,
                    out_channels,
                    groups=groups,
                    first_block=first_block,
                    combine=combine_mode,
                    conv_cfg=conv_cfg,
                    norm_cfg=norm_cfg,
                    act_cfg=act_cfg,
                    with_cp=with_cp))
            self.in_channels = out_channels

        super(ShuffleLayer, self).__init__(*layers)
