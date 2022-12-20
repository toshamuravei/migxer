from distutils.dir_util import copy_tree, remove_tree

from src.fileparser import MigrationsParser


MIGRATION_FILES_DIR = "tests/migration_files_fixtures/"


class TempDirectory:
    EXISTING_MIGRATIONS_FIXTURES_DIR = MIGRATION_FILES_DIR

    def __init__(self, dir_name: str):
        self.dir_name = dir_name
        self._copy_existing_migrations_into_new_dir()

    def _copy_existing_migrations_into_new_dir(self):
        copy_tree(self.EXISTING_MIGRATIONS_FIXTURES_DIR, self.dir_name)

    def __enter__(self) -> str:
        return self.dir_name

    def __exit__(self, *args, **kwargs):
        remove_tree(self.dir_name)


class TestFixWriting:

    def test_migration_fix(self):
        with TempDirectory("tests/tmp_revisions_dir/") as temp_dir:
            fileparser = MigrationsParser(_dir_name=temp_dir)
            storage = fileparser.revisions_storage
            multiparent = storage.find_first_multiparent()

            assert multiparent == "2d9f80797b0d"

            multiparent = storage.find_first_multiparent()
            storage.fix_revision_conflict(multiparent)
            storage.wtite_fix_to_file()

            new_fileparser = MigrationsParser(_dir_name=temp_dir)
            storage = new_fileparser.revisions_storage
            new_multiparent = storage.find_first_multiparent()
            assert new_multiparent is None
