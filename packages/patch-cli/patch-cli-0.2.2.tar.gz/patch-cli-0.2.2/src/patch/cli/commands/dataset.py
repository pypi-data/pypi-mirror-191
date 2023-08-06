import datetime
import os
import pyperclip
import click
import json
from rich import box
from rich.prompt import Confirm

from rich.table import Table

from patch.auth.auth_token import global_access_token
from patch.cli import PatchClickContext
from patch.cli.commands import active_source, pass_obj, with_as_tenant
from patch.cli.eap import eap_warning
from patch.cli.styled import StyledGroup, StyledCommand
from patch.cli.remote.dataset_client import DatasetClient
from patch.cli.tools.datasets.endpoint_renderer import EndpointRenderer
from patch.cli.tools.filters_reader import filters_to_claims
from patch.cli.tools.tables.source_app import SourceApp
from patch.cli.tools.tables.source_data import SourceMeta
from patch.cli.tools.tables.source_metadata_client import SourceMetadataClient

from patch.cli.tools.datasets.row_table_renderer import RowRenderer, RowTableRenderer

DEFAULT_PAXL_GQL_URL = 'https://api.patch.tech/query/graphql'

paxl_gql_url = os.environ.get('PATCH_PAXL_GQL_URL') or DEFAULT_PAXL_GQL_URL


@click.group(cls=StyledGroup, help='Create or edit datasets that Patch generates APIs over',
             hidden=not global_access_token.has_token())
def dataset():
    pass


def mutate_create_dataset(client, console, create_dataset_input):
    gql_query = client.prepare_mutation('createDataset', input=create_dataset_input)
    with console.status("[bold yellow]Creating dataset ...[/bold yellow]") as _status:
        gql_result = gql_query.execute()
    return gql_result


def create_dataset_interactive(client, console, name, local_state):
    interface = SourceMetadataClient(console, client, local_state)
    meta = SourceMeta(source_data=interface.get_source_metadata())

    if not meta.source_data.tables:
        console.print(f"No tables found in active source [blue]{local_state.active_source_name}[/blue].")
        console.print("If the active source is some type of object storage, use " +
            '\"pat dataset create -c <config.json>\" instead.')
        console.print("You can find the config file schema in the docs for the active source's type.")
        return None

    source_app = SourceApp(meta=meta)
    source_app.run()
    if meta.source_data.is_ready and interface.confirm_dataset(dataset_name=name,
                                                               tables=meta.source_data.selected_tables):
        return interface.build_create_dataset_input(dataset_name=name, tables=meta.source_data.selected_tables)

    console.print(f"Dataset creation [yellow]cancelled![/yellow]")
    return None


def create_dataset_from_file(_client, _console, name, source_id, config_file):
    config = json.load(config_file)
    return {
        'sourceId': source_id,
        'datasetName': name,
        'tables': config["tables"],
    }


@dataset.command(cls=StyledCommand, help='Configure dataset')
@click.option('-c', '--config', type=click.File(mode='r'), help='Configuration file')
@click.argument('name', type=click.STRING)
@with_as_tenant()
@pass_obj()
def create(patch_ctx: PatchClickContext, config, name):
    console = patch_ctx.console
    with active_source(patch_ctx) as local_state:
        client = patch_ctx.gql_client
        source_id = local_state.active_source_id
        dataset_client = DatasetClient(console, client, source_id=source_id)
        if dataset_client.datasource_exists(name):
            raise Exception(f"Dataset {name} already exists.  Please choose a different name.")

        if config:
            create_dataset_input = create_dataset_from_file(client, console, name, source_id, config)
        else:
            create_dataset_input = create_dataset_interactive(client, console, name, local_state)

        if create_dataset_input is not None:
            mutate_create_dataset(client, console, create_dataset_input)
            console.print("[bold green]Dataset submitted![/bold green] "
                          "Now, your dataset is being processed, and will be ready soon!")
            console.print(
                f"Check [yellow] pat dataset endpoints {name} [/yellow] for endpoints you can use to access it.")
            console.print(
                f"Check [yellow] pat dataset bearer {name} [/yellow] to obtain a bearer token.")


