import pdb

import torch

def check_isnan_or_isinf(data):
    if isinstance(data, (tuple, list)):
        # isnan_or_isinf = any([torch.isnan(d) or torch.isinf(d) for d in data])
        isnan_or_isinf = any([check_isnan_or_isinf(d) for d in data])
    elif isinstance(data, dict):
        try:
            isnan_or_isinf = any([check_isnan_or_isinf(v) for k,v in data.items()])
        except:
            pdb.set_trace()
    else:
        isnan_or_isinf = torch.isnan(data).any() or torch.isinf(data).any()

    return isnan_or_isinf


def check_is_all_zeros(data):
    if isinstance(data, (tuple, list)):
        is_all_zeros = any([torch.equal(d.cpu(), torch.zeros(d.shape)) for d in data])
    elif isinstance(data, dict):
        try:
            is_all_zeros = any([check_isnan_or_isinf(v) for k,v in data.items()])
        except:
            pdb.set_trace()
    else:
        is_all_zeros = torch.equal(data.cpu(), torch.zeros(data.shape))

    return is_all_zeros