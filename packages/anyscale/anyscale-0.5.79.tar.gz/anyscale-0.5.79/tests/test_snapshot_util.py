import json
import os
import shutil
import tempfile
from typing import Optional
from unittest.mock import patch
from zipfile import ZipFile

from anyscale import snapshot_util


class TestWorkspaceEnv:
    def __init__(self, idle_termination_dir: Optional[str] = None):
        workspace_id = "test_ws1"

        # setup working dir
        self.tmpdir = tempfile.mkdtemp()
        self.anyscale_working_dir = os.path.join(self.tmpdir, "work")
        os.makedirs(self.anyscale_working_dir)

        # setup EFS dir
        self.efs_dir = os.path.join(self.tmpdir, "efs")
        os.makedirs(self.efs_dir)

        # setup cluster storage
        self.efs_cluster_storage = os.path.join(
            self.efs_dir, workspace_id, "cluster_storage"
        )
        self.cluster_storage = os.path.join(self.tmpdir, "cluster_storage")
        os.makedirs(self.efs_cluster_storage)
        os.symlink(self.efs_cluster_storage, self.cluster_storage)

        # Rewire snapshot_util to use our test env setup.
        snapshot_util.WORKING_DIR = self.anyscale_working_dir
        snapshot_util.EFS_WORKSPACE_DIR = os.path.join(self.efs_dir, "workspaces")
        snapshot_util.WORKSPACE_ID = workspace_id
        snapshot_util.CLUSTER_STORAGE_DIR = self.cluster_storage

        self.idle_termination_dir = None
        if idle_termination_dir:
            self.idle_termination_dir = idle_termination_dir
            snapshot_util.IDLE_TERMINATION_DIR = idle_termination_dir
        # TODO: flesh this out.

    def __del__(self):
        shutil.rmtree(self.tmpdir)
        if self.idle_termination_dir and os.path.exists(self.idle_termination_dir):
            shutil.rmtree(self.idle_termination_dir)


def list_zip(zipfile):
    with ZipFile(zipfile, "r") as z:
        return z.namelist()


def test_snapshot_on_change():
    env = TestWorkspaceEnv(tempfile.mkdtemp())
    status_file = f"{snapshot_util.IDLE_TERMINATION_DIR}/workspace.json"
    os.chdir(env.anyscale_working_dir)

    # verify no workspace status on start
    assert not os.path.exists(status_file), status_file
    # Generate a test workspace with a single file.
    with open("foo.txt", "w"):
        pass

    # Create a snapshot.
    assert not snapshot_util.find_latest(True)
    snapshot_util.do_snapshot()
    s1 = snapshot_util.find_latest(True)
    assert s1 is not None, s1

    with open(status_file) as f:
        status_content = json.loads(f.read())
    # verify that we now have a status
    assert (
        status_content["last_activity_timestamp"] is not None
    ), "last_activity_timestamp is not set"

    # No change.
    snapshot_util.do_snapshot()
    s2 = snapshot_util.find_latest(True)
    assert s1 == s2, (s1, s2)

    with open(status_file) as f:
        status_content_1 = json.loads(f.read())

    # verify that the timestamp did not change since the snapshot is the same
    assert status_content == status_content_1, (status_content, status_content_1)

    # Generate a test workspace with a single file.
    with open("foo.txt", "w") as f:
        f.write("changed!")

    # Change.
    snapshot_util.do_snapshot()
    s3 = snapshot_util.find_latest(True)
    assert s2 != s3, (s2, s3)

    with open(status_file) as f:
        status_content_2 = json.loads(f.read())
    # verify that the timestamp is updated due to the new snapshot
    assert status_content != status_content_2, (status_content, status_content_2)


def test_status_without_mounted_directory():
    invalid_directory = "/dir/does/not/exist"
    assert not os.path.exists(invalid_directory), invalid_directory
    env = TestWorkspaceEnv(invalid_directory)
    status_file = f"{snapshot_util.IDLE_TERMINATION_DIR}/workspace.json"
    os.chdir(env.anyscale_working_dir)

    # verify no workspace status on start
    assert not os.path.exists(status_file), status_file
    # Generate a test workspace with a single file.
    with open("foo.txt", "w"):
        pass

    # Create a snapshot.
    assert not snapshot_util.find_latest(True)
    snapshot_util.do_snapshot()
    s1 = snapshot_util.find_latest(True)
    assert s1 is not None, s1

    # verify no workspace status after the snapshot
    assert not os.path.exists(status_file), status_file


