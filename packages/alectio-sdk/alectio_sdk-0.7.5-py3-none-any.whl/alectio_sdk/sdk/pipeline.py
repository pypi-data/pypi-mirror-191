# hardcoded task type as image_classification for testing
import numpy as np
import json
import os
import time
import ast
from scipy.special import softmax
import datetime
from .utils import seed_comparison
from typing import Dict
from copy import deepcopy
from collections import Counter
from .api_client import APIClient
from .multiple_seed_pool import DataPool
from alectio_sdk.metrics.object_detection import Metrics, batch_to_numpy
from alectio_sdk.metrics.classification import ClassificationMetrics
from alectio_sdk.metrics.object_segmentation import segmentation_metrics
from alectio_sdk.metrics.multilabel_classification import (
    MultiLabelClassificationMetrics,
)
from codecarbon import EmissionsTracker
import pandas as pd
from alectio_sdk.metrics.object_segmentation import SegMetrics
from rich.progress import track
from alectio_sdk.sdk.sql_client import create_connection
import logging
from .console import MainConsole
from .gcp_storage import GCP_Storage
import requests


class Pipeline(object):
    r"""
    A wrapper for your `train`, `test`, and `infer` function. The arguments for your functions should be specifed
    separately and passed to your pipeline object during creation.

    Args:
        name (str): experiment name
        train_fn (function): function to be executed in the train cycle of the experiment.
        test_fn (function): function to be executed in the test cycle of the experiment.
        infer_fn (function): function to be executed in the inference cycle of the experiment.
        getstate_fn (function): function specifying a mapping between indices and file names.


    """

    def __init__(
        self,
        name,
        train_fn,
        test_fn,
        infer_fn,
        getstate_fn,
        args,
        token,
        multiple_initialisations={"seeds": [], "limit_value": 0},
    ):
        self.console = MainConsole()
        # time saved functionality
        self.time_saved_dir = f"{args['LOG_DIR']}/time_saved"
        self.time_saved_file = "time_saved.csv"
        if not os.path.exists(self.time_saved_dir):
            os.mkdir(self.time_saved_dir)

        # tracking co2_emissions
        self.co2_dir = f"{args['LOG_DIR']}/co2"
        if not os.path.exists(self.co2_dir):
            os.mkdir(self.co2_dir)
        self.co2_tracker = EmissionsTracker(
            output_dir=self.co2_dir, log_level="critical"
        )

        self.train_fn = train_fn
        self.test_fn = test_fn
        self.infer_fn = infer_fn
        self.getstate_fn = getstate_fn
        self.args = args
        # new arg

        # specifically for multiple seeds
        self.multiple_seeds = multiple_initialisations["seeds"]
        self.limit_value = int(multiple_initialisations["limit_value"])
        self.best_seed = 42

        self.client = GCP_Storage()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, "config.json"), "r") as f:
            self.config = json.load(f)

        self.client_token = token

        self.labeled = []
        self._testUploaded = False
        self._uploaded_infer_index = []

        self.api_client = APIClient(
            backend_url=self.config["backend_ip"], token=self.client_token
        )
        self.auth_token = self.api_client.AUTH_TOKEN_REQ(self.client_token)
        # self.console.info("ALECTIO PIPELINE RECEIVED ENCRYPTED TOKEN")

    def notify_sdk_status(self, logdir):
        logging.basicConfig(
            filename=os.path.join(logdir, "Appstatus.log"), level=logging.INFO
        )
        self.console.success("SDK Alectio initialized successfully")
        self.console.message(
            "Training checkpoints and other logs for current experiment will be written into the folder {}".format(
                logdir
            )
        )
        self.console.message("Press CTRL + C to exit")

    def _checkdirs(self, dir_):
        if not os.path.exists(dir_):
            os.makedirs(dir_, exist_ok=True)

    def check_model_activations(self, model_outputs):
        supported_activations = {"pre_softmax", "softmax", "sigmoid", "logits"}
        activation_set = set()
        for k, v in model_outputs.items():
            if isinstance(v, dict):
                activation_set.update(set(v.keys()).intersection(supported_activations))
            if len(activation_set) == 0:
                raise TypeError("Incorrect logit output format encountered")

        return activation_set

    def _estimate_exp_time(self, last_time):
        """
        Estimates the compute time remaining for the experiment

        Args:
            train_times (list): training_times noted down so far
            n_loop (int): total number of loops
        """

        def convert(seconds):
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            return "%d:%02d:%02d" % (hour, minutes, seconds)

        loops_completed = self.cur_loop + 1
        time_left = convert(last_time * (self.n_loop - loops_completed))
        self.console.message(
            "Estimated time left for the experiment: {}".format(time_left)
        )
        return time_left

    def _estimate_seed_init_time(self, last_time):
        pass

    def time_saved(
        self, epoch, start_train, end_train, total_records, selected_records
    ):
        actual_train_time = end_train - start_train
        estimated_train_time = total_records * (actual_train_time / selected_records)
        total_time_saved = estimated_train_time - actual_train_time
        time_saved_file_path = os.path.join(self.time_saved_dir, self.time_saved_file)

        info = {
            "epoch": [epoch],
            "selected_records": [selected_records],
            "total_records": [total_records],
            "training_time": [actual_train_time],
            "estimated_train_time": [estimated_train_time],
            "time_saved": [total_time_saved],
        }

        if os.path.exists(time_saved_file_path):
            df = pd.read_csv(time_saved_file_path)
            last_epoch = df["epoch"].to_list()[-1]
            if last_epoch == epoch:
                data = [x[0] for x in list(info.values())]
                df.loc[epoch] = data
            else:
                new_df = pd.DataFrame(info)
                df = pd.concat([df, new_df], axis=0)
            df.to_csv(time_saved_file_path, index=False)
        else:
            df = pd.DataFrame(info)
            df.to_csv(time_saved_file_path, index=False)

        return

    def one_loop(self, request):
        # Get payload args

        self.console.message("Extracting payload arguments from Alectio")

        payload = {
            "tenant_id": request["tenant_id"],
            "experiment_id": request["experiment_id"],
            "project_id": request["project_id"],
            "cur_loop": request["cur_loop"],
            "bucket_name": request["bucket_name"],
            "task_type": request["task_type"].lower(),
            "dataset_type": request["dataset_type"].lower(),
            "training_set_size": request["training_set_size"],
            "n_rec_per_loop": request["n_rec_per_loop"],
            "n_loop": request["n_loop"],
            "class_labels": request["classes"],
            "num_of_classes": request["num_of_classes"],
        }
        self.logdir = payload["experiment_id"]
        self._checkdirs(self.logdir)
        self.training_set_size = payload["training_set_size"]
        self.notify_sdk_status(self.logdir)

        self.console.success("Valid payload arguments extracted")
        self.console.message("Initializing process to train and optimize your model")
        returned_payload = self.run_loop(payload, self.args)

        self.console.success("Optimization process complete !")
        self.console.info(
            "Results of the loop will be available in Alectio Platform soon"
        )

        error, response = self.api_client.POST_REQUEST(
            end_point="/sdk/v2/end_of_task",
            payload={
                "experiment_id": request["experiment_id"],
                "project_id": request["project_id"],
                "num_of_classes": request["num_of_classes"],
            },
        )
        if error:
            self.console.warning(
                "SOMETHING WENT WRONG WITH YOUR INFER FUNCTION !!\nRECHECK YOUR CODE OR REACH OUT TO ALECTIO ADMIN FOR ANY SUPPORT"
            )
            return {"Message": "Loop Failed - non 200 status returned"}

        else:
            self.console.message(
                "Experiment {} running".format(payload["experiment_id"])
            )
            return {"Message": "Loop Started - 200 status returned"}

    def run_loop(self, payload, args):
        r"""
        Executes one loop of active learning. Returns the read `payload` back to the user.

        Args:
           args: a dict with the key `sample_payload` (required path) and any arguments needed by the `train`, `test`
           and infer functions.
        Example::

            args = {sample_payload: 'sample_payload.json', EXPT_DIR : "./log", exp_name: "test", \
                                                                 train_epochs: 1, batch_size: 8}


        """
        self.experiment_id = payload["experiment_id"]
        self.project_id = payload["project_id"]
        self.tenant_id = payload["tenant_id"]
        self.console.info("Extracting essential experiment params")

        # read selected indices upto this loop
        payload["cur_loop"] = int(payload["cur_loop"])
        self.cur_loop = payload["cur_loop"]
        self.bucket_name = payload["bucket_name"]
        self.n_loop = payload["n_loop"]
        self.dataset_type = payload["dataset_type"].lower()
        self.class_labels = payload["class_labels"]
        self.num_of_classes = payload["num_of_classes"]
        self.training_set_size = payload["training_set_size"]

        # type of the ML problem

        self.task_type = payload["task_type"]
        self.task_type = self.task_type.lower()

        self.expt_dir = os.path.join(
            self.tenant_id, self.project_id, self.experiment_id
        )

        self.console.success("Essential experiment params have been extracted")

        self.console.info("Verifying the meta.json that was uploaded by the user")

        self.labeled = []
        self.console.info("Reading indices to train on")

        # for i in range(self.cur_loop + 1):
        for i in range(self.cur_loop + 1):  #! LOOK AT HERE ONCE YOU WILL COME BACK
            object_key = os.path.join(
                self.expt_dir, "selected_indices_{}.pkl".format(i)
            )
            selected_indices = self.client.read_file(
                storage_bucket=self.bucket_name, object_key=object_key, format="pkl"
            )
            self.labeled.extend(selected_indices)

        if self.cur_loop == 0:
            if self.multiple_seeds != []:
                initial_unlabeled = [i for i in range(self.limit_value)]
                data_pool = DataPool(unlabeled=initial_unlabeled)
                self.resume_from = None
                best_seed_info = dict()
                best_seed_info["seed"] = self.multiple_seeds[0]
                best_seed_info["metric"] = 0

                for seed in self.multiple_seeds:
                    # data generation code
                    self.labeled = list()
                    n_rec = self.limit_value // 10
                    selected_indices = data_pool.random_sample("unlabeled", n_rec, seed)
                    self.labeled.extend(selected_indices)

                    # train and test
                    self.train_seed(args, seed)
                    self.console.message("Initializing testing of your model !")
                    metrics = self.test_seed(args, seed)
                    self.console.success(f"Testing finished for seed {seed}!")

                    # compare metrics
                    new_seed_info = dict()
                    new_seed_info["seed"] = seed
                    if self.task_type == "object_detection":
                        new_seed_info["metric"] = metrics["mAP"]
                    else:
                        new_seed_info["metric"] = metrics["accuracy"]

                    best_seed_info = seed_comparison(best_seed_info, new_seed_info)

                self.best_seed = best_seed_info["seed"]

            # send seed to sdk-backend
            url = "https://api-v2-pro.alectio.com/sdk/v2/seed_value"

            payload = json.dumps({"seed_value": self.best_seed})
            headers = {
                "X-Alectio-Flavor": "PRO",
                "Authorization": "Bearer " + self.auth_token,
                "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            # Normal Flow
            self.resume_from = None
            self.console.info(
                "Extracting indices for our reference, this may take time ... Please be patient"
            )
            self.state_json = self.getstate_fn(args)
            object_key = os.path.join(self.expt_dir, "data_map.pkl")
            self.console.success("Extraction complete !!!")
            self.console.message(
                "Creating index to records data reference for the current experiment"
            )
            self.client.upload_object(
                object=self.state_json,
                storage_bucket=self.bucket_name,
                object_key=object_key,
                format="pkl",
            )
            self.console.success("Reference creation complete")

        else:
            self.console.info("Resuming from a checkpoint from a previous loop ")
            # two dag approach needs to refer to the previous checkpoint
            self.resume_from = "ckpt_{}".format(self.cur_loop - 1)

        self.ckpt_file = "ckpt_{}".format(self.cur_loop)
        self.console.message("Initializing training of your model")

        # time saved functionality
        train_start_time = time.time()
        self.train(args)
        train_end_time = time.time()
        self.time_saved(
            # self,
            epoch=self.cur_loop,
            start_train=train_start_time,
            end_train=train_end_time,
            total_records=self.training_set_size,
            selected_records=len(self.labeled),
        )
        self.console.success("Training finished !")
        self.console.message("Initializing testing of your model !")
        self.test(args)
        self.console.success("Testing finished !")
        self.console.message("Assessing current best model")
        self.infer(args)
        self.console.success("Assessment complete ")
        self.console.info(
            "Time to check what records to train on next loop , visit our front end for more details"
        )

        return payload

    def train(self, args):
        r"""
        A wrapper for your `train` function. Returns `None`.

        Args:
        args: a dict whose keys include all of the arguments needed for your `train` function which is defined in `processes.py`.

        """

        def get_hyperparams(hyperparameters: Dict):
            extracted_hyp = dict()

            hyp_parameter_names = [
                "optimizer_name",
                "loss",
                "running_loss",
                "epochs",
                "batch_size",
                "loss_function",
                "activation",
                "optimizer",
            ]

            for param in hyp_parameter_names[:-1]:
                if param in hyperparameters.keys():
                    extracted_hyp[param] = hyperparameters[param]
                else:
                    extracted_hyp[param] = None

            # optimizer
            if "optimizer" in hyperparameters.keys():
                try:
                    optimizer_params = hyperparameters["optimizer"]["param_groups"][0]
                    extracted_hyp["optimizer"] = optimizer_params
                except:
                    extracted_hyp["optimizer"] = hyperparameters["optimizer"]
            else:
                extracted_hyp["optimizer"] = None

            extracted_hyp["time"] = datetime.datetime.now()
            return extracted_hyp

        start = time.time()

        if self.labeled is not None and len(self.labeled) == 0:
            raise ValueError("Labeled indices from backend are empty or None")

        self.console.info("Labeled records are ready to be trained")
        self.labeled.sort()  # Maintain increasing order

        # if len(self.labeled) > len(set(self.labeled)):
        #     raise ValueError("There exist repeated records.")

        all_labeled = dict(Counter(self.labeled))
        duplicates = []
        for k, v in all_labeled.items():
            if v == 2:
                duplicates.append(k)

        self.labeled = list(set(self.labeled))

        train_op = self.train_fn(
            args,
            labeled=deepcopy(self.labeled),
            resume_from=self.resume_from,
            ckpt_file=self.ckpt_file,
        )
        extracted_hyperparams = {}
        if train_op is not None:
            labels = train_op["labels"]
            unique, counts = np.unique(labels, return_counts=True)
            num_queried_per_class = {u: c for u, c in zip(unique, counts)}

            if "hyperparams" in train_op.keys():
                extracted_hyperparams = get_hyperparams(train_op["hyperparams"])

        end = time.time()

        # @TODO compute insights from labels
        if train_op is not None:
            insights = {
                "train_time": end - start,
                "num_queried_per_class": num_queried_per_class,
            }
        else:
            insights = {"train_time": end - start}

        self._estimate_exp_time(insights["train_time"])
        object_key = os.path.join(
            self.expt_dir, "insights_{}.pkl".format(self.cur_loop)
        )

        self.client.upload_object(
            object=insights,
            storage_bucket=self.bucket_name,
            object_key=object_key,
            format="pkl",
        )

        object_key = os.path.join(
            self.expt_dir, "meta_temp_{}.pkl".format(self.cur_loop)
        )
        self.client.upload_object(
            object=extracted_hyperparams,
            storage_bucket=self.bucket_name,
            object_key=object_key,
            format="pkl",
        )

        return

    def train_seed(self, args, seed):
        r"""
        A wrapper for your `train` function. Used for training on mutiple seeds. Returns `None`.

        Args:
        args: a dict whose keys include all of the arguments needed for your `train` function which is defined in `processes.py`.

        """
        start = time.time()

        if self.labeled is not None and len(self.labeled) == 0:
            raise ValueError("Labeled indices from backend are empty or None")

        self.console.info("Labeled records are ready to be trained")
        self.labeled.sort()  # Maintain increasing order

        all_labeled = dict(Counter(self.labeled))
        duplicates = []
        for k, v in all_labeled.items():
            if v == 2:
                duplicates.append(k)

        self.labeled = list(set(self.labeled))

        train_op = self.train_fn(
            args,
            labeled=deepcopy(self.labeled),
            resume_from=self.resume_from,
            ckpt_file=self.ckpt_file,
        )

        if train_op is not None:
            labels = train_op["labels"]
            unique, counts = np.unique(labels, return_counts=True)
            num_queried_per_class = {u: c for u, c in zip(unique, counts)}

        end = time.time()

        # @TODO compute insights from labels
        if train_op is not None:
            insights = {
                "train_time": end - start,
                "num_queried_per_class": num_queried_per_class,
            }
        else:
            insights = {"train_time": end - start}

        self._estimate_exp_time(insights["train_time"])
        self.console.info(f"Training on seed: {seed} completed!")

        return

    def test(self, args):
        """
        A wrapper for your `test` function which writes predictions and ground truth to the specified S3 bucket. Returns `None`.

        Args:
        args: a dict whose keys include all of the arguments needed for your `test` function which is defined in `processes.py`.

        """
        self.console.info("Extracting test results ")

        # TODO: UPLOAD TEST DATA (IT IS OPTIONAL)
        """
            1. TAKE IMAGE/TEXT AS INPUT AND RETURN FROM TEST FUNCTION
            2. UPLOAD THE LABEL DATA
                I. IF TEXT DATA PUT IT INTO .PKL/ES
                II. IF IMAGE DATA, PUT IT TO S3 
            3. TEST DATA MAPPING
            4. SET IS_TEST UPLOAD TO TRUE(FOR EACH INITIAL CALL OF PIPELINE, IS_UPLOADTEST IS FALSE)
        
        """

        res = self.test_fn(args, ckpt_file=self.ckpt_file)

        # res = self.test_fn(args, ckpt_file=self.ckpt_file)

        if self.task_type == "3d_segmentation":
            if "rangebased" in res:
                (
                    _3D_predictions,
                    _3D_labels,
                    _2D_predictions,
                    _2D_labels,
                    range_filtered,
                    range_default,
                    input_data,
                ) = (
                    res["3Dpredictions"],
                    res["3Dlabels"],
                    res["2Dpredictions"],
                    res["2Dlabels"],
                    res["rangebased"],
                    res["default"],
                    res["input_data"] if "input_data" in res else [],
                )
            else:
                (
                    _3D_predictions,
                    _3D_labels,
                    _2D_predictions,
                    _2D_labels,
                    range_filtered,
                    range_default,
                    input_data,
                ) = (
                    res["3Dpredictions"],
                    res["3Dlabels"],
                    res["2Dpredictions"],
                    res["2Dlabels"],
                    None,
                    None,
                    res["input_data"] if "input_data" in res else [],
                )
        else:
            predictions, ground_truth, input_data = (
                res["predictions"],
                res["labels"],
                res["input_data"] if "input_data" in res else [],
            )
        self.console.message("Writing test results to BUCKET")

        # UPLOAD LABEL DATA TO S3
        """
        IF TEXT DATA:
            MAKE A DICTIONARY TO SAVE INDEX AND TEXT IN A .PKL FILE
        IF IMAGE DATA:
            MAKE A DICTIONARY TO SAVE INDEX AND IMAGE S3 KEY IN A .PKL FILE
        """

        if not self._testUploaded:
            msg = (
                "ℹ️  "
                + "Test data will be uploaded whenever you will start one experiment. \nYou can stop it from your code(Recommended to pass test data for better understanding)"
                + "\n"
            )

            self.console.message(msg)
            if "image" in self.dataset_type:
                data_map = []
                for i, image_array in enumerate(
                    track(input_data, description="Uploading test data...")
                ):
                    image_key = os.path.join(self.expt_dir, "test", str(i) + ".png")
                    data_map.append(
                        {
                            "index": i,
                            "image_path": image_key,
                            "project_id": self.project_id,
                            "experiment_id": self.experiment_id,
                            "datamap_type": "test_datamap",
                        }
                    )

                    self.client.upload_object(
                        storage_bucket=self.bucket_name,
                        object=image_array,
                        object_key=image_key,
                        format="png",
                    )

                # backup
                object_key = os.path.join(
                    self.expt_dir, "test_datamap.pkl".format(self.cur_loop)
                )
                self.client.upload_object(
                    object=data_map,
                    storage_bucket=self.bucket_name,
                    object_key=object_key,
                    format="pkl",
                )
                self._testUploaded = True

            # if "text" in self.dataset_type:
            #     data_map = []
            #     for i, label in enumerate(input_data):
            #         data_map.append(
            #             {
            #                 "index": i,
            #                 "text": label,
            #                 "project_id": self.project_id,
            #                 "experiment_id": self.experiment_id,
            #                 "datamap_type": "test_datamap",
            #             }
            #         )

            #     # backup data
            #     object_key = os.path.join(
            #         self.expt_dir, "test_datamap.pkl".format(self.cur_loop)
            #     )
            #     self.client.upload_object(
            #         predictions, self.bucket_name, object_key, "pickle"
            #     )
            #     # ES storing
            #     # Feature will be released in V2 with lake
            #     # es_upload_datmap(datamap=data_map)
            self._testUploaded = True

        # write predictions and labels to S3
        object_key = os.path.join(
            self.expt_dir, "test_predictions_{}.pkl".format(self.cur_loop)
        )
        self.client.upload_object(
            object=predictions,
            storage_bucket=self.bucket_name,
            object_key=object_key,
            format="pkl",
        )

        if self.cur_loop == 0:
            # write ground truth to S3
            object_key = os.path.join(
                self.expt_dir, "test_ground_truth.pkl".format(self.cur_loop)
            )
            self.client.upload_object(
                object=ground_truth,
                storage_bucket=self.bucket_name,
                object_key=object_key,
                format="pkl",
            )

        if "3D" in self.dataset_type:
            self.compute3D_metrics(
                _3D_predictions, _3D_labels, _2D_predictions, _2D_labels, range_filtered
            )
        else:
            self.compute_metrics(predictions, ground_truth)
        return

    def test_seed(self, args, seed):
        """
        A wrapper for your `test` function which writes predictions and ground truth to the specified S3 bucket. Returns `metrics`.
        Used for training on mutiple seeds.

        Args:
        args: a dict whose keys include all of the arguments needed for your `test` function which is defined in `processes.py`.

        """
        self.console.info(f"Extracting test results for seed: {seed}")

        # TODO: UPLOAD TEST DATA (IT IS OPTIONAL)
        """
            1. TAKE IMAGE/TEXT AS INPUT AND RETURN FROM TEST FUNCTION
            2. UPLOAD THE LABEL DATA
                I. IF TEXT DATA PUT IT INTO .PKL/ES
                II. IF IMAGE DATA, PUT IT TO S3 
            3. TEST DATA MAPPING
            4. SET IS_TEST UPLOAD TO TRUE(FOR EACH INITIAL CALL OF PIPELINE, IS_UPLOADTEST IS FALSE)
        
        """

        res = self.test_fn(args, ckpt_file=self.ckpt_file)

        if self.task_type == "3d_segmentation":
            if "rangebased" in res:
                (
                    _3D_predictions,
                    _3D_labels,
                    _2D_predictions,
                    _2D_labels,
                    range_filtered,
                    range_default,
                    input_data,
                ) = (
                    res["3Dpredictions"],
                    res["3Dlabels"],
                    res["2Dpredictions"],
                    res["2Dlabels"],
                    res["rangebased"],
                    res["default"],
                    res["input_data"] if "input_data" in res else [],
                )
            else:
                (
                    _3D_predictions,
                    _3D_labels,
                    _2D_predictions,
                    _2D_labels,
                    range_filtered,
                    range_default,
                    input_data,
                ) = (
                    res["3Dpredictions"],
                    res["3Dlabels"],
                    res["2Dpredictions"],
                    res["2Dlabels"],
                    None,
                    None,
                    res["input_data"] if "input_data" in res else [],
                )
        else:
            predictions, ground_truth, input_data = (
                res["predictions"],
                res["labels"],
                res["input_data"] if "input_data" in res else [],
            )

        if "3D" in self.dataset_type:
            metrics = self.compute3D_metrics(
                _3D_predictions,
                _3D_labels,
                _2D_predictions,
                _2D_labels,
                range_filtered,
                upload_metrics=False,
                return_metrics=True,
            )
        else:
            metrics = self.compute_metrics(
                predictions, ground_truth, upload_metrics=False, return_metrics=True
            )

        return metrics

    # correct the self.type when confirmed.
    def compute3D_metrics(
        self,
        pclpredictions,
        pcllabels,
        imgpredictions,
        imglabels,
        range_filtered,
        range_default,
        upload_metrics=True,
        return_metrics=False,
    ):
        metrics = {}
        if self.task_type == "3d_object_detection":
            raise NotImplementedError(
                "3D object detection evaluation has not been implemented yet"
            )

        elif self.task_type == "3d_segmentation":
            m = SegMetrics(
                n_classes=self.num_of_classes,
                labels=ast.literal_eval(self.class_labels),
                return_2D=True,
                return_3D=True,
                rangenet=True,
                default_ranges=range_default,
                include_ranges=True,
                range_labels=range_filtered,
            )

            m.evaluate3D(pcllabels, pclpredictions, rangelabels=range_filtered)
            m.evaluate2D(imglabels, imgpredictions)
            metrics = {
                "3DCM": m.get3DCM(),
                "3DrangeCM": m.get3DrangeCM(),
                "3DmIOU": m.get3DmIOU(),
                "3DrangemIOU": m.get3DrangemIOU(),
                "3DIOU": m.get3DIOU(),
                "3Drange3DIOU": m.get3DrangeIOU(),
                "3DDICE": m.get3DDICE(),
                "3DmDICE": m.get3DmDICE(),
                "3DrangeDICE": m.get3DrangeDICE(),
                "3DrangemDICE": m.get3DrangemDICE(),
                "3DAcc": m.get3Dacc(),
                "3DmAcc": m.get3Dmacc(),
                "3DrangeAcc": m.get3Drangeacc(),
                "3DrangemAcc": m.get3Drangemacc(),
                "class_labels": ast.literal_eval(self.class_labels),
            }

        # save metrics to S3
        if upload_metrics:
            object_key = os.path.join(
                self.expt_dir, "metrics_{}.pkl".format(self.cur_loop)
            )
            self.client.upload_object(
                object=metrics,
                storage_bucket=self.bucket_name,
                object_key=object_key,
                format="pkl",
            )

        if return_metrics:
            return metrics

        return

    def compute_metrics(
        self, predictions, ground_truth, upload_metrics=True, return_metrics=False
    ):
        metrics = {}
        if self.task_type == "object_detection":
            det_boxes, det_labels, det_scores, true_boxes, true_labels = batch_to_numpy(
                predictions, ground_truth
            )

            m = Metrics(
                det_boxes=det_boxes,
                det_labels=det_labels,
                det_scores=det_scores,
                true_boxes=true_boxes,
                true_labels=true_labels,
                num_classes=len(ast.literal_eval(self.class_labels)),
            )

            metrics = {
                "mAP": m.getmAP(),
                "AP": m.getAP(),
                "precision": m.getprecision(),
                "recall": m.getrecall(),
                "confusion_matrix": m.getCM().tolist(),
                "class_labels": ast.literal_eval(self.class_labels),
            }

        elif (
            (
                "single_label_classification" in self.task_type
                and self.dataset_type == "text"
            )
            or (
                "single_label_classification" in self.task_type
                and self.dataset_type == "2d_image"
            )
            or (
                "single_label_classification" in self.task_type
                and self.dataset_type == "numeric"
            )
        ):
            m = ClassificationMetrics(predictions, ground_truth)

            metrics = {
                "accuracy": m.get_accuracy(),
                "f1_score_per_class": m.get_f1_score_per_class(),
                "f1_score": m.get_f1_score(),
                "precision_per_class": m.get_precision_per_class(),
                "precision": m.get_precision(),
                "recall_per_class": m.get_recall_per_class(),
                "recall": m.get_recall(),
                "confusion_matrix": m.get_confusion_matrix(),
                "acc_per_class": m.get_acc_per_class(),
                "label_disagreement": m.get_label_disagreement(),
            }

        elif (
            self.task_type == "instance_segmentation"
            and self.dataset_type == "2d_image"
        ):
            metrics = segmentation_metrics(
                ground_truth,
                predictions,
                n_classes=self.num_of_classes,
            )

        elif (
            "multi_label_classification" in self.task_type
            and self.dataset_type == "text"
        ) or (
            "multi_label_classification" in self.task_type
            and self.dataset_type == "2d_image"
        ):
            m = MultiLabelClassificationMetrics(predictions, ground_truth)

            metrics = {
                "accuracy": m.get_accuracy(),
                "micro_f1": m.get_f1_score_micro(),
                "macro_f1": m.get_f1_score_macro(),
                "micro_precision": m.get_precision_micro(),
                "macro_precision": m.get_precision_macro(),
                "micro_recall": m.get_recall_micro(),
                "macro_recall": m.get_recall_macro(),
                "multilabel_confusion_matrix": m.get_confusion_matrix(),
                "hamming_loss": m.get_hamming_loss(),
            }

        else:
            raise ValueError(
                f"The selected task type is currently not supported, received type : {self.task_type}"
            )

        self.console.info(f"CURRENT LOOP---------------------->{self.cur_loop}")
        # save metrics to S3
        if upload_metrics:
            object_key = os.path.join(
                self.expt_dir, "metrics_{}.pkl".format(self.cur_loop)
            )
            self.console.warning(f"STORING METRIC FILE TO {object_key}")
            self.client.upload_object(
                object=metrics,
                storage_bucket=self.bucket_name,
                object_key=object_key,
                format="pkl",
            )

        if return_metrics:
            return metrics

        return

    def pre_softmax_to_softmax(self, pre_softmax_values):
        exp_values = np.exp(pre_softmax_values)
        softmax_values = exp_values / np.sum(exp_values)
        return softmax_values

    def logit_to_softmax(self, logit_values):
        return softmax(logit_values, dim=-1)

    def sigmoid_to_softmax(sigmoid_values):
        sigmoid_values = np.array(sigmoid_values)
        logits = np.log(sigmoid_values / (1 - sigmoid_values))
        exp_logits = np.exp(logits)
        softmax_values = exp_logits / (exp_logits + 1)
        return softmax_values

    def calculate_confidence(self, pre_softmax_values):
        return np.max(pre_softmax_values)

    def calculate_entropy(self, pre_softmax_values):
        exp_values = np.exp(pre_softmax_values)
        prob_distribution = exp_values / np.sum(exp_values)
        entropy = -np.sum(prob_distribution * np.log(prob_distribution))
        return entropy

    def calculate_margin(self, pre_softmax_values):
        max_value = np.max(pre_softmax_values)
        second_max_value = np.partition(pre_softmax_values, -2)[-2]
        margin = max_value - second_max_value
        return margin

    def infer(self, args):
        r"""
        A wrapper for your `infer` function which writes outputs to the specified S3 bucket. Returns `None`.

        Args:
            args: a dict whose keys include all of the arguments needed for your `infer` function which is defined in `processes.py`.

        """
        self.console.message(
            "Getting insights on currently unused/unlabelled train data"
        )
        self.console.message("This may take some time. Please be patient ............")

        ts = range(int(self.training_set_size))
        self.unlabeled = sorted(list(set(ts) - set(self.labeled)))
        args["cur_loop"] = self.cur_loop
        outputs = self.infer_fn(
            args, unlabeled=deepcopy(self.unlabeled), ckpt_file=self.ckpt_file
        )
        local_db = os.path.join(
            self.args["EXPT_DIR"], "infer_outputs_{}.db".format(self.cur_loop)
        )

        if os.path.exists(local_db) or outputs is not None:
            self.console.info(
                "Sending assessments on unlabelled train set to Alectio team"
            )
            self.console.warning(
                f"self.task_type--------------------->{self.task_type}"
            )
            if "classification" in self.task_type:
                outputs = outputs["outputs"]
                # finds correct activation as key i.e. 'sigmoid' or 'logits'
                activation = self.check_model_activations(outputs)

                # Remap to absolute indices
                logits_dict = {}
                remap_dict = {}
                try:
                    classification_distribution = self.client.read_file(
                        storage_bucket=self.bucket_name,
                        object_key=os.path.join(
                            self.expt_dir, "confidence_logit_entropy.pkl"
                        ),
                        format="pkl",
                    )
                except:
                    classification_distribution = {}
                # confidence_vals = []
                for key in outputs.keys():
                    remap_dict[key] = self.unlabeled.pop(0)

                while len(outputs) > 0:
                    for orig_ix, correct_ix in track(
                        remap_dict.items(), description="uploading infer data..."
                    ):
                        val = outputs.pop(orig_ix)
                        logits_dict[correct_ix] = {}

                        for a in activation:
                            logits_dict[correct_ix][a] = val[a]
                            if correct_ix not in classification_distribution:
                                classification_distribution[correct_ix] = {}
                            if a in ["pre_softmax", "logits"]:
                                softmax_val = softmax(val[a])
                            if a == "softmax":
                                softmax_val = val[a]
                            classification_distribution[correct_ix][self.cur_loop] = {
                                "confidence": self.calculate_confidence(softmax_val),
                                "margin": self.calculate_margin(softmax_val),
                                "entropy": self.calculate_entropy(softmax_val),
                            }

                            # if (
                            #     "input_data" in val
                            #     or correct_ix in self._uploaded_infer_index
                            # ):
                            #     image_key = os.path.join(
                            #         self.expt_dir, "infer", str(correct_ix) + ".png"
                            #     )
                            #     if correct_ix not in self._uploaded_infer_index:
                            #         self.client.upload_object(
                            #             object=val["input_data"],
                            #             storage_bucket=self.bucket_name,
                            #             object_key=image_key,
                            #             format="png",
                            #         )
                            #         self._uploaded_infer_index.append(correct_ix)
                            # else:
                            #     image_key = None
                            # confidence_vals.append(
                            #     {
                            #         "index": correct_ix,
                            #         "prediction": val["prediction"],
                            #         "confidence": round(
                            #             softmax(val[a])[val["prediction"]], 2
                            #         ),
                            #         "current_loop": self.cur_loop + 1,
                            #         "datamap_type": "infer_datamap",
                            #         "s3_image_path": image_key,
                            #         "project_id": self.project_id,
                            #         "experiment_id": self.experiment_id,
                            #     }
                            # )

                object_key = os.path.join(
                    self.expt_dir, "logits_{}.pkl".format(self.cur_loop)
                )
                self.client.upload_object(
                    object=logits_dict,
                    storage_bucket=self.bucket_name,
                    object_key=object_key,
                    format="pkl",
                )
                self.client.upload_object(
                    object=classification_distribution,
                    storage_bucket=self.bucket_name,
                    object_key=os.path.join(
                        self.expt_dir, "confidence_logit_entropy.pkl"
                    ),
                    format="pkl",
                )
            elif "object_detection" or "instance_segmentation" in self.task_type:
                object_key = os.path.join(
                    self.expt_dir, "infer_outputs_{}.db".format(self.cur_loop)
                )
                logits_conn = create_connection(local_db)

                if logits_conn is not None:
                    logits_cur = logits_conn.cursor()
                    sql = """
                            UPDATE indexes
                            SET row_id = ?
                            WHERE id = ?
                    """
                    for index, correct_ix in enumerate(self.unlabeled):
                        logits_cur.execute(sql, (correct_ix, index))

                    logits_conn.close()
                else:
                    raise ConnectionError("Cannot connect to softmax database")

                # upload sqlite db
                self.client.upload_file(local_db, self.bucket_name, object_key)
                # delete local version
                os.remove(local_db)
            else:
                raise ValueError("Use case not found")
        else:
            raise ValueError(
                "Infer outputs not returned. You must return outputs from the implemented infer() "
                "function. Please refer to the README on the Alectio SDK repository."
            )

        return

    def __call__(self):
        # SAVE DATAMAP SIZE
        datamap_size = len(self.getstate_fn(self.args).keys())
        self.console.info(f"TRAINING DATASET SIZE: {datamap_size}")
        error, response = self.api_client.POST_REQUEST(
            end_point="/sdk/v2/save_training_size",
            payload={"token": self.client_token, "train_dataset_size": datamap_size},
        )
        if error:
            self.console.error(
                "SOMETHING WENT WRONG WHILE SAVING YOUR TRAINING DATASET SIZE !\n PLEASE RECHECK"
            )
            return

        # START EXPERIMENT
        error, response = self.api_client.POST_REQUEST(
            end_point="/sdk/v2/start_experiment", payload={"token": self.client_token}
        )

        if response["status"] == "STARTED":
            count = 0
            while True:
                error, response = self.api_client.POST_REQUEST(
                    end_point="/sdk/v2/sdk_response",
                    payload={"token": self.client_token},
                )
                if error:
                    self.console.error(
                        "SOMETHING WENT WRONG WHILE TRYING TO CONNECT SDK WITH ALECITO SERVER !!\nREACH OUT TO ALECTIO ADMIN"
                    )
                    return
                if response["status"] == "FETCHED":
                    self.co2_tracker.start()
                    print("\n")
                    one_loop_response = self.one_loop(response)
                    count = 0
                    self.co2_tracker.stop()

                if response["status"] == "FINISHED":
                    print("\n")
                    self.console.message("Experiment complete")

                    # co2 emissions upload to bucket and delete local file
                    local_emission_file_path_json = os.path.join(
                        self.co2_dir, "emissions.json"
                    )
                    local_emission_file_path_csv = os.path.join(
                        self.co2_dir, "emissions.csv"
                    )
                    co2_df = pd.read_csv(local_emission_file_path_csv)
                    co2_df.to_json(local_emission_file_path_json)
                    emission_file_path = os.path.join(
                        self.expt_dir, f"emissions_{self.experiment_id}.json"
                    )
                    self.client.upload_file(
                        storage_bucket=self.bucket_name,
                        file_path=local_emission_file_path_json,
                        object_key=emission_file_path,
                    )
                    os.remove(local_emission_file_path_csv)
                    os.remove(local_emission_file_path_json)

                    # time_saved upload to bucket and delete local file
                    local_time_saved_file_path_json = os.path.join(
                        self.time_saved_dir, "time_saved.json"
                    )
                    local_time_saved_file_path_csv = os.path.join(
                        self.time_saved_dir, self.time_saved_file
                    )
                    time_saved_df = pd.read_csv(local_time_saved_file_path_csv)
                    time_saved_df.to_json(local_time_saved_file_path_json)
                    time_saved_file_path = os.path.join(
                        self.expt_dir, f"time_saved_{self.experiment_id}.json"
                    )
                    self.client.upload_file(
                        storage_bucket=self.bucket_name,
                        file_path=local_time_saved_file_path_json,
                        object_key=time_saved_file_path,
                    )
                    os.remove(local_time_saved_file_path_json)
                    os.remove(local_time_saved_file_path_csv)
                    break
                if response["status"] == "WAITING":
                    if count == 0:
                        print("\n")

                        self.console.warning("Waiting for server.")
                        count += 1
                        time.sleep(10)
                    else:
                        time.sleep(10)
                        print(".", end="", flush=True)
                if response["status"] == "FAILED":
                    self.console.warning("YOUR EXPERIMENT IS FAILED.")
                    break
