import datetime
from pathlib import Path

import pytest

from dropboxignore.commands.update import UpdateCommand
from dropboxignore.enums import IgnoreFile


def test_update_successful(tmp_path: Path):
    gi = tmp_path.joinpath(IgnoreFile.GITIGNORE.value)

    gi.write_text("*.txt")

    di = tmp_path.joinpath(IgnoreFile.DROPBOXIGNORE.value)
    di.touch()

    assert gi.exists()
    assert di.exists()

    cmd = UpdateCommand(path=tmp_path)
    cmd.run_on_item_path(tmp_path)

    assert di.read_text() == (
        f"# ----\n"
        f"# Automatically Generated .dropboxignore file at {{date}}\n"
        f"# ----\n"
        "*.txt"
    ).format(date=datetime.date.today().strftime("%Y-%m-%d"))
    assert cmd.c.updated == 1


def test_update_not_gitignore_file_input(tmp_path: Path):
    gi = tmp_path.joinpath("foo")
    gi.touch()

    cmd = UpdateCommand(path=tmp_path)
    with pytest.raises(
        ValueError, match=f"{IgnoreFile.GITIGNORE.value} does not exists$"
    ):
        cmd.run_on_item_path(tmp_path)

    assert cmd.c.updated == 0


def test_update_gitignore_file_not_exists(tmp_path: Path):
    gi = tmp_path.joinpath(IgnoreFile.GITIGNORE.value)

    assert not gi.exists()

    cmd = UpdateCommand(path=tmp_path)
    with pytest.raises(ValueError, match=f"{gi.name} does not exists$"):
        cmd.run_on_item_path(tmp_path)

    assert cmd.c.updated == 0


def test_update_dropboxignore_file_not_exists(tmp_path: Path):
    gi = tmp_path.joinpath(IgnoreFile.GITIGNORE.value)
    di = tmp_path.joinpath(IgnoreFile.DROPBOXIGNORE.value)

    gi.touch()

    assert gi.exists()
    assert not di.exists()

    cmd = UpdateCommand(path=tmp_path)
    with pytest.raises(ValueError, match=f"{di.name} does not exists$"):
        cmd.run_on_item_path(tmp_path)

    assert cmd.c.updated == 0


def test_update_gitignore_file_not_file(tmp_path: Path):
    gi = tmp_path.joinpath(IgnoreFile.GITIGNORE.value)

    gi.mkdir()

    assert gi.is_dir()

    cmd = UpdateCommand(path=tmp_path)
    with pytest.raises(ValueError, match=f"{gi.name} is not a file$"):
        cmd.run_on_item_path(tmp_path)

    assert cmd.c.generated == 0
