from src.fileparser import MigrationsParser


class TestMigrationsParser:

    def test_init(self):
        MIGRATION_FILES_DIR = "tests/migration_files_fixtures/"
        DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

        fileparser = MigrationsParser(_dir_name=MIGRATION_FILES_DIR)
        storage = fileparser.revisions_storage
        multiparent = storage.find_first_multiparent()
        assert multiparent == "2d9f80797b0d"
        upper_child, lower_child = storage[multiparent].children

        assert upper_child == "7954fsbh1i24"

        rev_date = storage[upper_child].revision_date.strftime(DATETIME_FMT)
        rev_date == "2022-10-03 14:33:55"

        assert lower_child == "7474fcfa1b90"
        rev_date = storage[upper_child].revision_date.strftime(DATETIME_FMT)
        rev_date == "2022-10-02 14:33:55"
