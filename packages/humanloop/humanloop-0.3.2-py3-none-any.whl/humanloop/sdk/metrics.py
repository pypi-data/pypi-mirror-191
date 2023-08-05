import inspect
from typing import Callable, List, Optional, Union

from humanloop.api.models.metric import (
    CreateMetricRequest,
    MetricResponse,
    UpdateMetricRequest,
)
from humanloop.sdk.init import _get_client


def get_project_metrics(project_id: str) -> List[MetricResponse]:
    """Get an array of existing metrics for a given project.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.get_project_metrics(project_id)


def create_metric(
    project_id: str,
    name: str,
    description: str,
    code: Union[Callable, str],
) -> MetricResponse:
    """Create a metric for your project.

    The metric will be calculated for all datapoints in the project.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        name: Metric name.
            Name of the created metric
        description: Metric description.
            Description of the created metric.
            Model configs to add to this experiment. More model configs can be added later.
        code: Metric code.
            Python code used to calculate a metric value on each logged datapoint.
            The last defined function in the code block will be called with a `log` dict, and should
            return a number, or `None`.
    """
    client = _get_client()
    code = _process_metric_code(code)
    return client.create_project_metric(
        project_id=project_id,
        metric=CreateMetricRequest(name=name, description=description, code=code),
    )


def update_metric(
    project_id: str,
    metric_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    code: Optional[str] = None,
    active: Optional[str] = None,
) -> MetricResponse:
    """Update a metric by its ID.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        metric_id: Metric ID.
            String ID of metric. Starts with `metric_`.
    """
    client = _get_client()

    if code is not None:
        code = _process_metric_code(code)

    return client.update_project_metric(
        project_id=project_id,
        metric_id=metric_id,
        update=UpdateMetricRequest(
            name=name,
            description=description,
            code=code,
            active=active,
        ),
    )


def delete_metric(project_id: str, metric_id: str):
    """Delete a metric by its ID.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        metric_id: Metric ID.
            String ID of metric. Starts with `metric_`.
    """
    client = _get_client()
    return client.delete_project_metric(project_id=project_id, metric_id=metric_id)


def _process_metric_code(code: Union[str, Callable]) -> str:
    """
    Validates that metric is valid for sending to client.
    The client expects a string, so if a function object is provided, it is converted to
    a string.
    TODO add compile and run checks (currently happen server side)
    """
    if isinstance(code, str):
        return code

    if callable(code):
        return inspect.getsource(code)
    else:
        raise ValueError("code is not a callable or a string")


__all__ = ["get_project_metrics", "create_metric", "update_metric", "delete_metric"]
