from dircleaner import func
from pathlib import Path
from shutil import copyfile
import pytest
import utils


def create_dummy_data(path: Path, extensions: list[str]) -> list[Path]:
    # create files
    files: list[Path] = list()
    for _ in range(50):
        ext = utils.get_random_extension(extensions)
        file = utils.create_random_filename(path, ext)
        files.append(file)
    return files


def test_organize_directory_moved_files(tmp_path: Path):
    extensions = ["pdf", "txt", "md"]
    files = create_dummy_data(tmp_path, extensions)
    name_to_hash = {x.name: func.compute_sha1_digest(x) for x in files}

    # create subdirectories
    mapping = {"doc": ["pdf"], "text": ["txt", "md"]}
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    for p in path_to_ext:
        func.normalize_dir(p)

    # organize directory
    ext_to_path = func.create_ext_to_path(path_to_ext)
    check_duplicates = False
    func.organize_directory(tmp_path, path_to_ext, check_duplicates)

    for file in files:
        assert not file.exists()
        subdir = ext_to_path[file.suffix.lstrip(".")]
        name = file.name
        dst = tmp_path.joinpath(subdir, name)
        dst_sha1 = func.compute_sha1_digest(dst)
        assert dst_sha1 == name_to_hash[name]


def test_organize_directory_ignored_files(tmp_path: Path):
    # zip is not in the mapping. Zip files should not be moved.
    extensions = ["pdf", "txt", "md", "zip"]
    files = create_dummy_data(tmp_path, extensions)
    name_to_hash = {x.name: func.compute_sha1_digest(x) for x in files}

    # create subdirectories
    mapping = {"doc": ["pdf"], "text": ["txt", "md"]}
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    for p in path_to_ext:
        func.normalize_dir(p)

    # organize directory
    ext_to_path = func.create_ext_to_path(path_to_ext)
    check_duplicates = False
    func.organize_directory(tmp_path, path_to_ext, check_duplicates)

    for file in files:
        ext = file.suffix.lstrip(".")
        name = file.name
        if ext == "zip":
            assert file.exists()
            assert func.compute_sha1_digest(file) == name_to_hash[name]
        else:
            assert not file.exists()
            subdir = ext_to_path[ext]
            dst = tmp_path.joinpath(subdir, name)
            dst_sha1 = func.compute_sha1_digest(dst)
            assert dst_sha1 == name_to_hash[name]


def test_organize_directory_directories(tmp_path: Path):

    # create an empty dir
    existing_dir_path = tmp_path.joinpath("new-dir")
    existing_dir_path.mkdir()

    # test that existing directories are not modified
    extensions = ["pdf", "txt", "md"]
    create_dummy_data(tmp_path, extensions)

    # create subdirectories
    mapping = {"doc": ["pdf"], "text": ["txt", "md"]}
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    for p in path_to_ext:
        func.normalize_dir(p)

    # organize directory
    check_duplicates = False
    func.organize_directory(tmp_path, path_to_ext, check_duplicates)

    # check that the dir has not been moved
    assert existing_dir_path.is_dir()


def test_organize_directory_duplicates_check_duplicates_false(tmp_path: Path):
    # check that duplicate files are moved
    extensions = ["pdf", "txt", "md"]
    files = create_dummy_data(tmp_path, extensions)

    # create subdirectories
    mapping = {"doc": ["pdf"], "text": ["txt", "md"]}
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    ext_to_path = func.create_ext_to_path(path_to_ext)
    for p in path_to_ext:
        func.normalize_dir(p)

    # create a duplicate of a file
    file = files[0]
    file_hash = func.compute_sha1_digest(file)
    duplicate_subdir = ext_to_path[file.suffix.strip(".")]
    duplicate = file.parent.joinpath(duplicate_subdir, file.name)
    copyfile(file, duplicate)

    # organize directory
    check_duplicates = False
    func.organize_directory(tmp_path, path_to_ext, check_duplicates)

    # check duplicated file moved
    file_moved = func.update_stem(duplicate)
    file_moved_hash = func.compute_sha1_digest(file_moved)
    duplicate_hash = func.compute_sha1_digest(duplicate)
    assert file_hash == duplicate_hash
    assert file_hash == file_moved_hash


