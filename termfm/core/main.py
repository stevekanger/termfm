import curses
import os

from termfm.core.app import App
from termfm.core.modes import modemap
from termfm.core.ui import Ui, UiElement, create_ui_element_wins, init_ui
from termfm.core.panels import Panel, panel_renderer, panel_resizer
from termfm.core.statusline import Statusline, statusline_renderer, statusline_resizer
from termfm.core.cmdline import Cmdline, cmdline_renderer, cmdline_resizer
from termfm.core.utils import debounce, debug


def main() -> None:
    os.environ.setdefault("ESCDELAY", "25")
    curses.wrapper(init)


def init(stdscr: curses.window) -> None:
    init_ui(stdscr)

    lpanel_win, rpanel_win, statusline_win, cmdline_win = create_ui_element_wins(stdscr)

    ui = Ui(
        stdscr=stdscr,
        lpanel=UiElement("lpanel", stdscr, lpanel_win),
        rpanel=UiElement("rpanel", stdscr, rpanel_win),
        statusline=UiElement("statusline", stdscr, statusline_win),
        cmdline=UiElement("cmdline", stdscr, cmdline_win),
    )

    app = App()
    lpanel = Panel("lpanel", True)
    rpanel = Panel("rpanel", False)
    statusline = Statusline()
    cmdline = Cmdline()

    ui.lpanel.render(panel_renderer(lpanel))
    ui.rpanel.render(panel_renderer(rpanel))
    ui.statusline.render(statusline_renderer(statusline))
    ui.cmdline.render(cmdline_renderer(cmdline, app.has_focus("cmdline")))

    run(ui, app, lpanel, rpanel, statusline, cmdline)


def run(
    ui: Ui,
    app: App,
    lpanel: Panel,
    rpanel: Panel,
    statusline: Statusline,
    cmdline: Cmdline,
) -> None:
    while app.exit_code == 0:
        keycode = ui.stdscr.getch()

        if keycode == curses.KEY_RESIZE:
            ui.stdscr.clear()
            ui.stdscr.refresh()
            ui.lpanel.resize(panel_resizer(lpanel))
            ui.rpanel.resize(panel_resizer(rpanel))
            ui.statusline.resize(statusline_resizer(statusline))
            ui.cmdline.resize(cmdline_resizer(cmdline, app.has_focus("cmdline")))
            continue

        modemap[app.mode](keycode, ui, app, lpanel, rpanel, statusline, cmdline)
