
from .builder import DATASETS
from .coco_pedestron import CocoDataset_Pedestron


@DATASETS.register_module()
class EuroCityDataset(CocoDataset_Pedestron):

    # CLASSES = ('person','rider','pedestrain')#???
    CLASSES = ('pedestrain',)#???
