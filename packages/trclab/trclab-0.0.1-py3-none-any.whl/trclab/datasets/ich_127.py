import os
import glob
import random

from trclab.datasets.dataset_file_manager import DatasetFileManager


class ICH127FileManager(DatasetFileManager):
    __DATASET_DIR = os.environ["DATASET_ICH_127_DIRNAME"]

    def __init__(self):
        super().__init__(ICH127FileManager.__DATASET_DIR)
        random.seed(int(os.environ["RANDOM_SEED"]))

        image_files = glob.glob(os.path.join(self.folder_path, "**/*.dcm"), recursive=True)
        label_files = glob.glob(os.path.join(self.folder_path, "**/*.tif"), recursive=True)

        dataset_paired: dict = dict()
        for image_file in image_files:
            image_basename = os.path.basename(image_file).lower()
            image_basename = image_basename.replace("_", "-").replace(" ", "")
            image_basename = image_basename.replace("case", "").replace("spion", "spon")
            image_basename = image_basename.replace("spon", "")[:-4]
            image_split = image_basename.split("-")

            def _find_target(label_name: str):
                label_basename = os.path.basename(label_name).lower()
                label_basename = label_basename.replace("_", "-").replace(" ", "").replace("v", "")
                label_basename = label_basename.replace("01", "1").replace("05", "5").replace("spion", "spon")
                label_basename = label_basename.replace("case", "").replace("spon", "")[:-4]
                label_split = label_basename.split("-")[:len(image_split)]

                return image_split == label_split

            result = tuple(filter(_find_target, label_files))
            if len(result) > 0:
                dataset_paired[image_file] = result

        dataset_list = list(dataset_paired.items())
        random.shuffle(dataset_list)

        self.__train_paired: dict = dict(dataset_list[:int(len(dataset_paired.keys()) * 0.8)])
        self.__test_paired: dict = dict(dataset_list[int(len(dataset_paired.keys()) * 0.8):])

    @property
    def train_image_filepaths(self) -> [str]:
        """
        獲取 ICH127 訓練集標記資料

        :return: ICH127 訓練集標記資料
        """
        return list(self.__train_paired.keys())

    @property
    def test_image_filepaths(self) -> [str]:
        """
        獲取 ICH127 測試集影像資料

        :return: ICH127 測試集影像資料
        """
        return list(self.__test_paired.keys())
