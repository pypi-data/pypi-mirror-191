import click
from pathlib import Path
from . import func
import json
from click import echo, style
from typing import Optional


def load_dir_to_ext_dict(json_path: Optional[Path], src_dir: Path) -> dict[Path, list[str]]:
    if json_path is None:
        mapping = func.get_default_file_mapping()
    else:
        try:
            mapping = func.parse_mapping(json_path)
        except json.JSONDecodeError as e:
            msg = "json file contains syntax errors"
            raise click.ClickException(msg) from e

    path_to_ext = func.create_path_to_ext(src_dir, mapping)

    try:
        for directory in path_to_ext:
            func.normalize_dir(directory)
    except (ValueError, NotADirectoryError) as e:
        raise click.ClickException(str(e)) from e
    return path_to_ext


def print_report(directory: Path, data: func.ReportData):
    total_moved = sum(data.count.values())
    total_deleted = len(data.duplicates)
    total_ignored = len(data.ignored)

    echo(style(f"Organized {directory}", bold=True))
    echo(style(f"{total_moved} files ", bold=True) + style("moved", bold=True, fg="blue"))
    echo(style(f"{total_deleted} files ", bold=True) + style("deleted", bold=True, fg="red"))
    echo(style(f"{total_ignored} files ignored", bold=True))
    echo("")
    echo(style("Moved files per directory", bold=True))
    for subdir, count in data.count.items():
        echo(style(f"{subdir}: {count} files"))
    if total_deleted:
        echo("Duplicate files:")
        for src, dst in data.duplicates:
            echo(
                style(f"{src}", bold=True, fg="red")
                + "\t"
                + style(f"{dst}", bold=True, fg="blue")
            )
    echo("")
    echo(style("✨ All Done! ✨", bold=True))


@click.command()
@click.argument(
    "directory",
    type=click.Path(path_type=Path, exists=True, file_okay=False, writable=True),
    default=Path.cwd(),
)
@click.option(
    "--delete-duplicates", "-d", is_flag=True, help="Enables deletion of duplicates."
)
@click.option(
    "--json-file",
    type=click.Path(exists=True, path_type=Path, dir_okay=False),
    default=None,
    help="path to a JSON file with mappings from directory to file extensions.",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    prompt="Confirm sort directory",
    help="proceed without confirmation.",
)
@click.option("--silent", "-s", is_flag=True, help="Run in silent mode.")
def app(directory, delete_duplicates, json_file, silent, force):
    """
    Sort files in DIRECTORY (current directory by default) into subdirectories
    based on file extensions.

    By default, the following subdirectories are created:

    \b
    audio:      flac, mp3, ogg, wav
    documents:  docx, pdf, pptx, xlsx
    misc:       7z, deb, exe, rar, zip
    pictures:   gif, jpg, png, svg, webp
    videos:     mkv, mov, mp4, webm

    Optionally,  duplicate files in DIRECTORY and within subdirectories are detected
    and deleted. Duplicates are searched only within files with the same name. If
    duplicate detection is disabled, files with the same name are renamed
    appending a suffix. Otherwise, files with the same name are compared, and if
    their, content is the same, the file in DIRECTORY is deleted.

    """
    if force:
        path_to_ext = load_dir_to_ext_dict(json_file, directory)
        data = func.organize_directory(directory, path_to_ext, delete_duplicates)
        if not silent:
            print_report(directory, data)
