import glob
import os
import pandas as pd
from typing import List

from ..application.datasets import DatasetFileManager


class RsnaICHFileManager(DatasetFileManager):
    __DATASET_DIR = os.environ["DATASET_RSNA_ICH_DIRNAME"]

    def __init__(self):
        super().__init__(RsnaICHFileManager.__DATASET_DIR)
        self.__dataset_train = os.path.join(self.folder_path, "stage_2_train")
        self.__dataset_test = os.path.join(self.folder_path, "stage_2_train")

    @property
    def train_image_filepaths(self) -> List[str]:
        """
        獲取 RSNA 資料集的訓練集檔案集路徑

        :return: RSNA訓練集檔案路徑
        """
        return glob.glob(os.path.join(self.__dataset_train, "*.dcm"))

    @property
    def test_image_filepaths(self) -> List[str]:
        """
        獲取 RSNA 資料集的測試集檔案集路徑

        :return: RSNA測試集檔案路徑
        """
        return glob.glob(os.path.join(self.__dataset_test, "*.dcm"))

    @property
    def train_labels(self) -> pd.DataFrame:
        """
        獲取 RSNA ICH 影像腦出血類行的標記資料

        :rtype: object
        :return: RSNA ICH 出血類型標記資料
        """
        rsna_df = pd.read_csv(os.path.join(self.folder_path, "stage_2_train.csv"))
        rsna_df[["ID", "Image", "Diagnosis"]] = rsna_df["ID"].str.split("_", expand=True)
        rsna_df = rsna_df[["Image", "Diagnosis", "Label"]]
        rsna_df.drop_duplicates(inplace=True)

        rsna_df = rsna_df.pivot(index="Image", columns="Diagnosis", values="Label").reset_index()
        rsna_df["Image"] = "ID_" + rsna_df["Image"]

        return rsna_df
