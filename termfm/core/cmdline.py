import curses
from typing import List, Literal

from termfm.core.colors import color_pair
from termfm.types import UiRenderer, UiResizer


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


class Cmdline:
    def __init__(self) -> None:
        self.id: Literal["cmdline"] = "cmdline"
        self.input: Input = Input()

    def clear(self):
        self.input.clear()


# Render And Resize functions
#
# These functions are passed to the UiElement as the resizer and renderer
# They render the content to the available curses window


def cmdline_resizer(cmdline: Cmdline, has_focus: bool) -> UiResizer:
    def resizer(win: curses.window):
        cmdline_renderer(cmdline, has_focus)(win)

    return resizer


def cmdline_renderer(cmdline: Cmdline, has_focus: bool) -> UiRenderer:
    def renderer(win: curses.window):
        if not has_focus:
            win.clear()
            cmdline.clear()
            return

        render_input(win, cmdline)

    return renderer


def render_input(win: curses.window, cmdline: Cmdline):
    start_range: int = 0
    _, width = win.getmaxyx()
    max_width = width - 3

    if cmdline.input.len > max_width:
        start_range = cmdline.input.len - max_width

    win.addstr(0, 0, ":")

    for i in range(start_range, cmdline.input.len):
        if i == cmdline.input.cursor_idx:
            win.addstr(
                0, i - start_range + 1, cmdline.input.text[i], color_pair("cursor")
            )
        else:
            win.addstr(0, i - start_range + 1, cmdline.input.text[i])

    if cmdline.input.cursor_idx == cmdline.input.len:
        win.addstr(
            0,
            cmdline.input.cursor_idx - start_range + 1,
            " ",
            color_pair("cursor"),
        )
