from dropboxignore.enums import IgnoreFile
from dropboxignore.filterers.base import BaseFilterer


class GitIgnoreFilterer(BaseFilterer):
    def __iter__(self):
        yield from self.path.glob(f"**/*{IgnoreFile.GITIGNORE.value}")