def test_organize_directory_duplicates_check_duplicates_true(tmp_path: Path):
    # check that duplicates are deleted
    extensions = ["pdf", "txt", "md"]
    files = create_dummy_data(tmp_path, extensions)

    # create subdirectories
    mapping = {"doc": ["pdf"], "text": ["txt", "md"]}
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    ext_to_path = func.create_ext_to_path(path_to_ext)
    for p in path_to_ext:
        func.normalize_dir(p)

    # create a duplicate of a file
    file = files[0]
    file_hash = func.compute_sha1_digest(file)
    duplicate_subdir = ext_to_path[file.suffix.strip(".")]
    duplicate = file.parent.joinpath(duplicate_subdir, file.name)
    copyfile(file, duplicate)

    # organize directory
    check_duplicates = True
    data = func.organize_directory(tmp_path, path_to_ext, check_duplicates)

    # check duplicated file moved
    assert not file.exists()
    duplicate_hash = func.compute_sha1_digest(duplicate)
    assert file_hash == duplicate_hash
    assert data.duplicates[0] == (file, duplicate)


def test_extension_to_dir_valid_dir_to_extension(tmp_path: Path):
    mapping = func.get_default_file_mapping()
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    ext_to_path = func.create_ext_to_path(path_to_ext)
    for ext, path in ext_to_path.items():
        assert isinstance(ext, str)
        assert isinstance(path, Path)


def test_ext_to_dir_repeated_ext(tmp_path: Path):
    mapping = {"doc": ["pdf", "txt", "docx"], "plain-text": ["md", "txt"]}
    path_to_ext = func.create_path_to_ext(tmp_path, mapping)
    with pytest.raises(ValueError):
        func.create_ext_to_path(path_to_ext)


def test_validate_mapping_valid_extensions():
    mapping = {"files": ["jpg", "png", "pdf"]}
    func.validate_mapping(mapping)


def test_validate_mapping_not_a_dict():
    mapping = list()
    with pytest.raises(ValueError):
        func.validate_mapping(mapping)


def test_validate_mapping_extension_is_not_str():
    mapping = {"files": ["jpg", "png", 2]}
    with pytest.raises(ValueError):
        func.validate_mapping(mapping)


def test_validate_mapping_extensions_is_not_list():
    mapping = {"files": "pdf"}
    with pytest.raises(ValueError):
        func.validate_mapping(mapping)


def test_validate_mapping_directory_name_is_not_string_():
    mapping = {3: "pdf"}
    with pytest.raises(ValueError):
        func.validate_mapping(mapping)


def test_validate_directory_valid_directory(tmp_path: Path):
    func.normalize_dir(tmp_path)


def test_validate_directory_non_writable_directory(tmp_path: Path):
    tmp_path.chmod(4)
    with pytest.raises(ValueError):
        func.normalize_dir(tmp_path)
    tmp_path.chmod(6)  # prevents errors while cleaning tmp data


def test_validate_directory_file(tmp_path: Path):
    tmp_file = tmp_path.joinpath("tmp-file")
    tmp_file.touch()
    with pytest.raises(NotADirectoryError):
        func.normalize_dir(tmp_file)


def test_move_file_no_same_filename_on_destination(tmp_path_factory):

    # create a file to move and compute its SHA1
    filename = "file.test"
    src_dir = tmp_path_factory.mktemp("src")
    src = src_dir / filename
    utils.fill_file_with_random_text(src)
    src_sha1 = func.compute_sha1_digest(src)

    # create a destination dir, move the file and compute its SHA1
    dst_dir = tmp_path_factory.mktemp("dst")
    dst, is_unique_file = func.move(src, dst_dir)
    if is_unique_file:
        dst_sha1 = func.compute_sha1_digest(dst)
        assert src_sha1 == dst_sha1
        assert not src.is_file()
        assert dst.is_file()


