import torch
import pdb
import torch.nn as nn
from torch.autograd import Function


class LabeledMatching(Function):

    @staticmethod
    def forward(ctx, features, pid_labels, lookup_table, is_test, counter, momentum=0.5):
        # The lookup_table can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.save_for_backward(features, pid_labels)
        ctx.lookup_table = lookup_table
        ctx.momentum = momentum
        ctx.is_test=is_test
        ctx.counter=counter

        scores = features.mm(lookup_table.t())
        #print(features, lookup_table, scores)
        pos_feats = lookup_table.clone().detach()
        pos_idx = pid_labels > 0
        pos_pids = pid_labels[pos_idx]
        #pos_pids里面的id是会重复
        # pdb.set_trace()
        pos_feats = pos_feats[pos_pids]
        #pos_feats是lut里的值，重复取了相同id的特征。
        #pos_feats.require_grad = False
        
        return scores, pos_feats, pos_pids

    @staticmethod
    def backward(ctx, grad_output, grad_feat, grad_pids):
        features, pid_labels = ctx.saved_tensors
        lookup_table = ctx.lookup_table
        momentum = ctx.momentum
        is_test = ctx.is_test
        counter = ctx.counter
        # pdb.set_trace()
        if is_test:
            counter[0] = counter[0] - 1
            print('alignps_'+str(counter[0]))

        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(lookup_table)

        update_condition1 = is_test and counter[0] % 3 == 0
        update_condition2 = not is_test
        if update_condition1 or update_condition2:
            # Update lookup table, but not by standard backpropagation with gradients
            for indx, label in enumerate(pid_labels):
                if label >= 0:
                    lookup_table[label] = (
                        momentum * lookup_table[label] + (1 - momentum) * features[indx]
                    )
                    #lookup_table[label] /= lookup_table[label].norm()

        return grad_feats, None, None, None, None, None


class LabeledMatchingLayerQueue(nn.Module):
    """
    Labeled matching of OIM loss function.
    """

    def __init__(self, num_persons=5532, feat_len=256, is_test=False):
        """
        Args:
            num_persons (int): Number of labeled persons.
            feat_len (int): Length of the feature extracted by the network.
        """
        super(LabeledMatchingLayerQueue, self).__init__()
        self.register_buffer("lookup_table", torch.zeros(num_persons, feat_len))
        if is_test:
            self.register_buffer("counter_alignps", torch.zeros(1))
        else:
            self.counter_alignps=None
        self.is_test=is_test

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, num_persons]): Labeled matching scores, namely the similarities
                                             between proposals and labeled persons.
        """
        scores, pos_feats, pos_pids = LabeledMatching.apply(features, pid_labels,
                                                            self.lookup_table,
                                                            self.is_test,
                                                            self.counter_alignps
                                                            )
        return scores, pos_feats, pos_pids


#=============================tyl add==========================================
class LabeledMatchingNorm(Function):
    @staticmethod
    def forward(ctx, features, pid_labels, lookup_table, is_test, counter, momentum=0.5):
        # The lookup_table can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.save_for_backward(features, pid_labels)
        ctx.lookup_table = lookup_table
        ctx.momentum = momentum
        ctx.is_test=is_test
        ctx.counter=counter

        scores = features.mm(lookup_table.t())
        # print(features, lookup_table, scores)
        pos_feats = lookup_table.clone().detach()
        pos_idx = pid_labels > 0
        pos_pids = pid_labels[pos_idx]
        pos_feats = pos_feats[pos_pids]
        # pos_feats.require_grad = False

        return scores, pos_feats, pos_pids

    @staticmethod
    def backward(ctx, grad_output, grad_feat, grad_pids):
        features, pid_labels = ctx.saved_tensors
        lookup_table = ctx.lookup_table
        momentum = ctx.momentum
        is_test = ctx.is_test
        counter = ctx.counter
        # pdb.set_trace()
        if is_test:
            counter[0] = counter[0] - 1
            # print('alignps_'+str(counter[0]))

        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(lookup_table)

        update_condition1 = is_test and counter[0] % 3 == 0
        update_condition2 = not is_test
        if update_condition1 or update_condition2:
            # Update lookup table, but not by standard backpropagation with gradients
            for indx, label in enumerate(pid_labels):
                if label >= 0:
                    lookup_table[label] = (
                            momentum * lookup_table[label] + (1 - momentum) * features[indx]
                    )

                    if lookup_table[label].norm() == 0:
                        pdb.set_trace()

                    lookup_table[label] /= lookup_table[label].norm()

                    if lookup_table[label].isnan().any():
                        pdb.set_trace()

        return grad_feats, None, None, None, None, None


class LabeledMatchingLayerQueueNorm(nn.Module):
    """
    Labeled matching of OIM loss function.
    """

    def __init__(self, num_persons=5532, feat_len=256, is_test=False):
        """
        Args:
            num_persons (int): Number of labeled persons.
            feat_len (int): Length of the feature extracted by the network.
        """
        super(LabeledMatchingLayerQueueNorm, self).__init__()
        self.register_buffer("lookup_table", torch.zeros(num_persons, feat_len))
        if is_test:
            self.register_buffer("counter_alignps", torch.zeros(1))
        else:
            self.counter_alignps=None
        self.is_test=is_test

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, num_persons]): Labeled matching scores, namely the similarities
                                             between proposals and labeled persons.
        """
        scores, pos_feats, pos_pids = LabeledMatchingNorm.apply(features, pid_labels,
                                                            self.lookup_table,
                                                            self.is_test,
                                                            self.counter_alignps
                                                            )
        return scores, pos_feats, pos_pids
