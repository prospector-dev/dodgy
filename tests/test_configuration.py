from unittest import TestCase

from dodgy.configuration import get_options


class TestGetOptions(TestCase):

    def test_zero_exit_disabled_by_default(self):
        args = get_options([])
        self.assertFalse(args.zero_exit)

    def test_zero_exit_enabled(self):
        args = get_options(['--zero-exit'])
        self.assertTrue(args.zero_exit)