def test_move_file_same_filename_on_dst_different_content(tmp_path_factory):
    # create a file to move and compute its SHA1
    filename = "file.test"
    src_dir = tmp_path_factory.mktemp("src")
    src = src_dir / filename
    utils.fill_file_with_random_text(src)
    src_sha1 = func.compute_sha1_digest(src)

    # create a file with the same name on destination dir
    dst_dir = tmp_path_factory.mktemp("dst")
    same_filename = dst_dir / filename
    utils.fill_file_with_random_text(same_filename)
    dst, is_unique_file = func.move(src, dst_dir)
    if is_unique_file:
        dst_sha1 = func.compute_sha1_digest(dst)
        expected_dst_stem = src.stem + "-1"

        assert src_sha1 == dst_sha1
        assert not src.is_file()
        assert dst.is_file()
        assert dst.stem == expected_dst_stem


def test_move_file_same_filename_on_dst_same_content_check_duplicates_false(
    tmp_path_factory,
):
    # create a file to move and compute its SHA1
    filename = "file.test"
    src_dir = tmp_path_factory.mktemp("src")
    src = src_dir / filename
    utils.fill_file_with_random_text(src)
    src_sha1 = func.compute_sha1_digest(src)

    # create a file with the same name on destination dir
    dst_dir = tmp_path_factory.mktemp("dst")
    same_filename = dst_dir / filename
    copyfile(src, same_filename)
    dst, is_unique_file = func.move(src, dst_dir)
    if is_unique_file:
        dst_sha1 = func.compute_sha1_digest(dst)
        expected_dst_stem = src.stem + "-1"

        assert src_sha1 == dst_sha1
        assert not src.is_file()
        assert dst.is_file()
        assert dst.stem == expected_dst_stem


def test_move_file_same_filename_on_dst_same_content_check_duplicates_true(
    tmp_path: Path,
):
    # create a file to move and compute its SHA1
    filename = "file.test"
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    src = src_dir / filename
    utils.fill_file_with_random_text(src)
    src_sha1 = func.compute_sha1_digest(src)

    # create a file with the same name and content on destination dir
    dst_dir = tmp_path / "dst"
    dst_dir.mkdir()
    same_filename = dst_dir / filename
    copyfile(src, same_filename)
    dst, is_unique_file = func.move(src, dst_dir, check_duplicates=True)
    dst_sha1 = func.compute_sha1_digest(same_filename)

    assert not is_unique_file
    assert src_sha1 == dst_sha1
    assert not src.is_file()
    assert dst.is_file()
    assert same_filename.stem == src.stem


def test_update_stem_suffix_no_suffix():
    stem = "test"
    renamed_stem = func._update_stem_suffix(stem)
    expected_stem = f"{stem}-1"
    assert expected_stem == renamed_stem


def test_update_stem_suffix_has_suffix():
    stem = "test"
    for k in range(1, 20):
        stem = func._update_stem_suffix(stem)
        expected_stem = f"test-{k}"
        assert stem == expected_stem


def test_update_stem_suffix_has_hyphen():
    stem = "test-1 asdf"
    expected = "test-1 asdf-1"
    renamed_stem = func._update_stem_suffix(stem)
    assert expected == renamed_stem


def test_update_stem(tmp_path: Path):

    filename = "file.test"
    path = tmp_path / filename
    renamed_path = func.update_stem(path)
    expected_renamed_stem = f"{path.stem}-1"
    assert path.parent == renamed_path.parent
    assert renamed_path.stem == expected_renamed_stem
    assert renamed_path.suffix == path.suffix


def test_update_stem_multiple_updates(tmp_path: Path):
    stem = "file"
    suffix = ".test"
    filename = stem + suffix
    path = tmp_path / filename
    for k in range(1, 10):
        path = func.update_stem(path)
        expected_stem = f"{stem}-{k}"
        assert path.stem == expected_stem
        assert path.parent == tmp_path
        assert path.suffix == suffix
