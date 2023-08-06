"""
Functions used to create test data.

"""

import json
from pathlib import Path
from typing import Optional
from dircleaner.func import get_default_file_mapping
import random
import string


def create_invalid_json_file(path: Path):
    with path.open("wt") as f:
        invalid_json_str = '{"data": ["zip", ]}\n'
        f.write(invalid_json_str)


def create_json_file(path: Path):
    with path.open("wt") as f:
        mappings = get_default_file_mapping()
        json.dump(mappings, f)


def fill_file_with_random_text(path: Path):
    """
    Writes random text into a file.

    Args:
        path (Path): Path to file
    """
    with path.open("wt") as fin:
        s = "".join(random.choices(string.ascii_letters, k=1000))
        fin.write(s)


def create_random_filename(path: Path, ext: str) -> Path:
    """
    Create a random filename, checking that the file does not exists.

    Args:
        path (Path): Path to directory to create the file
        ext (str): extension to append to the filename
    Returns:
        Path:
    """
    while True:
        name = "".join(random.choices(string.ascii_letters, k=12))
        filename = f"{name}.{ext}"
        file_path = path.joinpath(filename)
        if not file_path.exists():
            break
    fill_file_with_random_text(file_path)
    return file_path


def get_random_extension(extensions: Optional[list[str]] = None) -> str:
    if extensions is None:
        extensions = ["txt", "md", "zip", "pdf", "jpg"]
    return random.choice(extensions)
