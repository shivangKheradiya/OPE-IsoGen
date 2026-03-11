import os
import importlib.util
import glob

CONFIG_DEFAULT = "symbol_paths.txt"


def load_symbol_modules(config_path=None):
    """
    Reads a text file that contains paths to additional symbol folders.
    Returns imported modules.
    """

    if config_path is None:
        config_path = CONFIG_DEFAULT

    modules = []

    if not os.path.exists(config_path):
        print(f"[Config] No config file found at {config_path}")
        return modules

    with open(config_path, "r") as f:
        paths = [line.strip() for line in f.readlines() if line.strip()]

    for p in paths:
        if not os.path.isdir(p):
            print(f"[Config] Not a folder: {p}")
            continue

        py_files = glob.glob(os.path.join(p, "*.py"))
        for fpath in py_files:
            fname = os.path.basename(fpath)
            modname = fname.replace(".py", "")
            try:
                # Dynamic import — users can debug easily by editing these files
                spec = importlib.util.spec_from_file_location(modname, fpath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules.append(module)
                print(f"[Config] Loaded symbol module: {modname}")
            except Exception as e:
                print(f"[Config] ERROR loading {fpath}: {e}")

    return modules