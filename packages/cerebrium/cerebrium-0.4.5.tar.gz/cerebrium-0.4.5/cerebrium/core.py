from cerebrium.flow import CerebriumFlow
from cerebrium.conduit import Conduit, Hardware
from cerebrium.utils import _convert_input_data

import requests
import json
from typing import Union

from numpy import ndarray
from torch import Tensor


def model_api_request(
    model_endpoint: str,
    data: Union[list, ndarray, Tensor],
    api_key: str,
) -> dict:
    """
    Make a request to the Cerebrium model API.

    Args:
        model_endpoint (str): The endpoint of the model to make a request to.
        data (list): The data to send to the model.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data.
    """

    payload = _convert_input_data(data)
    headers = {"Authorization": api_key}
    response = requests.request(
        "POST", model_endpoint, headers=headers, data=json.dumps(payload), timeout=30
    )
    return {"status_code": response.status_code, "data": json.loads(response.text)}


def deploy(
    model_flow: CerebriumFlow,
    name: str,
    api_key: str,
    dry_run=False,
    loggers=[],
    hardware=Hardware.CPU,
) -> str:
    """
    Deploy a model to Cerebrium.

    Args:
        model_flow (CerebriumFlow): The flow to deploy. This is a list of ModelType, model path and postprocessor tuples, as such:
            [(ModelType.TORCH, "model.pt", postprocess_f)]
        name (str): The name to deploy the flow under.
        api_key (str): The API key for the Cerebrium account.
        dry_run (bool): Whether to run the deployment in dry-run mode.
            If True, the model will not be deployed, and deploy will return a flow function which can be used to test with.
        logger (dict): A logger configuration used to create logger which will log ML stats to a metrics platform.
        hardware (Hardware): The hardware to deploy the model on. Can be either "cpu" or "gpu".

    Returns:
        str: The newly deployed REST endpoint. If dry_run is True, a flow function will be returned instead.
    """
    # Check that the flow is valid and create the Conduit
    conduit = Conduit(name, api_key, model_flow, hardware)
    if loggers != []:
        for logger in loggers:
            conduit.add_logger(**logger)
    return conduit.deploy(dry_run=dry_run)