def join_with_limit(table_names, join_str='\n'):
    stretch = 0
    for i, name in enumerate(table_names):
        stretch += len(name)
    return join_str.join(table_names)


def safe_tables_limit(console_width, dataset_list):
    max_id = 0
    max_name = 0
    for elem in dataset_list:
        max_id = max(max_id, len(elem.id))
        max_name = max(max_name, len(elem.name))
    safe_margin = 5
    computed_limit = console_width - safe_margin - max_id - max_name
    return max(computed_limit, 0)


def create_edge_descriptions(tables, console):
    parts = []
    tables_by_id = {t.id: t.name for t in tables}
    for t in tables:
        for e in t.edges:
            from_table_name = tables_by_id.get(e.fromTableId)
            to_table_name = tables_by_id.get(e.toTableId)
            if from_table_name and to_table_name:
                parts.append(f'{e.name}: {from_table_name} → {to_table_name}')
            else:
                from_table_name = '[red]Unknown[/red]' if not from_table_name else from_table_name
                to_table_name = '[red]Unknown[/red]' if not to_table_name else to_table_name
                console.print(
                    f"Unknown edge endpoint: {e.fromTableId}({from_table_name}) → {e.toTableId}({to_table_name}).")
    return '\n'.join(parts)


def render_table(name, size):
    segments = [name]
    if size is not None:
        segments.append(f"({size})")
    return " ".join(segments)


