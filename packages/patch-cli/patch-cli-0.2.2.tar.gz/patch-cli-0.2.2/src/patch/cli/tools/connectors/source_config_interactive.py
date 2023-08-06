from typing import TextIO, Optional, List

from patch.cli.tools.connectors.source_config import SourceConfig
from rich.prompt import Prompt

from patch.cli.tools.field_spec import FieldSpec
from patch.cli.tools.base64_encryption import b64_encryption


class SourceConfigInteractive(SourceConfig):

    def __init__(self, console, file_config: Optional[TextIO], staging_db: Optional[str]):
        super().__init__(file_config, staging_db)
        self.console = console

    def check_connector_type(self):
        if not self.connector_spec.type:
            self.connector_spec.ask_connector_type(self.console)

    def verify_config(self):
        missing_fields = super().verify_file_config()
        if len(missing_fields) > 0:
            self._ask_missing_fields(missing_fields)
        return []

    def _ask_missing_fields(self, missing_fields: List[FieldSpec]):
        for missing_field in missing_fields:
            while True:
                value = Prompt.ask(missing_field.desc, console=self.console, password=missing_field.is_password)
                if missing_field.key == "credentialsKey":
                    value = b64_encryption(value)
                if len(value) > 0:
                    break
                self.console.print("[prompt.invalid]Value cannot be empty")
            self.config[missing_field.key] = value
