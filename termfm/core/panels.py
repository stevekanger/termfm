import curses
import os
import subprocess
from dataclasses import dataclass
from typing import List
from pathlib import Path

from termfm.core.colors import color_pair
from termfm.core.utils import debug, truncate_with_ellipsis
from termfm.types import (
    PanelId,
    UiRenderer,
    UiResizer,
)


@dataclass
class PanelHistoryState:
    dir: str
    current_idx: int
    scroll_offset: int


@dataclass
class PanelItem:
    name: str
    fullpath: str
    is_hidden: bool
    is_dir: bool


class PanelItems:
    def __init__(self, dir: str) -> None:
        self.items: List[PanelItem] = []
        self.len: int = 0
        self.set_items(dir)

    def set_items(self, dir: str):
        dir_content = get_dir_content(dir)

        def map_items(item: str) -> PanelItem:
            return create_panel_item(item, dir)

        items = sorted(
            list(map(map_items, dir_content)),
            key=lambda item: (not item.is_dir, item.name),
        )
        self.len = len(items)
        self.items = items

    def get_items(self) -> List[PanelItem]:
        return self.items

    def get_item(self, idx: int) -> PanelItem:
        return self.items[idx]

    def get_len(self):
        return self.len


class PanelHistory:
    def __init__(self) -> None:
        self.items: List[PanelHistoryState] = []

    def pop(self) -> PanelHistoryState | None:
        if not len(self.items):
            return None

        return self.items.pop()

    def append(self, dir: str, current_idx: int, scroll_offset: int):
        state = PanelHistoryState(
            dir=dir, current_idx=current_idx, scroll_offset=scroll_offset
        )
        self.items.append(state)


class Panel:
    def __init__(self, id: PanelId, is_active: bool) -> None:
        dir = get_dir_from_config(id)
        self.id: PanelId = id
        self.dir = dir
        self.is_active: bool = is_active
        self.current_idx: int = 0
        self.scroll_offset: int = 0
        self.history: PanelHistory = PanelHistory()
        self.items: PanelItems = PanelItems(self.dir)

    def increase_current_idx(self):
        self.current_idx = min(self.items.get_len() - 1, self.current_idx + 1)

    def decrease_current_idx(self):
        self.current_idx = max(0, self.current_idx - 1)

    def go_in(self):
        item = self.items.get_item(self.current_idx)
        if not item:
            return

        if item.is_dir:
            self.history.append(self.dir, self.current_idx, self.scroll_offset)
            self.current_idx = 0
            self.scroll_offset = 0
            self.change_dir(item.fullpath)
        else:
            subprocess.run(["xdg-open", item.fullpath], check=False)

    def go_out(self):
        path = Path(self.dir)
        parent = str(path.parent)
        if not parent or parent == self.dir:
            return

        prev_history_state = self.history.pop()
        if prev_history_state and prev_history_state.dir == parent:
            self.current_idx = prev_history_state.current_idx
            self.scroll_offset = prev_history_state.scroll_offset
        else:
            self.current_idx = 0
            self.scroll_offset = 0

        self.change_dir(parent)

    def change_dir(self, dir):
        if not dir or dir == self.dir:
            return

        self.dir = dir
        self.items.set_items(dir)


# Render And Resize functions
#
# These functions are passed to the UiElement as the resizer and renderer
# They render the content to the available curses window


def panel_resizer(panel: Panel) -> UiResizer:
    def resizer(win: curses.window):
        panel_renderer(panel)(win)

    return resizer


def panel_renderer(panel: Panel) -> UiRenderer:
    def renderer(win: curses.window):
        render_border(win, panel.is_active)
        render_panel_dir_name(win, panel.dir)
        render_panel_item_count(win, panel)
        render_panel_items(win, panel)

    return renderer


def render_border(win: curses.window, is_active: bool):
    color = color_pair("borders_active") if is_active else color_pair("borders")
    win.attron(color)
    win.border()
    win.attroff(color)


def render_panel_dir_name(win: curses.window, dir: str):
    _, width = win.getmaxyx()
    win.addstr(0, 2, truncate_with_ellipsis(dir, width - 4))


def render_panel_item_count(win: curses.window, panel: Panel):
    height, width = win.getmaxyx()
    items_len = panel.items.get_len()
    current_idx = panel.current_idx

    idx_str = "0" if not items_len else str(current_idx + 1)
    total_items = str(items_len)
    count_str = idx_str + " of " + total_items
    count_str_len = len(count_str)
    y = height - 1
    x = (width - 2) - count_str_len
    win.addstr(y, x, count_str)


def render_panel_items(win: curses.window, panel: Panel):
    height, width = win.getmaxyx()
    height = height - 2
    width = width - 4

    if (
        panel.current_idx >= panel.scroll_offset + height
        and panel.scroll_offset + height < panel.items.len
    ):
        panel.scroll_offset += 1
    elif panel.current_idx < panel.scroll_offset and panel.scroll_offset > 0:
        panel.scroll_offset -= 1

    visible_items = panel.items.get_items()[
        panel.scroll_offset : panel.scroll_offset + height
    ]

    for index, item in enumerate(visible_items):
        render_item_name(win, panel, index, item, width)
        render_item_icon(win, index, item)


def render_item_name(
    win: curses.window,
    panel: Panel,
    index: int,
    item: PanelItem,
    max_len: int,
):
    current_idx = panel.current_idx
    scroll_offset = panel.scroll_offset
    icon_width = 2
    y = index + 1
    x = icon_width + 1
    name = fill_empty_with_spaces(truncate_with_ellipsis(item.name, max_len), max_len)
    if scroll_offset + index == current_idx and panel.is_active:
        win.addstr(y, x, name, color_pair("current"))
    else:
        win.addstr(y, x, name)


def render_item_icon(win: curses.window, index: int, item: PanelItem):
    y = index + 1
    x = 1
    if item.is_dir:
        win.addstr(y, x, "\U0000f07b ", color_pair("icon_folder"))
    else:
        win.addstr(y, x, "\U0000f016 ", color_pair("icon_file"))


# Helper functions
#
# These help with the class but don't directly modify any state
def switch_active_panel(lpanel: Panel, rpanel: Panel):
    lpanel.is_active = not lpanel.is_active
    rpanel.is_active = not rpanel.is_active


def get_active_panel(lpanel: Panel, rpanel: Panel) -> Panel:
    return lpanel if lpanel.is_active else rpanel


def get_dir_content(dir) -> List[str]:
    try:
        return os.listdir(dir)
    except PermissionError:
        return []


def get_dir_from_config(id: PanelId):
    home_path = str(Path("~").expanduser())

    return home_path if id == "lpanel" else "/mnt/Storage"


def fill_empty_with_spaces(s: str, max_width: int):
    strlen = len(s)
    if strlen >= max_width:
        return s

    diff = max_width - strlen

    return s + (" " * diff)


def create_panel_item(item_name: str, dir: str) -> PanelItem:
    if dir == "/":
        fullpath = "/" + item_name
    else:
        fullpath = dir + "/" + item_name

    path = Path(fullpath)

    is_hidden = item_name[0] == "."
    is_dir = path.is_dir()

    return PanelItem(
        name=item_name, fullpath=fullpath, is_hidden=is_hidden, is_dir=is_dir
    )
