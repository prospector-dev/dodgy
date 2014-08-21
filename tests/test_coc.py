from unittest import TestCase
from dodgy.coc import calculate_line_scores
import os
import re

class TestCOC(TestCase):

    def test_coc(self):
        testdir = os.path.join(os.path.dirname(__file__), 'testdata', 'coc')
        testdir = os.path.abspath(testdir)
        for filename in os.listdir(testdir):
            filepath = os.path.join(testdir, filename)
            contents = open(filepath).readlines()
            expected = re.match(r'^# --CODE:(.*)$', contents[0]).group(1)
            expected = set(map(int, expected.split(',')))
            results = calculate_line_scores(''.join(contents))

            found = set(results.keys())
            # we ignore line 1, since it's the list if lines to expect
            found.remove(1)

            not_found = expected - found
            not_expected = found - expected

            if len(not_found) > 0:
                self.fail("The following lines should have been marked as code in file %s: %s" % (filename, not_found))
            if len(not_expected) > 0:
                self.fail("The following lines should not have been marked in file %s: %s" % (filename, not_expected))
