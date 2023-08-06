from cliriculum.utils import copy_files, copy_resources
import pytest
import os


def test_copy_files(tmp_path, fixtures_path):
    file_ = fixtures_path / "contact.json"
    with pytest.raises(TypeError):
        copy_files(file_, tmp_path)

    copy_files([file_], dst=tmp_path)


def test_copy_resources(tmp_path):
    target_dir = str(tmp_path / "resume")
    with pytest.raises(FileNotFoundError):
        copy_resources(target_dir)
    with open(target_dir, "w") as f:
        f.write("\n")
    with pytest.raises(FileExistsError):
        copy_resources(target_dir)
    os.remove(target_dir)
    os.mkdir(target_dir)
    copy_resources(target_dir)
