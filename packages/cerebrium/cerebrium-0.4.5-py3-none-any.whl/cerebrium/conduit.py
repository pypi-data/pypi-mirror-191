from cloudpickle import load as pickle_load, dump
from torch.jit import load as torchscript_load
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import os
import re
import tempfile
import zipfile
import requests
import json
import enum
from xgboost import XGBClassifier, XGBRegressor
from sklearn.base import ClassifierMixin, RegressorMixin, BaseEstimator
from torch.nn import Module as TorchModule
from torch import Tensor, device
from torch.cuda import is_available
from numpy import atleast_2d, ndarray
import onnxruntime
from inspect import getsource

from cerebrium import __version__
from cerebrium.flow import CerebriumFlow, _check_flow_type, _flow_string
from cerebrium.models.base import ModelType
from cerebrium.models.torch import TorchModel
from cerebrium.models.sklearn import (
    SKRegressorModel,
    SKClassifierModel,
    SKPreprocessorModel,
)
from cerebrium.models.onnx import OnnxModel
from cerebrium.logging.base import LoggingPlatform
from cerebrium.logging.censius import CensiusLogger
from cerebrium.logging.arize import ArizeLogger
from cerebrium.requests import _cerebrium_request, _poll_deployment_status

REGEX_NAME_PATTERN = "^[a-z0-9-]*$"


class Hardware(enum.Enum):
    CPU = "cpu"
    GPU = "gpu"


