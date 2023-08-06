import torch
import torch.nn.functional as F
from torch import autograd, nn

# from utils.distributed import tensor_gather


class OIM(autograd.Function):
    @staticmethod
    def forward(ctx, inputs, lut, cq, header):
        ctx.save_for_backward(lut, cq)
        outputs_labeled = inputs.mm(lut.t())
        outputs_unlabeled = inputs.mm(cq.t())
        return torch.cat([outputs_labeled, outputs_unlabeled], dim=1)

    @staticmethod
    def backward(ctx, grad_outputs):
        lut, cq = ctx.saved_tensors
        # print('===nae_oim_backforward===')

        grad_inputs = None
        if ctx.needs_input_grad[0]:
            grad_inputs = grad_outputs.mm(torch.cat([lut, cq], dim=0))
            if grad_inputs.dtype == torch.float16:
                grad_inputs = grad_inputs.to(torch.float32)

        return grad_inputs, None, None, None


def oim(inputs, lut, cq, header):
    return OIM.apply(inputs, lut, cq, torch.tensor(header))


class OIMLoss(nn.Module):
    def __init__(self, num_features=256, num_pids=5532, num_cq_size=5000, is_test=False, oim_momentum=0.5, oim_scalar=30):
        super(OIMLoss, self).__init__()
        self.num_features = num_features
        self.num_pids = num_pids
        self.num_unlabeled = num_cq_size
        self.momentum = oim_momentum
        self.oim_scalar = oim_scalar

        self.register_buffer("lut", torch.zeros(self.num_pids, self.num_features))
        self.register_buffer("cq", torch.zeros(self.num_unlabeled, self.num_features))
        self.is_test = is_test

        self.header_cq = 0

    def update_lut_and_queue_nae(self):
        # if not self.is_test:
        # print('===nae_oim_update===')
        if hasattr(self, 'targets'):
            for x, y in zip(self.inputs.data, self.targets):
                if y >= 0:
                    self.lut[y] = self.momentum * self.lut[y] + (1.0 - self.momentum) * x
                    self.lut[y] /= self.lut[y].norm()
                else:
                    self.cq[self.header_cq] = x
                    self.header_cq = (self.header_cq + 1) % self.cq.size(0)

    def forward(self, inputs, roi_label):
        # merge into one batch, background label = 0
        # targets = torch.cat(roi_label)
        # label = targets - 1  # background label = -1

        inds = roi_label >= -1
        label = roi_label[inds]
        inputs = inputs[inds.unsqueeze(1).expand_as(inputs)].view(-1, self.num_features)
        self.inputs = inputs
        self.targets = label

        projected = oim(inputs, self.lut, self.cq, self.header_cq)
        projected *= self.oim_scalar

        self.header_cq = (
            self.header_cq + (label == -1).long().sum().item()
        ) % self.num_unlabeled
        loss_oim = F.cross_entropy(projected, label, ignore_index=-1)
        return loss_oim
