# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
import torch
import torch.nn.functional as F
from torch import nn

# from models.da_loss import DALossComputation


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
            t = F.relu(self.conv1_da(feature))
            img_features.append(self.conv2_da(t))
        return img_features




class DomainAdaptationModule(torch.nn.Module):
    """
    Module for Domain Adaptation Component. Takes feature maps from the backbone and instance
    feature vectors, domain labels and proposals. Works for both FPN and non-FPN.
    """

    def __init__(self,num_domain=2,img_weight=1.0):
        super(DomainAdaptationModule, self).__init__()

        self.img_weight = img_weight  # cfg.MODEL.DA_HEADS.DA_IMG_LOSS_WEIGHT

        self.grl_img = GradientScalarLayer(-1.0 * 0.1)

        self.imghead = DAImgHead(1024,num_domain)
        self.loss_evaluator = DALossComputation()
        # self.weight_da_loss=weight_da_loss

    def forward(self, img_features,
                targets=None):
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

        if self.training:
            da_img_loss= self.loss_evaluator(
                da_img_features,
                targets
            )

            losses = {}
            if self.img_weight > 0:
                losses["loss_da_image"] = self.img_weight * da_img_loss

            return losses
        return {}


class DALossComputation(object):
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

    def __call__(self, da_img, targets):
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
        return da_img_loss
