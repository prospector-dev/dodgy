from unittest import TestCase

from dodgy.run import run
from mock import patch


class TestRun(TestCase):

    @patch('dodgy.run.run_checks')
    def test_return_zero_for_success(self, run_checks_mock):
        run_checks_mock.return_value = []
        self.assertEqual(run(), 0)

    @patch('dodgy.run.run_checks')
    def test_return_1_for_warnings(self, run_checks_mock):
        run_checks_mock.return_value = ['should-be-warning']
        self.assertEqual(run(), 1)
