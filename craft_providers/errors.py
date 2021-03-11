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

"""Craft provider errors."""
import dataclasses
import shlex
import subprocess
from typing import List, Optional, Union


def details_from_command_error(
    *,
    cmd: List[str],
    returncode: int,
    stdout: Optional[Union[bytes, str]] = None,
    stderr: Optional[Union[bytes, str]] = None,
) -> str:
    """Create a consistent ProviderError from Popen command errors.

    If stdout or stderr have undecodable bytes, they will be updated using
    decode(errors="replace").

    :param cmd: Command executed.
    :param stdout: Optional stdout to include.
    :param stderr: Optional stderr to include.

    :returns: Details string.
    """
    cmd_string = shlex.join(cmd)

    details = [
        f"* Command that failed: {cmd_string}",
        f"* Command exit code: {returncode}",
    ]

    if stdout:
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        details.append(f"* Command output: {stdout}")

    if stderr:
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        details.append(f"* Command standard error output: {stderr}")

    return "\n".join(details)


def details_from_called_process_error(
    error: subprocess.CalledProcessError,
) -> str:
    """Create a consistent ProviderError from command errors.

    :param error: CalledProcessError.

    :returns: Details string.
    """
    return details_from_command_error(
        cmd=error.cmd,
        stdout=error.stdout,
        stderr=error.stderr,
        returncode=error.returncode,
    )


@dataclasses.dataclass
class ProviderError(Exception):
    """Unexpected error.

    :param brief: Brief description of error.
    :param details: Detailed information.
    :param resolution: Recommendation, if any.
    """

    brief: str
    details: Optional[str] = None
    resolution: Optional[str] = None

    def __str__(self) -> str:
        parts = [self.brief]

        if self.details:
            parts.append(self.details)

        if self.resolution:
            parts.append(self.resolution)

        return "\n".join(parts)

    @classmethod
    def from_called_process_error(
        cls,
        *,
        brief: str,
        error: subprocess.CalledProcessError,
        resolution: Optional[str] = None,
    ) -> "ProviderError":
        """Create a consistent ProviderError from command errors.

        :param brief: Brief description of error.
        :param error: CalledProcessError from called process.
        :param resolution: Recommendation, if any.
        """
        details = details_from_called_process_error(error)

        return cls(brief=brief, details=details, resolution=resolution)
