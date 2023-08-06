from textual.keys import Keys


class StateManager:

    def __init__(self, app,
                 panel_search, panel_summary, panel_quota,
                 all_tables, selected_tables, primary_keys, row_coll_quota):
        self.app = app
        self.panel_search = panel_search
        self.panel_summary = panel_summary
        self.panel_quota = panel_quota
        self.all_tables = all_tables
        self.selected_tables = selected_tables
        self.primary_keys = primary_keys
        self.row_coll_quota = row_coll_quota
        self.panels = [self.all_tables, self.selected_tables, self.primary_keys]

    async def initialize(self):
        self.selected_tables.set_sub_panels(self.primary_keys, self.panel_summary, self.panel_quota)

    def panel_with_control(self):
        for idx, panel in enumerate(self.panels):
            if panel.has_control():
                return idx, panel
        return None, None

    def get_ranges_to_check(self, ctrl_idx, circular: bool, direction):
        """
        Returns a list of indexes of `self.panels` that should be checked for the next panel to gain focus.
        - For arrows <- and -> we search only panels on the left and right respectively.
        - For `tab` and `shift-tab, we search in circle (`tab` in the last column, means jumping to the first column).

        :param ctrl_idx: the index of the panel that has current focus. If none of panels has focus
                we behave like the first (the most on the left) panel has the focus.
        :param circular: whether we search in circle or just only to the left/right.
        :param direction: `1` means we search to the right, `-1` means we search to the left.
        :return: list of indexes than we should search for the panel that get the focus.
        """
        panels_count = len(self.panels)
        if ctrl_idx is None:
            ctrl_idx = 0
        if circular:
            check_count = panels_count - 1
        else:
            if direction == -1:
                check_count = ctrl_idx
            else:
                check_count = panels_count - ctrl_idx - 1
        idx = ctrl_idx + direction
        checks = []
        for _ in range(check_count):
            checks.append(idx % panels_count)
            idx += direction
        return checks

    def find_left(self, ctrl_idx, ctrl, circular: bool = False):
        return self.find_bi_dir(ctrl_idx, ctrl, circular, -1)

    def find_right(self, ctrl_idx, ctrl, circular: bool = False):
        return self.find_bi_dir(ctrl_idx, ctrl, circular, 1)

    def find_bi_dir(self, ctrl_idx, ctrl, circular: bool, direction: int):
        idx_to_check = self.get_ranges_to_check(ctrl_idx, circular, direction)
        for idx in idx_to_check:
            candidate = self.panels[idx]
            if candidate.can_have_control():
                return ctrl, candidate
        return ctrl, None

    @staticmethod
    def move_control(old, new):
        if new:
            if old:
                old.release_control()
            new.gain_control()

    def input_key(self, key):
        # Keystrokes not in the context of a panel
        if (key.isalnum() and len(key) == 1) or key == 'underscore':
            key_value = key.upper()
            if key == 'underscore':
                key_value = '_'
            self.panel_search.search_text = self.panel_search.search_text + key_value
            self.all_tables.filter = self.panel_search.search_text
            for panel in self.panels:
                panel.release_control(fully=True)
        elif key == Keys.ControlH or key == Keys.Backspace:
            self.panel_search.search_text = self.panel_search.search_text[0:-1]
            self.all_tables.filter = self.panel_search.search_text
            for panel in self.panels:
                panel.release_control(fully=True)
        else:
            # Keystrokes IN the context of a panel, common to all panels
            ctrl_idx, ctrl = self.panel_with_control()

            if key == Keys.Down:
                if not ctrl:
                    self.panels[0].gain_control()
                else:
                    ctrl.move_down()

            elif key == Keys.Up:
                if ctrl:
                    ctrl.move_up()

            elif key == Keys.Right:
                old, new = self.find_right(ctrl_idx, ctrl)
                self.move_control(old, new)

            elif key == Keys.Left:
                old, new = self.find_left(ctrl_idx, ctrl)
                self.move_control(old, new)

            elif key == Keys.Tab or key == Keys.ControlI:
                old, new = self.find_right(ctrl_idx, ctrl, circular=True)
                self.move_control(old, new)

            elif key == Keys.BackTab:
                old, new = self.find_left(ctrl_idx, ctrl, circular=True)
                self.move_control(old, new)

            # Keystrokes IN the context of a panel, that depends on the panel
            elif key == Keys.Enter:
                if ctrl is self.all_tables:
                    row = self.all_tables.remove_current_row()
                    if row:
                        self.selected_tables.append_row(row)
                if ctrl is self.selected_tables:
                    row = self.selected_tables.remove_current_row()
                    if row:
                        self.all_tables.append_row(row)
                if ctrl is self.primary_keys:
                    with self.primary_keys.modify_current_row() as row:
                        row.selected = not row.selected
                    self.selected_tables.refresh()
