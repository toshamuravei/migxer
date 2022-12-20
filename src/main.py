import argparse
import os

from src.fileparser import MigrationsParser


def parse_args():
    parser = argparse.ArgumentParser(description="a script to do stuff")
    parser.add_argument("--rev_dir")
    return parser.parse_args()


def main():
    inputs = parse_args()
    if not os.path.exists(inputs.rev_dir):
        raise AttributeError(
            f"Seems that path {inputs.rev_dir} does not exist"
        )

    fileparser = MigrationsParser(_dir_name=inputs.rev_dir)
    storage = fileparser.revisions_storage
    fix_was_maden: bool = storage.fix_revision_conflict()
    if fix_was_maden:
        storage.wtite_fix_to_file()
    else:
        print("Nothing to fix")


if __name__ == '__main__':
    main()
