from pathlib import Path

from commands.base import BaseCommand
from enums import IgnoreFiles


class DeleteCommand(BaseCommand):
    def run_on_item_path(self, item_path: Path) -> None:
        if not item_path.name == IgnoreFiles.DROPBOXIGNORE.value:
            raise ValueError(f"{item_path} is not a dropboxignore file.")
        try:
            item_path.unlink(missing_ok=False)
            self.c.deleted += 1
        except FileNotFoundError:
            pass

    def run_report(self) -> str:
        return f"Number of deleted files: {self.c.deleted}"