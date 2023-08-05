import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from .metric import BaseMetricResponse
from .model_config import ModelConfigResponse


class ExperimentModelConfigResponse(BaseModel):
    mean: Optional[float] = Field(
        title="Mean of experiment's metric",
        description="The mean performance of the model config, as measured by the experiment's metric.",
    )
    spread: Optional[float] = Field(
        title="Spread of experiment's metric",
        description="The spread of performance of the model config, as measured by the experiment's metric. "
        "A measure of the uncertainty in the model config's performance.",
    )
    trials_count: int = Field(
        title="The number of trials that have happened in this experiment",
        description="Number of datapoints with feedback associated to this experiment.",
    )
    active: bool = Field(
        title="Model config active",
        description="Whether the model config is active in the experiment. "
        "Only active model configs can be sampled from the experiment.",
    )
    id: str = Field(
        title="Model config ID",
        description="String ID of model config. Starts with `config_`.",
    )
    display_name: str = Field(
        title="Display name",
        description="Display name of model config. If this is not set by the user, a friendly name will be generated.",
    )
    model_config: ModelConfigResponse = Field(
        title="Model config",
        description="Full definition of model config used in the experiment.",
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PositiveLabel(BaseModel):
    type: str = Field(title="Feedback type")
    value: str = Field(title="Feedback value")


class ExperimentStatus(str, Enum):
    initialised = "Initialized"
    in_progress = "In progress"


class ExperimentResponse(BaseModel):
    id: str = Field(
        title="Experiment ID",
        description="String ID of experiment. Starts with `exp_`.",
    )
    project_id: str = Field(
        title="Project ID",
        description="String ID of project the experiment belongs to. Starts with `pr_`.",
    )
    name: str = Field(title="Experiment name", description="Name of experiment.")

    status: ExperimentStatus = Field(
        title="Experiment status", description="Status of experiment."
    )
    model_configs: Optional[List[ExperimentModelConfigResponse]] = Field(
        title="Experiment model configs",
        description="List of model configs associated to the experiment.",
    )
    metric: BaseMetricResponse = Field(
        title="Experiment metric",
        description="Metric used as the experiment's objective.",
    )
    positive_labels: List[PositiveLabel] = Field(
        title="Positive labels",
        description="Feedback labels to treat as positive user feedback. "
        "Used to monitor the performance of model configs in the experiment.",
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreateExperimentRequest(BaseModel):
    name: str = Field(title="Experiment name", description="Name of experiment.")
    model_config_ids: Optional[List[str]] = Field(
        title="Model config IDs",
        description="Model configs to add to this experiment. More model configs can be added later.",
    )
    positive_labels: List[PositiveLabel] = Field(
        title="Positive labels",
        description="Feedback labels to treat as positive user feedback. "
        "Used to monitor the performance of model configs in the experiment.",
    )
    set_active: bool = Field(
        default=False,
        title="Set as project's active experiment",
        description="Whether to set the created project as the project's active experiment.",
    )


class UpdateExperimentRequest(BaseModel):
    name: Optional[str] = Field(
        title="Experiment name", description="Name of experiment."
    )
    positive_labels: Optional[List[PositiveLabel]] = Field(
        title="Positive labels",
        description="Feedback labels to treat as positive user feedback. "
        "Used to monitor the performance of model configs in the experiment.",
    )
    config_ids_to_register: Optional[List[str]] = Field(
        title="Model config IDs to register",
        description="Model configs to add to this experiment.",
    )
    config_ids_to_deregister: Optional[List[str]] = Field(
        title="Model config IDs to deregister",
        description="Model configs in this experiment to be deactivated.",
    )
