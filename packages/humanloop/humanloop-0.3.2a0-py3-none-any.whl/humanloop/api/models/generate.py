import abc
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .model_config import ModelConfig, ModelProvider
from .utils import KeyValues, RootBaseModel


class BaseGenerate(BaseModel, abc.ABC):
    project: str = Field(
        title="Project name",
        description="Unique project name. The model configuration will be "
        "added to the project if necessary.",
    )
    inputs: KeyValues = Field(
        title="Model input data",
        description="List of name, value pairs for the inputs used by your prompt "
        "template, or directly by your model.",
    )
    source: Optional[str] = Field(
        title="Source",
        description="What was source of the model used for this generation?"
        "e.g. website-landing-page",
    )
    provider_api_keys: Dict[ModelProvider, str] = Field(
        title="Provider API Keys",
        description="API keys required by each provider to make API calls. "
        "These API keys are not stored by Humanloop.",
    )
    num_samples: Optional[int] = Field(
        title="Number of samples",
        description="How many generations to make for each set of inputs for the specified model config.",
        default=1,
    )
    logprobs: Optional[int] = Field(
        title="Log probabilities of most likely n tokens",
        description="Include the log probabilities of the top n tokens in the provider_response",
        default=None,
    )
    suffix: Optional[str] = Field(
        title="Completion suffix",
        description="The suffix that comes after a completion of inserted text. "
        "Useful for completions that act like inserts.",
    )
    user: Optional[str] = Field(
        title="End-user identifier",
        description="End-user id passed through to provider call.",
    )
    metadata: Optional[KeyValues] = Field(
        title="Metadata",
        description="Any additional metadata that you would like to log for reference.",
    )


class ProjectGenerate(BaseGenerate):
    project: str = Field(
        title="Project name",
        description="Unique project name. This project must already have an active deployment configured.",
    )


class ExperimentGenerate(BaseGenerate):
    experiment_id: str = Field(
        title="ID of experiment",
        description="If an experiment ID is provided a model config will be "
        "sampled from the experiments active model configs.",
    )
    # overrides description of BaseModel num_samples
    num_samples: Optional[int] = Field(
        title="Number of samples",
        description="How many generations to make for each set of inputs. "
        "Each generate will sample a model config for an experiment.",
        default=1,
    )


class ModelConfigGenerate(BaseGenerate):
    model_config_id: str = Field(
        title="ID of a model config",
        description="The model config specified will be used to create a generation.",
    )


class RawGenerate(BaseGenerate):
    model_config: ModelConfig = Field(
        title="The configuration of your model",
        description="The model config provided will be recorded and used to create a generation.",
    )


class GenerateRequest(RootBaseModel):
    # Used as Pydantic request body type for uplink client
    __root__: Union[
        RawGenerate, ModelConfigGenerate, ExperimentGenerate, ProjectGenerate
    ]


class DataResponse(BaseModel):
    id: str = Field(
        title="Data ID",
        description="Unique ID for the model inputs and output logged to Humanloop. "
        "Use this when recording feedback later.",
    )
    output: str = Field(
        title="Sanitized output text",
        description="Output text returned from the provider model "
        "with leading and trailing whitespaces stripped.",
    )
    raw_output: str = Field(
        title="Provider's output text",
        description="Raw output text returned from the provider model.",
    )
    inputs: KeyValues = Field(
        title="Inputs",
        description="The inputs passed to the prompt template to send to provider model.",
    )
    finish_reason: str = Field(
        title="Finish reason",
        description="Why the completion ended. Usually one of 'stop' "
        "(indicating a stop token was encountered), or 'length' "
        "(indicating the max tokens limit has been reached)",
    )
    model_config_id: str = Field(
        title="Model config ID",
        description="The identifier for the model config used to create the generation.",
    )


class GenerateUsage(BaseModel):
    prompt_tokens: int = Field(
        title="Prompt tokens",
        description="Number of tokens used in the prompt.",
    )
    generation_tokens: int = Field(
        title="Generation tokens",
        description="Number of tokens produced by the generation.",
    )
    total_tokens: int = Field(
        title="Total tokens",
        description="Total number of tokens used by the prompt and generation combined.",
    )


class GenerateResponse(BaseModel):
    project_id: str = Field(
        title="Project ID",
        description="Unique identifier of the parent project. Starts with `pr_`.",
    )
    num_samples: Optional[int] = Field(
        title="Number of samples",
        description="How many generates to make for each set of inputs.",
        default=1,
    )
    logprobs: Optional[int] = Field(
        title="Log probabilities of most likely n tokens",
        description="Include the log probabilities of the top n tokens in the provider_response",
        default=None,
    )
    suffix: Optional[str] = Field(
        title="Completion suffix",
        description="The suffix that comes after a completion of inserted text. "
        "Useful for completions that act like inserts.",
    )
    user: Optional[str] = Field(
        title="End-user identifier",
        description="End-user id passed through to provider call.",
    )
    data: List[DataResponse] = Field(
        title="Logged data",
        description="Array containing the details of the resulting generations.",
    )

    # Usage can be null when streaming because OpenAI does NOT provide usage in
    # their streaming response
    usage: Optional[GenerateUsage] = Field(
        title="Usage",
        description="Counts of the number of tokens used and related stats.",
    )
    metadata: Optional[KeyValues] = Field(
        title="Metadata",
        description="Any additional metadata that you would like to log for reference.",
    )
    provider_responses: List[Any] = Field(
        title="Provider responses",
        description="The full raw responses provided by the calls to the provider.",
    )
