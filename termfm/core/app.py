from termfm.types import ModeTypes, UiElementId


class App:
    def __init__(
        self,
    ) -> None:
        self.mode: ModeTypes = "panel"
        self.exit_code: int = 0
        self.focus: UiElementId = "lpanel"

    def set_mode(self, mode) -> None:
        self.mode = mode

    def set_exit_code(self, code: int) -> None:
        self.exit_code = code

    def set_focus(self, id: UiElementId):
        self.focus = id

    def has_focus(self, id: UiElementId):
        return id == self.focus
