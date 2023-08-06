import os

from trclab.datasets.dataset_file_manager import DatasetFileManager


class ICH2500FileManager(DatasetFileManager):
    __DATASET_DIR = os.environ["DATASET_ICH_2500_DIRNAME"]

    @property
    def test_image_filepaths(self) -> [str]:
        pass

    @property
    def train_image_filepaths(self) -> [str]:
        pass
