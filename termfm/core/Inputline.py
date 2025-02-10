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
        self.cursor_pos: int = 1
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
            self.win.addstr(0, 0, ":")
            for i in range(len(self.input)):
                if i + 1 == self.cursor_pos:
                    self.win.addstr(0, i + 1, self.input[i], color_pair("cursor"))
                else:
                    self.win.addstr(0, i + 1, self.input[i])

            if self.cursor_pos > len(self.input):
                self.win.addstr(0, len(self.input) + 1, " ", color_pair("cursor"))

        self.win.refresh()

    def add_char(self, key: str):
        if not key:
            return
        self.input.insert(self.cursor_pos - 1, key)
        self.increase_cursor_pos()

    def remove_char(self):
        input_len = len(self.input)
        if input_len <= 0:
            self.clear()
        else:
            del self.input[self.cursor_pos - 2]
            self.decrease_cursor_pos()

    def increase_cursor_pos(self):
        self.cursor_pos = min(len(self.input) + 1, self.cursor_pos + 1)

    def decrease_cursor_pos(self):
        self.cursor_pos = max(1, self.cursor_pos - 1)

    def clear(self):
        self.input = []
        self.cursor_pos = 1
        self.app.switch_mode("panel")
