import argparse
import inspect
import os
import json
import threading


def truncate_str(s: str, max_length: int):
    return s[:max_length] if len(s) > max_length else s


def truncate_str_from_end(s: str, max_length: int):
    return s[-max_length:] if len(s) > max_length else s


def truncate_with_ellipsis(s: str, max_length: int):
    return (s[: max_length - 3] + "...") if len(s) > max_length else s


def create_args():
    parser = argparse.ArgumentParser(
        description="TermFm - A terminal based file manager"
    )
    # parser.add_argument("-arg1", type=str, help="Description for arg")
    args = parser.parse_args()

    return args


def debounce(func, delay=0.2):
    timer = None

    def debounced(*args, **kwargs):
        nonlocal timer
        if timer:
            timer.cancel()
        timer = threading.Timer(delay, func, args, kwargs)
        timer.start()

    return debounced


def debug(*items):
    logFile = os.path.join(os.getcwd(), "debug.log")
    frame = inspect.currentframe()

    if frame and frame.f_back:
        frameinfo = inspect.getframeinfo(frame.f_back)
        linenumber = frameinfo.lineno
        filename = os.path.basename(frameinfo.filename)
    else:
        filename, linenumber = "Unknown", "Unknown"

    with open(logFile, "a") as debugFile:
        debugFile.write(f"[{filename}:{linenumber}]:")
        if debugFile:
            for item in items:
                debugFile.write(" ")
                json.dump(log_item_serialize(item), debugFile, indent=4)
        debugFile.write("\n")


# A little help  from chatgpt for this one
def log_item_serialize(obj, seen=None):
    if seen is None:
        seen = set()  # Prevent infinite recursion on cyclic references

    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    if isinstance(obj, list):
        return [
            log_item_serialize(item, seen) for item in obj
        ]  # Recursively serialize lists
    if isinstance(obj, dict):
        return {
            key: log_item_serialize(value, seen) for key, value in obj.items()
        }  # Serialize dict values
    if hasattr(obj, "__dict__") or hasattr(obj, "__class__"):
        if id(obj) in seen:
            return f"<Circular Reference: {obj.__class__.__name__}>"
        seen.add(id(obj))

        return {
            "class_name": obj.__class__.__name__,
            "attributes": {
                key: log_item_serialize(value, seen)  # Recursively serialize attributes
                for key, value in {
                    **getattr(obj, "__dict__", {}),
                    **vars(obj.__class__),
                }.items()
                if not callable(value) and not key.startswith("__")
            },
            "methods": [
                method
                for method in dir(obj)
                if callable(getattr(obj, method)) and not method.startswith("__")
            ],
        }
    return str(obj)
