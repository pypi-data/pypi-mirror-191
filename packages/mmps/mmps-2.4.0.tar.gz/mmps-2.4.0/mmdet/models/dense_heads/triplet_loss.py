import torch
import pdb
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable

class TripletLossFilter(nn.Module):
    """Triplet loss with hard positive/negative mining.

    Reference:
    Hermans et al. In Defense of the Triplet Loss for Person Re-Identification. arXiv:1703.07737.

    Code imported from https://github.com/Cysu/open-reid/blob/master/reid/loss/triplet.py.

    Args:
        margin (float): margin for triplet.
    """
    def __init__(self, margin=0.3):
        super(TripletLossFilter, self).__init__()
        self.margin = margin
        self.ranking_loss = nn.MarginRankingLoss(margin=margin)

    def forward(self, inputs, targets):
        """
        Does not calculate noise inputs with label -1
        Args:
            inputs: feature matrix with shape (batch_size, feat_dim)
            targets: ground truth labels with shape (num_classes)
        """

        # print(inputs.shape, targets.shape)#[680,256],[680]
        inputs_new = []
        targets_new = []
        targets_value = []
        for i in range(len(targets)):
            if targets[i] == -1:
                continue
            else:
                inputs_new.append(inputs[i])
                targets_new.append(targets[i])
                targets_value.append(targets[i].cpu().numpy().item())
        if len(set(targets_value)) < 2:
            # print('====triplet_loss: len(set(targets_value)) < 2====')
            # tmp_loss = torch.zeros(1, requires_grad=True)
            # tmp_loss = torch.zeros(1, device=targets.device)
            # tmp_loss = Variable(tmp_loss, requires_grad=True)


            tmp_loss = torch.zeros(1)
            tmp_loss = tmp_loss[0]
            tmp_loss = tmp_loss.to(targets.device)
            return tmp_loss
        #print(targets_value)
        # pdb.set_trace()
        inputs_new = torch.stack(inputs_new)#[657,256]
        targets_new = torch.stack(targets_new)
        #print(inputs_new.shape, targets_new.shape)
        n = inputs_new.size(0)
        # Compute pairwise distance, replace by the official when merged
        dist = torch.pow(inputs_new, 2).sum(dim=1, keepdim=True).expand(n, n) #[657, 1]->[657,657]
        dist = dist + dist.t()
        dist.addmm_(1, -2, inputs_new, inputs_new.t())# 1*dist-2*(inputs_new @ inputs_new.t())
        dist = dist.clamp(min=1e-12).sqrt()  # for numerical stability
        # sqrt(x**2+y**2-2xy)即sqrt((x-y)**2)),算input中每一个feature与其他feature的欧式距离
        #print("Triplet ", dist)
        # For each anchor, find the hardest positive and negative
        mask = targets_new.expand(n, n).eq(targets_new.expand(n, n).t())
        #print(mask)
        dist_ap, dist_an = [], []
        for i in range(n):
            dist_ap.append(dist[i][mask[i]].max())#取跟anchor距离值最大的正样本
            dist_an.append(dist[i][mask[i] == 0].min())#取跟anchor距离值最小的负样本
            # 正样本中相似度最小的》》负样本中相似度最大的
        #dist_ap = torch.cat(dist_ap)
        #dist_an = torch.cat(dist_an)
        # pdb.set_trace()
        dist_ap = torch.stack(dist_ap)#【657】
        dist_an = torch.stack(dist_an)#【657】
        # Compute ranking hinge loss
        y = torch.ones_like(dist_an)
        #y = dist_an.data.new()
        #y.resize_as_(dist_an.data)
        #y.fill_(1)
        #y = Variable(y)
        loss = self.ranking_loss(dist_an, dist_ap, y) #y=1表示dist_an排序排在dist_ap之前,即dist_an>dist_ap。
        # nn.MarginRankingLoss(margin=margin)   (x1,x2,y) loss=max(0, -y*(x1-x2)+margin)
        #y=1表示x1排序排在x2之前, x1>x2。
        return loss