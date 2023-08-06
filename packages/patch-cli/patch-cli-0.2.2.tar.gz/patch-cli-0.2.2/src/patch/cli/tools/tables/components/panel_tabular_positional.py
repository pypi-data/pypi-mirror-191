import dataclasses
from patch.cli.tools.tables.components.panel_tabular_positional_hierarchy import PanelTabularPositionalHierarchy


class PanelTabularPositional(PanelTabularPositionalHierarchy):

    def remove_current_row(self):
        row = None
        if self.cursor.current_row is not None and self.cursor.current_row <= self.visible_rows_count() - 1:
            candidate = self.viewport.row_entry(self.cursor.current_row)
            if candidate:
                candidate.is_visible = False
                row = dataclasses.replace(candidate, is_visible=True)
        if row and self.cursor.current_row == self.visible_rows_count() - 1:
            self.move_up()
        self.refresh()
        return row

    def append_row(self, row):
        now_candidate = dataclasses.replace(row, is_visible=False)
        for t in self.rows:
            if t == now_candidate:
                t.is_visible = True
                self.refresh()
