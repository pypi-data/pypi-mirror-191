import os
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from patch.cli.styled import NONE_BOX
from patch.cli.tools.tables.rows.table_data_row import TableDataRow, ColumnsDataRow
from patch.cli.tools.tables.source_data import SourceData
from patch.gql.client import Client
from patch.storage.state_file import StatePayload

default_ingest_mode = os.environ.get('PATCH_TABLE_INGEST_MODE', 'CONTINUOUS')


def get_hierarchy(table_id):
    segments = table_id.split('.')
    if len(segments) > 3:
        name = '.'.join(segments[2:])
        hierarchy = segments[0:2]
    else:
        name = segments[-1]
        hierarchy = segments[0:-1]
    return [name, hierarchy]


class SourceMetadataClient:

    def __init__(self, console: Console, gql_client: Client, state: StatePayload):
        self.console = console
        self.client = gql_client
        self.source_id = state.active_source_id
        self.source_name = state.active_source_name

    def query_source_description(self):
        gql_query = self.client.prepare_query('getSourceDescription', id=self.source_id)
        with gql_query as q:
            q.tables.__fields__()
            q.__fields__('quota', 'quotaUsed')
        with self.console.status("[bold green]Loading source structure...[/bold green]") as _status:
            return gql_query.execute()

    def get_source_metadata(self) -> SourceData:
        source_description = self.query_source_description()
        sorted_tables = sorted(source_description.tables, key=lambda tab: tab.id)
        tables = []
        for t in sorted_tables:
            columns = []
            for c in t.columns:
                column = ColumnsDataRow(name=c.name, type=c.type, index=c.index, selected=False)
                columns.append(column)
            sorted_columns = sorted(columns, key=lambda col: col.index)
            [name, hierarchy] = get_hierarchy(t.id)
            table = TableDataRow(
                id=t.id, database=t.database, name=name, type=t.type, columns=sorted_columns, hierarchy=hierarchy,
                size_bytes=t.sizeBytes, row_count=t.rowCount)
            tables.append(table)

        return SourceData(
            tables=tables,
            selected_tables=[],
            is_ready=False,
            quota=source_description.quota or 0,
            quota_used=source_description.quotaUsed or 0
        )

    def confirm_dataset(self, dataset_name, tables):
        self.console.print(f"\nYou are creating a dataset [cyan]{dataset_name}[/cyan] "
                           f"in the source [cyan]{self.source_name}[/cyan] "
                           f"(Source ID: [yellow]{self.source_id}[/yellow])")

        rt = Table(title=None, show_edge=True, box=NONE_BOX)
        rt.add_column("Location", justify="left", style="magenta", no_wrap=True)
        rt.add_column("Name", justify="left", style="cyan", no_wrap=True)
        rt.add_column("Primary key", justify="left", no_wrap=True)
        for table in tables:
            h = " . ".join(table.hierarchy)
            pk = []
            for column in table.columns:
                if column.selected:
                    pk.append(column.name)

            rt.add_row(h, table.name, ", ".join(pk))
        self.console.print(rt)
        return Confirm.ask("Proceed? ", console=self.console)

    def build_create_dataset_input(self, dataset_name, tables):
        tables_input = []
        for table in tables:
            columns_input = []
            for column in table.columns:
                if column.selected is True:
                    columns_input.append({'columnName': column.name})
            tables_input.append({
                'tableId': table.id,
                'primaryKeys': columns_input,
                'ingestMode': default_ingest_mode
            })
        return {
            'sourceId': self.source_id,
            'datasetName': dataset_name,
            'tables': tables_input
        }
