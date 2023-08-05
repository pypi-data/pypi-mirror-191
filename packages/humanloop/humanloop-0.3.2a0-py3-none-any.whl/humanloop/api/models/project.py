import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .experiment import ExperimentResponse, PositiveLabel
from .feedback import FeedbackClass, FeedbackType
from .model_config import ModelConfigResponse
from .utils import RootBaseModel


class LabelSentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    unset = "unset"


class UserResponse(BaseModel):
    email_address: str = Field(
        title="Email address", description="The user's email address."
    )
    full_name: Optional[str] = Field(
        title="Full name", description="The user's full name."
    )


class FeedbackLabelStatus(str, Enum):
    unset = "unset"
    active = "active"
    inactive = "inactive"


class CategoricalFeedbackLabel(BaseModel):
    value: str = Field(title="Label value")
    sentiment: LabelSentiment = Field(
        title="Feedback label sentiment",
        description="Whether the feedback sentiment is positive or negative.",
    )


class FeedbackTypeModel(BaseModel):
    type: Union[FeedbackType, str] = Field(
        title="Feedback type",
        description="The type of feedback. "
        "The default feedback types available are 'rating', 'action', 'issue', 'correction', and 'comment'.",
    )
    class_: FeedbackClass = Field(
        alias="class",
        title="Feedback class",
        description="The data type associated to this feedback type; whether it is a 'text'/'select'/'multi_select'.",
        hidden_from_schema=True,
    )
    values: Optional[List[CategoricalFeedbackLabel]] = Field(
        title="Allowed values for categorical feedback types",
        description="The allowed values for categorical feedback types. Not populated for `correction` and `comment`.",
    )

    class Config:
        allow_population_by_field_name = True  # Needed to populate class_ attribute.


class FeedbackTypes(RootBaseModel):
    __root__: List[FeedbackTypeModel]


class ProjectResponse(BaseModel):
    id: str = Field(title="Project ID", description="Project ID")
    internal_id: int = Field(
        title="Internal project ID",
        description="Project ID for internal Humanloop use.",
    )
    name: str = Field(title="Project name", description="Unique project name.")
    active_experiment: Optional[ExperimentResponse] = Field(
        title="Active experiment",
        description="Experiment that has been set as the project's active deployment. "
        "At most one of `active_experiment` or `active_model_config` can be set.",
    )
    active_model_config: Optional[ModelConfigResponse] = Field(
        title="Active model configuration",
        description="Model configuration that has been set as the project's active deployment. "
        "At most one of `active_experiment` or `active_model_config` can be set.",
    )
    users: List[UserResponse] = Field(
        title="Project users",
        description="Users associated to the project.",
    )
    data_count: int = Field(
        title="Number of datapoints",
        description="The count of datapoints that have been logged to the project.",
    )
    feedback_types: FeedbackTypes = Field(
        title="Feedback types",
        description="The feedback types that have been defined in the project.",
    )

    created_at: datetime.datetime
    updated_at: datetime.datetime


class FeedbackLabelRequest(BaseModel):
    value: str = Field(title="Feedback value", description="Name of feedback value.")
    sentiment: Optional[LabelSentiment] = Field(
        title="Feedback label sentiment",
        description="Sentiment of feedback label. If 'positive', the label will be treated as positive user feedback.",
    )


class FeedbackTypeRequest(BaseModel):
    type: str = Field(
        title="Feedback type", description="The type of feedback to update."
    )
    values: Optional[List[FeedbackLabelRequest]] = Field(
        title="Feedback label values",
        description="The feedback values to be available. "
        "This field should only be populated when updating a 'select' or 'multi_select' feedback class.",
    )
    class_: Optional[FeedbackClass] = Field(
        alias="class",
        title="Feedback class",
        description="The data type associated to this feedback type; whether it is a 'text'/'select'/'multi_select'. "
        "This is optional when updating the default feedback types (i.e. when `type` is 'rating', 'action' or 'issue').",
    )

    class Config:
        allow_population_by_field_name = True  # Needed to populate class_ attributes.


class CreateProjectRequest(BaseModel):
    name: str = Field(title="Project name", description="Unique project name.")
    feedback_types: Optional[List[FeedbackTypeRequest]] = Field(
        title="Feedback types", description="Feedback types to be created."
    )


class UpdateProjectRequest(BaseModel):
    active_experiment_id: Optional[str] = Field(
        title="Active experiment ID",
        description="ID for an experiment to set as the project's active deployment. "
        "Starts with 'exp_'. "
        "At most one of 'active_experiment_id' and 'active_model_config_id' can be set.",
    )
    active_model_config_id: Optional[str] = Field(
        title="Active model configuration ID",
        description="ID for a model configuration to set as the project's active deployment. "
        "Starts with 'config_'. "
        "At most one of 'active_experiment_id' and 'active_model_config_id' can be set.",
    )
    positive_labels: Optional[List[PositiveLabel]] = Field(
        title="List of feedback labels to consider as positive actions",
        description="The full list of labels to treat as positive user feedback.",
    )
