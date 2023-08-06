import os
import json

# ----------------local imports----------------#
from .api_client import APIClient
from .gcp_storage import GCP_Storage
from .console import MainConsole


class AlectioDataset:
    def __init__(self, token: str, root: str, framework: str):
        self.token = token
        self.root = root
        self.framework = framework
        self.console = MainConsole()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "config.json"), "r") as f:
            self.config = json.load(f)
        self.api_client = APIClient(
            backend_url=self.config["backend_ip"], token=self.token
        )
        self.gcp_client = GCP_Storage()

    def __is_exist(self, dataset_type: str):
        """
        THIS HIDDEN FUNCTION CHECK WHETHER THE DATASET IS EXIST OR NOT IN THE GIVEN ROOT DIR

        Returns:
            _type_: bool
        """
        return os.path.isdir(os.path.join(self.root, dataset_type))

    def __pull_dataset(self, dataset_type: str):
        self.console.info("PULLING DATASET FROM CLOUD")
        error, data = self.api_client.GET_REQUEST(
            end_point=f"/sdk/v2/token/{self.token}/type/{dataset_type}/get_public_dataset",
        )
        if error:
            self.console.error(
                "SOMETHING WENT WRONG WITH ALECTIO PUBLIC DATASET LIBRARY.\nCONTACT ALECTIO ADMIN"
            )

        if data["data"]["task_type"] == "CV":
            os.makedirs(os.path.join(self.root, dataset_type), exist_ok=True)
            self.gcp_client.download_file(
                storage_bucket=data["data"]["storage_bucket"],
                object_key=data["data"]["path"],
                format="zip",
                dest_path=os.path.join(self.root),
            )

        else:
            raise Exception("NLP DATASET IS NOT SUPPORTED YET")

    def __create_dataset(self, dataset_type: str, transforms=None, tf_args=None):
        if self.framework == "pytorch":
            from torchvision.datasets import ImageFolder
            dataset = ImageFolder(
                root=os.path.join(self.root, dataset_type), transform=transforms
            )
            return dataset, len(dataset), dataset.class_to_idx
        elif self.framework == "tensorflow":
            from tensorflow.keras.preprocessing.image import ImageDataGenerator
            data_gen = ImageDataGenerator(**self.transforms)
            dataset = data_gen.flow_from_directory(
                directory=os.path.join(self.root, dataset_type), **self.tf_args
            )
            return dataset, len(dataset), dataset.class_indices
        else:
            raise ValueError(
                f"Invalid framework {self.framework}, Framework should be one of [tensorflow, pytorch]"
            )

    def get_dataset(self, dataset_type: str, transforms=None, tf_args=None):
        if not self.__is_exist(dataset_type=dataset_type):
            self.__pull_dataset(dataset_type=dataset_type)

        dataset, dataset_len, class_to_idx = self.__create_dataset(
            dataset_type=dataset_type, transforms=transforms, tf_args=tf_args
        )
        return dataset, dataset_len, class_to_idx


# Testing
# if __name__ == "__main__":
#     alectio_dataset = AlectioDataset(
#         token="", root="", framework="pytorch"
#     )
#     train_dataset = alectio_dataset.get_dataset(dataset_type="train", transforms=None)
#     test_dataset = alectio_dataset.get_dataset(dataset_type="test")
#     validation_dataset = alectio_dataset.get_dataset(dataset_type="validation")
#     print(validation_dataset)
