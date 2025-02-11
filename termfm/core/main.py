import curses
import os

from termfm.core.App import App
from termfm.core.modes import modemap
from termfm.core.ui import init_ui


def main() -> None:
    os.environ.setdefault("ESCDELAY", "25")
    curses.wrapper(init)


def init(stdscr: curses.window) -> None:
    init_ui(stdscr)

    app = App(stdscr)
    app.lpanel.render()
    app.rpanel.render()
    app.statusline.render()
    app.promptline.render()

    run(app)


def run(app: App) -> None:
    while app.exit_code == 0:
        keycode = app.stdscr.getch()
        modemap[app.mode](keycode, app)
