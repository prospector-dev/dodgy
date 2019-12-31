import argparse


def get_options(argv=None):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--zero-exit",
        help="Dodgy will exit with a code of 1 if problems are found",
        action="store_true",
    )

    return parser.parse_args(argv)
