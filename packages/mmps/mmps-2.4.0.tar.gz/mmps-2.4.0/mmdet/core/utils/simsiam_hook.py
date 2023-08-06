# Copyright (c) OpenMMLab. All rights reserved.
import pdb

from mmcv.runner import HOOKS, Hook


@HOOKS.register_module()
class SimSiamHook(Hook):
    """Hook for SimSiam.

    This hook is for SimSiam to fix learning rate of predictor.

    Args:
        fix_pred_lr (bool): whether to fix the lr of predictor or not.
        lr (float): the value of fixed lr.
        adjust_by_epoch (bool, optional): whether to set lr by epoch or iter.
            Defaults to True.
    """

    def __init__(self, fix_pred_lr, lr, adjust_by_epoch=True, **kwargs):
        self.fix_pred_lr = fix_pred_lr
        self.lr = lr
        self.adjust_by_epoch = adjust_by_epoch

    def before_train_iter(self, runner):
        # pdb.set_trace()
        if self.adjust_by_epoch:
            return
        else:
            if self.fix_pred_lr:
                for param_group in runner.optimizer.param_groups:
                    # pdb.set_trace()
                    if 'fix_lr' in param_group and param_group['fix_lr']:
                        param_group['lr'] = self.lr

    def before_train_epoch(self, runner):
        """fix lr of predictor."""
        # pdb.set_trace()
        if self.fix_pred_lr:
            for param_group in runner.optimizer.param_groups:
                if 'fix_lr' in param_group and param_group['fix_lr']:
                    # pdb.set_trace()
                    param_group['lr'] = self.lr
                # pdb.set_trace()
                # if 'lr' in param_group:
                #     if param_group['lr']==0.01:
                #         pdb.set_trace()
