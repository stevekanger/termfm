import curses
from typing import List, Literal

from termfm.core.colors import color_pair
from termfm.core.ui import create_curses_win
from termfm.types import App
from termfm.core.utils import debug


class Inputline:
    def __init__(self, app: App) -> None:
        self.id: Literal["inputline"] = "inputline"
        self.app: App = app
        self.input: List[str] = []
        self.cursor_pos: int = 0
        self.win: curses.window = create_curses_win(app.stdscr, self.id)

    def resize(self):
        self.win = create_curses_win(self.app.stdscr, self.id)
        self.render()

    def input_max_width(self):
        _, width = self.win.getmaxyx()
        return width - 3

    def render(self):
        self.win.clear()
        if self.app.mode != "cmd":
            self.clear()
        else:
            start_range: int = 0
            max_width = self.input_max_width()
            input_len = len(self.input)

            if input_len > max_width:
                start_range = input_len - max_width

            self.win.addstr(0, 0, ":")

            for i in range(start_range, input_len):
                if i == self.cursor_pos:
                    self.win.addstr(
                        0, i - start_range + 1, self.input[i], color_pair("cursor")
                    )
                else:
                    self.win.addstr(0, i - start_range + 1, self.input[i])

            if self.cursor_pos == input_len:
                self.win.addstr(
                    0, self.cursor_pos - start_range + 1, " ", color_pair("cursor")
                )

        self.win.refresh()

    def add_char(self, key: str):
        if not key:
            return
        self.input.insert(self.cursor_pos, key)
        self.increase_cursor_pos()

    def remove_char(self):
        if self.cursor_pos == 0 and not len(self.input):
            self.clear()
        elif self.cursor_pos > 0:
            self.decrease_cursor_pos()
            del self.input[self.cursor_pos]

    def increase_cursor_pos(self):
        self.cursor_pos = min(len(self.input), self.cursor_pos + 1)

    def decrease_cursor_pos(self):
        self.cursor_pos = max(0, self.cursor_pos - 1)

    def clear(self):
        self.input = []
        self.cursor_pos = 0
        self.app.switch_mode("panel")

    def get_input(self):
        return "".join(self.input)
