import itertools
import logging
import os.path as osp
import re
import tempfile
import warnings
from collections import OrderedDict

import mmcv
import pdb
import numpy as np
from mmcv.utils import print_log
from terminaltables import AsciiTable
from torch.utils.data import Dataset

from mmdet.core import eval_recalls
from .api_wrappers import COCO, COCOeval
from .builder import DATASETS
from .custom import CustomDataset
from .re_id import ReIdDataset


@DATASETS.register_module()
class MSMT17Dataset(ReIdDataset):

    # CLASSES = ('person','rider','pedestrain')#???
    CLASSES = ('person',)#???

    # def __len__(self):
    #     """Total number of samples of data."""
    #     return len(self.data_infos)

    def load_annotations_train(self, ann_files):
        """Load annotation from annotation file."""

        if not isinstance(ann_files, list):
            ann_files = [ann_files]
        data_info = []
        for ann_file in ann_files:
            data = self._pluck_msmt(ann_file)
            data_info.extend(data)
        # pdb.set_trace()
        return data_info

    def _pluck_msmt(self, list_file, pattern=re.compile(r'([-\d]+)_([-\d]+)_([-\d]+)')):
        # pdb.set_trace()
        with open(list_file, 'r') as f:
            lines = f.readlines()
        ret = []
        pids = []
        for line in lines:
            line = line.strip()
            fname = line.split(' ')[0]
            pid, _, cam = map(int, pattern.search(osp.basename(fname)).groups())
            if pid not in pids:
                pids.append(pid)
            ret.append(
                {
                    'filename':fname,
                    'gt_pids': np.array([pid]),
                    'cam_id': int(cam)
                }
            )
            # ret.append((osp.join(subdir, fname), pid, cam))
        # return ret, pids
        # pdb.set_trace()
        self.num_pids= len(pids)#train 0-1040

        return ret

    def load_query(self, ann_file):
        return self._pluck_msmt(ann_file)

    def get_cat_ids(self, idx):
        """Get category ids by index.

        Args:
            idx (int): Index of data.

        Returns:
            list[int]: All categories in the image of specified index.
        """

        return self.data_infos[idx]['ann']['labels'].astype(np.int).tolist()

    def pre_pipeline(self, results):
        """Prepare results dict for pipeline."""
        results['img_prefix'] = self.img_prefix
        results['seg_prefix'] = self.seg_prefix
        results['proposal_file'] = self.proposal_file
        results['bbox_fields'] = []
        results['mask_fields'] = []
        results['seg_fields'] = []

    def _set_group_flag(self):
        """Set flag according to image aspect ratio.

        Images with aspect ratio greater than 1 will be set as group 1,
        otherwise group 0.
        """
        self.flag = np.zeros(len(self), dtype=np.uint8)
        for i in range(len(self)):
            # img_info = self.data_infos[i]
            # if img_info['width'] / img_info['height'] > 1:
            self.flag[i] = 1

    def prepare_train_img(self, idx):
        """Get training data and annotations after pipeline.

        Args:
            idx (int): Index of data.

        Returns:
            dict: Training data and annotation after pipeline with new keys \
                introduced by pipeline.
        """

        img_info = self.data_infos[idx]
        img_info, ann_info = self.get_ann_info(img_info)
        results = dict(img_info=img_info, ann_info=ann_info)

        # if self.proposals is not None:
        #     results['proposals'] = self.proposals[idx]
        self.pre_pipeline(results)
        # a = self.pipeline(results)
        # pdb.set_trace()
        if self.multi_view:
            return self.multi_view_transform(results)
        return self.pipeline(results)

    def get_ann_info(self, info):
        img_info = {}
        img_info['file_name'] = info['filename']
        img_info['filename'] = info['filename']

        gt_bboxes = np.zeros((1, 4), dtype=np.float32)
        # gt_bboxes = info['boxes']
        # pdb.set_trace()
        self.cat2label = {1: 0}
        gt_labels = np.array([self.cat2label[1] * len(gt_bboxes)], dtype=np.int64)
        # gt_labels = gt_labels[np.newaxis,:]
        gt_ids = info['gt_pids'] + self.base_pid
        gt_bboxes_ignore = np.zeros((0, 4), dtype=np.float32)

        ann = dict(
            bboxes=gt_bboxes,
            labels=gt_labels,
            ids=gt_ids,
            # attrs=gt_attrs,
            bboxes_ignore=gt_bboxes_ignore,
            data_type='re_id',
            domain_id = self.dataset_index
            # masks=gt_masks_ann,
            # seg_map=seg_map
            # flip=False,
            # flip_direction=None
        )
        return img_info, ann

    def _parse_query_info(self, info):
        return self.get_ann_info(info)

    # def prepare_test_img(self, idx):
    #     """Get testing data  after pipeline.
    #
    #     Args:
    #         idx (int): Index of data.
    #
    #     Returns:
    #         dict: Testing data after pipeline with new keys introduced by \
    #             pipeline.
    #     """
    #
    #     img_info = self.data_infos[idx]
    #     results = dict(img_info=img_info)
    #     if self.proposals is not None:
    #         results['proposals'] = self.proposals[idx]
    #     self.pre_pipeline(results)
    #     return self.pipeline(results)

    @classmethod
    def get_classes(cls, classes=None):
        """Get class names of current dataset.

        Args:
            classes (Sequence[str] | str | None): If classes is None, use
                default CLASSES defined by builtin dataset. If classes is a
                string, take it as a file name. The file contains the name of
                classes where each line contains one class name. If classes is
                a tuple or list, override the CLASSES defined by the dataset.

        Returns:
            tuple[str] or list[str]: Names of categories of the dataset.
        """
        if classes is None:
            return cls.CLASSES

        if isinstance(classes, str):
            # take it as a file path
            class_names = mmcv.list_from_file(classes)
        elif isinstance(classes, (tuple, list)):
            class_names = classes
        else:
            raise ValueError(f'Unsupported type {type(classes)} of classes.')

        return class_names

    def format_results(self, results, **kwargs):
        """Place holder to format result to dataset specific output."""


    def __repr__(self):
        """Print the number of instance number."""
        dataset_type = 'Test' if self.test_mode else 'Train'
        result = (f'\n{self.__class__.__name__} {dataset_type} dataset '
                  f'with number of images {len(self)}, '
                  f'and instance counts: \n')
        if self.CLASSES is None:
            result += 'Category names are not provided. \n'
            return result
        instance_count = np.zeros(len(self.CLASSES) + 1).astype(int)
        # count the instance number in each image
        for idx in range(len(self)):
            label = self.get_ann_info(idx)['labels']
            unique, counts = np.unique(label, return_counts=True)
            if len(unique) > 0:
                # add the occurrence number to each class
                instance_count[unique] += counts
            else:
                # background is the last index
                instance_count[-1] += 1
        # create a table with category count
        table_data = [['category', 'count'] * 5]
        row_data = []
        for cls, count in enumerate(instance_count):
            if cls < len(self.CLASSES):
                row_data += [f'{cls} [{self.CLASSES[cls]}]', f'{count}']
            else:
                # add the background number
                row_data += ['-1 background', f'{count}']
            if len(row_data) == 10:
                table_data.append(row_data)
                row_data = []

        table = AsciiTable(table_data)
        result += table.table
        return result
