import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src.visitor import MigxerVisitor
from src.revision_storage import RevisionItem, RevisionStorage


@dataclass
class MigrationsParser:
    _dir_env_varname: str = "MIGRATIONS_DIR"
    _files_extension: str = ".py"
    _dir_name: str = ""
    files: List[str] = field(default_factory=list)
    revisions_storage: RevisionStorage = field(default_factory=RevisionStorage)

    NUM_LINES_TO_READ_FOR_DATE: int = 10
    MIGRATION_DATE_PREFIX: str = "Create Date"
    MIGRATION_DATE_SPLIT_CHAR: str = "."
    MIGRATION_DATETIME_FMT: str = "%Y-%m-%d %H:%M:%S"

    def __post_init__(self):
        self._set_migration_files()
        self._set_revision_items()

    def _set_migration_files(self):
        mig_dir = os.environ.get(self._dir_env_varname) or self._dir_name
        for filename in os.listdir(mig_dir):
            if filename.endswith(self._files_extension):
                migration_path = mig_dir + filename
                self.files.append(migration_path)

    def _set_revision_items(self):
        for file in self.files:
            self.revisions_storage.add(
                self._migration_file_to_revision_item(file)
            )

    def _migration_file_to_revision_item(self, filepath: str) -> RevisionItem:
        visitor = MigxerVisitor(filepath)
        rev_item = RevisionItem(
            original_filepath=filepath,
            revision=visitor.revision_value,
            parent_revision=visitor.down_revision_value,
            revision_date=self._extract_datetime_from_comment(filepath),
        )
        return rev_item

    def _extract_datetime_from_comment(self, filepath: str) -> datetime:
        with open(filepath, "r") as file:
            for _ in range(self.NUM_LINES_TO_READ_FOR_DATE):
                line = next(file)
                if line.startswith(self.MIGRATION_DATE_PREFIX):
                    return self._cut_datetime_from_line(line)

    def _cut_datetime_from_line(self, line) -> datetime:
        date_substring_shift = len(self.MIGRATION_DATE_PREFIX) + 2
        date_string = line[date_substring_shift:-1]
        date_string = date_string.split(self.MIGRATION_DATE_SPLIT_CHAR)[0]
        _datetime = datetime.strptime(date_string, self.MIGRATION_DATETIME_FMT)
        return _datetime
