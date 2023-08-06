import click
import sys

from patch.cli.patch_click_context import PatchClickContext
from patch.debug import debug_enabled
from patch.cli.commands.connector import connector
from patch.cli.commands.login import login
from patch.cli.commands.source import source
from patch.cli.commands.dataset import dataset
from patch.cli.commands.dataset import edge
from patch.cli.commands.admin import admin
from patch.cli.commands.playground import playground
from patch.cli.commands.token import token
from patch.cli.commands.user import user
from patch.cli.commands.access import access
from rich.console import Console

from patch.cli.eap import eap_warning
from patch.cli.styled import StyledGroup


def safe_main():
    try:
        main()
    except Exception as e:
        console = Console(stderr=True)
        console.print(f"[red]error: {e}[/red]")
        if debug_enabled():
            console.print_exception()
        sys.exit(1)


@click.group(cls=StyledGroup)
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)
    ctx.obj = PatchClickContext(click_ctx=ctx, terminal_width=ctx.terminal_width)


main.add_command(login)
main.add_command(user)
main.add_command(connector)
main.add_command(source)
main.add_command(dataset)
main.add_command(edge)
main.add_command(admin)
main.add_command(playground)
main.add_command(token)
main.add_command(access)
