from typing import Dict, List, Optional, Union

from humanloop.api.models.experiment import PositiveLabel
from humanloop.api.models.feedback import FeedbackClass
from humanloop.api.models.generic import PaginatedData
from humanloop.api.models.log import LogResponse
from humanloop.api.models.project import (
    CreateProjectRequest,
    FeedbackLabelRequest,
    FeedbackTypeModel,
    FeedbackTypeRequest,
    ProjectResponse,
    UpdateProjectRequest,
)
from humanloop.sdk.init import _get_client


def get_projects(
    page: int = 0, size: int = 10, filter: Optional[str] = None
) -> PaginatedData[ProjectResponse]:
    """Retrieve a paginated list of projects associated to your user.

    Args:
        page: Page index
            Page offset for pagination
        size: Page size
            Page size for pagination. Number of projects to fetch.
        filter: Project name filter
            Case-insensitive filter for project name.
    """
    client = _get_client()
    return client.get_projects(page=page, size=size, filter=filter)


def get_project(project_id: str) -> ProjectResponse:
    """Get the project with the given ID.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.get_project(project_id=project_id)


def create_project(project: str) -> ProjectResponse:
    """Create a project with the specified name.

    An error will be raised if the user is already associated to a project with
    that name.

    Args:
        project: Project name
            Unique project name.
    """
    client = _get_client()
    return client.create_project(CreateProjectRequest(name=project))


def set_active_model_config(project_id: str, model_config_id: str) -> ProjectResponse:
    """Set the active model config for the project.

    This will unset the active experiment if one is set.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.update_project(
        project_id=project_id,
        update=UpdateProjectRequest(active_model_config_id=model_config_id),
    )


def set_active_experiment(project_id: str, experiment_id: str) -> ProjectResponse:
    """Set the active experiment for the project.

    This will unset the active model config if one is set.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.update_project(
        project_id=project_id,
        update=UpdateProjectRequest(active_experiment_id=experiment_id),
    )


def set_positive_labels(
    project_id: str, positive_labels: List[Union[PositiveLabel, Dict[str, str]]]
) -> ProjectResponse:
    """Set the feedback labels to be treated as positive user feedback used in
    calculating top-level project metrics.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
        positive_labels: List of labels to be considered as positive user feedback
            List of `{ "group": group, "label": label }` dicts.
    """
    client = _get_client()
    return client.update_project(
        project_id=project_id,
        update=UpdateProjectRequest(positive_labels=positive_labels),
    )


def remove_active_model_config(project_id: str) -> ProjectResponse:
    """Remove the project's active model config, if set.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.delete_active_model_config(project_id=project_id)


def remove_active_experiment(project_id: str) -> ProjectResponse:
    """Remove the project's active experiment, if set.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.delete_active_experiment(project_id=project_id)


def add_text_feedback_type(
    project_id: str,
    feedback_type: str,
) -> List[FeedbackTypeModel]:
    """Create a text-based feedback type.

    Adds a text feedback type to your project that allows you to record
    freeform text as feedback.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.update_feedback_types(
        project_id=project_id,
        feedback_types=[
            FeedbackTypeRequest(type=feedback_type, class_=FeedbackClass.text)
        ],
    ).__root__


def add_select_feedback_type(
    project_id: str,
    feedback_type: str,
    values: Optional[List[Union[FeedbackLabelRequest, dict]]] = None,
) -> List[FeedbackTypeModel]:
    """Create a multi-select feedback type.

    Adds a categorical feedback type to your project that allows the selection
    of one value per datapoint.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        values: Values to add.
            Can be provided as a list of `{ "value": str }` dicts.
    """
    client = _get_client()
    return client.update_feedback_types(
        project_id=project_id,
        feedback_types=[
            FeedbackTypeRequest(
                type=feedback_type, values=values, class_=FeedbackClass.select
            )
        ],
    ).__root__


def add_multi_select_feedback_type(
    project_id: str,
    feedback_type: str,
    values: Optional[List[Union[FeedbackLabelRequest, dict]]] = None,
) -> List[FeedbackTypeModel]:
    """Create a multi-select feedback type.

    Adds a categorical feedback type to your project that allows the selection
    of multiple values per datapoint.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        values: Values to add to the feedback type.
            Can be provided as a list of `{ "value": str }` dicts.
    """
    client = _get_client()
    return client.update_feedback_types(
        project_id=project_id,
        feedback_types=[
            FeedbackTypeRequest(
                type=feedback_type, values=values, class_=FeedbackClass.multi_select
            )
        ],
    ).__root__


def add_values_to_feedback_type(
    project_id: str, feedback_type: str, values: List[Union[FeedbackLabelRequest, dict]]
):
    """Update feedback types.

    Allows creation of the default feedback types and setting status of
    feedback types/categorical values.

    This behaves like an upsert; any feedback categorical values that do not
    already exist in the project will be created.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        values: Values to add.
            Can be provided as a list of `{ "value": str }` dicts.
    """
    client = _get_client()
    return client.update_feedback_types(
        project_id=project_id,
        feedback_types=[FeedbackTypeRequest(type=feedback_type, values=values)],
    ).__root__


def export_datapoints(
    project_id: str, page: int = 0, size: int = 10
) -> PaginatedData[LogResponse]:
    """Export all logged datapoints associated to your project.

    Results are paginated and sorts the logs based on `created_at` in descending order.

    Args:
        project_id: Project ID
            String ID of project. Starts with `pr_`.
        page: Page index
            Page offset for pagination
        size: Page size
            Page size for pagination. Number of projects to fetch.
    """
    client = _get_client()
    return client.export_datapoints(project_id=project_id, page=page, size=size)


__all__ = [
    "get_projects",
    "get_project",
    "create_project",
    "set_active_model_config",
    "set_active_experiment",
    "remove_active_model_config",
    "remove_active_experiment",
    "add_text_feedback_type",
    "add_select_feedback_type",
    "add_multi_select_feedback_type",
    "add_values_to_feedback_type",
    "export_datapoints",
]
