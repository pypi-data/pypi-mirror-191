import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .utils import RootBaseModel


class FeedbackClass(str, Enum):
    select = "select"
    multi_select = "multi_select"
    text = "text"


class FeedbackType(str, Enum):
    rating = "rating"
    action = "action"
    issue = "issue"
    correction = "correction"
    comment = "comment"


class BaseFeedback(BaseModel):
    type: Union[FeedbackType, str] = Field(
        title="Feedback type",
        description="The type of feedback. "
        "The default feedback types available are 'rating', 'action', 'issue', 'correction', and 'comment'.",
    )
    value: str = Field(
        title="Feedback value",
        description="The feedback value to set. "
        "This would be the appropriate text for 'correction' or 'comment', "
        "or a label to apply for 'rating', 'action', or 'issue'.",
    )
    data_id: Optional[str] = Field(
        title="Datapoint ID",
        description="ID to associate the feedback to a previously logged datapoint."
        "When providing instant feedback as part of the hl.log(...) call "
        "you don't need to provide a data_id.",
    )
    user: Optional[str] = Field(
        title="User",
        description="A unique identifier to who provided the feedback. "
        "This gets passed through to the provider as required.",
    )

    created_at: Optional[datetime.datetime] = Field(
        title="Created at",
        description="Timestamp for when the feedback was created. "
        "If not provided, the time the call was made will be used "
        "as a timestamp.",
    )


class Feedback(BaseFeedback):
    value: Optional[str] = Field(
        title="Feedback value",
        description="The feedback value to be set. "
        "This field should be left blank when unsetting 'rating', 'correction' or 'comment', but is required otherwise.",
    )
    unset: Optional[bool] = Field(
        title="Unset", description="If true, the value for this feedback type is unset."
    )


class ListFeedbackRequest(RootBaseModel):
    __root__: Union[List[Feedback], Feedback]


class FeedbackResponse(Feedback):
    id: str = Field(
        title="Feedback ID",
        description="String ID of user feedback. Starts with `ann_`, short for annotation.",
    )


class ListFeedbackResponse(RootBaseModel):
    __root__: Union[List[FeedbackResponse], FeedbackResponse]
