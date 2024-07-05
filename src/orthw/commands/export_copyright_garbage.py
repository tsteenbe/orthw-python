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

import tempfile
from pathlib import Path

from rich.pretty import pprint

from orthw import settings
from orthw.utils import logging
from orthw.utils.cmdgroups import command_group
from orthw.utils.process import run
from orthw.utils.required import require_initialized


def export_copyright_garbage() -> None:
    """Command export-copyright-garbage"""
    require_initialized()

    copyrights_file: Path = settings.copyrights_file
    ort_config_copyright_garbage_file: Path = settings.ort_config_copyright_garbage_file
    scan_result_file: Path = settings.scan_result_file
    if (
        copyrights_file.is_file() is None
        or not ort_config_copyright_garbage_file.is_file()
        or not scan_result_file.is_file()
    ):
        logging.error("Configuration invalid.")
        return

    logging.info(f"Exporting from {copyrights_file} to {ort_config_copyright_garbage_file}.")

    tmpdir = tempfile.TemporaryDirectory(prefix="orthw_")
    mapped_copyrights_file: Path = Path(tmpdir.name / "copyrights-mapped.txt")  # type: ignore

    args: list[str] = [
        "orth",
        "map-copyrights",
        "--input-copyrights-file",
        copyrights_file.as_posix(),
        "--output-copyrights-file",
        mapped_copyrights_file.as_posix(),
        "--ort-file",
        scan_result_file.as_posix(),
    ]
    run(args=args)

    logging.info("Mapped the given processed statements to the following unprocessed ones:")
    if mapped_copyrights_file.exists():
        with Path.open(mapped_copyrights_file) as f:
            pprint(f.readlines())

    args = [
        "orth",
        "import-copyright-garbage",
        "--input-copyright-garbage-file",
        mapped_copyrights_file.as_posix(),
        "--output-copyright-garbage-file",
        settings.ort_config_copyright_garbage_file.as_posix(),
    ]
    run(args=args)


@command_group.command(
    context="SCAN_CONTEXT",
    name="export-copyright-garbage",
    short_help=(
        "Import copyright garbage from a plain text file containing one "
        "copyright statement per line into the given copyright garbage file."
    ),
)
def __export_copyright_garbage() -> None:
    export_copyright_garbage()
