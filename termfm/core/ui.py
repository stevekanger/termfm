import curses
from typing import TypedDict

from termfm.types import ColorPairs, UiElementId
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
    promptline: UiMapItem


def init_ui(stdscr: curses.window) -> None:
    init_colors()

    stdscr.clear()
    stdscr.bkgd(" ", color_pair("normal"))
    curses.curs_set(0)
    stdscr.refresh()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)


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


def create_ui_map(stdscr) -> UiMap:
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
        "promptline": {
            "nlines": promptline_height,
            "ncols": width,
            "begin_y": 0,
            "begin_x": panel_height + statusline_height,
            "bkgd": "normal",
        },
    }

    return ui_map
