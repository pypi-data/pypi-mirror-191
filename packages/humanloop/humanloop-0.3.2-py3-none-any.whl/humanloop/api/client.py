import logging
from typing import List

import requests
from requests import HTTPError
from uplink import (
    Body,
    Consumer,
    Query,
    delete,
    get,
    json,
    patch,
    post,
    response_handler,
    returns,
)
from uplink.auth import ApiTokenHeader

from humanloop.api.models.experiment import (
    CreateExperimentRequest,
    ExperimentResponse,
    UpdateExperimentRequest,
)
from humanloop.api.models.feedback import ListFeedbackRequest, ListFeedbackResponse
from humanloop.api.models.generate import GenerateRequest, GenerateResponse
from humanloop.api.models.generic import PaginatedData
from humanloop.api.models.log import ListCreateLogResponse, ListLogRequest, LogResponse
from humanloop.api.models.metric import (
    CreateMetricRequest,
    MetricResponse,
    UpdateMetricRequest,
)
from humanloop.api.models.model_config import (
    GetModelConfigResponse,
    ProjectModelConfig,
    ProjectModelConfigResponse,
)
from humanloop.api.models.project import (
    CreateProjectRequest,
    FeedbackTypeRequest,
    FeedbackTypes,
    ProjectResponse,
    UpdateProjectRequest,
)
from humanloop.api.models.user import UserResponse

logger = logging.getLogger(__file__)


def raise_for_status(response: requests.Response):
    """Checks whether the response was successful."""
    try:
        response.raise_for_status()
        return response
    except HTTPError as e:
        # Attempt to log JSON error response.
        try:
            logger.error(f"Request to {e.request.url} failed with {e.response.json()}")
        except Exception:
            pass
        raise e


