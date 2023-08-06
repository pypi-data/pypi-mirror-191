import torch
import pdb
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

EPS = 1e-12


class Weighted_BCELoss(object):
    """
        Weighted_BCELoss was proposed in "Multi-attribute learning for pedestrian attribute recognition in surveillance scenarios"[13].
    """
    def __init__(self, experiment=None):
        super(Weighted_BCELoss, self).__init__()
        self.weights = None
        if experiment == 'pa100k':
            self.weights = torch.Tensor([0.460444444444,
                                        0.0134555555556,
                                        0.924377777778,
                                        0.0621666666667,
                                        0.352666666667,
                                        0.294622222222,
                                        0.352711111111,
                                        0.0435444444444,
                                        0.179977777778,
                                        0.185,
                                        0.192733333333,
                                        0.1601,
                                        0.00952222222222,
                                        0.5834,
                                        0.4166,
                                        0.0494777777778,
                                        0.151044444444,
                                        0.107755555556,
                                        0.0419111111111,
                                        0.00472222222222,
                                        0.0168888888889,
                                        0.0324111111111,
                                        0.711711111111,
                                        0.173444444444,
                                        0.114844444444,
                                        0.006]).cuda()
        elif experiment == 'rap':
            self.weights = torch.Tensor([0.311434,
                                        0.009980,
                                        0.430011,
                                        0.560010,
                                        0.144932,
                                        0.742479,
                                        0.097728,
                                        0.946303,
                                        0.048287,
                                        0.004328,
                                        0.189323,
                                        0.944764,
                                        0.016713,
                                        0.072959,
                                        0.010461,
                                        0.221186,
                                        0.123434,
                                        0.057785,
                                        0.228857,
                                        0.172779,
                                        0.315186,
                                        0.022147,
                                        0.030299,
                                        0.017843,
                                        0.560346,
                                        0.000553,
                                        0.027991,
                                        0.036624,
                                        0.268342,
                                        0.133317,
                                        0.302465,
                                        0.270891,
                                        0.124059,
                                        0.012432,
                                        0.157340,
                                        0.018132,
                                        0.064182,
                                        0.028111,
                                        0.042155,
                                        0.027558,
                                        0.012649,
                                        0.024504,
                                        0.294601,
                                        0.034099,
                                        0.032800,
                                        0.091812,
                                        0.024552,
                                        0.010388,
                                        0.017603,
                                        0.023446,
                                        0.128917]).cuda()
        elif experiment == 'peta':
            self.weights = torch.Tensor([0.5016,
                                        0.3275,
                                        0.1023,
                                        0.0597,
                                        0.1986,
                                        0.2011,
                                        0.8643,
                                        0.8559,
                                        0.1342,
                                        0.1297,
                                        0.1014,
                                        0.0685,
                                        0.314,
                                        0.2932,
                                        0.04,
                                        0.2346,
                                        0.5473,
                                        0.2974,
                                        0.0849,
                                        0.7523,
                                        0.2717,
                                        0.0282,
                                        0.0749,
                                        0.0191,
                                        0.3633,
                                        0.0359,
                                        0.1425,
                                        0.0454,
                                        0.2201,
                                        0.0178,
                                        0.0285,
                                        0.5125,
                                        0.0838,
                                        0.4605,
                                        0.0124]).cuda()
        #self.weights = None

    def forward(self, output, target):
        if self.weights is not None:
            cur_weights = torch.exp(target + (1 - target * 2) * self.weights)
            loss = cur_weights *  (target * torch.log(output + EPS)) + ((1 - target) * torch.log(1 - output + EPS))
        else:
            loss = target * torch.log(output + EPS) + (1 - target) * torch.log(1 - output + EPS)
        return torch.neg(torch.mean(loss))