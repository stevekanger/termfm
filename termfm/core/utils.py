import argparse
import inspect
import os
import json


def truncate_str(s, max_length):
    return s[:max_length] if len(s) > max_length else s


def truncate_with_ellipsis(s, max_length):
    return (s[: max_length - 3] + "...") if len(s) > max_length else s


def create_args():
    parser = argparse.ArgumentParser(
        description="TermFm - A terminal based file manager"
    )
    # parser.add_argument("--station", type=str, help="Radio station URL")
    # parser.add_argument("--volume", type=int, help="Set volume level (0-100)", default=50)
    args = parser.parse_args()

    return args


def debug(*items):
    logFile = "/mnt/Storage/Development/Projects/termfm/debug.log"
    frame = inspect.currentframe()

    if frame and frame.f_back:
        frameinfo = inspect.getframeinfo(frame.f_back)
        linenumber = frameinfo.lineno
        filename = os.path.basename(frameinfo.filename)
    else:
        filename, linenumber = "Unknown", "Unknown"

    with open(logFile, "a") as debugFile:
        debugFile.write(f"[{filename}:{linenumber}]: ")
        if debugFile:
            for item in items:
                if isinstance(item, (dict, list, tuple)):
                    json.dump(item, debugFile, indent=4)
                else:
                    debugFile.write(f"{item} ")
        debugFile.write("\n")