@response_handler(raise_for_status)
class Humanloop(Consumer):
    """Python Client for the Humanloop API"""

    @returns.json()
    @get()
    def health_check(self):
        """Health check"""
        pass

    @returns.json()
    @get("/users/me")
    def read_me(self) -> UserResponse:
        """Validate user exists with valid password and return access token"""
        pass

    ###
    # Projects
    ###

    @returns.json
    @get("/v3/projects")
    def get_projects(
        self, page: Query = 0, size: Query = 10, filter: Query = None
    ) -> PaginatedData[ProjectResponse]:
        """Retrieve a paginated list of projects associated to your user.

        Args:
            page: Page index.
                Page offset for pagination
            size: Page size.
                Page size for pagination. Number of projects to fetch.
            filter: Project name filter.
                Case-insensitive filter for project name.
        """

    @returns.json
    @get("/v3/projects/{project_id}")
    def get_project(self, project_id: str) -> ProjectResponse:
        """Get the project with the given ID.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @post("/v3/projects")
    def create_project(
        self, request: Body(type=CreateProjectRequest)
    ) -> ProjectResponse:
        """Creates a new project with the provided name.

        An error will be raised if the user is already associated to a project with
        that name.

        Args (Body):
            name: Project name.
                Unique project name.
        """

    @json
    @returns.json
    @patch("/v3/projects/{project_id}")
    def update_project(
        self, project_id: str, update: Body(type=UpdateProjectRequest)
    ) -> ProjectResponse:
        """Update the project with the specified ID.

        Set the project's active model config/experiment by passing either
        `active_experiment_id` or `active_model_config_id`.

        Set the feedback labels to be treated as positive user feedback used in
        calculating top-level project metrics by passing a list of labels in
        `positive_labels`.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.

        Args (Body):
            active_experiment_id: Active experiment ID.
                ID for an experiment to set as the project's active deployment.
                Starts with 'exp_'.
            active_model_config_id: Active model config ID.
                ID for a model config to set as the project's active deployment.
                Starts with 'config_'.
            positive_labels: List of feedback labels to consider as positive actions.
                The full list of labels to treat as positive user feedback.
                Specified as a list of {"type", "value"} pairs.

            At most one of `active_experiment_id' and 'active_model_config_id`
            can be set.
        """

    # TODO: Consider adding `get_project_model_configs()` endpoint.

    @returns.json
    @get("/v3/projects/{project_id}/model-config")
    def get_model_config_from_project(self, project_id: str) -> GetModelConfigResponse:
        """Retrieves a model config to use to execute your model.

        A model config will be selected based on the project's
        active model config/experiment settings.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @returns.json
    @delete("/v3/projects/{project_id}/active-model-config")
    def delete_active_model_config(self, project_id: str) -> ProjectResponse:
        """Remove the project's active model config, if set.

        This has no effect if the project does not have an active model config set.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @returns.json
    @delete("/v3/projects/{project_id}/active-experiment")
    def delete_active_experiment(self, project_id: str) -> ProjectResponse:
        """Remove the project's active experiment, if set.

        This has no effect if the project does not have an active experiment set.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @patch("/v3/projects/{project_id}/feedback-types")
    def update_feedback_types(
        self,
        project_id: str,
        feedback_types: Body(type=List[FeedbackTypeRequest]),
    ) -> FeedbackTypes:
        """Update feedback types.

        Allows creation of the default feedback types and setting status of
        feedback types/categorical values.

        This behaves like an upsert; any feedback categorical values that do not
        already exist in the project will be created.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @post("/v3/projects/{project_id}/export")
    def export_datapoints(
        self,
        project_id: str,
        page: Query = 0,
        size: Query = 10,
    ) -> PaginatedData[LogResponse]:
        """Export all logged datapoints associated to your project.

        Results are paginated and sorts the logs based on `created_at` in descending order.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
            page: Page index.
                Page offset for pagination
            size: Page size.
                Page size for pagination. Number of projects to fetch.
        """

    #
    # @json
    # @returns.json
    # @delete("/projects/{project_id}")
    # def _delete_project(self, project_id: int):
    #     """Delete a project by its internal Humanloop ID (of int type)."""

    ###
    # Generate
    ###

    @json
    @returns.json
    @post("/v3/generate")
    def generate(self, request: Body(type=GenerateRequest)) -> GenerateResponse:
        """Generates an output from your provider foundation model and automatically
        logs the results for feedback later.

        The model configuration used depends on how the method was called. The
        following signatures are accepted:

        1. Model config parameters:
            - The specific model configuration parameters will be used to link to an existing or create a new model
            configuration that will be used for this generation.
            - E.g. { "model: "text-davinci-002", "prompt_template", "parameters", ... }
        2. `model_config_id`:
            - The ID of an existing model configuration to be used.
            - E.g. { "model_config_id": "config_abcdef1234567" }
        3. `experiment_id`:
            - The ID of an existing experiment. A model configuration will be sampled from the experiment's list of
            active model configurations.
            - E.g. { "experiment_id": "exp_abcdef1234567" }
        4. `project`:
            - A model configuration will be selected based on the projects deployment settings.
            - E.g. { "project": "your-project-name-001" }


        (These signatures have been listed in decreasing priority. If multiple signatures are satisfied, the highest
        priority signature will be used. For example, if both model config parameters and an experiment ID is provided, the
        model config parameters will be used and the experiment ID will be ignored.)


        Note that all of the above signatures also require the following parameters: `project`, `inputs`, `source`,
        `provider_api_keys`.
        """

    ###
    # Logs
    ###
    @json
    @returns.json
    @post("/v3/logs")
    def log(
        self,
        request: Body(type=ListLogRequest),
    ) -> ListCreateLogResponse:
        """Log a datapoint to your Humanloop project."""

    ###
    # Feedback
    ###

    @json
    @returns.json
    @post("/v3/feedback")
    def feedback(
        self, feedback: Body(type=ListFeedbackRequest)
    ) -> ListFeedbackResponse:
        """Add feedback to an existing logged datapoint."""

    ###
    # Model configs
    ###

    @json
    @returns.json
    @post("/v3/model-configs")
    def register_project_model_config(
        self, model_config: Body(type=ProjectModelConfig)
    ) -> ProjectModelConfigResponse:
        """Register a model config to a project and optionally add it to an
        experiment.

        If the project provided does not exist, a new project will be created
        automatically.
        If an experiment name is provided, the specified experiment must already
        exist. Otherwise, an error will be raised.

        If the model config is the first to be associated to the project, it will
        be set as the active model config.
        """

    ###
    # Experiments
    ###

    @json
    @returns.json
    @get("/v3/projects/{project_id}/experiments")
    def get_project_experiments(self, project_id: str) -> List[ExperimentResponse]:
        """Get an array of experiments associated to your project.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @post("/v3/projects/{project_id}/experiments")
    def create_project_experiment(
        self, project_id: str, experiment: Body(type=CreateExperimentRequest)
    ) -> ExperimentResponse:
        """Create an experiment for your project.

        You can optionally specify IDs of your project's model configs to include
        in the experiment, along with a specific metric to optimise.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @patch("/v3/experiments/{experiment_id}")
    def update_experiment(
        self, experiment_id: str, update: Body(type=UpdateExperimentRequest)
    ) -> ExperimentResponse:
        """Update an experiment by its ID.

        You can change the experiment's name, register/de-register model
        configs, and update the list of labels to be considered positive.

        Args:
            experiment_id: Experiment ID.
                String ID of experiment. Starts with `exp_`.
        """

    @delete("/v3/experiments/{experiment_id}")
    def delete_experiment(self, experiment_id: str):
        """Delete an experiment by its ID.

        Args:
            experiment_id: Experiment ID.
                String ID of experiment. Starts with `exp_`.
        """

    @json
    @returns.json
    @get("/v3/experiments/{experiment_id}/model-config")
    def get_model_config_from_experiment(
        self, experiment_id: str
    ) -> GetModelConfigResponse:
        """Retrieves a model config to use to execute your model.

        A model config will be sampled from the experiment's list of active
        model configs.
        The response will include a `trial_id` to link this to a subsequent
        log() call.

        Args:
            experiment_id: Experiment ID.
                String ID of experiment. Starts with `exp_`.
        """

    ###
    # Metrics
    ###

    @returns.json
    @get("/v3/projects/{project_id}/metrics")
    def get_project_metrics(self, project_id: str) -> List[MetricResponse]:
        """Get an array of existing metrics for a given project.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @post("/v3/projects/{project_id}/metrics")
    def create_project_metric(
        self, project_id: str, metric: Body(type=CreateMetricRequest)
    ) -> MetricResponse:
        """Create a metric for your project.

        The metric will be calculated for all datapoints in the project.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
        """

    @json
    @returns.json
    @patch("/v3/projects/{project_id}/metrics/{metric_id}")
    def update_project_metric(
        self, project_id: str, metric_id: str, update: Body(type=UpdateMetricRequest)
    ) -> MetricResponse:
        """Update a metric by its ID.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
            metric_id: Metric ID.
                String ID of metric. Starts with `metric_`.
        """

    @delete("/v3/projects/{project_id}/metrics/{metric_id}")
    def delete_project_metric(self, project_id: str, metric_id: str):
        """Delete a metric by its ID.

        Args:
            project_id: Project ID.
                String ID of project. Starts with `pr_`.
            metric_id: Metric ID.
                String ID of metric. Starts with `metric_`.
        """

    @json
    @returns.json
    @delete("/projects/{project_id}")
    def _delete_project(self, project_id: int):
        """Delete a project by its internal Humanloop ID (of int type)."""


def get_humanloop_client(api_key: str, base_url: str) -> Humanloop:
    return Humanloop(base_url=base_url, auth=ApiTokenHeader("X-API-KEY", api_key))
