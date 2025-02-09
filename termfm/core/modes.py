from typing import TypedDict
import curses

from termfm.core.utils import debug
from termfm.types import ModeFn, ModeTypes, App


class ModeMap(TypedDict):
    panel: ModeFn
    cmd: ModeFn
    statusline: ModeFn
    popup: ModeFn
    search: ModeFn


def panel_mode(keycode: int, app: App) -> None:
    if keycode == 106:
        app.active_panel.increase_curent_idx()
    elif keycode == 107:
        app.active_panel.decrease_current_idx()
    elif keycode == 9:
        app.switch_active_panel()
    elif keycode == 104:
        app.active_panel.go_out()
    elif keycode == 108:
        app.active_panel.go_in()
    elif keycode == 113:
        app.exit_code = 1
    elif keycode == curses.KEY_RESIZE:
        pass

    elif keycode == curses.KEY_MOUSE:
        _, x, y, _, _ = curses.getmouse()

        # debug(
        #     curses.COLORS,
        #     x,
        #     y,
        #     curses.BUTTON1_CLICKED,
        #     curses.BUTTON2_CLICKED,
        #     curses.BUTTON3_CLICKED,
        # )

    app.lpanel.render()
    app.rpanel.render()


def cmd_mode(keycode: int, app: App) -> None:
    return


def statusline_mode(keycode: int, app: App) -> None:
    return


def popup_mode(keycode: int, app: App) -> None:
    return


def search_mode(keycode: int, app: App) -> None:
    return


modemap: dict[ModeTypes, ModeFn] = {
    "panel": panel_mode,
    "cmd": cmd_mode,
    "statusline": statusline_mode,
    "popup": popup_mode,
    "search": search_mode,
}
