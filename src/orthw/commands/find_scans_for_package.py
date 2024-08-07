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
from psycopg2.sql import Literal
from rich import print
from rich.pretty import pprint

from orthw.utils.cmdgroups import command_group
from orthw.utils.database import list_scan_results, query_scandb


def find_scans_for_package(package_id: str) -> None:
    list_scan_results(package_id=package_id)

    count_sql: Literal[str] = Literal(
        f"SELECT COUNT(*) FROM scan_results WHERE identifier LIKE '{package_id}'",  # noqa: S608
    )
    count: list[tuple[str, str]] | None = query_scandb(sql=count_sql)

    if not count:
        print("[bright_yellow]No results were found with this package id.[/bright_yellow]")

    print(f"[bright_blue]Found the above $count scan results for query string {package_id}.[/bright_blue]")
    print("[bright_blue]Press enter to delete them.[/bright_blue]")
    input()

    delete_sql: Literal[str] = Literal(f"DELETE FROM scan_results WHERE identifier LIKE {package_id}")  # noqa: S608
    result = query_scandb(sql=delete_sql)

    if result:
        pprint(result)


@command_group.command(
    context="NO_SCAN_CONTEXT",
    name="find-scans-for-package",
)
@click.argument("package_id")
def __find_scans_for_package(package_id: str) -> None:
    find_scans_for_package(package_id=package_id)
