import itertools
import json
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
import os

@DATASETS.register_module()
class LUPersonDataset(ReIdDataset):

    # CLASSES = ('person','rider','pedestrain')#???
    CLASSES = ('person',)#???

    """
    LUPersonDataset

    Reference:
    Fu et al. https://github.com/DengpanFu/LUPerson. CVPR 2021.

    URL: https://github.com/DengpanFu/LUPerson

    Dataset statistics:
    # identities: none
    # images: 4180243

    """

    def load_annotations_train(self, ann_file,mode='train'):
        import pickle
        keys = pickle.load(open(ann_file, "rb"))
        img_names=keys['keys']
        data_info = []
        for i, img_name in enumerate(img_names):
            if self.train_img > 0 and i>=self.train_img:
                break
            data_info.append(
                {
                    'filename': img_name+'.jpg',
                    'gt_pids': np.array([-1]),
                    'cam_id': int(0)
                }
            )
            # new_pid = self.dataset_name + "_" + str(pid)
            # new_camid = self.dataset_name + "_" + str(camid)
            # tmp_train.append((img_path, new_pid, new_camid))
        # train = tmp_train
        # del tmp_train
        # query = split['query']
        # gallery = split['gallery']
        # pdb.set_trace()
        self.num_pids=0
        return data_info

    def load_annotations_gallery(self, ann_file):
        print('LUPerson is nolabel dataset, should not test')
        raise NotImplementedError
        # return self.load_annotations_train(ann_file,mode='gallery')

    def load_query(self, ann_file):
        print('LUPerson is nolabel dataset, should not test')
        raise NotImplementedError
        # return self.load_annotations_train(ann_file,mode='query')

    # def __len__(self):
    #     """Total number of samples of data."""
    #     return len(self.data_infos)


    # def get_cat_ids(self, idx):
    #     """Get category ids by index.
    #
    #     Args:
    #         idx (int): Index of data.
    #
    #     Returns:
    #         list[int]: All categories in the image of specified index.
    #     """
    #
    #     return self.data_infos[idx]['ann']['labels'].astype(np.int).tolist()

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
        # gt_ids = info['gt_pids'] + self.base_pid
        gt_ids = info['gt_pids']
        gt_bboxes_ignore = np.zeros((0, 4), dtype=np.float32)

        ann = dict(
            bboxes=gt_bboxes,
            labels=gt_labels,
            ids=gt_ids,
            # attrs=gt_attrs,
            bboxes_ignore=gt_bboxes_ignore,
            data_type='re_id',
            domain_id=self.dataset_index
            # masks=gt_masks_ann,
            # seg_map=seg_map
            # flip=False,
            # flip_direction=None
        )
        # pdb.set_trace()
        return img_info, ann

    # def _parse_query_info(self, info):
    #     return self.get_ann_info(info)

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
