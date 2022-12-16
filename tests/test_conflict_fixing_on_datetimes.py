from src.migxer_fileparser import MigrationsParser


class TestConflictFixing:

    def test_conflict_fixing(self):
        MIGRATION_FILES_DIR = "tests/migration_files_fixtures/"

        fileparser = MigrationsParser(_dir_name=MIGRATION_FILES_DIR)
        storage = fileparser.revisions_storage
        multiparent = storage._find_first_multiparent()
        storage.fix_revision_conflict(multiparent)
        revisions = storage.get_revisions_line()
        expected_revisions = ['2d9f80797b0d', '7474fcfa1b90', '7954fsbh1i24', '8448frrr2a14']
        assert revisions == expected_revisions
