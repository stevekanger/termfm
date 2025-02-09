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
        app.active_panel.increase_current_idx()
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
        app.stdscr.clear()
        app.stdscr.refresh()
        app.lpanel.resize()
        app.rpanel.resize()
        app.statusline.resize()
        app.cmdline.resize()
    elif keycode == 103:
        pass
    elif keycode == curses.KEY_MOUSE:
        mouse_event = curses.getmouse()
        _, x, y, _, bstate = mouse_event

        if bstate & curses.BUTTON4_PRESSED:
            app.active_panel.decrease_current_idx()
        elif bstate & curses.BUTTON5_PRESSED:
            app.active_panel.increase_current_idx()
        elif bstate & curses.BUTTON1_PRESSED:
            debug(
                curses.COLORS,
                x,
                y,
                curses.BUTTON1_CLICKED,
                curses.BUTTON2_CLICKED,
                curses.BUTTON3_CLICKED,
            )

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
