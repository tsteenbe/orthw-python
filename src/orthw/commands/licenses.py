# Copyright 2023 The ORTHW Project Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE
from __future__ import annotations

import click

from orthw import settings
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def licenses(package_id: str, source_code_dir: str | None = None) -> None:
    """licenses

    :param package_id: Id of package
    :type package_id: str
    """

    require_initialized()

    args: list[str] = [
        "ort",
        "list-licenses",
        "--package-id",
        package_id,
        "--apply-license-finding-curations",
        "--omit-excluded",
    ]

    args += ["--ort-file", settings.evaluation_result_file.as_posix()]
    args += ["--repository-configuration-file", settings.repository_configuration_file.as_posix()]
    args += ["--package-configuration-dir", settings.ort_config_package_configuration_dir.as_posix()]

    if source_code_dir:
        args += ["--source-code-dir", source_code_dir]

    # Execute external run
    run(args=args)


@command_group.command(
    context="SCAN_CONTEXT",
    name="licenses",
    help="Lists the license findings for a given package id as distinct text locations.",
    short_help="Lists the license findings for a given package id as distinct text locations.",
)
@click.option("--source-code-dir", default=None)
@click.argument("package_id")
def __licenses(package_id: str, source_code_dir: str | None) -> None:
    licenses(package_id, source_code_dir=source_code_dir)
