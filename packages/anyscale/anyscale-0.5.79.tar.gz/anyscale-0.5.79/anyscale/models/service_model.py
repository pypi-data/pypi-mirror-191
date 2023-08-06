import enum
from typing import Any, Dict, Optional

from pydantic import Field, root_validator

from anyscale.controllers.job_controller import BaseHAJobConfig
from anyscale.utils.runtime_env import override_runtime_env_for_local_working_dir


class UserServiceAccessTypes(str, enum.Enum):
    private = "private"
    public = "public"


class ServiceConfig(BaseHAJobConfig):
    healthcheck_url: Optional[str] = Field(
        None, description="Healthcheck url for service."
    )
    access: UserServiceAccessTypes = Field(
        UserServiceAccessTypes.public,
        description=(
            "Whether user service (eg: serve deployment) can be accessed by public "
            "internet traffic. If public, a user service endpoint can be queried from "
            "the public internet with the provided authentication token. "
            "If private, the user service endpoint can only be queried from within "
            "the same Anyscale cloud and will not require an authentication token."
        ),
    )

    entrypoint: Optional[str] = Field(
        None,
        description="A script that will be run to start your job. This command will be run in the root directory of the specified runtime env. Eg. 'python script.py'",
    )

    ray_serve_config: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "The Ray Serve config to use for this Production service. It is supported only on v2 clouds."
            "This config defines your Ray Serve application, and will be passed directly to Ray Serve. "
            "You can learn more about Ray Serve config files here: https://docs.ray.io/en/latest/serve/production-guide/config.html"
        ),
    )

    # Version level fields for Services V2
    version: Optional[str] = Field(
        None,
        description="A version string that represents the version for this service. "
        "Will be populated with the hash of the config if not specified.",
    )
    canary_weight: Optional[int] = Field(
        None,
        description="A manual target weight for this service. "
        "If this field is not set, the service will automatically roll out. "
        "If set, this should be a number between 0 and 100 (inclusive). "
        "The newly created version will have weight `canary_weight` "
        "and the existing version will have `100 - canary_weight`.",
    )

    @root_validator
    def validates_config(cls, values) -> Dict[str, Any]:
        # entrypoint is used for Services V1 and serve config for Services V2
        is_entrypoint_present = bool(values.get("entrypoint"))
        is_serve_config_present = bool(values.get("ray_serve_config"))
        assert is_entrypoint_present != is_serve_config_present, (
            "Please specify one of 'entrypoint' or 'ray_serve_config'. "
            "'entrypoint' should be specified on v1 clouds, "
            "and 'ray_serve_config' should be specified on v2 clouds."
        )

        if is_entrypoint_present:
            assert (
                values.get("healthcheck_url") is not None
            ), "healthcheck_url should be set for Services on v1 clouds."
        if is_serve_config_present:
            assert (
                values.get("healthcheck_url") is None
            ), "healthcheck_url should not be set for Services on v2 clouds."
            assert (
                values.get("runtime_env") is None
            ), "runtime_env should not be set for Services on v2 clouds."

        return values

    @root_validator
    def overwrites_runtime_env_in_serve_config(cls, values) -> Dict[str, Any]:
        if values.get("ray_serve_config") and values.get("ray_serve_config").get(
            "runtime_env"
        ):
            runtime_env = values.get("ray_serve_config").get("runtime_env")
            values["ray_serve_config"] = {
                **(values["ray_serve_config"]),
                "runtime_env": override_runtime_env_for_local_working_dir(runtime_env),
            }
        return values
