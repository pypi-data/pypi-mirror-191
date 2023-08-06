from abc import ABC, abstractmethod
from typing import Optional, TextIO

from patch.cli.tools.connectors.connector_spec import ConnectorConfigSpec
from patch.cli.tools.json_reader import read_json


class SpecVerificationError(Exception):
    pass


class SourceConfig(ABC):
    """The source config.

    This class manages collecting and interpreting source configuration.
    There are two possible sources of the configuration:
    - configuration JSON file
    - interactive input
    A bit tricky part of the source configuration is that before we collect and validate
    the configuration attributes we need to know what is the connector type.
    - If the connector type was given in the configuration file, we take it from there,
        and remove from the configuration.
    - If the connector type is missing in the config file (or there was no config file)
        we need to ask about the type before anything else.

    """

    def __init__(self, file_config: Optional[TextIO], staging_db: Optional[str]):
        self.config = read_json(file_config, SpecVerificationError)

        str_connector_type = self.config.pop('type', None)
        self.connector_spec = ConnectorConfigSpec(str_connector_type)
        self.staging_db = staging_db

    @abstractmethod
    def check_connector_type(self) -> bool:
        pass

    @abstractmethod
    def verify_config(self):
        pass

    def verify_file_config(self):
        spec = self.connector_spec.get_spec_fields_plus_name()

        required_spec_keys = set([r.key for r in spec if r.required])
        result = {}
        for key, value in self.config.items():
            if key in required_spec_keys:
                required_spec_keys.remove(key)
                result[key] = value
            else:
                raise SpecVerificationError(f"Unknown key {key}")
        self.config = result
        return [s for s in spec if s.key in required_spec_keys]

    def send_to_gql(self, patch_ctx):
        client = patch_ctx.gql_client
        config = self.config.copy()
        if self.staging_db:
            config['stagingDatabase'] = self.staging_db
        mut = client.prepare_mutation(self.connector_spec.mutation_name, input=config)
        return mut.execute()
