import curses

from termfm.types import ModeTypes
from termfm.core.Panel import Panel
from termfm.core.Statusline import Statusline
from termfm.core.Promptline import Promptline


class App:
    def __init__(
        self,
        stdscr: curses.window,
    ) -> None:
        self.stdscr: curses.window = stdscr
        self.mode: ModeTypes = "panel"
        self.exit_code: int = 0

        self.active_panel: Panel = Panel(self, "lpanel")
        self.lpanel: Panel = self.active_panel
        self.rpanel: Panel = Panel(self, "rpanel")
        self.statusline: Statusline = Statusline(self)
        self.promptline: Promptline = Promptline(self)

    def switch_active_panel(self) -> None:
        self.active_panel = (
            self.lpanel if self.active_panel == self.rpanel else self.rpanel
        )

    def switch_mode(self, mode) -> None:
        self.mode = mode
