import os
from typing import List

from ..application.datasets import DatasetFileManager


class ICH420FileManager(DatasetFileManager):
    __DATASET_DIR = os.environ["DATASET_ICH_420_DIRNAME"]

    def __init__(self):
        super().__init__(ICH420FileManager.__DATASET_DIR)
        self.__segmentation_dir = os.path.join(self.folder_path, "ImageSets", "Segmentation")
        self.__image_dir = os.path.join(self.folder_path, "Images")
        self.__label_dir = os.path.join(self.folder_path, "Labels")

    @property
    def train_image_filepaths(self) -> List[str]:
        """
        獲取 ICH420 訓練集影像資料

        :return: ICH420 訓練集影像資料
        """
        return self.__load_from_imageset(self.__image_dir, "train.txt")

    @property
    def train_label_filepaths(self) -> List[str]:
        """
        獲取 ICH420 訓練集標記資料

        :return: ICH420 訓練集標記資料
        """
        return self.__load_from_imageset(self.__label_dir, "train.txt")

    @property
    def test_image_filepaths(self) -> List[str]:
        """
        獲取 ICH420 測試集影像資料

        :return: ICH420 測試集影像資料
        """
        return self.__load_from_imageset(self.__image_dir, "val.txt")

    @property
    def test_label_filepaths(self) -> List[str]:
        """
        獲取 ICH420 測試集標記資料

        :return: ICH420 測試集標記資料
        """
        return self.__load_from_imageset(self.__label_dir, "val.txt")

    def __load_from_imageset(self, image_dir: str, image_set_type: str) -> List[str]:
        """
        讀取資料集分割資料

        :param image_dir: 資料集路徑
        :param image_set_type: 資料集類型 ('train.txt' or 'val.txt')
        :return: 資料集分割集資料清單
        """
        with open(os.path.join(self.__segmentation_dir, image_set_type),
                  "r", encoding="utf-8") as seg_file:
            return [os.path.join(image_dir, filename)
                    for filename in seg_file.read().split("\n")[1:-1]]
