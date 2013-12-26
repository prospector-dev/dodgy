import re
import os
import mimetypes
import json
from dodgy.checks import check_file


IGNORE_PATHS = [re.compile(r % {'sep': os.path.pathsep}) for r in (
    r'(^|%(sep)s)\.',
    r'^tests?%(sep)s?',
    r'%(sep)stests?(%(sep)s|$)',
)]


def list_files(start_path):
    filepaths = []
    for root, _, files in os.walk(start_path):
        for file_name in files:
            filepaths.append(os.path.join(root, file_name))
    return filepaths


def run():
    warnings = []

    filepaths = list_files(os.getcwd())
    for filepath in filepaths:
        relpath = os.path.relpath(filepath, os.getcwd())
        if any([r.search(relpath) for r in IGNORE_PATHS]):
            continue

        # this is a naive check to skip binary files, it's probably okay for now
        mimetype = mimetypes.guess_type(filepath)
        if mimetype == (None, None) or not mimetype[0].startswith('text/'):
            continue

        for msg_parts in check_file(filepath):
            warnings.append({
                'path': relpath,
                'line': msg_parts[0],
                'code': msg_parts[1],
                'message': msg_parts[2]
            })

    print json.dumps({'warnings': warnings}, indent=2)


if __name__ == '__main__':
    run()
