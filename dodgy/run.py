import sys
import re
import os
import mimetypes
import json
from dodgy import passwords, coc


IGNORE_PATHS = [re.compile(patt % {'sep': os.path.sep}) for patt in (
    r'(^|%(sep)s)\.[^\.]',   # ignores any files or directories starting with '.'
    r'^tests?%(sep)s?',
    r'%(sep)stests?(%(sep)s|$)',
)]


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

    checks = [passwords, coc]

    filepaths = list_files(directory)
    for filepath in filepaths:
        relpath = os.path.relpath(filepath, directory)
        if any([ignore.search(relpath) for ignore in ignore_paths]):
            continue

        # this is a naive check to skip binary files, it's probably okay for now
        mimetype = mimetypes.guess_type(filepath)
        if mimetype[0] is None or not mimetype[0].startswith('text/'):
            continue

        for check in checks:
            contents = open(filepath).read()
            for msg_parts in check.check_file(filepath, contents):
                warnings.append({
                    'path': relpath,
                    'line': msg_parts[0],
                    'code': msg_parts[1],
                    'message': msg_parts[2]
                })

    def _sort(a, b):
        if a['path'] == b['path']:
            return a['line'] < b['line']
        return a['path'] < b['path']
    warnings.sort(cmp=_sort)

    return warnings


def run():
    warnings = run_checks(os.getcwd())
    output = json.dumps({'warnings': warnings}, indent=2)
    sys.stdout.write(output + '\n')


if __name__ == '__main__':
    run()
