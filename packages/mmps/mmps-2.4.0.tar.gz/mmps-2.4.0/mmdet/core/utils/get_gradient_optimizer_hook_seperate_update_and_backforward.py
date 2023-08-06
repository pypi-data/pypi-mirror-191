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

from mmcv.runner import HOOKS, Hook, OptimizerHook


@HOOKS.register_module()
class GetGradientOptimizerHook_LUT_UPDATE(OptimizerHook):

    def __init__(self, loss_num, **kwargs):
        super(GetGradientOptimizerHook_LUT_UPDATE, self).__init__(**kwargs)
        self.sim_arr = np.zeros((loss_num, loss_num))
        self.count = np.zeros((loss_num, loss_num))
        self.loss_num = loss_num

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
        #                 '/visual/weight_grl'
        # else:
        #     save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
        #                 '/visual/weight_grl'
        # pdb.set_trace()

        save_path = './work_dirs/' + runner.meta['exp_name'].split('.')[0] + \
                    '/visual/weight_grl'
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

    def before_iter(self, runner):
        # pdb.set_trace()
        assert self.sim_arr is not None
        assert self.count is not None


    def after_train_iter(self, runner):#backbone:159,model:284

        loss_all = runner.outputs['loss_dict']
        model = runner.model

        assert len(loss_all.keys()) == self.loss_num
        # pdb.set_trace()

        loss_grads = []
        for loss_name, loss_value in loss_all.items():
            # print(loss_name)

            runner.optimizer.zero_grad() #####
            flag=False
            try:
                if loss_value.requires_grad:
                    loss_value.backward(retain_graph=True) ####
                else:
                    # print(loss_name)
                    flag=True
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
                    temp = {key: copy.deepcopy(value.grad)}
                    if flag:
                        assert len(value.grad.nonzero()) == 0
                    loss_grad_dict.update(temp)
            loss_grads.append(loss_grad_dict)

        for index in range(len(loss_all.keys())):

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

        runner.optimizer.zero_grad()
        # if self.detect_anomalous_params:
        #     self.detect_anomalous_parameters(runner.outputs['loss'], runner)
        # pdb.set_trace()
        runner.outputs['loss'].backward()

        # model.module.roi_head.bbox_head.loss_oim.update_lut_and_queue_nae()
        # model.module.bbox_head.unlabeled_matching_layer.update_queue()
        # model.module.bbox_head.labeled_matching_layer.update_lut()

        model.module.bbox_head.unlabeled_matching_layer.update_queue()
        model.module.bbox_head.labeled_matching_layer.update_lut()


        if self.grad_clip is not None:
            grad_norm = self.clip_grads(runner.model.parameters())
            if grad_norm is not None:
                # Add grad norm to the logger
                runner.log_buffer.update({'grad_norm': float(grad_norm)},
                                         runner.outputs['num_samples'])
        runner.optimizer.step()
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