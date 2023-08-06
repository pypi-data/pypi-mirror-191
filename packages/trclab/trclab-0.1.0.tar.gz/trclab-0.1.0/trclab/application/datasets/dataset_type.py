import os

from enum import Enum


class DatasetType(Enum):
    ICH_127 = os.environ["DATASET_ICH_127_DIRNAME"]
    ICH_420 = os.environ["DATASET_ICH_420_DIRNAME"]
    ICH_2500 = os.environ["DATASET_ICH_2500_DIRNAME"]
    RSNA_ICH = os.environ["DATASET_RSNA_ICH_DIRNAME"]
