import curses

from termfm.core.ui import create_curses_win
from termfm.types import App


class Cmdline:
    def __init__(self, app: App) -> None:
        self.id = "cmdline"
        self.app: App = app
        self.win: curses.window = create_curses_win(app.stdscr, self.id)
        pass

    def render(self):
        self.win.refresh()
