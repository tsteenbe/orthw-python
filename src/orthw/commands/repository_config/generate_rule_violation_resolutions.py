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

from orthw import settings
from orthw.utils.cmdgroups import repository_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def generate_rule_violation_resolutions() -> None:
    require_initialized()

    evaluation_result_file: Path = settings.evaluation_result_file
    repository_configuration_file: Path = settings.repository_configuration_file

    args: list[str] = [
        "orth",
        "repository-configuration",
        "generate-rule-violation-resolutions",
        "--ort-file",
        evaluation_result_file.as_posix(),
        "--repository-configuration-file",
        repository_configuration_file.as_posix(),
        "--severity ERROR",
    ]

    run(args=args)


@repository_group.command(
    context="REPOSITORY_CONFIG",
    name="generate-rule-violation-resolutions",
    help="""
        Generates resolutions in the ort.yml file for all unresolved rule violations.
    """,
    short_help="Generates resolutions in the ort.yml file for all unresolved rule violations.",
)
def __generate_rule_violation_resolutions() -> None:
    """Generates resolutions in the ort.yml file for all unresolved rule violations."""
    generate_rule_violation_resolutions()
