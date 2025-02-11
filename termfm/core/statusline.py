import curses
from typing import Literal

from termfm.core.colors import color_pair
from termfm.core.ui import create_curses_win
from termfm.types import App


class Statusline:
    def __init__(self, app: App) -> None:
        self.id: Literal["statusline"] = "statusline"
        self.app: App = app
        self.win: curses.window = create_curses_win(app.stdscr, self.id)
        pass

    def resize(self):
        self.win = create_curses_win(self.app.stdscr, self.id)
        self.render()

    def render(self):
        self.win.bkgd(" ", color_pair("statusline"))
        self.win.addstr(0, 1, "Main Menu")
        self.win.refresh()
        pass
