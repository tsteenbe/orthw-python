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

from pathlib import Path

import click

from orthw import config
from orthw.utils.cmdgroups import package_config_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def export_curations(package_id: str, source_code_dir: str) -> None:
    require_initialized()

    package_configuration_file = "FIXME find_package(package_id)"
    exports_license_finding_curations_file: Path = config.exports_license_finding_curations_file
    exports_vcs_url_mapping_file: Path = config.exports_vcs_url_mapping_file

    args: list[str] = [
        "orth",
        "package-configuration",
        "export-license-finding-curations",
        "--package-configuration-file",
        package_configuration_file,
        "--license-finding-curations-file",
        exports_license_finding_curations_file.as_posix(),
        "--source-code-dir",
        source_code_dir,
        "--vcs-url-mapping-file",
        exports_vcs_url_mapping_file.as_posix(),
    ]

    run(args=args)


@package_config_group.command(
    context="PACKAGE_CONFIG",
    name="export-curations",
    help="""
        Exports the license finding curations to '{file}' which maps repository URLs
        to the license finding curations for the respective repository.

        Examples:

        orthw package-config export-curations {package_id} /home/ort-user/code-repo/
    """.format(
        file=config.exports_license_finding_curations_file,
        package_id="Maven:org.apache.curator:curator-framework:2.13.0",
    ),
    short_help=f"Exports the license finding curations to '{config.exports_license_finding_curations_file}'.",
)
@click.argument("package_id")
@click.argument("source_code_dir")
def __export_curations(package_id: str, source_code_dir: str) -> None:
    """Exports the license finding curations to a file."""
    export_curations(package_id=package_id, source_code_dir=source_code_dir)
