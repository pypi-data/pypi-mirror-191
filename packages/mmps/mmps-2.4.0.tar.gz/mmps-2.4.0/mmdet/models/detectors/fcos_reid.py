import pdb
import torch
import torch.distributed as dist
from collections import defaultdict, OrderedDict
from ..builder import DETECTORS
from .single_stage_reid import SingleStageReidDetector


@DETECTORS.register_module()
class FCOSReid(SingleStageReidDetector):
    """Implementation of `FCOS <https://arxiv.org/abs/1904.01355>`_"""

    def __init__(self,
                 backbone,
                 neck,
                 bbox_head,
                 loss_weights=None,
                 train_cfg=None,
                 test_cfg=None,
                 pretrained=None):
        super(FCOSReid, self).__init__(backbone, neck, bbox_head, train_cfg,
                                   test_cfg, pretrained)
        self.loss_weights = loss_weights

    def train_step(self, data, optimizer):
        """The iteration step during training.

        This method defines an iteration step during training, except for the
        back propagation and optimizer updating, which are done in an optimizer
        hook. Note that in some complicated cases or models, the whole process
        including back propagation and optimizer updating is also defined in
        this method, such as GAN.

        Args:
            data (dict): The output of dataloader.
            optimizer (:obj:`torch.optim.Optimizer` | dict): The optimizer of
                runner is passed to ``train_step()``. This argument is unused
                and reserved.

        Returns:
            dict: It should contain at least 3 keys: ``loss``, ``log_vars``, \
                ``num_samples``.

                - ``loss`` is a tensor for back propagation, which can be a \
                weighted sum of multiple losses.
                - ``log_vars`` contains all the variables to be sent to the
                logger.
                - ``num_samples`` indicates the batch size (when the model is \
                DDP, it means the batch size on each GPU), which is used for \
                averaging the logs.
        """
        # pdb.set_trace()
        losses = self(**data)
        loss, log_vars, loss_dict = self._parse_losses(losses)

        outputs = dict(
            loss=loss, loss_dict=loss_dict, log_vars=log_vars, num_samples=len(data['img_metas']))

        return outputs

    def _parse_losses(self, losses):
        """Parse the raw outputs (losses) of the network.

        Args:
            losses (dict): Raw output of the network, which usually contain
                losses and other necessary infomation.

        Returns:
            tuple[Tensor, dict]: (loss, log_vars), loss is the loss tensor \
                which may be a weighted sum of all losses, log_vars contains \
                all the variables to be sent to the logger.
        """
        log_vars = OrderedDict()
        for loss_name, loss_value in losses.items():
            if isinstance(loss_value, torch.Tensor):
                log_vars[loss_name] = loss_value.mean()
            elif isinstance(loss_value, list):
                log_vars[loss_name] = sum(_loss.mean() for _loss in loss_value)
            else:
                raise TypeError(
                    f'{loss_name} is not a tensor or list of tensors')

        loss = sum(_value for _key, _value in log_vars.items()
                   if 'loss' in _key)

        log_vars['loss'] = loss
        for loss_name, loss_value in log_vars.items():
            # reduce loss when distributed training
            if dist.is_available() and dist.is_initialized():
                loss_value = loss_value.data.clone()
                dist.all_reduce(loss_value.div_(dist.get_world_size()))
            log_vars[loss_name] = loss_value.item()

        return loss, log_vars, losses


    def forward_train(self,
                      img,
                      img_metas,
                      gt_bboxes,
                      gt_labels,
                      gt_ids,
                      gt_bboxes_ignore=None):
        losses = super(FCOSReid, self).forward_train(img, img_metas, gt_bboxes,
                                              gt_labels, gt_ids, gt_bboxes_ignore)
        # pdb.set_trace()
        if self.loss_weights is not None:
            weighted_keys = self.loss_weights.keys()
            for key, val_ in losses.items():
                if key in weighted_keys:
                    losses[key] = val_ * self.loss_weights[key]
        return losses