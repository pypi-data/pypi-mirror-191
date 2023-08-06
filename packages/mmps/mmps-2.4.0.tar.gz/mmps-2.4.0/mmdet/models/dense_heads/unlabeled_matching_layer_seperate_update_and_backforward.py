import pdb

import torch
import torch.nn as nn
from torch.autograd import Function


class UnlabeledMatching(Function):
    @staticmethod
    def forward(ctx, features, queue):
        # The queue/tail can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.queue = queue

        scores = features.mm(queue.t())
        return scores

    @staticmethod
    def backward(ctx, grad_output):
        # print('===alingps_oim_queue_backforward===')
        queue = ctx.queue

        grad_feats = None
        if ctx.needs_input_grad[0]:
            grad_feats = grad_output.mm(queue.data)

        return grad_feats, None


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
        self.is_test=is_test

    def update_queue(self):
        # if not self.is_test:
        # print('===alignps_oim_update_queue===')
        # Update circular queue, but not by standard backpropagation with gradients
        # pdb.set_trace()
        if hasattr(self, 'pid_labels'):
            for indx, label in enumerate(self.pid_labels):
                if label == -1:
                    #queue[tail, :32] = features[indx, :32]
                    self.queue[self.tail, :64] = self.features[indx, :64].data
                    #queue[tail, :] = features[indx, :]
                    self.tail += 1
                    if self.tail >= self.queue.size(0):
                        self.tail -= self.queue.size(0)

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, queue_size]): Unlabeled matching scores, namely the similarities
                                            between proposals and unlabeled persons.
        """
        # pdb.set_trace()
        scores = UnlabeledMatching.apply(features, self.queue)
        self.features = features
        self.pid_labels = pid_labels
        return scores


class UnlabeledMatchingFull(Function):
    @staticmethod
    def forward(ctx, features, queue):
        # The queue/tail can't be saved with ctx.save_for_backward(), as we would
        # modify the variable which has the same memory address in backward()
        ctx.queue = queue

        scores = features.mm(queue.t())
        return scores

    @staticmethod
    def backward(ctx, grad_output):
        try:
            queue = ctx.queue

            grad_feats = None
            if ctx.needs_input_grad[0]:
                grad_feats = grad_output.mm(queue.data)
        except RuntimeError as e:
            print(e)
            pdb.set_trace()

        # queue = ctx.queue
        #
        # grad_feats = None
        # if ctx.needs_input_grad[0]:
        #     grad_feats = grad_output.mm(queue.data)
        return grad_feats, None

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
        self.is_test=is_test

    def update_queue(self):
        # if not self.is_test:
        # Update circular queue, but not by standard backpropagation with gradients

        if hasattr(self, 'pid_labels'):
            for indx, label in enumerate(self.pid_labels):
                if label == -1:
                    self.queue[self.tail] = self.features[indx].data
                    #queue[tail, :] = features[indx, :]
                    self.tail += 1
                    if self.tail >=self.queue.size(0):
                        self.tail -= self.queue.size(0)

    def forward(self, features, pid_labels):
        """
        Args:
            features (Tensor[N, feat_len]): Features of the proposals.
            pid_labels (Tensor[N]): Ground-truth person IDs of the proposals.

        Returns:
            scores (Tensor[N, queue_size]): Unlabeled matching scores, namely the similarities
                                            between proposals and unlabeled persons.
        """

        scores = UnlabeledMatchingFull.apply(features, pid_labels, self.queue)
        self.pid_labels = pid_labels
        self.features = features
        return scores
