from rich.console import Console
from rich.table import Table

import datetime


def parse_date(date_string):
    source_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    return str(
        datetime.datetime.strptime(date_string, source_fmt).replace(microsecond=0)
    )


def print_table(columns, list_of_list_values):
    table = Table(title=None)

    for column in columns:
        table.add_column(column)

    for values in list_of_list_values:
        table.add_row(*values)

    console = Console()
    console.print(table)
