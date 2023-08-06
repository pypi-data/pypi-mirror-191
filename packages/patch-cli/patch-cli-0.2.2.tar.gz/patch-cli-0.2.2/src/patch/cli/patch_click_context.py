import click
from rich.console import Console
from patch.gql.client import Client
from typing import Optional


class PatchClickContext:

    def __init__(self, *, click_ctx: click.Context, terminal_width: Optional[int]):
        self._click_ctx = click_ctx
        self._console = Console(width=terminal_width)

    @property
    def console(self):
        return self._console

    def exit(self, code=0):
        """
        Exits the application with a given exit code.
        Exit nonzero only for errors, not warnings.
        """
        self._click_ctx.exit(code)

    def switch_to_data_output(self) -> Console:
        """Switch default console to stderr and return the original console
        to stdout. Call this when preparing to output data that users may
        want to redirect to text-processing tools."""
        if self._console.stderr:
            raise RuntimeError('Method called more than once.')

        stdout_console = self._console
        self._console = Console(stderr=True)
        return stdout_console

    @property
    def gql_client(self):
        params = click.get_current_context().params
        as_tenant = params.get('as_tenant', None) if params else None
        return Client(as_tenant=as_tenant)
