
from .builder import DATASETS
from .coco_pedestron import CocoDataset_Pedestron


@DATASETS.register_module()
class CrowdHumanDataset(CocoDataset_Pedestron):

    # CLASSES = ('person','rider','pedestrain')#???
    CLASSES = ('person',)#???
