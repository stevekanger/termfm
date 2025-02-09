import curses
from typing import Literal

from termfm.core.ui import create_curses_win
from termfm.types import App


class Cmdline:
    def __init__(self, app: App) -> None:
        self.id: Literal["cmdline"] = "cmdline"
        self.app: App = app
        self.win: curses.window = create_curses_win(app.stdscr, self.id)

    def resize(self):
        self.win = create_curses_win(self.app.stdscr, self.id)
        self.render()

    def render(self):
        self.win.refresh()
