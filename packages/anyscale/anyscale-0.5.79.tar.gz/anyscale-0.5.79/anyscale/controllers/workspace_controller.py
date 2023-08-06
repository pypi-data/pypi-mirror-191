import os
import shlex
import subprocess
from typing import Any, Dict, List, Optional, Sequence

from pydantic import BaseModel

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.experimental_workspace import (
    ExperimentalWorkspace,
)
from anyscale.cluster_config import configure_for_session
from anyscale.controllers.base_controller import BaseController
from anyscale.sdk.anyscale_client.models.cloud_version import CloudVersion
from anyscale.shared_anyscale_utils.conf import V2_RAY_MOUNT_PATH
from anyscale.util import get_working_dir
from anyscale.utils.imports.all import try_import_ray
from anyscale.workspace import load_workspace_id_or_throw, write_workspace_id_to_disk


class WorkspaceCommandContext(BaseModel):
    cluster_config: Dict[str, Any]
    head_ip: str
    project_id: str
    cluster_id: str


class WorkspaceController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log

    def clone(self, workspace: ExperimentalWorkspace) -> None:
        dir_name = workspace.name
        os.makedirs(dir_name)

        workspace_id = workspace.id
        write_workspace_id_to_disk(workspace_id, dir_name)

    def get_activated_workspace(self) -> ExperimentalWorkspace:
        workspace_id = load_workspace_id_or_throw()
        return self.api_client.get_workspace_api_v2_experimental_workspaces_workspace_id_get(
            workspace_id
        ).result

    def get_workspace_dir_name(self) -> str:
        """
        Currently the directory name of Workspaces/Clusters
        is determiend by the project name.
        """
        workspace = self.get_activated_workspace()
        project = self.api_client.get_project_api_v2_projects_project_id_get(
            workspace.project_id
        ).result
        return project.name

    def _get_workspace_command_context(self) -> WorkspaceCommandContext:
        workspace = self.get_activated_workspace()

        cluster_id = workspace.cluster_id
        project_id = workspace.project_id

        cluster_config = configure_for_session(
            cluster_id, api_client=self.api_client, disable_project_sync=True
        )
        head_ip = self.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
            cluster_id
        ).result.head_ip

        return WorkspaceCommandContext(
            cluster_config=cluster_config,
            head_ip=head_ip,
            project_id=project_id,
            cluster_id=cluster_id,
        )

    def run_cmd(self, ssh_option: Sequence[str], cmd: str):
        workspace_command_context = self._get_workspace_command_context()
        cluster_config = workspace_command_context.cluster_config

        key_path = cluster_config["auth"]["ssh_private_key"]

        head_ip = workspace_command_context.head_ip
        ssh_user = cluster_config["auth"]["ssh_user"]
        target_host = f"{ssh_user}@{head_ip}"

        command = shlex.quote(cmd)

        ssh_command = (
            ["ssh"]
            + list(ssh_option)
            + ["-o", f"ProxyCommand=ssh -W %h:%p -i {key_path} {target_host}"]
            + ["-tt", "-i", key_path]
            + ["ray@0.0.0.0", "-p", "5020"]
            + [f"sh -c {command}"]
        )

        subprocess.run(ssh_command)  # noqa: B1

    def run_rsync(
        self,
        ssh_option: Sequence[str],
        local_path: str,
        *,
        down: bool,
        rsync_filters: List[str],
        rsync_excludes: List[str],
    ) -> None:
        try_import_ray()
        from ray.autoscaler.sdk import get_docker_host_mount_location

        workspace_command_context = self._get_workspace_command_context()
        cluster_config = workspace_command_context.cluster_config
        head_ip = workspace_command_context.head_ip
        project_id = workspace_command_context.project_id
        cluster_id = workspace_command_context.cluster_id

        ssh_user = cluster_config["auth"]["ssh_user"]
        key_path = cluster_config["auth"]["ssh_private_key"]

        base_ssh_command = ["ssh"] + ["-i", key_path] + list(ssh_option)

        directory_name = get_working_dir(cluster_config, project_id, self.api_client)

        cloud_id = self.anyscale_api_client.get_session(cluster_id).result.cloud_id
        cloud_version = self.anyscale_api_client.get_cloud(cloud_id).result.version
        mount_path = (
            V2_RAY_MOUNT_PATH
            if not cloud_version or cloud_version == CloudVersion.V2
            else get_docker_host_mount_location(cluster_config["cluster_name"])
        )
        source_directory = mount_path + directory_name + "/"

        rsync_command = [
            "rsync",
            "--rsh",
            subprocess.list2cmdline(base_ssh_command),
            "-avz",
            "--delete",
        ]

        for rsync_exclude in rsync_excludes:
            rsync_command.extend(["--exclude", rsync_exclude])

        for rsync_filter in rsync_filters:
            rsync_command.extend(["--filter", f"dir-merge,- {rsync_filter}"])

        if down:
            rsync_command += [
                f"{ssh_user}@{head_ip}:{source_directory}",
                local_path,
            ]
        else:
            rsync_command += [
                local_path,
                f"{ssh_user}@{head_ip}:{source_directory}",
            ]

        subprocess.run(rsync_command)  # noqa: B1
