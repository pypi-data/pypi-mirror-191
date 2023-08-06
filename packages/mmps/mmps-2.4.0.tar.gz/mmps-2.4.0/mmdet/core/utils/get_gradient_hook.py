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

from mmcv.runner import HOOKS, Hook


@HOOKS.register_module()
class GetGradientHook(Hook):

    def __init__(self, loss_num, gradient_layer='all'):
        self.sim_arr = np.zeros((loss_num, loss_num))
        self.count = np.zeros((loss_num, loss_num))
        self.loss_num = loss_num
        self.gradient_layer = gradient_layer
        # pass

    # def before_run(self, runner):
    #     self.sim_data_matrix = {'sims_data': []}
    #     # pass

    # def after_run(self, runner):
    #     pass
    #
    def before_epoch(self, runner):
        # pdb.set_trace()
        assert self.sim_arr is not None
        assert self.count is not None
        self.sim_arr = np.zeros((self.loss_num, self.loss_num))
        self.count = np.zeros((self.loss_num, self.loss_num))
        self.grad_magnitude_all = np.zeros((self.loss_num,))
        self.count_grad_magnitude_all = np.zeros((self.loss_num,))
        self.grad_magnitude_layer2 = np.zeros((self.loss_num,))
        self.count_grad_magnitude_layer2 = np.zeros((self.loss_num,))
        self.grad_magnitude_layer3 = np.zeros((self.loss_num,))
        self.count_grad_magnitude_layer3 = np.zeros((self.loss_num,))


    def after_epoch(self, runner):
        # pdb.set_trace()
        assert self.sim_arr is not None
        loss_all = runner.outputs['loss_dict']
        keys = loss_all.keys()
        assert len(keys) == self.loss_num
        epoch = runner.epoch

        # pdb.set_trace()
        # if runner.meta['exp_name'] == '6_0_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_gradient_all_bs3.py' or runner.meta['exp_name'] == '6_5_faster_rcnn_r50_caffe_c4_1x_cuhk_single_two_stage17_6_nae1_prw_seperate_atrr_labelnorem_t15_u10_gradient_all_bs3.py':
        #     save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + '_1' + \
        #                 '/visual/weight_grl_' + self.gradient_layer
        # else:
        #     save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
        #                 '/visual/weight_grl_' + self.gradient_layer
        # pdb.set_trace()

        save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
                    '/visual/weight_grl_' + self.gradient_layer
        mmcv.mkdir_or_exist(osp.abspath(save_path))

        """
            plot gradient angle
        """
        # for i, keys_i in enumerate(keys):
        #     for j, keys_j in enumerate(keys):
        #         if i == j:
        #             continue
        #         sim = self.sim_arr[i][j] / self.count[i][j]
        #         filename = keys_i + '_' + keys_j + '_epoch' \
        #                     + str(epoch) + '.jpg'
        #         plot_point([0, 0], math.acos(np.mean(sim)), 1, save_path,filename, keys_i, keys_j)

        """
            write loss_gradient similarity to file [n * n matrix] for each epoch
        """
        # pdb.set_trace()
        # filename_sim = 'gradient_sim_epoch.txt'
        # out_sim_arr = osp.join(save_path, filename_sim)
        # if epoch == 0:
        #     with open(out_sim_arr, 'a') as f:
        #         f.writelines([key + ' ' for key in list(keys)])
        #         f.writelines('\n')
        #         # json.dump(list(keys), f)
        #     print('Gradient_data_key: write into {} has done!'.format(out_sim_arr))
        # loss_sim_matrix_epoch = np.true_divide(self.sim_arr, self.count)
        # with open(out_sim_arr, 'a') as f:
        #     f.writelines(str(epoch))
        #     f.writelines('\n')
        #     for index in range(len(keys)):
        #         sim_arr = self.loss_sim_matrix_epoch[index]
        #         f.writelines([str(sim) + ' ' for sim in sim_arr])
        #         f.writelines('\n')
        #     f.writelines('\n')
        # print('Gradient_sim: write into {} has done!'.format(out_sim_arr))

        """
            write loss gradient magnitude to file [n] for each epoch
        """
        # pdb.set_trace()
        filename = 'gradient_magnitude_all_epoch.txt'
        out_grads_magnitude_all = osp.join(save_path, filename)
        if epoch == 0:
            with open(out_grads_magnitude_all, 'w') as f:
                f.writelines([key + ' ' for key in list(keys)])
                f.writelines('\n')
                # json.dump(list(keys), f)
            print('Gradient_magnitude_all_key: write into {} has done!'.format(out_grads_magnitude_all))

        loss_grad_epoch = np.true_divide(self.grad_magnitude_all, self.count_grad_magnitude_all)
        with open(out_grads_magnitude_all, 'a') as f:
            # json.dump(loss_grad_epoch, f)
            f.writelines([str(grad) + ' ' for grad in loss_grad_epoch])
            f.writelines('\n')
        print('Gradient_magnitude_all: write into {} has done!'.format(out_grads_magnitude_all))
        filename = 'gradient_magnitude_layer2_epoch.txt'
        out_grads_magnitude_layer2 = osp.join(save_path, filename)
        if epoch == 0:
            with open(out_grads_magnitude_layer2, 'w') as f:
                f.writelines([key + ' ' for key in list(keys)])
                f.writelines('\n')
                # json.dump(list(keys), f)
            print('Gradient_magnitude_layer2_key: write into {} has done!'.format(out_grads_magnitude_layer2))

        loss_grad_epoch = np.true_divide(self.grad_magnitude_layer2, self.count_grad_magnitude_layer2)
        with open(out_grads_magnitude_layer2, 'a') as f:
            # json.dump(loss_grad_epoch, f)
            f.writelines([str(grad) + ' ' for grad in loss_grad_epoch])
            f.writelines('\n')
        print('Gradient_magnitude_layer2: write into {} has done!'.format(out_grads_magnitude_layer2))
        filename = 'gradient_magnitude_layer3_epoch.txt'
        out_grads_magnitude_layer3 = osp.join(save_path, filename)
        if epoch == 0:
            with open(out_grads_magnitude_layer3, 'w') as f:
                f.writelines([key + ' ' for key in list(keys)])
                f.writelines('\n')
                # json.dump(list(keys), f)
            print('Gradient_magnitude_layer3_key: write into {} has done!'.format(out_grads_magnitude_layer3))

        loss_grad_epoch = np.true_divide(self.grad_magnitude_layer3, self.count_grad_magnitude_layer3)
        with open(out_grads_magnitude_layer3, 'a') as f:
            # json.dump(loss_grad_epoch, f)
            f.writelines([str(grad) + ' ' for grad in loss_grad_epoch])
            f.writelines('\n')
        print('Gradient_magnitude_layer3: write into {} has done!'.format(out_grads_magnitude_layer3))



        # pdb.set_trace()



        # if epoch == 0:
        #     # pdb.set_trace()
        #
        #     self.sim_data_matrix['keys'] = list(keys)
        #
        # # epoch = runner._inner_iter
        # sim_epoch_arr = np.zeros((self.loss_num, self.loss_num))
        # # keys = loss_all.keys()
        # for i, keys_i in enumerate(keys):
        #     for j, keys_j in enumerate(keys):
        #         sim_epoch_arr[i][j] = self.sim_arr[i][j] / self.count[i][j]
        #
        # epoch_data = {'epoch': epoch, 'sim': sim_epoch_arr.tolist()}
        # self.sim_data_matrix['sims_data'].append(epoch_data)
        #
        # if epoch == runner._max_epochs - 1:
        #     # pdb.set_trace()
        #     filename = 'gradient_sim_epoch.json'
        #     out = osp.join(save_path, filename)
        #     with open(out, 'w') as f:
        #         json.dump(self.sim_data_matrix, f)
        #     print('Gradient_data: write into {} has done!'.format(out))


    def before_iter(self, runner):
        # pdb.set_trace()
        assert self.sim_arr is not None
        assert self.count is not None


    def after_iter(self, runner):#backbone:159,model:284
        # pdb.set_trace()
        # runner.optimizer.zero_grad()
        # if self.detect_anomalous_params:
        #     self.detect_anomalous_parameters(runner.outputs['loss'], runner)

        # pdb.set_trace()
        # iter =
        # if runner._iter%1902 > 900:
        #     # pdb.set_trace()
        # print(runner._iter%1902)
        loss_all = runner.outputs['loss_dict']
        model = runner.model

        assert len(loss_all.keys()) == self.loss_num

        # loss_grads = dict()
        # runner.optimizer.zero_grad()
        # # runner.model.zero_grad()
        # runner.outputs['loss_dict']['loss_bbox'].backward(retain_graph=True)
        # runner.model.zero_grad()
        # pdb.set_trace()

        # params = list(
        #     filter(lambda p: p.requires_grad and p.grad is not None, runner.model.parameters()))
        # print(len(params))
        #
        # m=[]
        # for group in runner.optimizer.param_groups:
        #     for p in group['params']:
        #         if p.grad is not None:
        #             m.append(p.grad)
        # print(len(m))
        # pdb.set_trace()

        # m=0
        # n=0
        # k=0
        # for key, value in runner.model.module.backbone.named_parameters():  # layer2,layer3
        #     m=m+1
        #
        #     # if key == 'layer2.0.conv1.weight':
        #     #     pdb.set_trace()
        #     if 'layer4' in key:
        #         continue
        #         # pdb.set_trace()
        #     k=k+1
        #     if value.requires_grad:
        #         n=n+1
        #         # pdb.set_trace()
        #
        #         temp = {key: copy.deepcopy(value.grad)}
        #         # temp = {key: value.grad.data}
        #         # temp = {key: value.grad.clone()}
        #         # temp = {key: value.grad.clone().detach()}
        #         # temp = {key: value.clone().detach().grad}
        #         loss_grads.update(temp)
        # print(m)
        # print(n)
        # print(k)
        # runner.model.zero_grad()

        loss_grads = []
        for loss_name, loss_value in loss_all.items():
            # print(loss_name)

            # j=0
            # for group in runner.optimizer.param_groups:
            #     for p in group['params']:
            #         if p.grad is not None:
            #             pdb.set_trace()
            #             break
            #         j=j+1

            # for key, value in model.module.backbone.named_parameters():  # layer2,layer3
            #     if key == 'layer2.0.conv1.weight':
            #         pdb.set_trace()
            #
            # pdb.set_trace()
            runner.optimizer.zero_grad() #####
            # runner.model.zero_grad()

            # l = 0
            # for group in runner.optimizer.param_groups:
            #     for p in group['params']:
            #         if p.grad is not None:
            #             pdb.set_trace()
            #             break
            #         l = l+1
            # for key, value in model.module.backbone.named_parameters():  # layer2,layer3
            #     if key == 'layer1.0.conv1.weight':
            #         pdb.set_trace()
            #     if key == 'layer2.0.conv1.weight':
            #         pdb.set_trace()
            condition1 = loss_value == 0 and loss_name=='loss_tri_alignps'
            condition2 = loss_value == 0 and loss_name=='loss_attr'
            flag=False
            try:
                if condition1 or condition2:
                    if condition1:
                        loss_all['loss_oim_alignps'].backward(retain_graph=True)
                        runner.optimizer.zero_grad()  #####
                    print('======')
                    print('condition1(loss_tri):{}'.format(condition1))
                    print('condition2(loss_attr):{}'.format(condition2))
                    print('======')
                    flag=True
                else:
                    loss_value.backward(retain_graph=True) ####

                # loss_value.backward(retain_graph=True)  ####
                # if loss_name=='loss_tri_alignps':
                #     pdb.set_trace()
                #     model.module.bbox_head.labeled_matching_layer.counter_alignps = model.module.bbox_head.labeled_matching_layer.counter_alignps + 1
                #     pdb.set_trace()
                # else:
                #     loss_value.backward(retain_graph=True)  ####
                # raise RuntimeError
            except RuntimeError as e:
                print(e)
                pdb.set_trace()

            # w = 0
            # for group in runner.optimizer.param_groups:
            #     for p in group['params']:
            #         if p.grad is not None:
            #             pdb.set_trace()
            #             break
            #         w = w+1

            # loss_grad=[]
            loss_grad_dict = dict()
            # pdb.set_trace()
            # model = runner.model
            # n=0
            for key, value in model.module.backbone.named_parameters():#layer2,layer3
                # if key == 'layer1.0.conv1.weight':
                #     pdb.set_trace()
                # if key == 'layer2.0.conv1.weight':
                #     pdb.set_trace()
                # if key == 'layer2.0.conv1.weight' and loss_name=='loss_oim':
                #     pdb.set_trace()
                #     print(value.grad)

                if 'layer4' in key:
                    continue
                    # pdb.set_trace()
                # n=n+1
                if value.requires_grad:
                    # pdb.set_trace()
                    if self.gradient_layer == 'layer2':
                        if 'layer2' not in key:
                            continue
                    if self.gradient_layer == 'layer3':
                        if 'layer3' not in key:
                            continue
                    if value.grad is None:
                        pdb.set_trace()
                    temp = {key: copy.deepcopy(value.grad)}
                    if flag:
                        assert len(value.grad.nonzero()) == 0
                    # temp = {key: value.grad.data}
                    # temp = {key: value.grad.clone()}
                    # temp = {key: value.grad.clone().detach()}
                    # print('==')
                    loss_grad_dict.update(temp)
            loss_grads.append(loss_grad_dict)
            # if flag:
            #     pdb.set_trace()
            # pdb.set_trace()
            # m=0
            # for group in runner.optimizer.param_groups:
            #     for p in group['params']:
            #         m=m+1
            #         if p.grad is None:
            #             loss_grad.append(torch.zeros_like(p).to(p.device))
            #             continue
            #         loss_grad.append(p.grad.clone())
            # loss_grads.append(loss_grad)
            # pdb.set_trace()

        # pdb.set_trace()


        # for key in range(len(loss_grads[0])):
        # dict_keys(
        #     ['layer2.0.conv1.weight', 'layer2.0.conv2.weight', 'layer2.0.conv3.weight', 'layer2.0.downsample.0.weight',
        #      'layer2.1.conv1.weight', 'layer2.1.conv2.weight', 'layer2.1.conv3.weight', 'layer2.2.conv1.weight',
        #      'layer2.2.conv2.weight', 'layer2.2.conv3.weight', 'layer2.3.conv1.weight', 'layer2.3.conv2.weight',
        #      'layer2.3.conv3.weight', 'layer3.0.conv1.weight', 'layer3.0.conv2.weight', 'layer3.0.conv3.weight',
        #      'layer3.0.downsample.0.weight', 'layer3.1.conv1.weight', 'layer3.1.conv2.weight', 'layer3.1.conv3.weight',
        #      'layer3.2.conv1.weight', 'layer3.2.conv2.weight', 'layer3.2.conv3.weight', 'layer3.3.conv1.weight',
        #      'layer3.3.conv2.weight', 'layer3.3.conv3.weight', 'layer3.4.conv1.weight', 'layer3.4.conv2.weight',
        #      'layer3.4.conv3.weight', 'layer3.5.conv1.weight', 'layer3.5.conv2.weight', 'layer3.5.conv3.weight'])
        # for key in loss_grads[0].keys():#32
        #     loss_grads_key = []  # 11
        #     for loss_grad_tmp in loss_grads:
        #         loss_grads_key.append(loss_grad_tmp[key])
        #     for i, loss_i_grad in enumerate(loss_grads_key):
        #         if loss_i_grad is not None:
        #             loss_i_grad_ = loss_i_grad.view(-1)
        #             for j, loss_j_grad in enumerate(loss_grads_key):
        #                 if loss_j_grad is not None:
        #                     loss_j_grad_ = loss_j_grad.view(-1)
        #                     if loss_i_grad_.mean() != 0 and loss_j_grad_.mean() != 0:
        #                         # pdb.set_trace()
        #                         # loss_i_grad_.shape = torch.Size([32768])
        #                         cos_sim = torch.nn.functional.cosine_similarity(loss_i_grad_, loss_j_grad_, dim=0)
        #                         self.count[i][j] = self.count[i][j] + 1
        #                         self.sim_arr[i][j] = self.sim_arr[i][j] + cos_sim.cpu().numpy()

        # pdb.set_trace()
        # print("hhhhhhhhhhh=======")
        # loss_grads_arr = dict()
        for index in range(len(loss_all.keys())):
            # if loss_name not in loss_grads_dict.keys():

            for key in loss_grads[0].keys():
                loss_grad = loss_grads[index][key]
                assert loss_grad is not None
                loss_grad_ = loss_grad.view(-1).cpu().numpy()
                magnitude = np.sqrt((loss_grad_ * loss_grad_).sum())
                if 'layer2' in key:
                    self.grad_magnitude_layer2[index] = self.grad_magnitude_layer2[index] + magnitude
                    self.count_grad_magnitude_layer2[index] = self.count_grad_magnitude_layer2[index] + 1
                if 'layer3' in key:
                    self.grad_magnitude_layer3[index] = self.grad_magnitude_layer3[index] + magnitude
                    self.count_grad_magnitude_layer3[index] = self.count_grad_magnitude_layer3[index] + 1
                self.grad_magnitude_all[index] = self.grad_magnitude_all[index] + magnitude

                # self.loss_grads_arr[index] = self.loss_grads_arr[index] + loss_grad_
                self.count_grad_magnitude_all[index] = self.count_grad_magnitude_all[index] + 1
        # pdb.set_trace()


def plot_point(point, angle, length, save_path, filename, loss_i, loss_j):
    # pdb.set_trace()
    x, y = point

    # endy = y + length*math.sin(angle)
    # endx = length * math.cos(angle)

    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111)

    # if len(angle) > 1:
    colors = ['r']
    labels = [loss_i]
    # else:
    #     colors = ['r']

    for i, ang in enumerate([angle]):
        endy = y + length * math.sin(ang)
        endx = length * math.cos(ang)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.set_ylim([-1.5, 1.5])
        ax.set_xlim([-1.5, 1.5])

        ax.plot([x, endx], [y, endy], color=colors[i], label=labels[i])
        ax.arrow(x, y, endx - x, endy - y, length_includes_head=True, head_width=0.05, lw=1, color=colors[i],
                 label=labels[i])
    ax.plot([x, x + length], [y, y], color='black', label=loss_j)
    ax.arrow(x, y, length, 0, length_includes_head=True, head_width=0.05, lw=1, color='black', label=loss_j)
    ax.legend(shadow=True, fancybox=True)
    # pdb.set_trace()

    plt.yticks([])
    plt.xticks([])
    mmcv.mkdir_or_exist(osp.abspath(save_path))
    # fig.show()
    fig.savefig(osp.join(save_path, filename))