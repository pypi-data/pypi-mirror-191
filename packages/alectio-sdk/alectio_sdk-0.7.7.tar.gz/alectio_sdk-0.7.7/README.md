## Requirements

Python3 (Required)
PIP3 (Required)
Ubuntu 16.04+ / MacOS / Windows 10

GCC / C++ (Will depend on the OS you are using. Ubuntu, and MacOS it comes by default. Some flavors of Linux distribution like Amazon Linux/RED Hat Linux might not have GCC or C++-related libraries installed)

For this tutorial, we are assuming you are using Python3 and PIP3. Also, make sure you have the necessary build tools installed (might vary from OS to OS). If you get any errors while installing any dependent packages feel free to reach out to us but most of it can quickly be solved by a simple Google search.

## Alectio SDK

AlectioSDK is a package that enables developers to build an ML pipeline as a Flask app to interact with Alectio's platform. It is designed for Alectio's clients, who prefer to keep their model and data on their own server.

The package is currently under active development. More functionalities that aim to enhance robustness will be added soon, but for now, the package provides a class `alectio_sdk.sdk.Pipeline` that interfaces with customer-side processes in a consistent manner. Customers need to implement 4 processes as python functions:

- A process to train the model
- A process to test the model
- A process to apply the model to infer unlabeled data
- A process to assign each data point in the dataset to a unique index (Refer to one of the examples to know how)

A Pipeline can be created inside the `main.py` file using the following syntax:

```python
import yaml
from alectio_sdk.sdk import Pipeline
from processes import train, test, infer, getdatasetstate

# All the variables can be declared inside the .yaml file
with open("./config.yaml", "r") as stream:
 args = yaml.safe_load(stream)

# Initialising the Experiment Pipeline
AlectioPipeline = Pipeline(
 name=args["exp_name"],
 train_fn=train, # A process to train the model
 test_fn=test, # A process to test the model
 infer_fn=infer, # A process to apply the model to infer unlabeled data
 getstate_fn=getdatasetstate, # A process to assign each data point in the dataset to a unique index
 args=args, # Any arguments that user ants to use inside his train, test, infer functions.
 token="xxxxxx7041a6xxxxx7948cexxxxxxxx", # Experiment token
 multiple_initialisations={"seeds": [], "limit_value": 0}, # Multiple seed initialisation feature
)
```

Refer to the alectio examples for more clarity on the use of the Pipeline class.

## Train the Model

The logic for training the model should be implemented in this process. The function should look like this:

```python
def train(args, labeled, resume_from, ckpt_file):
    """
    Training Function
    
    Input args:
    args* # Arguments passed to Alectio Pipeline
    labeled: list # List of labeled indices for training
    resume_from: str # Path to last checkpoint file
    ckpt_file: str # Path to saved model
    
    Returns:
    None
    or
    output_dict: dict # Labels and Hyperparams
    """

    # implement your logic to train the model
    # with the selected data indexed by `labeled`
    # lbs <- dictionary of indices of train data and their ground-truth
    
    return {'labels': lbs, 'hyperparams': hyperparameters}
```

The name of the function can be anything you like. It takes an argument as shown in the example above.
| key | value |
|--|--|
| resume_from | a string that specifies which checkpoint to resume from |
| ckpt_file | a string that specifies the name of checkpoint to be saved for the current loop |
| labeled | a list of indices of selected samples used to train the model in this loop |

Depending on your situation, the samples indicated in labeled might not be labeled (despite the variable name). We call it labeled because, in the active learning setting, this list represents the pool of samples iteratively labeled by the human oracle.

## Test the Model

The logic for testing the model should be implemented in this process. The function representing this process should look like this:

```python
def test(args, ckpt_file):
    """
    testing function

    Input args:
    args* # Arguments passed to Alectio Pipeline
    ckpt_file: str # Path to saved model

    Returns:
    output_dict: dict # Preds and Labels
    """
    # implement your testing logic here

    # put the predictions and labels into
    # two dictionaries

    # lbs <- dictionary of indices of test data and their ground-truth
    # prd <- dictionary of indices of test data and their prediction
    
    return {'predictions': prd, 'labels': lbs}
```

The test function takes arguments as shown in the example above.

| key | value |
|--|--|
| ckpt_file | a string that specifies which checkpoint to test model |

The test function needs to return a dictionary with two keys:

| key | value |
|--|--|
| predictions | a dictionary of an index and a prediction for each test sample |
| labels | a dictionary of an index and a ground truth label for each test sample |

The format of the values depends on the type of ML problem. Please refer to the examples directory for details.

## Apply Inference

The logic for applying the model to infer the unlabeled data should be implemented in this process. The function representing this process should look like this:

