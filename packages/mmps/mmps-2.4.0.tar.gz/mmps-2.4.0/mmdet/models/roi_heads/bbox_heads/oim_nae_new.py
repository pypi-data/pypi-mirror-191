import torch
import torch.nn.functional as F
from torch import autograd, nn

# from utils.distributed import tensor_gather


class OIM(autograd.Function):
    @staticmethod
    def forward(ctx, inputs, targets, lut, cq, header, is_test, counter, momentum):
        ctx.save_for_backward(inputs, targets, lut, cq, header, momentum)
        ctx.is_test = is_test
        ctx.counter = counter
        outputs_labeled = inputs.mm(lut.t())
        outputs_unlabeled = inputs.mm(cq.t())
        return torch.cat([outputs_labeled, outputs_unlabeled], dim=1)

    @staticmethod
    def backward(ctx, grad_outputs):
        inputs, targets, lut, cq, header, momentum = ctx.saved_tensors
        is_test = ctx.is_test
        counter = ctx.counter
        if is_test:
            counter[0] = counter[0] - 1
            # print('nae_'+str(counter[0]))

        # inputs, targets = tensor_gather((inputs, targets))

        grad_inputs = None
        if ctx.needs_input_grad[0]:
            grad_inputs = grad_outputs.mm(torch.cat([lut, cq], dim=0))
            if grad_inputs.dtype == torch.float16:
                grad_inputs = grad_inputs.to(torch.float32)

        update_condition1 = is_test and counter[0] % 2 == 0
        update_condition2 = not is_test
        if update_condition1 or update_condition2:
            for x, y in zip(inputs, targets):
                if y >= 0:
                    lut[y] = momentum * lut[y] + (1.0 - momentum) * x
                    lut[y] /= lut[y].norm()
                else:
                    cq[header] = x
                    header = (header + 1) % cq.size(0)
        return grad_inputs, None, None, None, None, None, None, None


def oim(inputs, targets, lut, cq, header, is_test, counter, momentum=0.5):
    return OIM.apply(inputs, targets, lut, cq, torch.tensor(header), is_test, counter, torch.tensor(momentum))


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
        if is_test:
            self.register_buffer("counter", torch.zeros(1))
        else:
            self.counter=None

        self.header_cq = 0

    def forward(self, inputs, roi_label):
        # merge into one batch, background pid = -2
        # unlabeled pid=-1
        # labeled pid >=0

        inds = roi_label >= -1
        label = roi_label[inds]
        inputs = inputs[inds.unsqueeze(1).expand_as(inputs)].view(-1, self.num_features)

        projected = oim(inputs, label, self.lut, self.cq, self.header_cq, self.is_test,
                                                            self.counter, momentum=self.momentum)
        projected *= self.oim_scalar

        self.header_cq = (
            self.header_cq + (label == -1).long().sum().item()
        ) % self.num_unlabeled
        loss_oim = F.cross_entropy(projected, label, ignore_index=-1)
        return loss_oim
