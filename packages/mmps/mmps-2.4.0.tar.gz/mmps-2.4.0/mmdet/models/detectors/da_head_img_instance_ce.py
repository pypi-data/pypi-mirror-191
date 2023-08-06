# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
import pdb

import torch
import torch.nn.functional as F
from torch import nn

# from models.da_loss import DALossComputation

def consistency_loss(img_feas, ins_fea, size_average=True):
    """
    Consistency regularization as stated in the paper
    `Domain Adaptive Faster R-CNN for Object Detection in the Wild`
    L_cst = \sum_{i,j}||\frac{1}{|I|}\sum_{u,v}p_i^{(u,v)}-p_{i,j}||_2
    """
    loss = []
    len_ins = ins_fea.size(0)
    # intervals = [torch.nonzero(ins_labels).size(0), len_ins-torch.nonzero(ins_labels).size(0)]
    for img_fea_per_level in img_feas:
        N, A, H, W = img_fea_per_level.shape
        img_fea_per_level = torch.mean(img_fea_per_level.reshape(N, -1), 1)
        img_feas_per_level = []
        # if N!=2:
        #     return 0
        # assert N==2, \
        #     "only batch size=2 is supported for consistency loss now, received batch size: {}".format(N)
        for i in range(N):
            # img_fea_mean = img_fea_per_level[i].view(1, 1).repeat(intervals[i], 1)
            img_fea_mean = img_fea_per_level[i].view(1, 1).repeat(len_ins//N, 1)
            img_feas_per_level.append(img_fea_mean)
        if len_ins%N!=0:
            img_feas_per_level.append(img_fea_per_level[N-1].view(1, 1).repeat(len_ins%N, 1))
        img_feas_per_level = torch.cat(img_feas_per_level, dim=0)
        loss_per_level = torch.abs(img_feas_per_level - ins_fea)
        loss.append(loss_per_level)
    loss = torch.cat(loss, dim=1)
    if size_average:
        return loss.mean()
    return loss.sum()

class _GradientScalarLayer(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, weight):
        ctx.weight = weight
        return input.view_as(input)

    @staticmethod
    def backward(ctx, grad_output):
        grad_input = grad_output.clone()
        return ctx.weight * grad_input, None


gradient_scalar = _GradientScalarLayer.apply


class GradientScalarLayer(torch.nn.Module):
    def __init__(self, weight):
        super(GradientScalarLayer, self).__init__()
        self.weight = weight

    def forward(self, input):
        return gradient_scalar(input, self.weight)

    def __repr__(self):
        tmpstr = self.__class__.__name__ + "("
        tmpstr += "weight=" + str(self.weight)
        tmpstr += ")"
        return tmpstr


class DAImgHead(nn.Module):
    """
    Adds a simple Image-level Domain Classifier head
    """

    def __init__(self, in_channels,num_domain):
        """
        Arguments:
            in_channels (int): number of channels of the input feature
            USE_FPN (boolean): whether FPN feature extractor is used
        """
        super(DAImgHead, self).__init__()

        self.conv1_da = nn.Conv2d(in_channels, 512, kernel_size=1, stride=1)
        # self.conv2_da = nn.Conv2d(512, 1, kernel_size=1, stride=1)
        self.conv2_da = nn.Conv2d(512, num_domain, kernel_size=1, stride=1)

        for l in [self.conv1_da, self.conv2_da]:
            torch.nn.init.normal_(l.weight, std=0.001)
            torch.nn.init.constant_(l.bias, 0)

    def forward(self, x):
        img_features = []
        for feature in x:
            # print('????????shape:{}'.format(feature.shape))
            t = F.relu(self.conv1_da(feature))
            img_features.append(self.conv2_da(t))
        return img_features

class DAInsHead(nn.Module):
    """
    Adds a simple Instance-level Domain Classifier head
    """

    def __init__(self, in_channels,num_domain):
        """
        Arguments:
            in_channels (int): number of channels of the input feature
        """
        super(DAInsHead, self).__init__()
        self.fc1_da = nn.Linear(in_channels, 1024)
        self.fc2_da = nn.Linear(1024, 1024)
        self.fc3_da = nn.Linear(1024, num_domain)
        # self.fc3_da = nn.Linear(1024, 1)
        for l in [self.fc1_da, self.fc2_da]:
            nn.init.normal_(l.weight, std=0.01)
            nn.init.constant_(l.bias, 0)
        nn.init.normal_(self.fc3_da.weight, std=0.05)
        nn.init.constant_(self.fc3_da.bias, 0)

    def forward(self, x):
        # print("!!!shape={}".format(x.shape))
        x = F.relu(self.fc1_da(x))
        x = F.dropout(x, p=0.5, training=self.training)

        x = F.relu(self.fc2_da(x))
        x = F.dropout(x, p=0.5, training=self.training)

        x = self.fc3_da(x)
        return x



class DomainAdaptationModule(torch.nn.Module):
    """
    Module for Domain Adaptation Component. Takes feature maps from the backbone and instance
    feature vectors, domain labels and proposals. Works for both FPN and non-FPN.
    """

    def __init__(self,num_domain=2,img_weight=1.0, ins_weight=1.0,cst_weight=-0.1,
                 imgda_channel=1024,insda_channel=2048):
        super(DomainAdaptationModule, self).__init__()

        self.img_weight = img_weight  # cfg.MODEL.DA_HEADS.DA_IMG_LOSS_WEIGHT
        self.ins_weight = ins_weight #cfg.MODEL.DA_HEADS.DA_INS_LOSS_WEIGHT
        self.cst_weight = cst_weight #cfg.MODEL.DA_HEADS.DA_CST_LOSS_WEIGHT

        self.grl_img = GradientScalarLayer(-1.0 * 0.1)
        self.grl_ins = GradientScalarLayer(-1.0 * 0.1)
        self.grl_img_consist = GradientScalarLayer(1.0 * 0.1)
        self.grl_ins_consist = GradientScalarLayer(1.0 * 0.1)

        # self.imghead = DAImgHead(1024,num_domain)
        # self.inshead = DAInsHead(2048,num_domain)
        self.imghead = DAImgHead(imgda_channel, num_domain)
        self.inshead = DAInsHead(insda_channel, num_domain)
        self.loss_evaluator = DALossComputation()
        # self.weight_da_loss=weight_da_loss

    def forward(self, img_features,
                targets=None, instance_features=None,
                instance_domians=None
                ):
        """
        Arguments:
            img_features (list[Tensor]): features computed from the images that are
                used for computing the predictions.
            da_ins_feature (Tensor): instance-level feature vectors
            da_ins_labels (Tensor): domain labels for instance-level feature vectors
            targets (list[BoxList): ground-truth boxes present in the image (optional)

        Returns:
            losses (dict[Tensor]): the losses for the model during training. During
                testing, it is an empty dict.
        """
        # print('input.shape={}'.format(img_features[0].shape))
        img_grl_fea = [self.grl_img(fea) for fea in img_features]
        # print('imghead.shape={}'.format(img_grl_fea[0].shape))
        # print('len--imghead.shape={}'.format(len(img_grl_fea)))
        da_img_features = self.imghead(img_grl_fea)

        # pdb.set_trace()
        ins_num=instance_features.size(0)
        da_ins_feaure=instance_features.view(ins_num,-1)
        ins_grl_fea=self.grl_ins(da_ins_feaure)
        da_ins_features=self.inshead(ins_grl_fea)

        img_grl_consist_fea = [self.grl_img_consist(fea) for fea in img_features]
        ins_grl_consist_fea = self.grl_ins_consist(da_ins_feaure)

        # ins_num_per_img=ins_num//len(targets)
        # ins_targets_list=[]
        # for i in range(len(targets)):
        #     ins_target_per_img=torch.stack([targets[i]] * ins_num_per_img)
        #     ins_targets_list.append(ins_target_per_img)
        # ins_targets=torch.cat(ins_targets_list)
        ins_targets=instance_domians
        # pdb.set_trace()
        if ins_targets is not None and ins_targets.shape[0] != da_ins_features.shape[0]:
            print('===ins_target.shape={}'.format(ins_targets.shape))#336
            print('===ins_features.shape={}'.format(instance_features.shape))#338
            pdb.set_trace()

        if self.training:
            da_img_loss, da_ins_loss, da_cst_loss= self.loss_evaluator(
                da_img_features,
                targets,
                da_ins_features,
                ins_targets,
                img_grl_consist_fea,
                ins_grl_consist_fea
            )


            losses = {}
            if self.img_weight > 0:
                losses["loss_da_image"] = self.img_weight * da_img_loss
            if self.ins_weight > 0:
                losses["loss_da_ins"] = self.ins_weight * da_ins_loss
            if self.ins_weight > 0:
                losses["loss_da_consist"] = self.cst_weight * da_cst_loss

            return losses
        return {}


class DALossComputation(object):
    """
    This class computes the DA loss.
    """

    def __init__(self):
        # self.avgpool = nn.AvgPool2d(kernel_size=7, stride=7)
        self.loss = nn.CrossEntropyLoss()

    def prepare_masks(self, targets):
        masks = []
        for targets_per_image in targets:
            # is_source = targets_per_image["domain_labels"]
            # mask_per_image = is_source.new_ones(1, dtype=torch.bool) if is_source.any() else is_source.new_zeros(1,
            #           
            # targets_per_image                                                                                 dtype=torch.bool)
            mask_per_image=targets_per_image
            masks.append(mask_per_image)
        return masks

    def __call__(self, da_img, targets,da_ins_features, ins_targets,da_img_consist,da_ins_consist):
        """
        Arguments:
            da_img (list[Tensor])
            da_img_consist (list[Tensor])
            da_ins (Tensor)
            da_ins_consist (Tensor)
            da_ins_labels (Tensor)
            targets (list[BoxList])

        Returns:
            da_img_loss (Tensor)
            da_ins_loss (Tensor)
            da_consist_loss (Tensor)
        """

        # masks = self.prepare_masks(targets)
        # masks = torch.cat(masks, dim=0)
        # masks = torch.stack(targets)

        da_img_flattened = []
        da_img_labels_flattened = []
        # for each feature level, permute the outputs to make them be in the
        # same format as the labels. Note that the labels are computed for
        # all feature levels concatenated, so we keep the same representation
        # for the image-level domain alignment

        loss=[]
        for da_img_per_level in da_img:
            N, A, H, W = da_img_per_level.shape
            # da_img_per_level = da_img_per_level.permute(0, 2, 3, 1)
            # da_img_label_per_level = torch.zeros_like(da_img_per_level, dtype=torch.float32)
            da_img_label_per_level=torch.zeros((N,H,W),dtype=torch.long,device=da_img_per_level.device)
            for i, t in enumerate(targets):
                da_img_label_per_level[i,:]=t
            # da_img_label_per_level[masks, :] = 1

            da_img_per_level = da_img_per_level.reshape(N, A,-1)
            da_img_label_per_level = da_img_label_per_level.reshape(N, -1)
            loss_per_level=self.loss(da_img_per_level,da_img_label_per_level)
            loss.append(loss_per_level)

        da_img_loss=sum(loss)
        # pdb.set_trace()
        da_ins_loss=self.loss(da_ins_features, ins_targets.long())
        da_consist_loss = consistency_loss(da_img_consist, da_ins_consist, size_average=True)

        # pdb.set_trace()

        return da_img_loss, da_ins_loss,da_consist_loss

class DomainAdaptationModule_(torch.nn.Module):
    """
    Module for Domain Adaptation Component. Takes feature maps from the backbone and instance
    feature vectors, domain labels and proposals. Works for both FPN and non-FPN.
    """

    def __init__(self,num_domain=2,img_weight=1.0, ins_weight=1.0,cst_weight=-0.1):
        super(DomainAdaptationModule_, self).__init__()

        self.img_weight = img_weight  # cfg.MODEL.DA_HEADS.DA_IMG_LOSS_WEIGHT
        self.ins_weight = ins_weight #cfg.MODEL.DA_HEADS.DA_INS_LOSS_WEIGHT
        self.cst_weight = cst_weight #cfg.MODEL.DA_HEADS.DA_CST_LOSS_WEIGHT

        self.grl_img = GradientScalarLayer(-1.0 * 0.1)
        self.grl_ins = GradientScalarLayer(-1.0 * 0.1)
        self.grl_img_consist = GradientScalarLayer(1.0 * 0.1)
        self.grl_ins_consist = GradientScalarLayer(1.0 * 0.1)

        self.imghead = DAImgHead(1024,num_domain)
        # self.inshead = DAInsHead(2048,num_domain)
        self.inshead = DAInsHead(256, num_domain)
        self.loss_evaluator = DALossComputation_()
        # self.weight_da_loss=weight_da_loss

    def forward(self, img_features,
                targets=None, instance_features=None,
                # instance_pids=None
                ):
        """
        Arguments:
            img_features (list[Tensor]): features computed from the images that are
                used for computing the predictions.
            da_ins_feature (Tensor): instance-level feature vectors
            da_ins_labels (Tensor): domain labels for instance-level feature vectors
            targets (list[BoxList): ground-truth boxes present in the image (optional)

        Returns:
            losses (dict[Tensor]): the losses for the model during training. During
                testing, it is an empty dict.
        """



        img_grl_fea = [self.grl_img(fea) for fea in img_features]
        da_img_features = self.imghead(img_grl_fea)

        # pdb.set_trace()
        ins_num=instance_features.size(0)
        da_ins_feaure=instance_features.view(ins_num,-1)
        ins_grl_fea=self.grl_ins(da_ins_feaure)
        da_ins_features=self.inshead(ins_grl_fea)

        img_grl_consist_fea = [self.grl_img_consist(fea) for fea in img_features]
        ins_grl_consist_fea = self.grl_ins_consist(da_ins_feaure)

        ins_num_per_img=ins_num//len(targets)
        ins_targets_list=[]
        for i in range(len(targets)):
            ins_target_per_img=torch.stack([targets[i]] * ins_num_per_img)
            ins_targets_list.append(ins_target_per_img)
        ins_targets=torch.cat(ins_targets_list)

        if self.training:
            da_img_loss, da_ins_loss, da_cst_loss= self.loss_evaluator(
                da_img_features,
                targets,
                da_ins_features,
                ins_targets,
                img_grl_consist_fea,
                ins_grl_consist_fea
            )


            losses = {}
            if self.img_weight > 0:
                losses["loss_da_image"] = self.img_weight * da_img_loss
            if self.ins_weight > 0:
                losses["loss_da_ins"] = self.ins_weight * da_ins_loss
            if self.ins_weight > 0:
                losses["loss_da_consist"] = self.cst_weight * da_cst_loss

            return losses
        return {}


class DALossComputation_(object):
    """
    This class computes the DA loss.
    """

    def __init__(self):
        self.avgpool = nn.AvgPool2d(kernel_size=7, stride=7)
        self.loss = nn.CrossEntropyLoss()

    def prepare_masks(self, targets):
        masks = []
        for targets_per_image in targets:
            # is_source = targets_per_image["domain_labels"]
            # mask_per_image = is_source.new_ones(1, dtype=torch.bool) if is_source.any() else is_source.new_zeros(1,
            #
            # targets_per_image                                                                                 dtype=torch.bool)
            mask_per_image=targets_per_image
            masks.append(mask_per_image)
        return masks

    def __call__(self, da_img, targets,da_ins_features, ins_targets,da_img_consist,da_ins_consist):
        """
        Arguments:
            da_img (list[Tensor])
            da_img_consist (list[Tensor])
            da_ins (Tensor)
            da_ins_consist (Tensor)
            da_ins_labels (Tensor)
            targets (list[BoxList])

        Returns:
            da_img_loss (Tensor)
            da_ins_loss (Tensor)
            da_consist_loss (Tensor)
        """

        # masks = self.prepare_masks(targets)
        # masks = torch.cat(masks, dim=0)
        # masks = torch.stack(targets)

        da_img_flattened = []
        da_img_labels_flattened = []
        # for each feature level, permute the outputs to make them be in the
        # same format as the labels. Note that the labels are computed for
        # all feature levels concatenated, so we keep the same representation
        # for the image-level domain alignment
        loss=[]
        for da_img_per_level in da_img:
            N, A, H, W = da_img_per_level.shape
            # da_img_per_level = da_img_per_level.permute(0, 2, 3, 1)
            # da_img_label_per_level = torch.zeros_like(da_img_per_level, dtype=torch.float32)
            da_img_label_per_level=torch.zeros((N,H,W),dtype=torch.long,device=da_img_per_level.device)
            for i, t in enumerate(targets):
                da_img_label_per_level[i,:]=t
            # da_img_label_per_level[masks, :] = 1

            da_img_per_level = da_img_per_level.reshape(N, A,-1)
            da_img_label_per_level = da_img_label_per_level.reshape(N, -1)
            loss_per_level=self.loss(da_img_per_level,da_img_label_per_level)
            loss.append(loss_per_level)

        da_img_loss=sum(loss)
        da_ins_loss=self.loss(da_ins_features, ins_targets)
        da_consist_loss = consistency_loss(da_img_consist, da_ins_consist, size_average=True)

        # pdb.set_trace()

        return da_img_loss, da_ins_loss,da_consist_loss

