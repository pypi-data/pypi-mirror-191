import hashlib
import json
import os
import re
from dataclasses import dataclass
from filecmp import cmp
from pathlib import Path
from typing import Tuple


@dataclass
class ReportData:
    """
    Container class for data of moved/deleted files after organizing a directory.

    Attributes
        count (dict[str, int]): Number of files moved into each subdirectory.
        duplicates (list[Tuple[Path, Path]]): Duplicates detected.
        ignored (list[Path]): Files ignored after organizing the directory.

    """

    count: dict[str, int]
    duplicates: list[Tuple[Path, Path]]
    ignored: list[Path]


def organize_directory(
    directory: Path, path_to_ext: dict[Path, list[str]], check_duplicates: bool
) -> ReportData:
    """
    Organizes files into subdirectories based on file extension.

    Args:
        directory (Path): Directory to organize.
        path_to_ext (dict[Path, list[str]]): A mapping from subdirectories inside
        `directory` to a list of file extensions.
        check_duplicates (bool): Check duplicates files in `directory`. Duplicates
        are files with the same name in `directory` and the destination subdirectory
        defined by `path_to_ext`. If set to ``True``, the files content are compared
        and if they are the same, the file on `directory` is deleted. If set to
        ``False``, their the duplicate file is renamed appending a numerical suffix.

    Returns:
        DirectoryData: Data of files moved and deleted
    """

    # moved data stats
    move_count = {x.name: 0 for x in path_to_ext}
    duplicates = list()
    ignored = list()

    ext_to_path = create_ext_to_path(path_to_ext)

    for file in directory.glob("*"):
        if file.is_file():
            ext = file.suffix.strip(".").lower()
            dst_dir = ext_to_path.get(ext)
            if dst_dir:
                dst_file, is_unique_file = move(file, dst_dir, check_duplicates)
                if is_unique_file:
                    move_count[dst_dir.name] += 1
                else:
                    duplicates.append((file, dst_file))
            else:
                ignored.append(file)
    return ReportData(move_count, duplicates, ignored)


def parse_mapping(json_path: Path) -> dict[str, list[str]]:
    """
    Parse a JSON file into a dictionary of subdirectory names to a list of file extensions.

    Args:
        json_path (Path): Path to a JSON file.

    Returns:
        dict[str, list[str]]: Mapping of subdirectory names to a list of file extensions.
    """
    with json_path.open() as fin:
        res = json.load(fin)
    validate_mapping(res)
    return res


def validate_mapping(mapping):
    if not isinstance(mapping, dict):
        msg = "mapping must be a dictionary."
        raise ValueError(msg)

    for dir_name, extensions in mapping.items():
        if not isinstance(dir_name, str):
            msg = f"subdirectory names must be strings, got {dir_name}"
            ValueError(msg)

        if isinstance(extensions, list):
            for ext in extensions:
                if not isinstance(ext, str):
                    msg = (
                        f"Invalid mapping: '{ext}' extension for directory "
                        f"'{dir_name}' is not valid."
                    )
                    raise ValueError(msg)
        else:
            msg = (
                f"Invalid mapping: extensions must be organized inside a list. "
                f"Got {extensions} for directory = {dir_name}."
            )
            raise ValueError(msg)


def create_ext_to_path(dir_to_extension: dict[Path, list[str]]) -> dict[str, Path]:
    """
    Creates a dictionary of file extensions to subdirectory paths.

    Args:
        dir_to_extension (dict[Path, list[str]]): A mapping of subdirectory paths
        to a list of extensions, created with _create_path_to_ext

    Raises:
        ValueError: If extensions are listed for multiple subdirectories.

    Returns:
        dict[str, Path]: Mapping from file extension to subdirectory paths.
    """
    res: dict[str, Path] = dict()
    for path, extensions in dir_to_extension.items():
        for ext in extensions:
            if ext in res:
                msg = f"Repeated extension in subdirectories {res[ext].name} and {path.name}"
                raise ValueError(msg)
            res[ext] = path
    return res


def normalize_dir(directory: Path) -> None:
    """
    Checks if a directory exists and it is writable. If the directory does not
    exists it is created.

    Args:
        directory (Path): Directory to check

    Raises:
        ValueError: If the directory exists and it is not writable.
        NotADirectoryError: If a file with the specified name exists.

    """

    # directory always exists, checked when receiving arguments from cli
    if directory.is_dir():
        if not os.access(directory, os.W_OK):
            msg = f"Invalid directory: {directory} is not writable"
            raise ValueError(msg)
    elif directory.is_file():
        msg = f"Invalid directory: {directory} is not a directory."
        raise NotADirectoryError(msg)
    else:
        directory.mkdir()


def get_default_file_mapping() -> dict[str, list[str]]:
    mapping = {
        "documents": ["pdf", "docx", "doc"],
        "pictures": ["jpeg", "jpg", "png"],
        "misc": ["zip", "rar", "7z", "deb", "exe"],
        "text": ["txt", "md", "py"],
    }
    return mapping


def create_path_to_ext(path: Path, mapping: dict[str, list[str]]) -> dict[Path, list[str]]:
    # list set remove duplicate extensions
    return {path.joinpath(k): list(set(v)) for k, v in mapping.items()}


def compute_sha1_digest(path: Path) -> str:
    """
    Computes the SHA1 digest of a file.

    Args:
        path (Path): path to a file

    Returns:
        str: digest in hexadecimal format.

    """

    sha1 = hashlib.sha1()
    BUFFER_SIZE = 64 * 1024
    with path.open("rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)  # loads chunks of 64 kb
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def move(src: Path, dst_dir: Path, check_duplicates: bool = False) -> Tuple[Path, bool]:
    """
    Move a file into a new directory.

    If dst exist, its name is updated until a filename is available to mode src.

    Args:
        src (Path): Path to source file
        dst_dir (Path): destination directory
        check_duplicates (bool): If True, and the destination file exists, the src file
            is deleted.

    Returns:
      Path: New path of the file. If `check_duplicates` is ``True`` and the
        file exists in `dst_dir`, it returns ``None``
      bool: True if a file with the same content exists at `dst_dir`

    """
    dst = dst_dir / (src.stem + src.suffix)

    while dst.is_file() and src.is_file():

        if check_duplicates:
            is_duplicate = cmp(src, dst)
            if is_duplicate:
                src.unlink()
                break

        dst = update_stem(dst)

    is_unique_file = src.is_file()
    if is_unique_file:
        src.rename(dst)
    return dst, is_unique_file


def update_stem(path: Path) -> Path:
    """
    Adds a suffix to the stem of a path if it already exists.

    Prevents overwriting files.

    Args:
        path (Path): file to be renamed

    Returns:
        Path: renamed path

    """
    renamed_stem = _update_stem_suffix(path.stem)
    renamed_path = path.parent.joinpath(renamed_stem + path.suffix)
    return renamed_path


def _update_stem_suffix(stem: str) -> str:
    """
    Updates the suffix in a stem

    Args:
        stem (str): Path stem

    Returns:
        str: renamed stem

    """
    match = re.search("-[0-9]+$", stem)
    if match is None:
        stem = stem + "-1"
    else:
        suffix_start = match.start()
        suffix_end = match.end()
        suffix = int(stem[suffix_start + 1 : suffix_end]) + 1
        stem = f"{stem[:suffix_start]}-{suffix}"
    return stem
