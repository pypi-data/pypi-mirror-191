from patch.cli.tools.connectors.source_config import SourceConfig, SpecVerificationError


class SourceConfigNonInteractive(SourceConfig):

    def check_connector_type(self):
        if not self.connector_spec.type:
            raise SpecVerificationError("Missing field 'type' with connector specification")

    def verify_config(self):
        missing_fields = super().verify_file_config()
        if len(missing_fields) > 0:
            missing_field_names = [f.key for f in missing_fields]
            raise SpecVerificationError(f"[red]Missing fields: {', '.join(missing_field_names)} [/red]")
        return []
