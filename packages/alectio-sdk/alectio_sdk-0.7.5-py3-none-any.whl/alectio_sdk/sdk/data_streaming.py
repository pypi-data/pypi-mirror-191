# TODO
""" 
ALECTIO PUBLIC DATASET


WE HAVE TO STREAM DATASET FROM BUCKET


TRAIN 
TEST
VALIDATION

SUPPORTED FRAMEWORK 
    1. TORCH DATASET
    2. TENSORFLOW DATASET
    
    

"""
# --------------------------PYTHON IMPORT--------------------------#
import os
import requests
from typing import Any
import concurrent.futures
from torchvision.datasets import ImageFolder
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm
from rich.progress import track

# --------------------------LOCAL IMPORT--------------------------#
from .api_client import APIClient
from .gcp_storage import GCP_Storage


class __AlectioDataset:
    def __init__(
        self,
        root: str,
        framework: str,
        dataset_type: str,
        transforms=None,
        tf_args=None,
    ):
        self.framework = framework
        self.dataset_type = dataset_type.lower()
        self.api_client = APIClient()
        self.data_dir = os.path.join(root, dataset_type)
        self.transforms = transforms
        self.tf_args = tf_args
        self.gcp_client = GCP_Storage()

    def __pull_dataset(self):
        error, data = APIClient.GET_REQUEST(
            end_point="/v2/project/{project_id}/get_public_dataset/",
            payload={"dataset_type": "", "dataset_id": ""},
        )

        data = {
            "task_type": "CV",
            "storage_bucket": "alectio-public-datasets",
            "json_path": "CV/100Sports/train.zip",
        }
        if data["task_type"] == "CV":
            self.storage_bucket = data["storage_bucket"]
            json_data = self.gcp_client.read_file(
                storage_bucket=self.storage_bucket,
                object_key=data["json_path"],
                format="json",
            )
            json_data = dict(list(json_data.items())[:100])

        else:
            raise Exception("NLP DATASET IS NOT SUPPORTED YET")

        os.makedirs(self.data_dir, exist_ok=True)

        # SAVE IMAGES TO ROOT DIR/DATASET_TYPE
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(
                    self.gcp_client.download_file,
                    self.storage_bucket,
                    image_path,
                    "jpg",
                    os.path.join(
                        self.data_dir,
                        image_path[
                            image_path.index(self.dataset_type)
                            + len(self.dataset_type)
                            + 1 :
                        ],
                    ),
                )
                for idex, image_path in json_data.items()
            ]

            for future in track(
                concurrent.futures.as_completed(futures),
                total=len(json_data.keys()),
                description=f"Downloading {self.dataset_type} dataset",
            ):
                pass

    def __is_exist(self):
        """
        THIS HIDDEN FUNCTION CHECK WHETHER THE DATASET IS EXIST OR NOT IN THE GIVEN ROOT DIR

        Returns:
            _type_: bool
        """
        return os.path.isdir(self.data_dir)

    def __create_dataset(self):
        """
        THIS HIDDEN FUNCTION CREATES DATASET
        Returns:
            _type_: _description_
        """

        if self.framework == "pytorch":
            return ImageFolder(root=self.data_dir, transform=self.transforms)
        elif self.framework == "tensorflow":
            data_gen = ImageDataGenerator(**self.transforms)
            return data_gen.flow_from_directory(directory=self.data_dir, **self.tf_args)
        else:
            raise ValueError(
                f"Invalid framework {self.framework}, Framework should be one of [tensorflow, pytorch]"
            )

    def __get_dataset(self):
        if not self.__is_exist():
            self.__pull_dataset()
        return self.__create_dataset()

    def __call__(self):
        if self.dataset_type in ["train", "test", "validation"]:
            return self.__get_dataset()
        else:
            raise Exception(
                "UNSUPPORTED DATASET TYPE\nSUPPORTED DATASET TYPES ARE TRAIN,TEST,VALIDATION"
            )
            return


def public_dataset(root: str, framework: str, dataset_type: str, transforms=None):
    alectio_dataset = __AlectioDataset(
        root=root,
        framework=framework,
        dataset_type=dataset_type,
        transforms=transforms,
    )
    dataset = alectio_dataset()
    return dataset, len(dataset), dataset.class_to_idx


if __name__ == "__main__":
    # EXAMPLE
    train_dataset, len_dataset, class_to_idx = public_dataset(
        root="./data", framework="pytorch", dataset_type="train"
    )