```python
def infer(args, unlabeled, ckpt_file):
    """
    Inference Function

    Input args:
    args* # Arguments passed to Alectio Pipeline
    unlabeled: list # List of labeled indices for inference
    ckpt_file: str # Path to saved model

    returns:
    output_dict: dict
    """
    # implement your inference logic here

    # outputs <- save the output from the model on the unlabeled data as a dictionary
    return {'outputs': outputs}
```

The infer function takes an argument payload, which is a dictionary with 2 keys:

| key | value |
|--|--|
| ckpt_file | a string that specifies which checkpoint to use to infer on the unlabeled data |
| unlabeled | a list of of indices of unlabeled data in the training set |

The infer function needs to return a dictionary with one key.

| key | value |
|--|--|
| outputs | a dictionary of indexes mapped to the models output before an activation function is applied |

For example, if it is a classification problem, return the output **before** applying softmax.
For more details about the format of the output, please refer to the [examples](./examples) directory.

## config.yaml

Put in all the requirements that are required for the model to train. This will be read and used in processes.py when the model trains. For example if config.yaml looks like this:

``` python
LOG_DIR:  "./log"
DATA_DIR: "./data"
EXPT_DIR: "./log"
exptname:  "ManualAL"  

# Model configs
backbone:     "Resnet101"
description:  "Pedestrian detection"
epochs: 10
.
.
```

You can access them inside your any of the above 4 processes as lets say args["backbone"] , args["description"] etc.

## SDK- Features

### 1. Tracking CO2 emissions

The alectio SDK is capable of tracking the CO2 emissions during the experiment. The SDK uses an open-source package called code carbon to track the CO2 emissions along with the (CPU, GPU, and RAM) usage. This data is tracked and synced, once the experiment ends, with the user account where the user can see the total CO2 emission on his dashboard.

### 2. Time-Saved Information

The SDK uses linear interpolation to estimate the time that a user saved to train his model in each active learning cycle. The time-saved information is logged after each AL cycle and gets synced with the platform at the end of the experiment. The time-saved insights can be seen on the user dashboard.

### 3. Storing Hyperparameters

The SDK has the ability to track the hyperparameters for each AL cycle. To use this feature the user just needs to return a dictionary of their hyperparameters. Currently, the SDK supports a limited number of hyperparameters, the list of these parameters is shown below:

```python
hyperparameter_names = [
                "optimizer_name", # Name of the optimizer used
                "loss", # Loss of the training process
                "running_loss", # Running Loss 
                "epochs", # Number of epochs for which the model was trained 
                "batch_size", # batch size on which the model was trained
                "loss_function", # name of loss function used for training
                "activation", # List of activation functions used 
                "optimizer", # Can be a state_dict in case of Pytorch
            ]
```

The syntax for storing these values is shown in the train function section.

### 4. Running Multiple Seed Initialization

The SDK can also help the user choose the right seed for his experiment by training his model on a range of seed values and selecting the best seed depending on the performance of models on these seed values. In order to use this feature the user can just use the multiple_initialisations argument of the Alectio Pipeline. The syntax is as shown below:

```python
from alectio_sdk.sdk import Pipeline

AlectioPipeline = Pipeline(
    name=args["exp_name"],
    train_fn=train,
    test_fn=test,
    infer_fn=infer,
    getstate_fn=getdatasetstate,
    args=args,
    token="xxxxxx7041a6xxxxx7948cexxxxxxxx",
    multiple_initialisations={"seeds": [10, 42, 36, 78], "limit_value": 4000},
)
```

The input of this argument is a dict with 2 keys.

| key | value |
|--|--|
| seed | a list containing different seed values you want to test your model on. |
| limit_value | The number of samples from which you want to select the training samples from. |

## Installation

### 0. Key Management

If you have not already created your Client ID and Client Secret then do so by visiting:

 1. Open <https://portal.alectio.com>
 2. Login here and create a project and an experiment.
 3. An experiment token will be generated.
 4. Enter your experiment token in main.py to authenticate.
 5. Please visit <https://github.com/alectio/AlectioExamples> for detailed examples.

### 1. Set up a virtual environment

We recommend to set-up a virtual environment.
For example, you can use python's built-in virtual environment via:

```python
python3 -m venv env
source env/bin/activate
```

### 2. Install AlectioSDK/requirements
  
```python
pip install .
pip install -r requirements.txt
```

### 3. Run Examples

The remaining installation instructions are detailed in the [examples](./examples) directory. We cover one example for [topic classification](./examples/topic_classification), one example for [image classification](./examples/image_classification) and one example for [object detection](./examples/object_detection)