class Conduit:
    """
    The Conduit class encompasses the logic required to create a computational graph from a given model flow, as well as the logic required to run the graph on a given input.

    Args:
        name (str): The name to deploy the flow under.
        api_key (str): The API key for the Cerebrium account.
        flow (CerebriumFlow): The flow to deploy. This is a list of ModelType, model path and postprocessor tuples, as such:
            [(model_type.TORCH, "model.pt", postprocess_f)]
        hardware (Hardware): The hardware to deploy the model on.
    """

    def __init__(
        self,
        name: str = "",
        api_key: str = "",
        flow: CerebriumFlow = [],
        hardware: Hardware = None,
        from_json: str = "",
    ):
        if from_json == "":
            assert name != "" and api_key != ""
            # Check that the flow name is valid
            if len(name) > 20:
                raise ValueError("Conduit name must be less than 20 characters")
            if not bool(re.match(REGEX_NAME_PATTERN, name)):
                raise ValueError(
                    "Conduit name can only contain lowercase alphanumeric characters and hyphens"
                )
            self.name = name
            self.api_key = api_key
            if flow is not None:
                self.flow = _check_flow_type(flow)
            self.logger_configs = {}
        else:
            raise NotImplementedError("Loading from JSON is not yet implemented")
            # self.init_json(from_json)
        self.graph = []
        self.ready = False
        self.loggers = {}
        if hardware:
            self.hardware = hardware
        else:
            self.hardware = self._determine_hardware()
        self.device = (
            "cuda" if self.hardware == Hardware.GPU and is_available() else "cpu"
        )

    def _determine_hardware(self):
        # Set the default hardware to GPU if the flow contains a Torch model or a ONNX model
        if any(
            [
                model_type in [ModelType.TORCH, ModelType.ONNX]
                for model_type, _, _ in self.flow
            ]
        ):
            return Hardware.GPU
        else:
            return Hardware.CPU

    def load(self, directory: str = "/cache/", direct_from_flow: bool = False):
        """
        Load the Conduit components from the stored Model Flow into the computation graph.

        Args:
            directory (str): The directory to load the Conduit components from.
        """
        if self.flow == []:
            raise ValueError("Conduit is empty. Please add models to the Conduit flow.")
        else:
            for model_type, model_path, _ in self.flow:
                # Use correct path
                if direct_from_flow:
                    model_path = os.path.abspath(model_path)
                else:
                    model_path = directory + model_path.split("/")[-1]

                # Torch
                if model_type == ModelType.TORCH:
                    if model_path.endswith(".pt"):
                        model: TorchModule = torchscript_load(model_path)
                    else:
                        with open(model_path, "rb") as f:
                            model: TorchModule = pickle_load(f)
                    model.to(self.device)
                    self.graph.append(TorchModel(model))

                # ONNX
                elif model_type == ModelType.ONNX:
                    model = onnxruntime.InferenceSession(
                        model_path,
                        providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
                    )
                    self.graph.append(OnnxModel(model))

                # XGBoost
                elif model_type == ModelType.XGBOOST_CLASSIFIER:
                    if model_path.endswith("json"):
                        model = XGBClassifier()
                        model.load_model(model_path)
                    else:
                        with open(model_path, "rb") as f:
                            model: XGBClassifier = pickle_load(f)
                    self.graph.append(SKClassifierModel(model))
                elif model_type == ModelType.XGBOOST_REGRESSOR:
                    if model_path.endswith("json"):
                        model = XGBRegressor()
                        model.load_model(model_path)
                    else:
                        with open(model_path, "rb") as f:
                            model: XGBRegressor = pickle_load(f)
                    self.graph.append(SKRegressorModel(model))

                # Scikit-Learn Interface
                elif model_type == ModelType.SKLEARN_CLASSIFIER:
                    with open(model_path, "rb") as f:
                        model: ClassifierMixin = pickle_load(f)
                    self.graph.append(SKClassifierModel(model))
                elif model_type == ModelType.SKLEARN:
                    with open(model_path, "rb") as f:
                        model: RegressorMixin = pickle_load(f)
                    self.graph.append(SKRegressorModel(model))
                elif model_type == ModelType.SKLEARN_PREPROCESSOR:
                    with open(model_path, "rb") as f:
                        model: BaseEstimator = pickle_load(f)
                    self.graph.append(SKPreprocessorModel(model))
            self.ready = True

    def run(self, data: list):
        """
        Run the Conduit on the given input with the stored computational graph.

        Args:
            data (list): The input data to run the Conduit on.
        """
        if not self.ready:
            return "Conduit not ready. Conduit components have not been loaded."
        else:
            if self.flow[0][0] == ModelType.TORCH:
                data = Tensor(atleast_2d(data)).to(self.device)
            elif self.flow[0][0] == ModelType.ONNX:
                if isinstance(data, list):
                    data = data[0]
                else:
                    pass
            else:
                data = atleast_2d(data)

            for (model_type, _, processors), (model) in zip(self.flow, self.graph):
                # Run the preprocessor
                preprocessor, postprocessor = processors.get(
                    "pre", None
                ), processors.get("post", None)
                if preprocessor:
                    data = preprocessor(data)

                # Ensure that the input data is the correct type
                if model_type == ModelType.TORCH and not isinstance(data, Tensor):
                    data = Tensor(data).to(self.device)
                elif model_type != ModelType.TORCH and isinstance(data, Tensor):
                    data = data.detach().to("cpu").numpy()

                # Run the model
                data = model.predict(data)

                # Run the postprocessor
                if postprocessor:
                    data = postprocessor(data)

            # Ensure that final output is a list
            if isinstance(data, Tensor):
                data = data.detach().to("cpu").numpy().tolist()
            elif isinstance(data, ndarray):
                data = data.tolist()
            elif not isinstance(data, list) and not isinstance(data, dict):
                data = [data]
            return data

    def add_model(self, model_type, model_path, postprocessor=None):
        temp_flow = self.flow
        temp_flow.append((model_type, model_path, postprocessor))
        self.flow = _check_flow_type(temp_flow)
        self._determine_hardware()

    def add_logger(
        self,
        platform: LoggingPlatform,
        platform_authentication: dict,
        features: list,
        targets: list,
        platform_args: dict = {},
        log_ms: bool = False,
    ):
        platform = platform.value
        self.logger_configs[platform] = {
            "platform_authentication": platform_authentication,
            "features": features,
            "targets": targets,
            "platform_args": platform_args,
            "log_ms": log_ms,
        }

    def setup_loggers(self):
        for platform, config in self.logger_configs.items():
            if platform == "Censius":
                self.loggers["Censius"] = CensiusLogger(
                    config["platform_authentication"],
                    self.name,
                    config["features"],
                    config["targets"],
                    config["platform_args"],
                    config["log_ms"],
                )
            elif platform == "Arize":
                self.loggers["Arize"] = ArizeLogger(
                    config["platform_authentication"],
                    self.name,
                    config["features"],
                    config["targets"],
                    config["platform_args"],
                    config["log_ms"],
                )

    def create_json_config(self, filename):
        """
        Return the Conduit's configuration as a JSON string.

        Returns:
            str: The Conduit's configuration as a JSON string.
        """

        def get_function_names(processors):
            names = {}
            if "pre" in processors:
                names["pre"] = processors["pre"].__name__
            else:
                names["pre"] = None
            if "post" in processors:
                names["post"] = processors["post"].__name__
            else:
                names["post"] = None
            return names

        json_flow = [
            (model_type.value, model_path, get_function_names(processors))
            for model_type, model_path, processors in self.flow
        ]
        with open(filename, "w") as f:
            json.dump(
                {
                    "name": self.name,
                    "flow": json_flow,
                    "api_key": self.api_key,
                    "logger_configs": str(self.logger_configs),
                    "processors": [
                        {
                            "pre": None
                            if p[2].get("pre", None) is None
                            else getsource(p[2]["pre"]),
                            "post": None
                            if p[2].get("post", None) is None
                            else getsource(p[2]["post"]),
                        }
                        for p in self.flow
                    ],
                },
                f,
            )

    def init_json(self, json_config_path):
        """
        Initialize the Conduit from a JSON configuration.

        Args:
            json_config_path (str): The path to the Conduit's JSON configuration.
        """
        with open(json_config_path, "r") as f:
            json_config = json.load(f)
        self.name = json_config["name"]
        self.api_key = json_config["api_key"]
        self.logger_configs = json_config["logger_configs"]
        for postprocessor in json_config["postprocessors"]:
            if postprocessor is not None:
                exec(postprocessor)
        self.flow = [
            (ModelType(model_type), model_path, eval(postprocessor))
            for model_type, model_path, postprocessor in json_config["flow"]
        ]

    def _upload(self, url):
        """
        Upload the Conduit to Cerebrium.

        Args:
            url (str): The upload URL.

        Returns:
            dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the flow token if successful.
        """
        if self.flow == []:
            raise ValueError("Conduit is empty. Please add models to the Conduit.")
        else:
            # Clear the graph
            if self.ready:
                print("Clearing the Conduit graph...")
                self.graph = []
                self.ready = False
            # Clear the loggers
            if self.loggers:
                print("Clearing the Conduit loggers...")
                self.loggers = {}
            self.graph = []
            self.ready = False
            # Create a temporary directory to store the Conduit zip
            with tempfile.TemporaryDirectory() as tmpdir:
                # Create a zip file of the Conduit, writing the model files and Conduit object to the zip
                with zipfile.ZipFile(tmpdir + f"/{self.name}.zip", "w") as zip:
                    for _, model_path, _ in self.flow:
                        true_path = os.path.abspath(model_path)
                        zip.write(true_path, os.path.basename(true_path))
                    self.create_json_config("conduit.json")
                    zip.write("conduit.json")
                    with open("conduit.pkl", "wb") as f:
                        dump(self, f)
                    zip.write("conduit.pkl")
                # Upload the Conduit zip, chunking with tqdm for progress bar
                with open(tmpdir + f"/{self.name}.zip", "rb") as f:
                    headers = {
                        "Content-Type": "application/zip",
                    }
                    with tqdm(
                        total=os.path.getsize(tmpdir + f"/{self.name}.zip"),
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        colour="#EB3A6F",
                    ) as pbar:
                        wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                        response = requests.put(
                            url,
                            headers=headers,
                            data=wrapped_f,
                            timeout=60,
                            stream=True,
                        )
                    data = {} if not response.text else json.loads(response.text)
                    return {"status_code": response.status_code, "data": data}

    def deploy(self, dry_run=False):
        """
        Deploy the Conduit to Cerebrium.

        Returns:
            dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the flow token if successful.
        """
        # Deploy the conduit
        if not dry_run:
            # Check that the user is authenticated
            upload_url_response = _cerebrium_request(
                "getUploadUrl",
                self.api_key,
                payload={
                    "name": self.name,
                    "cerebriumVersion": __version__,
                    "hardware": self.hardware.value,
                },
                enable_spinner=(
                    True,
                    ("Authenticating...", "Authenticated with Cerebrium!"),
                ),
            )
            upload_url = upload_url_response["data"]["uploadUrl"]

            # If Prebuilt model, register with modal
            if self.flow[0][0] == ModelType.PREBUILT:
                print("Registering with Cerebrium...")
                prebuilt_model_response = _cerebrium_request(
                    "pre-built-model",
                    self.api_key,
                    payload={
                        "arguments": {
                            "name": self.name,
                            "externalId": self.flow[0][1],
                            "modelType": _flow_string(self.flow),
                        }
                    },
                    enable_spinner=(
                        True,
                        ("Registering with Cerebrium...", "Registered with Cerebrium!"),
                    ),
                )
                endpoint = prebuilt_model_response["data"]["internalEndpoint"]
                print("🌍 Endpoint:", endpoint)
                return endpoint
            else:
                # Upload the conduit artefacts to Cerebrium
                print("⬆️  Uploading conduit artefacts...")
                self._upload(upload_url)
                print("✅ Conduit artefacts uploaded successfully.")
                endpoint = _poll_deployment_status(self.name, self.api_key)
                print("🌍 Endpoint:", endpoint)
                return endpoint
        else:
            if self.flow[0][0] == ModelType.PREBUILT:
                raise NotImplementedError("Dry run not supported for prebuilt models")
            self.load(direct_from_flow=True)
            return self
