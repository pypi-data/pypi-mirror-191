from humanloop.api.models.model_config import (
    ProjectModelConfig,
    ProjectModelConfigResponse,
)
from humanloop.sdk.init import _get_client


def register(*args, **kwargs) -> ProjectModelConfigResponse:
    """Register a model config to a project and optionally add it to an
    experiment.

    If the project provided does not exist, a new project will be created
    automatically.
    If an experiment name is provided, the specified experiment must already
    exist. Otherwise, an error will be raised.

    If the model config is the first to be associated to the project, it will
    be set as the active model config.

    This function accepts a `model_config: ProjectModelConfig`, or a
    `model_config` passed in as kwargs.
    """
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError(
                "When passing arguments, only a single argument is accepted. "
                "This should be a single `ProjectModelConfig` object."
            )
        if len(kwargs) != 0:
            raise ValueError(
                "Either pass arguments of type `ProjectModelConfig` or the keyword arguments required, not both. "
            )
        return _register(args[0])
    elif len(kwargs) > 0:
        return _register(ProjectModelConfig(**kwargs))
    else:
        raise ValueError(
            "Provide a ModelConfig or the keyword arguments to create a `ProjectModelConfig` object. "
        )


def _register(model_config: ProjectModelConfig) -> ProjectModelConfigResponse:
    client = _get_client()
    return client.register_project_model_config(model_config)


__all__ = ["register"]
