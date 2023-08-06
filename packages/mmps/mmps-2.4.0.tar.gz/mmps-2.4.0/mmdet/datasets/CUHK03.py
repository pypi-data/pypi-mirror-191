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


@DATASETS.register_module()
class CUHK03Dataset(ReIdDataset):

    # CLASSES = ('person','rider','pedestrain')#???
    CLASSES = ('person',)#???

    """
    CUHK03

    Reference:
    Li et al. DeepReID: Deep Filter Pairing Neural Network for Person Re-identification. CVPR 2014.

    URL: http://www.ee.cuhk.edu.hk/~xgwang/CUHK_identification.html#!

    Dataset statistics:
    # identities: 1360
    # images: 13164
    # cameras: 6
    # splits: 20 (classic)

    Args:
        split_id (int): split index (default: 0)
        cuhk03_labeled (bool): whether to load labeled images; if false, detected images are loaded (default: False)
    """

    def __init__(self,data_root,split_id=0,cuhk03_labeled=True,
                 cuhk03_classic_split=False,
                 test_mode=False,
                 **kwargs):
        # pdb.set_trace()
        # self.root = data_root
        self.dataset_dir=data_root
        # self.dataset_dir = osp.join(self.root, self.dataset_dir)

        self.data_dir = osp.join(self.dataset_dir, 'cuhk03_release')
        self.raw_mat_path = osp.join(self.data_dir, 'cuhk-03.mat')

        self.imgs_detected_dir = osp.join(self.dataset_dir, 'images_detected')
        self.imgs_labeled_dir = osp.join(self.dataset_dir, 'images_labeled')

        self.split_classic_det_json_path = osp.join(self.dataset_dir, 'splits_classic_detected.json')
        self.split_classic_lab_json_path = osp.join(self.dataset_dir, 'splits_classic_labeled.json')

        self.split_new_det_json_path = osp.join(self.dataset_dir, 'splits_new_detected.json')
        self.split_new_lab_json_path = osp.join(self.dataset_dir, 'splits_new_labeled.json')

        self.split_new_det_mat_path = osp.join(self.dataset_dir, 'cuhk03_new_protocol_config_detected.mat')
        self.split_new_lab_mat_path = osp.join(self.dataset_dir, 'cuhk03_new_protocol_config_labeled.mat')
        self.preprocess_split()
        self.split_id=split_id
        # self.base_pid=base_pid


        if cuhk03_labeled:
            split_path = self.split_classic_lab_json_path if cuhk03_classic_split else self.split_new_lab_json_path
            img_prefix = self.imgs_labeled_dir
        else:
            split_path = self.split_classic_det_json_path if cuhk03_classic_split else self.split_new_det_json_path
            img_prefix = self.imgs_detected_dir
        ann_file = split_path
        if not test_mode:
            query_file=None
        else:
            query_file = split_path
        # pdb.set_trace()
        super(CUHK03Dataset, self).__init__(ann_file, query_file=query_file,img_prefix=img_prefix,
                                            test_mode=test_mode,**kwargs)



    def load_annotations_train(self, ann_file,mode='train'):

        if isinstance(ann_file, list):
            ann_file = ann_file[0]
        with open(ann_file) as f:
            splits = json.load(f)
        assert self.split_id < len(splits), 'Condition split_id ({}) < len(splits) ({}) is false'.format(split_id,
                                                                              len(splits))
        # pdb.set_trace()
        split = splits[self.split_id]

        train = split[mode]
        data_info = []
        for img_path, pid, camid in train:
            data_info.append(
                {
                    'filename': img_path.split('/')[-1],
                    'gt_pids': np.array([pid]),
                    'cam_id': int(camid)
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
        self.num_pids=split['num_train_pids']#train 767  0-766
        return data_info

    def load_annotations_gallery(self, ann_file):
        return self.load_annotations_train(ann_file,mode='gallery')

    def load_query(self, ann_file):
        return self.load_annotations_train(ann_file,mode='query')

    # def __len__(self):
    #     """Total number of samples of data."""
    #     return len(self.data_infos)


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
            domain_id=self.dataset_index
            # masks=gt_masks_ann,
            # seg_map=seg_map
            # flip=False,
            # flip_direction=None
        )
        # pdb.set_trace()
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

    def preprocess_split(self):
        # This function is a bit complex and ugly, what it does is
        # 1. extract data from cuhk-03.mat and save as png images
        # 2. create 20 classic splits (Li et al. CVPR'14)
        # 3. create new split (Zhong et al. CVPR'17)
        if osp.exists(self.imgs_labeled_dir) \
                and osp.exists(self.imgs_detected_dir) \
                and osp.exists(self.split_classic_det_json_path) \
                and osp.exists(self.split_classic_lab_json_path) \
                and osp.exists(self.split_new_det_json_path) \
                and osp.exists(self.split_new_lab_json_path):
            return

        import h5py
        from imageio import imwrite
        from scipy import io

        mmcv.mkdir_or_exist(self.imgs_detected_dir)
        mmcv.mkdir_or_exist(self.imgs_labeled_dir)
        # PathManager.mkdirs(self.imgs_detected_dir)
        # PathManager.mkdirs(self.imgs_labeled_dir)

        print('Extract image data from "{}" and save as png'.format(self.raw_mat_path))
        mat = h5py.File(self.raw_mat_path, 'r')

        def _deref(ref):
            return mat[ref][:].T

        def _process_images(img_refs, campid, pid, save_dir):
            img_paths = []  # Note: some persons only have images for one view
            for imgid, img_ref in enumerate(img_refs):
                img = _deref(img_ref)
                if img.size == 0 or img.ndim < 3:
                    continue  # skip empty cell
                # images are saved with the following format, index-1 (ensure uniqueness)
                # campid: index of camera pair (1-5)
                # pid: index of person in 'campid'-th camera pair
                # viewid: index of view, {1, 2}
                # imgid: index of image, (1-10)
                viewid = 1 if imgid < 5 else 2
                img_name = '{:01d}_{:03d}_{:01d}_{:02d}.png'.format(campid + 1, pid + 1, viewid, imgid + 1)
                img_path = osp.join(save_dir, img_name)
                if not osp.isfile(img_path):
                    imwrite(img_path, img)
                img_paths.append(img_path)
            return img_paths

        def _extract_img(image_type):
            print('Processing {} images ...'.format(image_type))
            meta_data = []
            imgs_dir = self.imgs_detected_dir if image_type == 'detected' else self.imgs_labeled_dir
            for campid, camp_ref in enumerate(mat[image_type][0]):
                camp = _deref(camp_ref)
                num_pids = camp.shape[0]
                for pid in range(num_pids):
                    img_paths = _process_images(camp[pid, :], campid, pid, imgs_dir)
                    assert len(img_paths) > 0, 'campid{}-pid{} has no images'.format(campid, pid)
                    meta_data.append((campid + 1, pid + 1, img_paths))
                print('- done camera pair {} with {} identities'.format(campid + 1, num_pids))
            return meta_data

        meta_detected = _extract_img('detected')
        meta_labeled = _extract_img('labeled')

        def _extract_classic_split(meta_data, test_split):
            train, test = [], []
            num_train_pids, num_test_pids = 0, 0
            num_train_imgs, num_test_imgs = 0, 0
            for i, (campid, pid, img_paths) in enumerate(meta_data):

                if [campid, pid] in test_split:
                    for img_path in img_paths:
                        camid = int(osp.basename(img_path).split('_')[2]) - 1  # make it 0-based
                        test.append((img_path, num_test_pids, camid))
                    num_test_pids += 1
                    num_test_imgs += len(img_paths)
                else:
                    for img_path in img_paths:
                        camid = int(osp.basename(img_path).split('_')[2]) - 1  # make it 0-based
                        train.append((img_path, num_train_pids, camid))
                    num_train_pids += 1
                    num_train_imgs += len(img_paths)
            return train, num_train_pids, num_train_imgs, test, num_test_pids, num_test_imgs

        print('Creating classic splits (# = 20) ...')
        splits_classic_det, splits_classic_lab = [], []
        for split_ref in mat['testsets'][0]:
            test_split = _deref(split_ref).tolist()

            # create split for detected images
            train, num_train_pids, num_train_imgs, test, num_test_pids, num_test_imgs = \
                _extract_classic_split(meta_detected, test_split)
            splits_classic_det.append({
                'train': train,
                'query': test,
                'gallery': test,
                'num_train_pids': num_train_pids,
                'num_train_imgs': num_train_imgs,
                'num_query_pids': num_test_pids,
                'num_query_imgs': num_test_imgs,
                'num_gallery_pids': num_test_pids,
                'num_gallery_imgs': num_test_imgs
            })

            # create split for labeled images
            train, num_train_pids, num_train_imgs, test, num_test_pids, num_test_imgs = \
                _extract_classic_split(meta_labeled, test_split)
            splits_classic_lab.append({
                'train': train,
                'query': test,
                'gallery': test,
                'num_train_pids': num_train_pids,
                'num_train_imgs': num_train_imgs,
                'num_query_pids': num_test_pids,
                'num_query_imgs': num_test_imgs,
                'num_gallery_pids': num_test_pids,
                'num_gallery_imgs': num_test_imgs
            })

        with open(self.split_classic_det_json_path, 'w') as f:
            json.dump(splits_classic_det, f, indent=4, separators=(',', ': '))
        with open(self.split_classic_lab_json_path, 'w') as f:
            json.dump(splits_classic_lab, f, indent=4, separators=(',', ': '))

        def _extract_set(filelist, pids, pid2label, idxs, img_dir, relabel):
            tmp_set = []
            unique_pids = set()
            for idx in idxs:
                img_name = filelist[idx][0]
                camid = int(img_name.split('_')[2]) - 1  # make it 0-based
                pid = pids[idx]
                if relabel:
                    pid = pid2label[pid]
                img_path = osp.join(img_dir, img_name)
                tmp_set.append((img_path, int(pid), camid))
                unique_pids.add(pid)
            return tmp_set, len(unique_pids), len(idxs)

        def _extract_new_split(split_dict, img_dir):
            train_idxs = split_dict['train_idx'].flatten() - 1  # index-0
            pids = split_dict['labels'].flatten()
            train_pids = set(pids[train_idxs])
            pid2label = {pid: label for label, pid in enumerate(train_pids)}
            query_idxs = split_dict['query_idx'].flatten() - 1
            gallery_idxs = split_dict['gallery_idx'].flatten() - 1
            filelist = split_dict['filelist'].flatten()
            train_info = _extract_set(filelist, pids, pid2label, train_idxs, img_dir, relabel=True)
            query_info = _extract_set(filelist, pids, pid2label, query_idxs, img_dir, relabel=False)
            gallery_info = _extract_set(filelist, pids, pid2label, gallery_idxs, img_dir, relabel=False)
            return train_info, query_info, gallery_info

        print('Creating new split for detected images (767/700) ...')
        train_info, query_info, gallery_info = _extract_new_split(
            io.loadmat(self.split_new_det_mat_path),
            self.imgs_detected_dir
        )
        split = [{
            'train': train_info[0],
            'query': query_info[0],
            'gallery': gallery_info[0],
            'num_train_pids': train_info[1],
            'num_train_imgs': train_info[2],
            'num_query_pids': query_info[1],
            'num_query_imgs': query_info[2],
            'num_gallery_pids': gallery_info[1],
            'num_gallery_imgs': gallery_info[2]
        }]

        with open(self.split_new_det_json_path, 'w') as f:
            json.dump(split, f, indent=4, separators=(',', ': '))

        print('Creating new split for labeled images (767/700) ...')
        train_info, query_info, gallery_info = _extract_new_split(
            io.loadmat(self.split_new_lab_mat_path),
            self.imgs_labeled_dir
        )
        split = [{
            'train': train_info[0],
            'query': query_info[0],
            'gallery': gallery_info[0],
            'num_train_pids': train_info[1],
            'num_train_imgs': train_info[2],
            'num_query_pids': query_info[1],
            'num_query_imgs': query_info[2],
            'num_gallery_pids': gallery_info[1],
            'num_gallery_imgs': gallery_info[2]
        }]
        with open(self.split_new_lab_json_path, 'w') as f:
            json.dump(split, f, indent=4, separators=(',', ': '))


# if __name__=='__main__':
#     from mmdet.datasets.builder import build_dataset
#     dataset = build_dataset(cfg.data.train)