@dataset.command(cls=StyledCommand, help='List datasets')
@with_as_tenant()
@pass_obj()
def ls(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    with active_source(patch_ctx, show_state=True) as local_state:
        client = patch_ctx.gql_client
        gql_query = client.prepare_query('datasets', input={
            'sourceId': local_state.active_source_id,
        })
        with gql_query as q:
            q.__fields__('id', 'name')
            q.tables.__fields__('id', 'name', 'tableState', 'lastRowCount', 'edges', 'lastCdcSuccessTimeAgo')
        dataset_list = gql_query.execute()

        if len(dataset_list) == 0:
            console.print("[yellow]No datasets found[/yellow]")
        else:
            has_edges = any(t.edges for d in dataset_list for t in d.tables)

            table = Table(title="Datasets", box=box.ROUNDED, border_style="grey37")
            table.add_column("Name", style="cyan", no_wrap=True, overflow="fold")
            table.add_column("ID", style="yellow", overflow="fold")
            table.add_column("Tables", justify="left", overflow="fold")
            if has_edges:
                table.add_column("Edges", justify="left", overflow="fold")

            dataset_list_sorted = sorted(dataset_list, key=lambda d: d.name)
            for dataset_elem in dataset_list_sorted:
                table_names = []
                for t in dataset_elem.tables:
                    table_info = [t.lastRowCount, t.tableState]
                    if t.lastCdcSuccessTimeAgo:
                        table_info.append("Synced " + t.lastCdcSuccessTimeAgo + " ago")
                    table_names.append(render_table(t.name, table_info))
                joined_table_names = join_with_limit(table_names).replace("[", "").replace("]", "").replace("'", "")
                if has_edges:
                    edge_descriptions = create_edge_descriptions(dataset_elem.tables, console)
                    table.add_row(dataset_elem.name, dataset_elem.id, joined_table_names, edge_descriptions)
                else:
                    table.add_row(dataset_elem.name, dataset_elem.id, joined_table_names)
            console.print(table)


@dataset.command(cls=StyledCommand, help='Remove dataset')
@click.argument('name', type=click.STRING)
@click.option('-y', '--assume-yes', '--yes', help='Skip confirmation', is_flag=True)
@with_as_tenant()
@pass_obj()
def remove(patch_ctx: PatchClickContext, name, assume_yes):
    console = patch_ctx.console
    with active_source(patch_ctx, show_state=True) as local_state:
        confirmation = assume_yes or Confirm.ask(f"Would you like to remove Dataset [cyan]{name}[/cyan] " +
                                                 f"from Source [cyan]{local_state.active_source_name}[/cyan]? ",
                                                 console=console)
        if confirmation:
            client = patch_ctx.gql_client
            gql_mutation = client.prepare_mutation('removeDataset', input={'sourceId': local_state.active_source_id,
                                                                           'datasetName': name})
            gql_mutation.execute()
            console.print(f"[green]Dataset queued for deletion[/green]")
        else:
            console.print(f"Command [red]aborted[/red]")


@dataset.command(cls=StyledCommand, help='Endpoints for the dataset')
@click.argument('name', type=click.STRING)
@click.option('-o', '--output',
    type=click.Choice(['json', 'table']), default='table', show_default=True,
    help='Output format (choices: json, table)')
@with_as_tenant()
@pass_obj()
def endpoints(patch_ctx: PatchClickContext, name, output):
    if output == 'json':
        console = patch_ctx.switch_to_data_output()
    else:
        console = patch_ctx.console

    eap_warning(patch_ctx.console)

    with active_source(patch_ctx, show_state=True) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_query = client.prepare_query('datasetByName', input={
            'sourceId': source_id,
            'datasetName': name
        })
        with gql_query as q:
            q.__fields__('id', 'name', 'tables')

        result = gql_query.execute()
        eh = EndpointRenderer(console, local_state, name, output)
        eh.render_query_result(result)


def match_primary_keys(table_pk, input_pk):
    len_table_pk = len(table_pk)
    table_names = [t.name.lower() for t in table_pk]
    if len(input_pk) != len_table_pk:
        tn = ", ".join(table_names)
        raise Exception(f"[red]Arity of primary keys ({tn}) do not match table specification[/red].")
    pk_map = {}
    pk_result = []
    for input_value in input_pk:
        pkey, *values = input_value.split("=", maxsplit=1)
        if len(values) == 0:
            if len_table_pk == 1:
                key_name = table_names[0]
                return [{'name': key_name, 'value': input_value}]
            else:
                raise Exception(f"[red]Primary key {pkey} must be in format: key=value [/red].")
        value = values[0]
        pk_map[pkey.lower()] = value
        pk_result.append({'name': pkey, 'value': value})
    for name in table_names:
        if pk_map.get(name, None) is None:
            raise Exception(f"[red]Missing value for primary key column {name}[/red].")
    return pk_result


@dataset.command(cls=StyledCommand, help='Inspect single record by primary key')
@click.argument('dataset_name', type=click.STRING)
@click.argument('table_name', type=click.STRING)
@click.argument('primary_key', type=click.STRING, nargs=-1)
@with_as_tenant()
@pass_obj()
def inspect(patch_ctx: PatchClickContext, dataset_name, table_name, primary_key):
    console = patch_ctx.console
    eap_warning(console)
    with active_source(patch_ctx, show_state=True) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_query = client.prepare_query('datasetByName', input={
            'sourceId': source_id,
            'datasetName': dataset_name
        })
        with gql_query as q:
            q.__fields__('id', 'name', 'tables')

        result = gql_query.execute()
        table_name_lc = table_name.lower()
        table_spec = None
        for ts in result.tables:
            if ts.name.lower() == table_name_lc:
                table_spec = ts
        if not table_spec:
            raise Exception(f"[red]Unknown table {table_name}[/red]")
        if table_spec.tableState == 'INIT':
            raise Exception(f"[red]Table {table_name} is in the INIT state, records are not available yet.[/red]")
        pks = match_primary_keys(table_spec.primaryKey, primary_key)

        gql_query_inspection = client.prepare_query('recordInspection', input={
            'sourceId': source_id,
            'datasetName': dataset_name,
            'tableName': table_name,
            'primaryKey': pks
        })
        with gql_query_inspection as q:
            q.__fields__('sourceRecordCount')
            q.sourceRecords.columns.__fields__('name', 'value')
            q.cacheRecord.columns.__fields__('name', 'value')

        result_inspection = gql_query_inspection.execute()
        if len(result_inspection.sourceRecords) == 0 and RowRenderer.is_empty(result_inspection.cacheRecord):
            raise Exception(f"[red]Record not found {table_name}[/red]")
        r_1 = RowRenderer(result_inspection.cacheRecord, "Cache", "yellow")
        r_2 = RowRenderer(result_inspection.sourceRecords[0], "Source", "green", result_inspection.sourceRecordCount)
        tr = RowTableRenderer([r_1, r_2])
        console.print(tr.render_table(table_name))

        if len(result_inspection.sourceRecords) > 1:
            show_more = Confirm.ask("More thant one record in source. Show more (up to 10)?", default="y")
            if show_more:
                more_records = result_inspection.sourceRecords[1:]
                i = 2
                while len(more_records) > 0:
                    batch_rows = [RowRenderer(more_records.pop(), f"Source {i}", "green")]
                    i += 1
                    if len(more_records) > 0:
                        batch_rows.append(RowRenderer(more_records.pop(), f"Source {i}", "green"))
                        i += 1
                    tr = RowTableRenderer(batch_rows)
                    console.print(tr.render_table(None))


@dataset.command(cls=StyledCommand, help='Bearer tokens for endpoints.')
@click.argument('name', type=click.STRING)
@click.option('-f', '--filter', type=str, help='Filter of the authorization scope', multiple=True)
@with_as_tenant()
@pass_obj()
def bearer(patch_ctx: PatchClickContext, name, filter):
    with active_source(patch_ctx) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_mutation = client.prepare_mutation('generateQueryAuth', input={
            'sourceId': source_id,
            'datasetName': name,
            'filters': filters_to_claims(filter)
        })
        with gql_mutation as m:
            m.__fields__('accessToken')

        result = gql_mutation.execute()
        print(result.accessToken)


@dataset.command(cls=StyledCommand, help='Launch GraphQL Playground.')
@click.argument('name', type=click.STRING)
@click.option('-f', '--filter', type=str, help='Filter of the authorization scope', multiple=True)
@with_as_tenant()
@pass_obj()
def playground(patch_ctx: PatchClickContext, name, filter):
    with active_source(patch_ctx, show_state=True) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_mutation = client.prepare_mutation('generateQueryAuth', input={
            'sourceId': source_id,
            'datasetName': name,
            'filters': filters_to_claims(filter)
        })
        with gql_mutation as m:
            m.__fields__('accessToken')

        mutation_result = gql_mutation.execute()
        token = mutation_result.accessToken

        console = patch_ctx.console

        console.print("You are about to open GraphQL Playground.")
        console.print(
            "The configuration below will be copied to your clipboard. You can paste it in [yellow]HTTP HEADERS[/yellow] tab in the Playground console.\n")
        headers = json.dumps({'Authorization': token})
        console.out(headers)

        console.input("\nPress Enter to continue...")
        paxl_gql_prompt_url = f"{paxl_gql_url}#prompt"
        result = click.launch(paxl_gql_prompt_url)
        if result != 0:
            console.input(f"Now, open [magenta]{paxl_gql_url}#prompt[/magenta]")
        else:
            console.print(
                f"If your default browser hasn't loaded it, open this url in your browser: [magenta]{paxl_gql_url}#prompt[/magenta]")
        pyperclip.copy(headers)


@click.group(cls=StyledGroup, help='Create, edit, or delete edges between tables of a dataset',
             hidden=not global_access_token.has_token())
def edge():
    pass


def validate_table_names(table1_name, table2_name, known_tables_by_name):
    unknown_tables = {table1_name, table2_name} - known_tables_by_name.keys()
    if unknown_tables:
        raise Exception(f"[red]Unknown table(s) {', '.join(unknown_tables)}[/red]")


@edge.command(cls=StyledCommand, help='Create table->table edge.')
@click.argument('name', type=click.STRING)
@click.argument('dataset_name', type=click.STRING)
@click.argument('from_table_name', type=click.STRING)
@click.argument('to_table_name', type=click.STRING)
@click.option(
    '-c',
    '--on-columns',
    multiple=True,
    nargs=2,
    required=True,
    type=click.STRING,
    help='Pairs of columns used to join table1 and table2, e.g. -c <table1-cola> <table2-colb>')
@click.option('-u', '--is-unique', is_flag=True, required=False, default=False, show_default=True, help='Is this a 1:1 relationship?')
@with_as_tenant()
@pass_obj()
def create(patch_ctx: PatchClickContext, name, dataset_name, from_table_name, to_table_name, on_columns, is_unique):
    console = patch_ctx.console
    eap_warning(console)
    with active_source(patch_ctx, show_state=True) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_query = client.prepare_query('datasetByName', input={
            'sourceId': source_id,
            'datasetName': dataset_name
        })
        with gql_query as q:
            q.__fields__('id', 'name', 'tables')

        result = gql_query.execute()

        tables_by_name = {}
        for t in result.tables:
            tables_by_name[t.name] = t

        validate_table_names(from_table_name, to_table_name, tables_by_name)

        # NB: Validating column type match in the client requires a lot more
        # changes than anticipated because the table metadata returned by
        # `datasetByName` does not include column schemas. We defer to the
        # config-api to validate column types.

        gql_mutation = client.prepare_mutation('createTableEdge', input={
            'name': name,
            'fromTableId': tables_by_name[from_table_name].id,
            'toTableId': tables_by_name[to_table_name].id,
            'onColumns': [{'fromColumnName': c1, 'toColumnName': c2} for c1, c2 in on_columns],
            'unique': is_unique
        })
        success = gql_mutation.execute()
        if success:
            console.print(f"Created edge {name} from {from_table_name} to {to_table_name} successfully")


@dataset.group(cls=StyledGroup, help='Create, list, and revoke Data Access Keys',
               hidden=not global_access_token.has_token())
def key():
    pass


@key.command(cls=StyledCommand, help='Create Data Access Key')
@click.argument('dataset_name', type=click.STRING)
@click.argument('name', type=click.STRING)
@click.option('-f', '--filter', type=str, help='Filter of the authorization scope', multiple=True)
@with_as_tenant()
@pass_obj()
def create(patch_ctx: PatchClickContext, dataset_name, name, filter):
    with active_source(patch_ctx) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_mutation = client.prepare_mutation('generateDataAccessKey', input={
            'name': name,
            'sourceId': source_id,
            'datasetName': dataset_name,
            'filters': filters_to_claims(filter)
        })
        with gql_mutation as m:
            m.__fields__('accessKey')

        result = gql_mutation.execute()
        print(result.accessKey)


def render_access_keys(console, access_keys):
    table = Table(title="Data Access Keys", box=box.ROUNDED, border_style="grey37")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("ID", justify="left", style="yellow", no_wrap=True)
    table.add_column("Created At", justify="left", style="white", no_wrap=True)
    table.add_column("Data Access Key", justify="left", style="yellow", no_wrap=True)
    for access_key in access_keys:
        dt = datetime.datetime.fromtimestamp(int(access_key.createdAt) / 1000)
        table.add_row(access_key.name, access_key.id, dt.strftime("%m/%d/%Y, %H:%M:%S"), access_key.accessKey)
    console.print(table)


@key.command(cls=StyledCommand, help='List Data Access Keys')
@click.argument('dataset_name', type=click.STRING)
@with_as_tenant()
@pass_obj()
def ls(patch_ctx: PatchClickContext, dataset_name):
    with active_source(patch_ctx) as local_state:
        source_id = local_state.active_source_id
        client = patch_ctx.gql_client
        gql_query = client.prepare_query('dataAccessKeys', input={
            'showKey': False,
            'sourceId': source_id,
            'datasetName': dataset_name
        })
        with gql_query as m:
            m.__fields__('id', 'name', 'createdAt', 'accessKey')

        result = gql_query.execute()
        render_access_keys(patch_ctx.console, result)


@key.command(cls=StyledCommand, help='Get Data Access Key by ID')
@click.argument('access_key_id', type=click.STRING)
@with_as_tenant()
@pass_obj()
def get(patch_ctx: PatchClickContext, access_key_id):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    gql_query = client.prepare_query('dataAccessKey', id=access_key_id)
    with gql_query as m:
        m.__fields__('id', 'name', 'createdAt', 'accessKey')

    result = gql_query.execute()
    console.print(result.accessKey)


@key.command(cls=StyledCommand, help='Revoke Data Access Key by ID')
@click.argument('access_key_id', type=click.STRING)
@with_as_tenant()
@pass_obj()
def revoke(patch_ctx: PatchClickContext, access_key_id):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    prepare_mutation = client.prepare_mutation('revokeDataAccessKey', input={
        'dataAccessKeyId': access_key_id
    })
    prepare_mutation.execute()
    console.print(f"Data Access Key [yellow]{access_key_id}[/yellow] has been revoked")
