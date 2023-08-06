from logging import Logger
from typing import Dict, Union, Optional

from .dataset import Dataset
from .dataset_type import DatasetType


class DatasetManager(object):

    def __init__(self, logger: Logger):
        self.__logger: Logger = logger
        self.__datasets: Dict[str, Dataset.__subclasses__()] = {}

    def register(self, dataset_name: Union[str, DatasetType], dataset_class: Dataset.__subclasses__()) -> bool:
        """
        向系統註冊資料集

        :return: 是否註冊成功
        :param dataset_name: 資料集名稱 (內部名稱)
        :param dataset_class: 資料集類別
        """
        # is DatasetType
        if isinstance(dataset_name, DatasetType):
            dataset_name = dataset_name.name

        # is DatasetType
        if not issubclass(dataset_class, Dataset):
            self.__logger.error(f"Dataset class '{dataset_class.__name__}' must inherit class '{Dataset.__name__}'")
            return False

        if self.is_register(dataset_name):
            self.__logger.warning(f"Dataset '{dataset_name}' is existed")
            return False

        self.__datasets[dataset_name] = dataset_class
        self.__logger.info(f"Register dataset '{dataset_name}' with class '{dataset_class.__name__}'")
        return True

    def get_dataset(self, dataset_name: Union[str, DatasetType]) -> Optional[Dataset]:
        """
        取的指定的資料集

        :param dataset_name: 資料集名稱
        :return: 資料集 or None
        """
        # is DatasetType
        if isinstance(dataset_name, DatasetType):
            dataset_name = dataset_name.name

        # Check Dataset Exists or not
        if not self.is_register(dataset_name):
            self.__logger.warning(f"Dataset '{dataset_name}' must be registered first")
            return None

        return self.__datasets.get(dataset_name)()

    def is_register(self, dataset_name: Union[str, DatasetType]) -> bool:
        """
        確認資料集是否已經註冊

        :param dataset_name: 資料集名稱
        :return: 是否以註冊
        """
        return dataset_name in self.__datasets.keys()

    @property
    def registered(self) -> tuple:
        return tuple(self.__datasets.keys())
