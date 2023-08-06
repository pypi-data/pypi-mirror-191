from typing import Tuple, List
from enum import Enum
from types import FunctionType
from inspect import getsource
from cerebrium.models.base import ModelType


CerebriumFlow = List[Tuple[ModelType, str, FunctionType]]


def _flow_string(flow: CerebriumFlow):
    """
    Convert a flow to a string.

    Args:
        flow (CerebriumFlow): The flow to convert.

    Returns:
        str: The flow as a string.
    """
    string = ""
    for i, component in enumerate(flow):
        val = component[0].value
        string += val
        if i != len(flow) - 1:
            string += "->"
    return string


def _get_function_arg(def_string: str) -> List[str]:
    """
    Return the arguments of a string function definition as a list of strings.

    Args:
        def_string: The string function definition line.

    Returns:
        A list of strings containing the arguments of the function.
    """
    argument_bracket_1 = def_string.find("(")
    argument_bracket_2 = def_string.find(")")
    argument_str = def_string[argument_bracket_1 + 1 : argument_bracket_2]
    return argument_str.split(",")


def _check_input_tuple(model_flow: CerebriumFlow):
    if len(model_flow) == 2:
        if (
            not isinstance(model_flow[0], list)
            and not isinstance(model_flow[0], tuple)
            and not isinstance(model_flow[1], list)
            and not isinstance(model_flow[1], tuple)
        ):
            model_flow = [model_flow]
    elif len(model_flow) == 3:
        if (
            not isinstance(model_flow[0], list)
            and not isinstance(model_flow[0], tuple)
            and not isinstance(model_flow[1], list)
            and not isinstance(model_flow[1], tuple)
            and not isinstance(model_flow[2], list)
            and not isinstance(model_flow[2], tuple)
        ):
            model_flow = [model_flow]
    return model_flow


def _check_special_model(model_flow: CerebriumFlow):
    """
    Check if the model flow is a special model type. (These are handled differently, and so require a different check.)

    Args:
        model_flow: The model flow to check.

    Returns:
        A boolean indicating whether the model flow is a special model.
    """
    if model_flow[0][0] == ModelType.PREBUILT:
        if len(model_flow) != 1:
            raise TypeError(
                f"Prebuilt models must be a tuple or list of length 1, but is {len(model_flow)}"
            )


def _check_valid_model(
    model_type: ModelType, model_filepath: str, pipeline_position: int
):
    """
    Check that the model is valid, raising an error if not.

    Args:
        model_type: The type of the model.
        model_filepath: The filepath of the model.
        pipeline_position: The position of the model in the pipeline.
    """
    # Check typing
    if not isinstance(model_type, ModelType):
        raise TypeError(
            f"Model {pipeline_position}: model_type must be of type ModelType, but is {type(model_type)}. Please ensure you use a valid Cerebrium typing."
        )
    if not isinstance(model_filepath, str):
        raise TypeError(
            f"Model {pipeline_position}: model_filepath must be of type str, but is {type(model_filepath)}"
        )

    # Check that the models are not "special" models
    if pipeline_position > 0:
        if model_type == ModelType.PREBUILT:
            raise TypeError(
                f"Model {pipeline_position}: Prebuilt models can only be used as the first model in a pipeline."
            )

    # Check valid file type
    if (
        model_type != ModelType.PREBUILT
        and not model_filepath.endswith(".pkl")
        and not model_filepath.endswith(".pt")
        and not model_filepath.endswith(".json")
        and not model_filepath.endswith(".onnx")
    ):
        raise TypeError(
            f"Model {pipeline_position}: model_filepath must be be a valid file type, but is {model_filepath}"
        )


def _check_processor(processor: FunctionType, pipeline_position: int, stage: str):
    """
    Check that the postprocessor is valid, raising an error if not.

    Args:
        processor: The processor function.
        pipeline_position: The position of the post-processor in the pipeline.
    """
    if not isinstance(processor, FunctionType) and processor is not None:
        raise TypeError(
            f"Model {pipeline_position}: The post-processing function must be of type FunctionType, but is {type(processor)}"
        )
    else:
        if processor is not None:
            processor_str = getsource(processor).replace("\t", "    ").split("\n")
            processor_args = _get_function_arg(processor_str[0])
            if processor_args[0] == "":
                processor_args = []
            if len(processor_args) != 1:
                raise NotImplementedError(
                    f"Model {processor}: The {stage}-processing function must have exactly one argument, but has {len(processor_args)}"
                )

            contains_return = [s.strip()[:6] == "return" for s in processor_str]
            if not any(contains_return):
                raise NotImplementedError(
                    f"Model {processor}: The {stage}-processing function must return a value, but does not."
                )


def _check_flow_type(model_flow: any) -> CerebriumFlow:
    """
    Check if the given model_flow is a valid CerebriumFlow.

    Args:
        model_flow: The model_flow to check.

    Returns:
        CerebriumFlow: The model_flow if it is valid. Adds post-process and outer list of necessary.

    Raises:
        TypeError: If the model_flow is not a valid CerebriumFlow.
    """

    # Raise error if model_flow is not a list or tuple
    if not isinstance(model_flow, list) and not isinstance(model_flow, tuple):
        raise TypeError(
            f"model_flow must be a tuple or list, but is {type(model_flow)}"
        )

    # If the model_flow is a list or tuple, check if all elements are tuples for single model flow
    model_flow = _check_input_tuple(model_flow)

    # Check if the model_flow is a special model
    _check_special_model(model_flow)

    # Check if the model_flow is a valid model flow
    for i, flow_component in enumerate(model_flow):
        model_type, model_filepath = flow_component[0], flow_component[1]
        _check_valid_model(model_type, model_filepath, i)
        if len(flow_component) == 3:
            if not isinstance(flow_component[2], dict):
                # Assume a post-process function, backwards compatibility
                _check_processor(flow_component[2], i, "post")
                model_flow[i] = (
                    model_type,
                    model_filepath,
                    {"post": flow_component[2]},
                )
            else:
                # Check if the processing functions are valid
                keys = set(flow_component[2].keys())
                if keys - {"post", "pre"} != set():
                    raise TypeError(
                        f"Model {i}: The processing functions contains invalid keys {str(keys - {'post', 'pre'})}. Please use only 'post' and 'pre'."
                    )
                if "post" in flow_component[2]:
                    post = flow_component[2]["post"]
                    _check_processor(post, i, "post")
                if "pre" in flow_component[2]:
                    pre = flow_component[2]["pre"]
                    _check_processor(pre, i, "pre")
        else:
            model_flow[i] = (model_type, model_filepath, {})
    return model_flow
