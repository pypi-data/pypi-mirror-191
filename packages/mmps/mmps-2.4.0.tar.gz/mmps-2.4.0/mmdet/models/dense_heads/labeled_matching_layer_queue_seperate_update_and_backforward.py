import torch
import pdb
import torch.nn as nn
from torch.autograd import Function


class LabeledMatching(Function):

    @staticmethod
    def forward(ctx, features, pid_labels, lookup_table):
        # The lookup_table can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.lookup_table = lookup_table

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
        # print('===alingps_oim_lut_backforward===')
        try:
            lookup_table = ctx.lookup_table

            grad_feats = None
            if ctx.needs_input_grad[0]:
                grad_feats = grad_output.mm(lookup_table)
            # raise RuntimeError
        except RuntimeError as e:
            print(e)
            pdb.set_trace()

        # lookup_table = ctx.lookup_table
        #
        # grad_feats = None
        # if ctx.needs_input_grad[0]:
        #     grad_feats = grad_output.mm(lookup_table)

        return grad_feats, None, None

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
        self.is_test=is_test

    def update_lut(self, momentum=0.5):
        # if not self.is_test:
        # print('===alignps_oim_update_lut===')
        # Update lookup table, but not by standard backpropagation with gradients
        # pdb.set_trace()
        if hasattr(self, 'pid_labels'):
            for indx, label in enumerate(self.pid_labels):
                if label >= 0:
                    self.lookup_table[label] = (
                            momentum * self.lookup_table[label].data + (1 - momentum) * self.features[indx].data
                    )
                    # lookup_table[label] /= lookup_table[label].norm()
            # pdb.set_trace()

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, num_persons]): Labeled matching scores, namely the similarities
                                             between proposals and labeled persons.
        """
        # pdb.set_trace()
        self.features = features
        self.pid_labels = pid_labels
        scores, pos_feats, pos_pids = LabeledMatching.apply(features, pid_labels,
                                                            self.lookup_table
                                                            )
        return scores, pos_feats, pos_pids


#=============================tyl add==========================================
class LabeledMatchingNorm(Function):
    @staticmethod
    def forward(ctx, features, pid_labels, lookup_table):
        # The lookup_table can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.lookup_table = lookup_table

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
        lookup_table = ctx.lookup_table
        # pdb.set_trace()

        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(lookup_table)


        return grad_feats, None, None


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
        self.is_test=is_test

    def update_lut(self, momentum=0.5):
        # if not self.is_test:
        # Update lookup table, but not by standard backpropagation with gradients
        if hasattr(self, 'pid_labels'):
            for indx, label in enumerate(self.pid_labels):
                if label >= 0:
                    self.lookup_table[label] = (
                            momentum * self.lookup_table[label].data + (1 - momentum) * self.features[indx].data
                    )
                    self.lookup_table[label] /= self.lookup_table[label].data.norm()

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, num_persons]): Labeled matching scores, namely the similarities
                                             between proposals and labeled persons.
        """
        self.pid_labels = pid_labels
        self.features = features
        scores, pos_feats, pos_pids = LabeledMatching.apply(features, pid_labels,
                                                            self.lookup_table
                                                            )
        return scores, pos_feats, pos_pids
