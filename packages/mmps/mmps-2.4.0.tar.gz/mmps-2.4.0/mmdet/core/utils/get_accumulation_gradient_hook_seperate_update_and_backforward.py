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
class AccumulationGradOptimizerHook_LUT_UPDATE(OptimizerHook):

    def __init__(self, loss_num, epoch, bs, dataset, **kwargs):
        super(AccumulationGradOptimizerHook_LUT_UPDATE, self).__init__(**kwargs)
        self.loss_num = loss_num
        self.epoch = epoch
        self.bs = bs
        self.dataset = dataset
        assert dataset in ['cuhk', 'prw']


    def after_train_iter(self, runner):
        #zero_grad--> save grad --> zero_gard --> save grad --> ... --> step
        # pdb.set_trace()
        model = runner.model
        loss_all = runner.outputs['loss_dict']
        keys = loss_all.keys()
        epoch = runner.epoch
        assert epoch == self.epoch ####
        if self.dataset == 'cuhk':
            train_num = 11206
            start_iter = 1500  #### cuhk:1500 prw:500
            # start_iter = 0  #### cuhk:1500 prw:500
        if self.dataset == 'prw':
            train_num = 5704
            start_iter = 500  #### cuhk:1500 prw:500
        temp = math.ceil(train_num/self.bs)
        iter = runner._iter % temp  #### cuhk:11206/bs3=3736 prw:5704/bs3=1902
        end_iter = start_iter + 35  #### cuhk:1535 prw:535
        #check
        if self.bs == 3:
             assert temp == 3736 or temp ==1902

        assert len(loss_all.keys()) == self.loss_num

        # pdb.set_trace()
        if runner.meta[
            'exp_name'] == '6_0_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_gradient_all_bs3.py' or \
                runner.meta[
                    'exp_name'] == '6_5_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_atrr_labelnorem_t15_u10_gradient_all_bs3.py' or \
                runner.meta[
                    'exp_name'] == '6_3_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_labelnorem_t15_u10_gradient_all_bs3.py' or \
                runner.meta[
                    'exp_name'] == 'cuhk0_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_seperate_gradient_all_bs3_fix.py' or \
                runner.meta[
                    'exp_name'] == '6_17_0_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_attr_neck_conv_bce_gradient_all_bs3.py':
            save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + '_acc' + \
                        '/visual/before_gard_clip'
        else:
            save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
                        '/visual/before_gard_clip'

        # pdb.set_trace()

        # save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
        #             '/visual/weight_grad/before_gard_clip'

        mmcv.mkdir_or_exist(osp.abspath(save_path))

        if iter == start_iter:
            print("!!!! accumulation start !!!!")
        if iter >= start_iter:
            loss_grads = []
            for loss_name, loss_value in loss_all.items():
                # print(loss_name)

                runner.optimizer.zero_grad()  #####
                flag = False
                try:
                    if loss_value.requires_grad:
                        loss_value.backward(retain_graph=True)  ####
                    else:
                        # print(loss_name)
                        flag = True
                    # raise RuntimeError
                except RuntimeError as e:
                    print(e)
                    pdb.set_trace()

                loss_grad_dict = dict()
                for key, value in model.module.backbone.named_parameters():  # layer2,layer3

                    if 'layer4' in key:
                        continue
                        # pdb.set_trace()
                    # n=n+1
                    if value.requires_grad:
                        if value.grad is None:
                            pdb.set_trace()
                        # temp = {key: copy.deepcopy(value.grad)}
                        temp = {key: copy.deepcopy(value.grad).view(-1).cpu().numpy().tolist()}
                        if flag:
                            assert len(value.grad.nonzero()) == 0
                        loss_grad_dict.update(temp)
                loss_grads.append(loss_grad_dict)

            gard_data = {'loss_key': list(keys),'iter': iter, 'grad_data': []}

            filename = 'gradient_for_accumulation_' + str(iter) + '.json'
            out_grads = osp.join(save_path, filename)
            with open(out_grads, 'w') as f:

                for index in range(len(loss_all.keys())):
                    gard_data['grad_data'].append(loss_grads[index])
                # pdb.set_trace()
                json.dump(gard_data, f)

            print('Gradient_saved at iter {} : write into {} has done!'.format(iter, out_grads))
        # pdb.set_trace()

        if iter == end_iter:
            print("!!!! accumulation end !!!!")
            pdb.set_trace()

        runner.optimizer.zero_grad()

        runner.outputs['loss'].backward()

        if iter < start_iter:
            print('==step at iter {}=='.format(iter))

            model.module.roi_head.bbox_head.loss_oim.update_lut_and_queue_nae()
            model.module.bbox_head.unlabeled_matching_layer.update_queue()
            model.module.bbox_head.labeled_matching_layer.update_lut()
            if self.grad_clip is not None:
                grad_norm = self.clip_grads(runner.model.parameters())
                if grad_norm is not None:
                    # Add grad norm to the logger
                    runner.log_buffer.update({'grad_norm': float(grad_norm)},
                                             runner.outputs['num_samples'])
            runner.optimizer.step()
