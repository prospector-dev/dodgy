import json
import mimetypes
import os
import re
import sys
from argparse import ArgumentParser

from dodgy.checks import check_file

IGNORE_PATHS = [
    re.compile(patt % {"sep": re.escape(os.path.sep)})
    for patt in (
        r"(^|%(sep)s)\.[^\.]",  # ignores any files or directories starting with '.'
        r"^tests?%(sep)s?",
        r"%(sep)stests?(%(sep)s|$)",
        # Ignore foo_test(s)/.
        r"_tests?(%(sep)s|$)",
    )
]


def list_files(start_path):
    filepaths = []
    for root, _, files in os.walk(start_path):
        for file_name in files:
            filepaths.append(os.path.join(root, file_name))
    return filepaths


def run_checks(directory, ignore_paths=None):
    warnings = []

    ignore_paths = ignore_paths or []
    ignore_paths = [re.compile(patt) for patt in ignore_paths]
    ignore_paths += IGNORE_PATHS

    filepaths = list_files(directory)
    for filepath in filepaths:
        relpath = os.path.relpath(filepath, directory)
        if any([ignore.search(relpath) for ignore in ignore_paths]):
            continue

        # this is a naive check to skip binary files, it's probably okay for now
        mimetype = mimetypes.guess_type(filepath)
        if mimetype[0] is None or not mimetype[0].startswith("text/"):
            continue

        try:
            for msg_parts in check_file(filepath):
                warnings.append(
                    {
                        "path": relpath,
                        "line": msg_parts[0],
                        "code": msg_parts[1],
                        "message": msg_parts[2],
                    }
                )
        except UnicodeDecodeError as err:
            # This is a file which cannot be opened using codecs with UTF-8
            print("Unable to read {!r}: {}".format(filepath, err))

    return warnings


def run(ignore_paths=None, zero_exit=False):
    warnings = run_checks(os.getcwd(), ignore_paths=ignore_paths)

    output = json.dumps({"warnings": warnings}, indent=2)
    sys.stdout.write(output + "\n")

    if zero_exit:
        sys.exit(0)
    sys.exit(1 if warnings else 0)

def main(argv=None):
    argv = argv or sys.argv
    desc = (
        'A very basic tool to run against your codebase to search for "dodgy" looking values. '
        "It is a series of simple regular expressions designed to detect things such as "
        "accidental SCM diff checkins, or passwords/secret keys hardcoded into files."
    )
    parser = ArgumentParser("dodgy", description=desc)
    parser.add_argument(
        "--ignore-paths",
        "-i",
        nargs="+",
        type=str,
        dest="ignore",
        default=None,
        metavar="IGNORE_PATH",
        help="Paths to ignore",
    )
    parser.add_argument(
        "--zero-exit",
        "-0",
        dest="zero_exit",
        help="Dodgy will exit with a code of 1 if problems are found. This flag ensures that it always returns with 0 unless an exception is raised.",
        action="store_true",
    )

    args, _ = parser.parse_known_args(argv)

    run(ignore_paths=args.ignore, zero_exit=args.zero_exit)

if __name__ == "__main__":
    main()
