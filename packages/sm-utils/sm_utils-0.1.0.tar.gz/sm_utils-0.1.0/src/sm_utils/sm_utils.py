#region Execution Timer
import timeit

def timer(func: callable) -> callable:
    """Time the execution of a provided delegate function"""
    def wrapped(*args, **kwargs):
        start = timeit.default_timer()
        res = func(*args, **kwargs)
        end = timeit.default_timer()
        delta = end - start

        if delta > 60: ex_time = f"{int(delta // 60)} m : {round(delta % 60, 4)} s"
        elif delta * 1_000_000 < 1: ex_time = f"{round(delta * 1_000_000_000, 4)} ns"
        elif delta * 1_000 < 1: ex_time = f"{round(delta * 1_000_000, 4)} µs"
        elif delta < 1: ex_time = f"{round(delta * 1000, 4)} ms"
        else: ex_time = f"{round(delta, 4)} s"        
        print(f"Execution Time: {ex_time}")

        return res
    return wrapped
#endregion

#region Relative Path Functions
import sys, os, json

"""Default folder for accessing files"""
default_path = None

def root_path() -> str:
    """Return the root execution path of the script"""
    return os.path.dirname(sys.argv[0])

def set_path(folder: str = None) -> str:
    """Set the default folder for accessing files"""
    if folder: return folder
    json_path = os.path.join(root_path(), "sm_utils.json")
    if not os.path.isfile(json_path): return "data"
    with open(os.path.join(root_path(), "sm_utils.json")) as f:
        data = json.load(f)
    global default_path
    default_path = data["default_path"]
    return data["default_path"]

set_path()

def dir_path(folder_path: str = default_path) -> str:
    """Return the specified path under the root directory"""
    if not folder_path: return root_path()
    return os.path.join(root_path(), folder_path)

def file_path(filename: str, folder_path: str = default_path) -> str:
    """Return the specified complete file path"""
    return os.path.join(dir_path(folder_path), filename)
#endregion
