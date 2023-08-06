from pathlib import Path

import pandas as pd  # noqa pandas comes with geopandas


def _remove_dir_recursively(dir_path: Path) -> None:
    for child in dir_path.glob("*"):
        if child.is_file():
            child.unlink()
        else:
            _remove_dir_recursively(dir_path=child)
    dir_path.rmdir()
