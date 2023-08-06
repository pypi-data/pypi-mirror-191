import json
import pdb
import torch
import copy
import mmcv
import os.path as osp
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as col
from torch.nn.utils import clip_grad
from mmcv.runner import HOOKS, Hook, OptimizerHook

@HOOKS.register_module()
class AccumulationGradOptimizerHook(OptimizerHook):

    def __init__(self, grad_clip=None, loss_num = 0):
        self.grad_clip = grad_clip
        self.loss_num = loss_num

    def clip_grads(self, params):
        params = list(
            filter(lambda p: p.requires_grad and p.grad is not None, params))
        if len(params) > 0:
            return clip_grad.clip_grad_norm_(params, **self.grad_clip)

    def after_train_iter(self, runner):
        #zero_grad--> save grad --> zero_gard --> save grad --> ... --> step
        # pdb.set_trace()
        model = runner.model
        loss_all = runner.outputs['loss_dict']

        assert len(loss_all.keys()) == self.loss_num

        loss_grads = []
        for loss_name, loss_value in loss_all.items():
            runner.optimizer.zero_grad()  #####
            try:
                loss_value.backward(retain_graph=True) ####
                # raise RuntimeError
            except RuntimeError as e:
                print(e)
                pdb.set_trace()
            loss_grad_dict = dict()
            for key, value in model.module.backbone.named_parameters():#layer2,layer3

                if 'layer4' in key:
                    continue
                    # pdb.set_trace()
                # n=n+1
                if value.requires_grad:
                    if value.grad is None:
                        pdb.set_trace()
                    temp = {key: copy.deepcopy(value.grad).view(-1).cpu().numpy().tolist()}
                    loss_grad_dict.update(temp)
            loss_grads.append(loss_grad_dict)

        keys = loss_all.keys()
        epoch = runner.epoch
        assert epoch == 23
        iter = runner._iter %1902
        start_iter = 500
        end_iter = 550

        # pdb.set_trace()
        if runner.meta['exp_name'] == '6_0_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_gradient_all_bs3.py' or \
                runner.meta['exp_name'] == '6_5_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_atrr_labelnorem_t15_u10_gradient_all_bs3.py' or \
                runner.meta['exp_name'] == '6_3_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_labelnorem_t15_u10_gradient_all_bs3.py':
            save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + '_acc' + \
                        '/visual/before_gard_clip'
        else:
            save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
                        '/visual/before_gard_clip'
        # pdb.set_trace()

        # save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
        #             '/visual/weight_grad/before_gard_clip'


        gard_data = {'loss_key': list(keys),'iter': iter, 'grad_data': []}
        if iter >= start_iter:
            print("!!!! accumulation start !!!!")
            mmcv.mkdir_or_exist(osp.abspath(save_path))
            filename = 'gradient_for_accumulation_' + str(iter) + '.json'
            out_grads = osp.join(save_path, filename)
            with open(out_grads, 'w') as f:

                for index in range(len(loss_all.keys())):
                    gard_data['grad_data'].append(loss_grads[index])

                json.dump(gard_data, f)

            print('Gradient_saved at iter {} : write into {} has done!'.format(iter, out_grads))
        # pdb.set_trace()
        if iter == end_iter:
            pdb.set_trace()




        # print('===before zero')
        # for key, value in model.module.backbone.named_parameters():  # layer2,layer3
        #     if key == 'layer2.0.conv1.weight':
        #         if value.grad is not None:
        #             print(value.grad.view(-1)[:4])
        runner.optimizer.zero_grad()
        # print('===after zero')
        # for key, value in model.module.backbone.named_parameters():  # layer2,layer3
        #     if key == 'layer2.0.conv1.weight':
        #         if value.grad is not None:
        #             print(value.grad.view(-1)[:4])

        runner.outputs['loss'].backward()

        # print('===after backward')
        # for key, value in model.module.backbone.named_parameters():  # layer2,layer3
        #     if key == 'layer2.0.conv1.weight':
        #         if value.grad is not None:
        #             print(value.grad.view(-1)[:4])

        if iter < start_iter:
            print('==step at iter {}=='.format(iter))
            if self.grad_clip is not None:
                grad_norm = self.clip_grads(runner.model.parameters())
                if grad_norm is not None:
                    # Add grad norm to the logger
                    runner.log_buffer.update({'grad_norm': float(grad_norm)},
                                             runner.outputs['num_samples'])
            runner.optimizer.step()
        # print('===after step')
        # for key, value in model.module.backbone.named_parameters():  # layer2,layer3
        #     if key == 'layer2.0.conv1.weight':
        #         if value.grad is not None:
        #             print(value.grad.view(-1)[:4])
