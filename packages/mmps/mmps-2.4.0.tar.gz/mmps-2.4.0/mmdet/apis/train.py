import pdb
import random
import os

import numpy as np
import torch

import torch.distributed as dist
from mmcv.parallel import MMDataParallel, MMDistributedDataParallel
from mmcv.runner import (HOOKS, DistSamplerSeedHook, EpochBasedRunner,
                         OptimizerHook, build_optimizer, get_dist_info)
from mmcv.utils import build_from_cfg

from mmdet.core import DistEvalHook, EvalHook, Fp16OptimizerHook
from mmdet.datasets import build_dataloader, build_dataset
from mmdet.utils import get_root_logger


def init_random_seed(seed=None, device='cuda'):
    """Initialize random seed.
    If the seed is not set, the seed will be automatically randomized,
    and then broadcast to all processes to prevent some potential bugs.
    Args:
        seed (int, Optional): The seed. Default to None.
        device (str): The device where the seed will be put on.
            Default to 'cuda'.
    Returns:
        int: Seed to be used.
    """
    if seed is not None:
        return seed

    # Make sure all ranks share the same random seed to prevent
    # some potential bugs. Please refer to
    # https://github.com/open-mmlab/mmdetection/issues/6339
    rank, world_size = get_dist_info()
    seed = np.random.randint(2**31)
    if world_size == 1:
        return seed

    if rank == 0:
        random_num = torch.tensor(seed, dtype=torch.int32, device=device)
    else:
        random_num = torch.tensor(0, dtype=torch.int32, device=device)
    dist.broadcast(random_num, src=0)
    return random_num.item()

def set_random_seed(seed, deterministic=False):
    """Set random seed.

    Args:
        seed (int): Seed to be used.
        deterministic (bool): Whether to set the deterministic option for
            CUDNN backend, i.e., set `torch.backends.cudnn.deterministic`
            to True and `torch.backends.cudnn.benchmark` to False.
            Default: False.
    """
    # random.seed(seed)#
    # os.environ['PYTHONHASHSEED'] = str(seed)
    # np.random.seed(seed)#
    # torch.backends.cudnn.benchmark = False
    # torch.manual_seed(seed)#
    # torch.backends.cudnn.enabled = True
    # torch.cuda.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)#  # if you are using multi-GPU.
    # torch.backends.cudnn.deterministic = True#


    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # torch.set_deterministic(True)

    if deterministic:
        print('++++++++++++++++++++++++++++')
        print('set_random_seed:{}'.format(seed))
        print('++++++++++++++++++++++++++++')
        torch.backends.cudnn.deterministic = True#cudnn加速中优化算法是否取默认，即算法固定
        torch.backends.cudnn.benchmark = False#是否使用cudnn加速,不确定计算
        # torch.backends.cudnn.enabled = True#是否启用cudnn

        # os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'


