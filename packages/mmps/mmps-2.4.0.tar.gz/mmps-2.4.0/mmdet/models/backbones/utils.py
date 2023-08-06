import gdown
import os
import errno
from torch.hub import get_dir
import torch


def load_state_dict_from_google_drive(file_id, filename,map_location=None,model_dir=None,progress=True):
    r"""Loads the Torch serialized object at the given URL.

    If downloaded file is a zip file, it will be automatically
    decompressed.

    If the object is already present in `model_dir`, it's deserialized and
    returned.
    The default value of `model_dir` is ``<hub_dir>/checkpoints`` where
    `hub_dir` is the directory returned by :func:`~torch.hub.get_dir`.

    Args:
        file_name (string): name for the downloaded file. Filename from `url` will be used if not set.
        file_id (string): URL of the object to download
        model_dir (string, optional): directory in which to save the object
        map_location (optional): a function or a dict specifying how to remap storage locations (see torch.load)
        progress (bool, optional): whether or not to display a progress bar to stderr.
            Default: True
    """
    if model_dir is None:
        hub_dir = get_dir()
        model_dir = os.path.join(hub_dir, 'checkpoints')
    try:
        os.makedirs(model_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists, ignore.
            pass
        else:
            # Unexpected OSError, re-raise.
            raise
    cached_file = os.path.join(model_dir, filename)
    if not os.path.exists(cached_file):#!!!when published, uncomment these lines.
        gdown.download(id=file_id, output=cached_file,quiet=not progress)
    return torch.load(cached_file, map_location=map_location)

if __name__ == "__main__":
    # https://drive.google.com/file/d/1q1u-KgaJ51LTlUVgLtQmc9jNwsZFaFE2/view?usp=share_link
    file_id = '1q1u-KgaJ51LTlUVgLtQmc9jNwsZFaFE2'
    destination = 'resnet50-12.pth'
    state=load_state_dict_from_google_drive(file_id, destination)
    print("downloaded")
