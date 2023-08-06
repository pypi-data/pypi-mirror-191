import torch
import torch.nn as nn
from torch.autograd import Function


class UnlabeledMatching(Function):
    @staticmethod
    def forward(ctx, features, pid_labels, queue, tail, is_test, counter):
        # The queue/tail can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.save_for_backward(features, pid_labels)
        ctx.queue = queue
        ctx.tail = tail
        ctx.is_test = is_test
        ctx.counter = counter

        scores = features.mm(queue.t())
        return scores

    @staticmethod
    def backward(ctx, grad_output):
        features, pid_labels = ctx.saved_tensors
        queue = ctx.queue
        tail = ctx.tail
        is_test = ctx.is_test
        counter = ctx.counter
        # pdb.set_trace()
        if is_test:
            counter[0] = counter[0] - 1
            print('alignps_unlabel_'+str(counter[0]))

        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(queue.data)

        update_condition1 = is_test and counter[0] % 2 == 0
        update_condition2 = not is_test
        if update_condition1 or update_condition2:
            # Update circular queue, but not by standard backpropagation with gradients
            for indx, label in enumerate(pid_labels):
                if label == -1:
                    #queue[tail, :32] = features[indx, :32]
                    queue[tail, :64] = features[indx, :64]
                    #queue[tail, :] = features[indx, :]
                    tail += 1
                    if tail >= queue.size(0):
                        tail -= queue.size(0)

        return grad_feats, None, None, None, None, None


class UnlabeledMatchingLayer(nn.Module):
    """
    Unlabeled matching of OIM loss function.
    """

    def __init__(self, queue_size=5000, feat_len=256, is_test=False):
        """
        Args:
            queue_size (int): Size of the queue saving the features of unlabeled persons.
            feat_len (int): Length of the feature extracted by the network.
        """
        super(UnlabeledMatchingLayer, self).__init__()
        self.register_buffer("queue", torch.zeros(queue_size, feat_len))
        self.register_buffer("tail", torch.tensor(0))
        if is_test:
            self.register_buffer("counter_unlabel_alignps", torch.zeros(1))
        else:
            self.counter_unlabel_alignps=None
        self.is_test=is_test

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, queue_size]): Unlabeled matching scores, namely the similarities
                                            between proposals and unlabeled persons.
        """
        scores = UnlabeledMatching.apply(features, pid_labels, self.queue, self.tail,
                                         self.is_test, self.counter_unlabel_alignps )
        return scores


class UnlabeledMatchingFull(Function):
    @staticmethod
    def forward(ctx, features, pid_labels, queue, tail, is_test, counter):
        # The queue/tail can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.save_for_backward(features, pid_labels)
        ctx.queue = queue
        ctx.tail = tail
        ctx.is_test = is_test
        ctx.counter = counter

        scores = features.mm(queue.t())
        return scores

    @staticmethod
    def backward(ctx, grad_output):
        features, pid_labels = ctx.saved_tensors
        queue = ctx.queue
        tail = ctx.tail
        is_test = ctx.is_test
        counter = ctx.counter
        # pdb.set_trace()
        if is_test:
            counter[0] = counter[0] - 1
            # print('alignps_unlabel_'+str(counter[0]))

        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(queue.data)

        update_condition1 = is_test and counter[0] % 2 == 0
        update_condition2 = not is_test
        if update_condition1 or update_condition2:
            # Update circular queue, but not by standard backpropagation with gradients
            for indx, label in enumerate(pid_labels):
                if label == -1:
                    queue[tail] = features[indx]
                    #queue[tail, :] = features[indx, :]
                    tail += 1
                    if tail >= queue.size(0):
                        tail -= queue.size(0)

        return grad_feats, None, None, None, None, None

class UnlabeledMatchingFullLayer(nn.Module):
    """
    Unlabeled matching of OIM loss function.
    """

    def __init__(self, queue_size=5000, feat_len=256, is_test=False):
        """
        Args:
            queue_size (int): Size of the queue saving the features of unlabeled persons.
            feat_len (int): Length of the feature extracted by the network.
        """
        super(UnlabeledMatchingFullLayer, self).__init__()
        self.register_buffer("queue", torch.zeros(queue_size, feat_len))
        self.register_buffer("tail", torch.tensor(0))
        if is_test:
            self.register_buffer("counter_unlabel_alignps", torch.zeros(1))
        else:
            self.counter_unlabel_alignps=None
        self.is_test=is_test

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, queue_size]): Unlabeled matching scores, namely the similarities
                                            between proposals and unlabeled persons.
        """
        scores = UnlabeledMatchingFull.apply(features, pid_labels, self.queue, self.tail,
                                             self.is_test, self.counter_unlabel_alignps)
        return scores
