import curses
from dataclasses import dataclass
from typing import Tuple, TypedDict

from termfm.types import (
    ColorPairs,
    UiElementId,
    UiRenderer,
    UiResizer,
)
from termfm.core.colors import init_colors, color_pair


class UiMapItem(TypedDict):
    nlines: int
    ncols: int
    begin_y: int
    begin_x: int
    bkgd: ColorPairs


class UiMap(TypedDict):
    lpanel: UiMapItem
    rpanel: UiMapItem
    statusline: UiMapItem
    cmdline: UiMapItem


class UiElement:
    def __init__(
        self,
        id: UiElementId,
        stdscr: curses.window,
        win: curses.window,
    ) -> None:
        self.id: UiElementId = id
        self.stdscr: curses.window = stdscr
        self.win: curses.window = win

    def resize(self, resizer: UiResizer):
        self.win.clear()
        self.win.refresh()
        del self.win
        self.win = create_curses_win(self.stdscr, self.id)
        resizer(self.win)
        self.win.refresh()

    def render(self, renderer: UiRenderer):
        self.win.clear()
        self.win.refresh()
        renderer(self.win)
        self.win.refresh()


@dataclass
class Ui:
    stdscr: curses.window
    lpanel: UiElement
    rpanel: UiElement
    statusline: UiElement
    cmdline: UiElement


def init_ui(stdscr: curses.window) -> None:
    init_colors()

    stdscr.clear()
    stdscr.bkgd(" ", color_pair("normal"))
    curses.curs_set(0)
    stdscr.refresh()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)


def create_ui_element_wins(
    stdscr: curses.window,
) -> Tuple[curses.window, curses.window, curses.window, curses.window]:
    lpanel = create_curses_win(stdscr, "lpanel")
    rpanel = create_curses_win(stdscr, "rpanel")
    statusline = create_curses_win(stdscr, "statusline")
    cmdline = create_curses_win(stdscr, "cmdline")

    return (lpanel, rpanel, statusline, cmdline)


def create_curses_win(stdscr: curses.window, id: UiElementId) -> curses.window:
    mapped_item = create_ui_map(stdscr)[id]
    nlines, ncols, begin_y, begin_x, bkgd = (
        mapped_item["nlines"],
        mapped_item["ncols"],
        mapped_item["begin_y"],
        mapped_item["begin_x"],
        mapped_item["bkgd"],
    )

    win = curses.newwin(nlines, ncols, begin_x, begin_y)
    win.bkgd(" ", color_pair(bkgd))
    win.refresh()

    return win


def create_ui_map(stdscr: curses.window) -> UiMap:
    height, width = stdscr.getmaxyx()
    half_width = width // 2
    statusline_height = 1
    promptline_height = 1
    panel_height = height - statusline_height - promptline_height

    ui_map: UiMap = {
        "lpanel": {
            "nlines": panel_height,
            "ncols": half_width,
            "begin_y": 0,
            "begin_x": 0,
            "bkgd": "normal",
        },
        "rpanel": {
            "nlines": panel_height,
            "ncols": half_width,
            "begin_y": half_width,
            "begin_x": 0,
            "bkgd": "normal",
        },
        "statusline": {
            "nlines": statusline_height,
            "ncols": width,
            "begin_y": 0,
            "begin_x": panel_height,
            "bkgd": "statusline",
        },
        "cmdline": {
            "nlines": promptline_height,
            "ncols": width,
            "begin_y": 0,
            "begin_x": panel_height + statusline_height,
            "bkgd": "normal",
        },
    }

    return ui_map
