import curses
from typing import Literal

from termfm.core.colors import color_pair
from termfm.types import UiRenderer, UiResizer


class Statusline:
    def __init__(self) -> None:
        self.id: Literal["statusline"] = "statusline"
        pass


# Render And Resize functions
#
# These functions are passed to the UiElement as the resizer and renderer
# They render the content to the available curses window


def statusline_resizer(statusline: Statusline) -> UiResizer:
    def resizer(win: curses.window):
        statusline_renderer(statusline)(win)

    return resizer


def statusline_renderer(statusline: Statusline) -> UiRenderer:
    def renderer(win: curses.window):
        win.bkgd(" ", color_pair("statusline"))
        win.addstr(0, 1, "Main Menu")
        win.refresh()

    return renderer
