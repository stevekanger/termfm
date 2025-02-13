from typing import TypedDict
import curses

from termfm.core.cmdline import cmdline_renderer
from termfm.core.panels import (
    get_active_panel,
    panel_renderer,
    switch_active_panel,
)
from termfm.core.utils import debug
from termfm.types import Cmdline, ModeFn, App, Panel, Statusline, Ui


class ModeMap(TypedDict):
    panel: ModeFn
    statusline: ModeFn
    cmd: ModeFn


def panel_mode(
    keycode: int,
    ui: Ui,
    app: App,
    lpanel: Panel,
    rpanel: Panel,
    statusline: Statusline,
    cmdline: Cmdline,
) -> None:
    if chr(keycode) == "j":
        get_active_panel(lpanel, rpanel).increase_current_idx()
    elif chr(keycode) == "k":
        get_active_panel(lpanel, rpanel).decrease_current_idx()
    elif chr(keycode) == "\t":
        switch_active_panel(lpanel, rpanel)
        app.set_focus(get_active_panel(lpanel, rpanel).id)
    elif chr(keycode) == "h":
        get_active_panel(lpanel, rpanel).go_out()
    elif chr(keycode) == "l":
        get_active_panel(lpanel, rpanel).go_in()
    elif chr(keycode) == "q":
        app.exit_code = 1
    elif chr(keycode) == ":":
        app.set_mode("cmd")
        app.set_focus("cmdline")
        ui.cmdline.render(cmdline_renderer(cmdline, True))
    elif chr(keycode) == 103:
        pass
    elif keycode == curses.KEY_MOUSE:
        mouse_event = curses.getmouse()
        _, x, y, _, bstate = mouse_event

        if bstate & curses.BUTTON4_PRESSED:
            get_active_panel(lpanel, rpanel).decrease_current_idx()
        elif bstate & curses.BUTTON5_PRESSED:
            get_active_panel(lpanel, rpanel).increase_current_idx()
        elif bstate & curses.BUTTON1_PRESSED:
            debug(
                curses.COLORS,
                x,
                y,
                curses.BUTTON1_CLICKED,
                curses.BUTTON2_CLICKED,
                curses.BUTTON3_CLICKED,
            )

    ui.lpanel.render(panel_renderer(lpanel))
    ui.rpanel.render(panel_renderer(rpanel))


def cmd_mode(
    keycode: int,
    ui: Ui,
    app: App,
    lpanel: Panel,
    rpanel: Panel,
    statusline: Statusline,
    cmdline: Cmdline,
) -> None:
    if keycode == 27:
        app.set_mode("panel")
        app.set_focus(get_active_panel(lpanel, rpanel).id)
        ui.cmdline.render(cmdline_renderer(cmdline, False))
    elif keycode == 10:
        debug(cmdline.input.get_text())
        pass
    elif keycode == 263:
        cmdline.input.remove_char()
    elif keycode == 260:
        cmdline.input.decrease_cursor_pos()
    elif keycode == 261:
        cmdline.input.increase_cursor_pos()
    else:
        cmdline.input.add_char(chr(keycode))

    ui.cmdline.render(cmdline_renderer(cmdline, app.has_focus("cmdline")))


def statusline_mode(
    keycode: int,
    ui: Ui,
    app: App,
    lpanel: Panel,
    rpanel: Panel,
    statusline: Statusline,
    cmdline: Cmdline,
) -> None:
    return


modemap: ModeMap = {
    "panel": panel_mode,
    "statusline": statusline_mode,
    "cmd": cmd_mode,
}
