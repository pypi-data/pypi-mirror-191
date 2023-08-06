import torch
import torch.distributed as dist
import torch.nn as nn
from mmcv.runner import get_dist_info
from torch.autograd import Function


@torch.no_grad()
def all_gather_tensor(x, gpu=None, save_memory=False):
    # rank, world_size, is_dist = get_dist_info()
    ank, world_size = get_dist_info()
    # if not is_dist:
    #     return [x]
    if not save_memory:
        # all gather features in parallel
        # cost more GPU memory but less time
        # x = x.cuda(gpu)
        x_gather = [torch.empty_like(x) for _ in range(world_size)]
        dist.all_gather(x_gather, x, async_op=False)
    #         x_gather = torch.cat(x_gather, dim=0)
    else:
        # broadcast features in sequence
        # cost more time but less GPU memory
        container = torch.empty_like(x).cuda(gpu)
        x_gather = []
        for k in range(world_size):
            container.data.copy_(x)
            print("gathering features from rank no.{}".format(k))
            dist.broadcast(container, k)
            x_gather.append(container.cpu())
    #         x_gather = torch.cat(x_gather, dim=0)
    # return cpu tensor
    return x_gather


def undefined_l_gather(features, pid_labels):
    resized_num = 10000
    pos_num = min(features.size(0), resized_num)
    if features.size(0) > resized_num:
        print(f'{features.size(0)}out of {resized_num}')
    resized_features = torch.empty((resized_num, features.size(1))).to(features.device)
    resized_features[:pos_num, :] = features[:pos_num, :]
    resized_pid_labels = torch.empty((resized_num,)).to(pid_labels.device)
    resized_pid_labels[:pos_num] = pid_labels[:pos_num]
    pos_num = torch.tensor([pos_num]).to(features.device)
    all_pos_num = all_gather_tensor(pos_num)
    all_features = all_gather_tensor(resized_features)
    all_pid_labels = all_gather_tensor(resized_pid_labels)
    gather_features = []
    gather_pid_labels = []
    for index, p_num in enumerate(all_pos_num):
        gather_features.append(all_features[index][:p_num, :])
        gather_pid_labels.append(all_pid_labels[index][:p_num])
    gather_features = torch.cat(gather_features, dim=0)
    gather_pid_labels = torch.cat(gather_pid_labels, dim=0)
    return gather_features, gather_pid_labels


class LabeledMatching(Function):
    @staticmethod
    def forward(ctx, features, pid_labels, lookup_table, momentum=0.5):
        # The lookup_table can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        #         ctx.save_for_backward(features, pid_labels)
        gather_features, gather_pid_labels = undefined_l_gather(features, pid_labels)
        ctx.save_for_backward(gather_features, gather_pid_labels)
        ctx.lookup_table = lookup_table
        ctx.momentum = momentum
        scores = features.mm(lookup_table.t())
        # print(features, lookup_table, scores)
        # pos_feats = lookup_table.clone().detach()
        # pos_idx = pid_labels > 0
        # pos_pids = pid_labels[pos_idx]
        # pos_feats = pos_feats[pos_pids]
        # pos_feats.require_grad = False
        # return scores, pos_feats, pos_pids

        return scores

    @staticmethod
    def backward(ctx, grad_output):
        features, pid_labels = ctx.saved_tensors
        pid_labels = pid_labels.long()
        lookup_table = ctx.lookup_table
        momentum = ctx.momentum
        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(lookup_table)
        # Update lookup table, but not by standard backpropagation with gradients
        for indx, label in enumerate(pid_labels):
            if label >= 0:
                lookup_table[label] = (
                        momentum * lookup_table[label] + (1 - momentum) * features[indx]
                )
                # lookup_table[label] /= lookup_table[label].norm()
        return grad_feats, None, None, None


class LabeledMatchingLayer(nn.Module):
    """
    Labeled matching of OIM loss function.
    """

    def __init__(self, num_persons=5532, feat_len=256):
        """
        Args:
            num_persons (int): Number of labeled persons.
            feat_len (int): Length of the feature extracted by the network.
        """
        super(LabeledMatchingLayer, self).__init__()
        self.register_buffer("lookup_table", torch.zeros(num_persons, feat_len))

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, num_persons]): Labeled matching scores, namely the similarities
                                             between proposals and labeled persons.
        """
        scores = LabeledMatching.apply(features, pid_labels, self.lookup_table)
        return scores


class LabeledMatchingNorm(Function):
    @staticmethod
    def forward(ctx, features, pid_labels, lookup_table, momentum=0.5):
        # The lookup_table can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()

        gather_features, gather_pid_labels = undefined_l_gather(features, pid_labels)
        ctx.save_for_backward(gather_features, gather_pid_labels)
        ctx.lookup_table = lookup_table
        ctx.momentum = momentum
        scores = features.mm(lookup_table.t())
        # print(features, lookup_table, scores)
        # pos_feats = lookup_table.clone().detach()
        # pos_idx = pid_labels > 0
        # pos_pids = pid_labels[pos_idx]
        # pos_feats = pos_feats[pos_pids]
        # pos_feats.require_grad = False
        return scores

        # return scores, pos_feats, pos_pids

    @staticmethod
    def backward(ctx, grad_output):

        features, pid_labels = ctx.saved_tensors
        pid_labels = pid_labels.long()
        lookup_table = ctx.lookup_table
        momentum = ctx.momentum
        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(lookup_table)
        # Update lookup table, but not by standard backpropagation with gradients
        for indx, label in enumerate(pid_labels):
            if label >= 0:
                lookup_table[label] = (
                        momentum * lookup_table[label] + (1 - momentum) * features[indx]
                )
                lookup_table[label] /= lookup_table[label].norm()
        return grad_feats, None, None, None


class LabeledMatchingLayerNorm(nn.Module):
    """
    Labeled matching of OIM loss function.
    """

    def __init__(self, num_persons=5532, feat_len=256):
        """
        Args:
            num_persons (int): Number of labeled persons.
            feat_len (int): Length of the feature extracted by the network.
        """
        super(LabeledMatchingLayerNorm, self).__init__()
        self.register_buffer("lookup_table", torch.zeros(num_persons, feat_len))

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, num_persons]): Labeled matching scores, namely the similarities
                                             between proposals and labeled persons.
        """
        scores = LabeledMatchingNorm.apply(features, pid_labels, self.lookup_table)
        return scores
