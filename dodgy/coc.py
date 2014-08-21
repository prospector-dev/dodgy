"""
Simple module to tokenize a python module to extract comments, then
analyse the comments line-by-line for a probability of being code.
If a certain threshold is reached, then a warning about the comment
being commented-out-code is created.
"""
import re
import tokenize
import keyword
from tokenize import TokenError
from collections import defaultdict
from cStringIO import StringIO


_TOKEN_WEIGHTS = {
    # Comments inside comments is a very strong indicator
    # that this was code commented out automatically!
    tokenize.COMMENT: 2
}

_KEYWORD_WEIGHTS = {
    'and': 0.5,
    'def': 2,
    'elif': 2,
    'exec': 2,
    'is': 0.5,
    'lambda': 2,
}

_MESSAGE_KEY = 'coc'
_MESSAGE_TEXT = 'Commented out code'
_THRESHOLD = 0.75

# PEP263, see http://legacy.python.org/dev/peps/pep-0263/
_ENCODING_REGEXP = re.compile(r'coding[:=]\s*([-\w.]+)')


def _make_tokens(string):
    readline = StringIO(string).readline
    return tokenize.generate_tokens(readline)


def _calculate_token_scores(text):
    # First, let's ignore any "special" comments
    if _ENCODING_REGEXP.search(text):
        return None, None

    # token.NAME indicates either a variable or a keyword. If the
    # text is mostly variables, then it's probably just a normal
    # comment. The presence of non-NAME tokens indicates it is
    # code, and the higher the number of non-NAME tokens, the higher the
    # probability that this particular piece of text is code.
    try:
        tokens = list(_make_tokens(text))
    except TokenError:
        # We won't be able to tokenize every line properly, and if we
        # can't, that likely means that the line is not real code.
        return None, None

    weight = 0.0
    for tok in tokens:
        tok_weight = _TOKEN_WEIGHTS.get(tok[0], 1)
        if tok[0] == tokenize.NAME:
            # This may be a keyword
            if keyword.iskeyword(tok[1]):
                tok_weight *= _KEYWORD_WEIGHTS.get(tok[1], 1)
            else:
                tok_weight = 0
        weight += tok_weight

    return weight, len(tokens)


def calculate_line_scores(text):
    lines = defaultdict(lambda:[0.0, 0])
    # first parse the contents and get the comments
    tokens = _make_tokens(text)
    for token in tokens:
        if token[0] != tokenize.COMMENT:
            continue
        text = re.sub('^\s*#\s*', '', token[1])
        score, token_count = _calculate_token_scores(text)
        if score is None:
            continue
        start_line = token[2][0]
        lines[start_line][0] += score
        lines[start_line][1] += token_count

    return { lno: w[0]/w[1] for lno, w in lines.iteritems() }


def check_file(filepath, contents):
    if not filepath.endswith('.py'):
        return []
    scores = calculate_line_scores(contents)
    scores = list(scores.iteritems())
    scores.sort(key=lambda x:x[0])
    print scores

    # Combine adjacent lines - multiple lines containing probable code
    # increases the likelyhood we have a correct match
    combined = {}
    for lno, weight in scores:
        if lno-1 in combined:
            combined[lno-1].append(weight)
        else:
            combined[lno] = [weight]

    print combined

    return 1
    return [(lno, _MESSAGE_KEY, _MESSAGE_TEXT)
            for lno, w in combined.iteritems() if w >= _THRESHOLD]