def train_detector(model,
                   dataset,
                   cfg,
                   distributed=False,
                   validate=False,
                   timestamp=None,
                   meta=None):
    logger = get_root_logger(cfg.log_level)

    # prepare data loaders
    dataset = dataset if isinstance(dataset, (list, tuple)) else [dataset]
    if 'imgs_per_gpu' in cfg.data:
        logger.warning('"imgs_per_gpu" is deprecated in MMDet V2.0. '
                       'Please use "samples_per_gpu" instead')
        if 'samples_per_gpu' in cfg.data:
            logger.warning(
                f'Got "imgs_per_gpu"={cfg.data.imgs_per_gpu} and '
                f'"samples_per_gpu"={cfg.data.samples_per_gpu}, "imgs_per_gpu"'
                f'={cfg.data.imgs_per_gpu} is used in this experiments')
        else:
            logger.warning(
                'Automatically set "samples_per_gpu"="imgs_per_gpu"='
                f'{cfg.data.imgs_per_gpu} in this experiments')
        cfg.data.samples_per_gpu = cfg.data.imgs_per_gpu

    # cfg.data.shuffle
    train_shuffle = cfg.get('train_shuffle', True)
    drop_last = cfg.data.get('drop_last', False)
    data_loaders = [
        build_dataloader(
            ds,
            cfg.data.samples_per_gpu,
            cfg.data.workers_per_gpu,
            # cfg.gpus will be ignored if distributed
            len(cfg.gpu_ids),
            dist=distributed,
            # triplet sampler
            shuffle=train_shuffle,
            #triplet=True,
            # seed=166541891
            seed=cfg.seed_dataloader,
            # seed = cfg.seed
            drop_last=drop_last
        ) for ds in dataset
    ]

    # put model on gpus
    if distributed:
        find_unused_parameters = cfg.get('find_unused_parameters', False)
        # Sets the `find_unused_parameters` parameter in
        # torch.nn.parallel.DistributedDataParallel
        model = MMDistributedDataParallel(
            model.cuda(),
            device_ids=[torch.cuda.current_device()],
            broadcast_buffers=False,
            find_unused_parameters=find_unused_parameters)
    else:
        model = MMDataParallel(
            model.cuda(cfg.gpu_ids[0]), device_ids=cfg.gpu_ids)

    # parameters = []
    #
    # for name, p in model.named_parameters():
    #
    #     p.requires_grad = False
    #     #"module.neck.fpt"
    #     if name.split('.')[2] == "fpt":
    #         # pdb.set_trace()
    #         p.requires_grad = True
    #         # parameters.append(p)

    # optimizer = torch.optim.SGD(
    #     parameters, lr=cfg.optimizer['lr'], momentum=cfg.optimizer['momentum'],
    #     weight_decay=cfg.optimizer['weight_decay']
    # )
    # pdb.set_trace()
    if cfg.get('train_part', None):
        for name, p in model.named_parameters():
            p.requires_grad = False
            # "module.neck.fpt"
            if name.split('.')[2] == "fpt":
                p.requires_grad = True
        # parameters = filter(lambda p: p.requires_grad, model.parameters())
        # optimizer = torch.optim.SGD(
        #     parameters, lr=cfg.optimizer['lr'], momentum=cfg.optimizer['momentum'],
        #     weight_decay=cfg.optimizer['weight_decay']
        # )

        optimizer = build_optimizer(model.module.neck.fpt, cfg.optimizer)
    else:
        optimizer = build_optimizer(model, cfg.optimizer)

    # build runner

    runner = EpochBasedRunner(
        model,
        optimizer=optimizer,
        work_dir=cfg.work_dir,
        logger=logger,
        meta=meta)
    # an ugly workaround to make .log and .log.json filenames the same
    runner.timestamp = timestamp

    # fp16 setting
    fp16_cfg = cfg.get('fp16', None)
    if fp16_cfg is not None:
        optimizer_config = Fp16OptimizerHook(
            **cfg.optimizer_config, **fp16_cfg, distributed=distributed)
    elif distributed and 'type' not in cfg.optimizer_config:
        print('+++++++++++')
        optimizer_config = OptimizerHook(**cfg.optimizer_config)
    else:
        print('?????????????')
        optimizer_config = cfg.optimizer_config
        if cfg.get('test_accumulate_grad', None):
            from mmdet.core import AccumulationGradOptimizerHook
            optimizer_config = AccumulationGradOptimizerHook(**cfg.optimizer_config)
        if cfg.get('GetGradientOptimizerHook_LUT_UPDATE', None):
            print('####GetGradientOptimizerHook_LUT_UPDATE########')
            from mmdet.core import GetGradientOptimizerHook_LUT_UPDATE
            optimizer_config = GetGradientOptimizerHook_LUT_UPDATE(**cfg.optimizer_config)
        if cfg.get('AccumulationGradOptimizerHook_LUT_UPDATE', None):
            print('####AccumulationGradOptimizerHook_LUT_UPDATE########')
            from mmdet.core import AccumulationGradOptimizerHook_LUT_UPDATE
            optimizer_config = AccumulationGradOptimizerHook_LUT_UPDATE(**cfg.optimizer_config)


    # register hooks
    runner.register_training_hooks(cfg.lr_config, optimizer_config,
                                   cfg.checkpoint_config, cfg.log_config,
                                   cfg.get('momentum_config', None))
    if distributed:
        runner.register_hook(DistSamplerSeedHook())

    # register eval hooks
    if validate:
        val_dataset = build_dataset(cfg.data.val, dict(test_mode=True))
        val_dataloader = build_dataloader(
            val_dataset,
            samples_per_gpu=1,
            workers_per_gpu=cfg.data.workers_per_gpu,
            dist=distributed,
            shuffle=False)
        eval_cfg = cfg.get('evaluation', {})
        eval_hook = DistEvalHook if distributed else EvalHook
        runner.register_hook(eval_hook(val_dataloader, **eval_cfg))

    # user-defined hooks
    if cfg.get('custom_hooks', None):
        custom_hooks = cfg.custom_hooks
        assert isinstance(custom_hooks, list), \
            f'custom_hooks expect list type, but got {type(custom_hooks)}'
        for hook_cfg in cfg.custom_hooks:
            assert isinstance(hook_cfg, dict), \
                'Each item in custom_hooks expects dict type, but got ' \
                f'{type(hook_cfg)}'
            hook_cfg = hook_cfg.copy()
            priority = hook_cfg.pop('priority', 'NORMAL')
            hook = build_from_cfg(hook_cfg, HOOKS)
            runner.register_hook(hook, priority=priority)

    # pdb.set_trace()
    if cfg.resume_from:
        runner.resume(cfg.resume_from)
    elif cfg.load_from:
        if cfg.get('train_part', None):
            pretrained_model = torch.load(cfg.load_from)
            # pdb.set_trace()
            model_dict = model.module.state_dict()

            for k, v in pretrained_model["state_dict"].items():
                if k not in model_dict:
                    print(k)
                    pdb.set_trace()

            pretrained_dict = {k: v for k, v in pretrained_model["state_dict"].items() if k in model_dict}
            assert pretrained_dict == pretrained_model["state_dict"]
            model_dict.update(pretrained_dict)
            model.module.load_state_dict(model_dict)

            # with open(osp.join('/tianyanling/AlignPS/work_dirs/prw_base_focal_labelnorm_sub_ldcn_fg15_wd1-3_dis_bs_2_lr_0.0005', 'lookup_table.pkl'), 'rb') as fid:
            #     lookup_table = pickle.load(fid)
            #     model.module.bbox_head.labeled_matching_layer.lookup_table = lookup_table

            # runner.load_checkpoint(model, cfg.load_from, strict=True)

            # pdb.set_trace()

        else:
            runner.load_checkpoint(cfg.load_from)
    runner.run(data_loaders, cfg.workflow, cfg.total_epochs)
