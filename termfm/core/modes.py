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
    if chr(keycode) == "j":
        app.active_panel.increase_current_idx()
    elif chr(keycode) == "k":
        app.active_panel.decrease_current_idx()
    elif chr(keycode) == "\t":
        app.switch_active_panel()
    elif chr(keycode) == "h":
        app.active_panel.go_out()
    elif chr(keycode) == "l":
        app.active_panel.go_in()
    elif chr(keycode) == "q":
        app.exit_code = 1
    elif chr(keycode) == ":":
        app.switch_mode("input")
        app.promptline.render()
    elif keycode == curses.KEY_RESIZE:
        app.stdscr.clear()
        app.stdscr.refresh()
        app.lpanel.resize()
        app.rpanel.resize()
        app.statusline.resize()
        app.promptline.resize()
    elif chr(keycode) == 103:
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


def input_mode(keycode: int, app: App) -> None:
    if keycode == 27:
        app.switch_mode("panel")
    elif keycode == 10:
        debug(app.promptline.get_input())
    elif keycode == 263:
        app.promptline.remove_char()
    elif keycode == 260:
        app.promptline.decrease_cursor_pos()
    elif keycode == 261:
        app.promptline.increase_cursor_pos()
    else:
        app.promptline.add_char(chr(keycode))

    app.promptline.render()


def statusline_mode(keycode: int, app: App) -> None:
    return


def search_mode(keycode: int, app: App) -> None:
    return


modemap: dict[ModeTypes, ModeFn] = {
    "panel": panel_mode,
    "statusline": statusline_mode,
    "search": search_mode,
    "input": input_mode,
}
