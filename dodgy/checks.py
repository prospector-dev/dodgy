import re


STRING_VALS = (
    ('aws_access_key',
     'Amazon Web Services access key',
     re.compile(r'(\'|")[A-Z0-9]{20}(\'|")')
    ),
    ('aws_secret_key',
     'Amazon Web Services secret key',
     re.compile(r'(\'|")[A-Za-z0-9\\\+]{40}(\'|")')
    )
)

LINE_VALS = (
    ('diff',
     'Possible SCM diff in code',
     (re.compile(r'^<<<<<<< .*$'), re.compile(r'^>>>>>>> .*$'))
    ),
)

VAR_NAMES = (
    ('password',
     'Possible hardcoded password',
     re.compile(r'(\b|_)PASSWORD(_|\b)')
    ),
    ('secret',
     'Possible hardcoded secret key',
     re.compile(r'(\b|_)SECRET(_|\b)')
    ),
)


def check_line(line, check_list):
    messages = []

    for key, msg, regexps in check_list:
        if not isinstance(regexps, (list, tuple)):
            regexps = [regexps]
        for regexp in regexps:
            if regexp.search(line):
                messages.append((key, msg))

    return messages


def check_file(filepath):
    with open(filepath) as f:
        return check_file_contents(f.read())


def check_file_contents(file_contents):
    messages = []

    for line_number0, line in enumerate(file_contents.split('\n')):
        for check_list in (STRING_VALS, LINE_VALS, VAR_NAMES):
            messages += [(line_number0+1, key, msg) for key,msg in check_line(line, check_list)]

    return messages
