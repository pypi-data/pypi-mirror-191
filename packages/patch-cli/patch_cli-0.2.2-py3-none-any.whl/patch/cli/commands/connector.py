import click

from patch.auth.auth_token import global_access_token
from patch.cli.commands import pass_obj
from patch.cli.styled import StyledGroup, StyledCommand
from patch.cli.tools.connectors.connector_spec import ConnectorConfigSpec


@click.group(cls=StyledGroup, help='Review the requirements to connect to supported data sources',
             hidden=not global_access_token.has_token())
@click.pass_context
def connector(_ctx, ):
    pass


@connector.group(cls=StyledGroup, help='List of sources that Patch can observe')
def spec():
    pass


class StyledComm:
    pass


@spec.command(cls=StyledCommand, help='Fields required for connection to Azure Blob Storage')
@pass_obj()
def azureblob(patch_ctx):
    console = patch_ctx.console
    connector_spec = ConnectorConfigSpec('azureblob')
    table = connector_spec.render_connector_spec()
    console.print(table)


@spec.command(cls=StyledCommand, help='Fields required for connection to BigQuery')
@pass_obj()
def bigquery(patch_ctx):
    console = patch_ctx.console
    connector_spec = ConnectorConfigSpec('bigquery')
    table = connector_spec.render_connector_spec()
    console.print(table)


@spec.command(cls=StyledCommand, help='Fields required for connection to Snowflake')
@pass_obj()
def snowflake(patch_ctx):
    console = patch_ctx.console
    connector_spec = ConnectorConfigSpec('snowflake')
    table = connector_spec.render_connector_spec()
    console.print(table)
