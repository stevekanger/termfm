from typing import TYPE_CHECKING, List, Literal, Callable, TypeAlias, TypedDict

if TYPE_CHECKING:
    from termfm.core.App import App as AppClass
    from termfm.core.Panel import Panel as PanelClass
    from termfm.core.Statusline import Statusline as StatuslineClass
    from termfm.core.Cmdline import Cmdline as CmdlineClass

App: TypeAlias = "AppClass"
Panel: TypeAlias = "PanelClass"
Statusline: TypeAlias = "StatuslineClass"
Cmdline: TypeAlias = "CmdlineClass"

UiWindows = Literal["lpanel", "rpanel", "statusline", "cmdline"]

ColorPairs = Literal[
    "normal",
    "statusline",
    "borders",
    "borders_active",
    "selected",
    "current",
    "icon_folder",
    "icon_file",
    "cursor",
]

ModeTypes = Literal["panel", "prompt", "statusline", "search"]

ModeFn = Callable[[int, App], None]

PanelId = Literal["lpanel", "rpanel"]

PanelItemType = Literal[
    "directory",
    "file",
]


class PanelItem(TypedDict):
    name: str
    fullpath: str
    is_hidden: bool
    is_dir: bool


PanelItems = List[PanelItem]


class PanelHistoryState(TypedDict):
    dir: str
    current_idx: int
    scroll_offset: int


PanelHistory = List[PanelHistoryState]
