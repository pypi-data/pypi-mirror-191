import os
import abc


class DatasetFileManager(abc.ABC):

    def __init__(self, dataset_dir: str):
        from ...application.trclab import TRCLabApp
        self.__folder_path = ""

        if TRCLabApp.RUNTIME_TYPE == "LOCAL":
            self.__folder_path = os.environ["DATASET_DIR"]
        elif TRCLabApp.RUNTIME_TYPE == "CONTAINER":
            self.__folder_path = os.environ["DOCKER_MOUNT_DATASET_DIR"]
        else:
            raise TypeError

        self.__dataset_dir = os.path.join(self.__folder_path, dataset_dir)

    @property
    def folder_path(self) -> str:
        return self.__dataset_dir

    @property
    @abc.abstractmethod
    def train_image_filepaths(self) -> [str]:
        return NotImplemented

    @property
    @abc.abstractmethod
    def test_image_filepaths(self) -> [str]:
        return NotImplemented
