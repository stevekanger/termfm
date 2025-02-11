import curses
from typing import List, Literal

from termfm.core.colors import color_pair
from termfm.core.ui import create_curses_win
from termfm.types import App
from termfm.core.utils import debug


class Promptline:
    def __init__(self, app: App) -> None:
        self.id: Literal["promptline"] = "promptline"
        self.app: App = app
        self.win: curses.window = create_curses_win(app.stdscr, self.id)
        self.input: Input = Input()

    def resize(self):
        self.win = create_curses_win(self.app.stdscr, self.id)
        self.render()

    def input_max_width(self):
        _, width = self.win.getmaxyx()
        return width - 3

    def render(self):
        self.win.clear()
        if self.app.mode != "prompt":
            self.input.clear()
            self.win.refresh()
            return

        self.render_input()
        self.win.refresh()

    def render_input(self):
        start_range: int = 0
        max_width = self.input_max_width()

        if self.input.len > max_width:
            start_range = self.input.len - max_width

        self.win.addstr(0, 0, ":")

        for i in range(start_range, self.input.len):
            if i == self.input.cursor_idx:
                self.win.addstr(
                    0, i - start_range + 1, self.input.text[i], color_pair("cursor")
                )
            else:
                self.win.addstr(0, i - start_range + 1, self.input.text[i])

        if self.input.cursor_idx == self.input.len:
            self.win.addstr(
                0,
                self.input.cursor_idx - start_range + 1,
                " ",
                color_pair("cursor"),
            )


class ContextMenu:
    def __init__(self) -> None:
        pass


class CmdPrompt:
    def __init__(self) -> None:
        self.input: Input = Input()
        self.prompt_text: str = ":"


class Input:
    def __init__(self) -> None:
        self.text: List[str] = []
        self.cursor_idx: int = 0
        self.len: int = 0

    def add_char(self, key: str):
        if not key:
            return
        self.text.insert(self.cursor_idx, key)
        self.increase_cursor_pos()
        self.len += 1

    def remove_char(self):
        if self.cursor_idx == 0 and not len(self.text):
            self.clear()
        elif self.cursor_idx > 0:
            self.decrease_cursor_pos()
            del self.text[self.cursor_idx]
            self.len -= 1

    def increase_cursor_pos(self):
        self.cursor_idx = min(len(self.text), self.cursor_idx + 1)

    def decrease_cursor_pos(self):
        self.cursor_idx = max(0, self.cursor_idx - 1)

    def clear(self):
        self.text = []
        self.cursor_idx = 0
        self.len = 0

    def get_text(self):
        return "".join(self.text)
