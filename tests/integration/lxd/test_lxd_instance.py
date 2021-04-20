# Copyright 2021 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import pathlib

import pytest

from craft_providers.lxd import LXDInstance

from . import conftest


@pytest.fixture()
def instance(instance_name, project):
    with conftest.tmp_instance(
        instance_name=instance_name,
        project=project,
    ):
        instance = LXDInstance(name=instance_name, project=project)

        yield instance


@pytest.fixture(scope="module")
def reusable_instance():
    """Reusable instance for tests that don't require a fresh instance."""
    instance_name = conftest.generate_instance_name()
    with conftest.tmp_instance(
        instance_name=instance_name,
        ephemeral=False,
        project="default",
    ):
        instance = LXDInstance(name=instance_name, project="default")

        yield instance


@pytest.mark.parametrize("content", [b"", b"\x00\xaa\xbb\xcc", "test-string".encode()])
@pytest.mark.parametrize("mode", ["644", "600", "755"])
@pytest.mark.parametrize("user,group", [("root", "root"), ("ubuntu", "ubuntu")])
def test_create_file(reusable_instance, content, mode, user, group):
    reusable_instance.create_file(
        destination=pathlib.Path("/tmp/file-test.txt"),
        content=io.BytesIO(content),
        file_mode=mode,
        user=user,
        group=group,
    )

    proc = reusable_instance.execute_run(
        command=["cat", "/tmp/file-test.txt"],
        capture_output=True,
    )

    assert proc.stdout == content

    proc = reusable_instance.execute_run(
        command=["stat", "--format", "%a:%U:%G", "/tmp/file-test.txt"],
        capture_output=True,
        text=True,
    )

    assert proc.stdout.strip() == f"{mode}:{user}:{group}"

    reusable_instance.execute_run(
        command=["rm", "/tmp/file-test.txt"],
        capture_output=True,
    )


def test_delete(instance):
    assert instance.exists() is True

    instance.delete()

    assert instance.exists() is False


def test_exists(reusable_instance):
    assert reusable_instance.exists() is True


def test_exists_false():
    fake_instance = LXDInstance(name="does-not-exist")

    assert fake_instance.exists() is False


def test_launch(instance_name):
    instance = LXDInstance(name=instance_name)

    assert instance.exists() is False

    instance.launch(
        image="20.04",
        image_remote="ubuntu",
    )

    try:
        assert instance.exists() is True
    finally:
        instance.delete()


def test_mount_unmount(reusable_instance, tmp_path):
    tmp_path.chmod(0o755)

    host_source = tmp_path
    target = pathlib.Path("/tmp/mnt")

    test_file = host_source / "test.txt"
    test_file.write_text("this is a test")

    assert reusable_instance.is_mounted(host_source=host_source, target=target) is False

    reusable_instance.mount(host_source=host_source, target=target)

    assert reusable_instance.is_mounted(host_source=host_source, target=target) is True

    proc = reusable_instance.execute_run(
        command=["cat", "/tmp/mnt/test.txt"],
        capture_output=True,
    )

    assert proc.stdout == test_file.read_bytes()

    reusable_instance.unmount(target=target)

    assert reusable_instance.is_mounted(host_source=host_source, target=target) is False


def test_mount_unmount_all(reusable_instance, tmp_path):
    tmp_path.chmod(0o755)

    source1 = tmp_path / "1"
    source1.mkdir()
    target_1 = pathlib.Path("/tmp/mnt/1")

    source2 = tmp_path / "2"
    source2.mkdir()
    target_2 = pathlib.Path("/tmp/mnt/2")

    reusable_instance.mount(host_source=source1, target=target_1)
    reusable_instance.mount(host_source=source2, target=target_2)

    assert reusable_instance.is_mounted(host_source=source1, target=target_1) is True
    assert reusable_instance.is_mounted(host_source=source2, target=target_2) is True

    reusable_instance.unmount_all()

    assert reusable_instance.is_mounted(host_source=source1, target=target_1) is False
    assert reusable_instance.is_mounted(host_source=source2, target=target_2) is False


def test_start_stop(reusable_instance):
    assert reusable_instance.is_running() is True

    reusable_instance.stop()

    assert reusable_instance.is_running() is False

    reusable_instance.start()

    assert reusable_instance.is_running() is True