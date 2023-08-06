from typing import Dict

from patch.cli.tools.config_spec import ConfigSpec
from patch.cli.tools.field_spec import FieldSpec, InputSpec
from rich.prompt import Prompt
from rich import box
from rich.table import Table

name_spec = FieldSpec(key="name", desc="Source name", required=True)

conn_spec: Dict[str, InputSpec] = {
    'snowflake': InputSpec(
        name='Snowflake',
        create_mutation_name='sourceConnectSnowflake',
        fields=[
            FieldSpec(key="user", desc="User", required=True),
            FieldSpec(key="password", desc="Password", required=True, is_password=True),
            FieldSpec(key="host", desc="Host", required=True),
            FieldSpec(key="warehouse", desc="Warehouse", required=True),
            FieldSpec(key="database", desc="Database", required=True),
            FieldSpec(key="schema", desc="Schema", required=True),
            FieldSpec(key="stagingDatabase", desc="Staging Database", required=False),
        ]),
    'bigquery': InputSpec(
        name='BigQuery',
        create_mutation_name='sourceConnectBigQuery',
        fields=[
            FieldSpec(key="credentialsKey", desc="Path to BigQuery credentials file", required=True),
            FieldSpec(key="projectId", desc="Project ID", required=True),
            FieldSpec(key="location", desc="BigQuery location", required=False),
            FieldSpec(key="dataset", desc="BigQuery Dataset", required=False),
            FieldSpec(key="stagingProjectId", desc="Patch Staging Project", required=True),
        ]),
    'azureblob': InputSpec(
        name='Azure Blob Storage',
        create_mutation_name='sourceConnectAzureBlob',
        fields=[
            FieldSpec(key="containerName", desc="The name of the Blob Storage container", required=True),
            FieldSpec(key="accountName", desc="The name of the storage account that owns the container", required=True),
            FieldSpec(key="sasToken", desc="A SAS token that grants access to the container (or a directory within)", required=True),
        ]),
}


def render_bool(value: bool):
    return "True" if value else "False"


class ConnectorConfigSpec(ConfigSpec):

    def __init__(self, str_connector_type):
        super().__init__(conn_spec, name_spec, str_connector_type)

    def ask_connector_type(self, console):
        connector_type_str = Prompt.ask("Select connector type",
                                        choices=['snowflake', 'bigquery', 'azureblob'],
                                        console=console)
        self.set_type_from_str(connector_type_str)

    def render_connector_spec(self):
        name = self.get_spec().name
        table = Table(title=name, box=box.SIMPLE, border_style="grey37", show_lines=False)
        table.add_column("Key", justify="right", style="cyan", no_wrap=True)
        table.add_column("Description", justify="left", style="green", no_wrap=True)
        table.add_column("Required?", justify="left", style="green", no_wrap=True)
        for line in self.get_spec_fields():
            table.add_row(line.key, line.desc, render_bool(line.required))
        return table