@patch("os.path.ismount")
def test_env_hook_doesnt_delete_snapshots(mock_is_mount):
    env = TestWorkspaceEnv()
    os.chdir(env.anyscale_working_dir)

    # Generate a test workspace with a single file.
    with open("foo.txt", "w"):
        pass

    # Sanity check.
    r = snapshot_util.env_hook({})
    assert r == {"working_dir": "/tmp/ray_latest_runtime_env.zip"}

    # Create a snapshot.
    assert not snapshot_util.find_latest(True)
    snapshot_util.do_snapshot()
    s1 = snapshot_util.find_latest(True)
    assert s1 is not None, s1

    # Snapshot shouldn't be deleted or otherwise affected by env hook.
    r = snapshot_util.env_hook({})
    assert r == {"working_dir": "/tmp/ray_latest_runtime_env.zip"}
    s2 = snapshot_util.find_latest(True)
    assert s1 == s2, (s1, s2)


@patch("os.path.ismount")
def test_env_hook_rel_mode(mock_is_mount):
    env = TestWorkspaceEnv()
    os.chdir(env.anyscale_working_dir)

    os.makedirs("subdir")
    os.chdir("subdir")
    with open("foo.txt", "w"):
        pass

    # Test absolute mode.
    snapshot_util.RELATIVE_WORKING_DIR = False
    r = snapshot_util.env_hook({})
    assert r == {"working_dir": "/tmp/ray_latest_runtime_env.zip"}
    assert list_zip("/tmp/ray_latest_runtime_env.zip") == ["subdir/", "subdir/foo.txt"]

    # Test relative mode.
    snapshot_util.RELATIVE_WORKING_DIR = True
    r = snapshot_util.env_hook({})
    assert r == {"working_dir": "/tmp/ray_latest_runtime_env.zip"}
    assert list_zip("/tmp/ray_latest_runtime_env.zip") == ["foo.txt"]


def test_vscode_setup():
    env = TestWorkspaceEnv()
    vscode_desktop_data_dir = os.path.join(env.tmpdir, "vscode_desktop")
    remote_folder = os.path.join(env.cluster_storage, "vscode_desktop")
    real_remote_folder = os.path.join(env.efs_cluster_storage, "vscode_desktop")

    snapshot_util.VSCODE_DESKTOP_SERVER_DIR = vscode_desktop_data_dir

    # Test skipping EFS setup for vscode desktop
    snapshot_util.SKIP_VSCODE_DESKTOP_SETUP = True
    snapshot_util.setup_vscode_desktop()
    assert not os.path.exists(vscode_desktop_data_dir), vscode_desktop_data_dir
    assert not os.path.exists(remote_folder), vscode_desktop_data_dir
    assert not os.path.exists(real_remote_folder), vscode_desktop_data_dir

    # Test EFS setup for vscode desktop
    snapshot_util.SKIP_VSCODE_DESKTOP_SETUP = False
    snapshot_util.setup_vscode_desktop()
    assert os.path.exists(vscode_desktop_data_dir), vscode_desktop_data_dir

    # verify sub folders are created and symlinked
    sub_folders = ["data", "extensions"]
    for sub_folder in sub_folders:
        assert os.path.exists(
            f"{vscode_desktop_data_dir}/{sub_folder}"
        ), f"{vscode_desktop_data_dir}/{sub_folder}"
        assert os.path.islink(
            f"{vscode_desktop_data_dir}/{sub_folder}"
        ), f"{vscode_desktop_data_dir}/{sub_folder}"
        assert os.path.exists(
            f"{remote_folder}/{sub_folder}"
        ), f"{remote_folder}/{sub_folder}"
        assert (
            os.path.realpath(f"{vscode_desktop_data_dir}/{sub_folder}")
            == f"{real_remote_folder}/{sub_folder}"
        )
        assert (
            os.path.realpath(f"{remote_folder}/{sub_folder}")
            == f"{real_remote_folder}/{sub_folder}"
        )
