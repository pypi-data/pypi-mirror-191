# Copyright (C) 2021-2022 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from pathlib import Path

from pontos.git import Git, TagSort

from .helper import (
    VersionError,
    check_develop,
    is_version_pep440_compliant,
    safe_version,
    versions_equal,
)
from .version import UpdatedVersion, VersionCommand

TEMPLATE = """package main

// THIS IS AN AUTOGENERATED FILE. DO NOT TOUCH!

var version = "{}"
\n"""


# This class is used for Python Version command(s)
class GoVersionCommand(VersionCommand):
    project_file_name = Path("go.mod")
    version_file_path = Path("version.go")

    def _update_version_file(self, new_version: str) -> None:
        """
        Update the version file with the new version
        """
        self.version_file_path.write_text(
            TEMPLATE.format(new_version), encoding="utf-8"
        )

    def get_current_version(self) -> str:
        """Get the current version of this project
        In go the version is only defined within the repository
        tags, thus we need to check git, what tag is the latest"""
        if self.version_file_path.exists():
            version_file_text = self.version_file_path.read_text(
                encoding="utf-8"
            )
            match = re.search(
                r'var version = "([deprv0-9.]+)"', version_file_text
            )
            if match:
                return match.group(1)
            else:
                raise VersionError(
                    f"No version found in the {self.version_file_path} file."
                )
        else:
            raise VersionError(
                f"No {self.version_file_path} file found. "
                "This file is required for pontos"
            )

    def verify_version(self, version: str) -> None:
        """Verify the current version of this project"""
        current_version = self.get_current_version()
        if not is_version_pep440_compliant(current_version):
            raise VersionError(
                f"The version {current_version} is not PEP 440 compliant."
            )

        if not versions_equal(current_version, version):
            raise VersionError(
                f"Provided version {version} does not match the "
                f"current version {current_version}."
            )

    def update_version(
        self, new_version: str, *, develop: bool = False, force: bool = False
    ) -> UpdatedVersion:
        """Update the current version of this project"""
        new_version = safe_version(new_version)
        if not check_develop(new_version) and develop:
            new_version = f"{new_version}.dev1"

        try:
            current_version = self.get_current_version()
        except VersionError:
            git = Git()
            current_version = git.list_tags(sort=TagSort.VERSION)[-1]

        if not force and versions_equal(new_version, current_version):
            return UpdatedVersion(previous=current_version, new=new_version)

        self._update_version_file(new_version=new_version)

        return UpdatedVersion(previous=current_version, new=new_version)
