from typing import Dict, List, Optional, Union

from humanloop.api.models.experiment import (
    ExperimentResponse,
    PositiveLabel,
    UpdateExperimentRequest,
)
from humanloop.sdk.init import _get_client


def get_project_experiments(project_id: str) -> List[ExperimentResponse]:
    """Get an array of experiments associated to your project.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
    """
    client = _get_client()
    return client.get_project_experiments(project_id=project_id)


def create_experiment(
    project_id: str,
    name: str,
    model_config_ids: Optional[List[str]] = None,
    positive_labels: Optional[List[Union[PositiveLabel, Dict[str, str]]]] = None,
    set_active: bool = False,
) -> ExperimentResponse:
    """Create an experiment for your project.

    You can optionally specify IDs of your project's model configs to include
    in the experiment, along with a specific metric to optimise.

    Args:
        project_id: Project ID.
            String ID of project. Starts with `pr_`.
        name: Experiment name.
        model_config_ids: Model config IDs.
            Model configs to add to this experiment. More model configs can be added later.
        positive_labels: List of labels to be considered as positive user feedback.
            List of `{ "group": group, "label": label }` dicts.
        set_active: Set as project's active experiment.
            Whether to set the created project as the project's active experiment.
    """
    client = _get_client()
    return client.create_project_experiment(
        project_id=project_id,
        experiment={
            "name": name,
            "model_config_ids": model_config_ids,
            "positive_labels": positive_labels if positive_labels is not None else [],
            "set_active": set_active,
        },
    )


def update_experiment(
    experiment_id: str,
    name: Optional[str] = None,
    positive_labels: Optional[List[Union[PositiveLabel, Dict[str, str]]]] = None,
    model_config_ids_to_register: Optional[List[str]] = None,
    model_config_ids_to_deregister: Optional[List[str]] = None,
):
    """Update an experiment by its ID.

    Args:
        experiment_id: Experiment ID.
            String ID of experiment. Starts with `exp_`.
        name: Experiment name.
            Name of experiment.
        positive_labels: Positive labels.
            Feedback labels to treat as positive user feedback. Used to monitor
            the performance of model configs in the experiment.
        model_config_ids_to_register: Model config IDs to register.
            Model configs to add to this experiment.
        model_config_ids_to_deregister: Model config IDs to deregister.
            Model configs in this experiment to be deactivated.
    """
    client = _get_client()
    return client.update_experiment(
        experiment_id=experiment_id,
        update=UpdateExperimentRequest(
            name=name,
            positive_labels=positive_labels,
            config_ids_to_register=model_config_ids_to_register,
            config_ids_to_deregister=model_config_ids_to_deregister,
        ),
    )


def delete_experiment(experiment_id: str):
    """Delete an experiment by its ID.

    Args:
        experiment_id: Experiment ID.
            String ID of experiment. Starts with `exp_`.
    """
    client = _get_client()
    return client.delete_experiment(experiment_id=experiment_id)


__all__ = [
    "get_project_experiments",
    "create_experiment",
    "update_experiment",
    "delete_experiment",
]
