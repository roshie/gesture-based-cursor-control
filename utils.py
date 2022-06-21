import os, sys

def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and set the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)