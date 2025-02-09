import curses
import os
import subprocess
from typing import List
from pathlib import Path

from termfm.core.ui import create_curses_win, create_ui_map
from termfm.types import (
    PanelHistoryState,
    PanelHistory,
    PanelId,
    PanelItems,
    PanelItem,
    App,
)
from termfm.core.colors import color_pair
from termfm.core.utils import debug, truncate_with_ellipsis


class Panel:
    def __init__(self, app: App, id: PanelId) -> None:
        dir = get_dir_from_config(id)
        self.id: PanelId = id
        self.app = app
        self.win: curses.window = create_curses_win(app.stdscr, id)
        self.dir = dir
        self.items: PanelItems = self.get_items()
        self.items_len = len(self.items)
        self.current_idx: int = 0
        self.scroll_offset: int = 0
        self.history: PanelHistory = []

    def is_active(self):
        return self.app.active_panel == self

    def resize(self):
        self.win = create_curses_win(self.app.stdscr, self.id)
        self.render()

    def render(self):
        self.win.clear()
        self.set_border()
        self.render_panel_meta()
        self.render_items()
        self.win.refresh()

    def render_panel_meta(self):
        height, width = self.win.getmaxyx()
        self.win.addstr(0, 2, self.dir)
        idx_str = "0" if not self.items_len else str(self.current_idx + 1)
        total_items = str(self.items_len)
        count_str = idx_str + "/" + total_items + " items"
        count_str_len = len(count_str)
        x = (width - 2) - count_str_len
        self.win.addstr(height - 1, x, count_str)

    def render_items(self):
        height, width = self.win.getmaxyx()
        height = height - 2
        width = width - 4

        if (
            self.current_idx >= self.scroll_offset + height
            and self.scroll_offset + height < len(self.items)
        ):
            self.scroll_offset += 1
        elif self.current_idx < self.scroll_offset and self.scroll_offset > 0:
            self.scroll_offset -= 1

        visible_items = self.items[self.scroll_offset : self.scroll_offset + height]

        for index, item in enumerate(visible_items):
            self.render_item_name(index, item, width)
            self.render_item_icon(index, item)

    def render_item_name(self, index: int, item: PanelItem, max_len: int):
        name = fill_empty_with_spaces(
            truncate_with_ellipsis(item["name"], max_len), max_len
        )
        if self.scroll_offset + index == self.current_idx and self.is_active():
            self.win.addstr(index + 1, 3, name, color_pair("current"))
        else:
            self.win.addstr(index + 1, 3, name)

    def render_item_icon(self, index: int, item: PanelItem):
        if item["is_dir"]:
            self.win.addstr(index + 1, 1, "\U0000f07b ", color_pair("icon_folder"))
        else:
            self.win.addstr(index + 1, 1, "\U0000f016 ", color_pair("icon_file"))

    def set_border(self):
        color = (
            color_pair("borders_active") if self.is_active() else color_pair("borders")
        )
        self.win.attron(color)
        self.win.border()
        self.win.attroff(color)

    def decrease_current_idx(self):
        self.current_idx = max(0, self.current_idx - 1)

    def increase_current_idx(self):
        self.current_idx = min(self.items_len - 1, self.current_idx + 1)

    def get_items(self) -> PanelItems:
        dir_content = get_dir_content(self.dir)

        def map_items(item: str) -> PanelItem:
            return create_panel_item(item, self.dir)

        items = sorted(
            list(map(map_items, dir_content)),
            key=lambda item: (not item["is_dir"], item["name"]),
        )
        self.items_len = len(items)
        return items

    def get_current_item(self) -> PanelItem | None:
        if not self.items_len:
            return None
        return self.items[self.current_idx]

    def go_in(self):
        item = self.get_current_item()
        if not item:
            return

        if item["is_dir"]:
            self.history_append()
            self.current_idx = 0
            self.scroll_offset = 0
            self.change_dir(item["fullpath"])
        else:
            subprocess.run(["xdg-open", item["fullpath"]], check=False)

    def go_out(self):
        path = Path(self.dir)
        parent = str(path.parent)
        if not parent or parent == self.dir:
            return

        prev_history_state = self.history_pop()
        if prev_history_state and prev_history_state["dir"] == parent:
            self.current_idx = prev_history_state["current_idx"]
            self.scroll_offset = prev_history_state["scroll_offset"]
        else:
            self.current_idx = 0
            self.scroll_offset = 0

        self.change_dir(parent)

    def change_dir(self, dir):
        if not dir or dir == self.dir:
            return

        self.dir = dir
        self.items = self.get_items()
        self.render()

    def history_pop(self) -> PanelHistoryState | None:
        if not len(self.history):
            return None

        return self.history.pop()

    def history_append(self):
        state = create_panel_history_state(
            self.dir, self.current_idx, self.scroll_offset
        )
        self.history.append(state)


# Utility functions
#
# Helper functions for the class
# These help with the class but don't modify any state
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

    return {
        "name": item_name,
        "fullpath": fullpath,
        "is_hidden": is_hidden,
        "is_dir": is_dir,
    }


def create_panel_history_state(
    dir: str, current_idx: int, scroll_offset: int
) -> PanelHistoryState:
    return {"dir": dir, "current_idx": current_idx, "scroll_offset": scroll_offset}
