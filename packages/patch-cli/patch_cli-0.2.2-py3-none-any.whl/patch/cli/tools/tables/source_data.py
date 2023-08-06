from dataclasses import dataclass
from typing import List

from patch.cli.tools.tables.rows.table_data_row import TableDataRow


@dataclass
class SourceData:
    quota: int
    quota_used: int
    tables: List[TableDataRow]
    selected_tables : List[TableDataRow]
    is_ready: bool


@dataclass
class SourceMeta:
    source_data: SourceData

