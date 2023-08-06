import unittest

import logging
logger = logging.getLogger(__name__)

from . import *


class TestUtil(unittest.TestCase):
    def test_set_limit_0(self):
        self.assertEqual(
            set_limit('SELECT * FROM test LIMIT 1', 1),
            'SELECT * FROM test LIMIT 1'
        )

    def test_set_limit_1(self):
        self.assertEqual(
            set_limit('SELECT * FROM test', 1),
            'SELECT * FROM test LIMIT 1'
        )

    def test_set_limit_2(self):
        self.assertEqual(
            set_limit('SELECT * FROM test LIMIT 10', 2),
            'SELECT * FROM test LIMIT 2'
        )

    def test_set_limit_3(self):
        self.assertEqual(
            set_limit('SELECT * FROM test LIMIT 10, 2', 3),
            'SELECT * FROM test LIMIT 3'
        )

    def test_set_limit_4(self):
        self.assertEqual(
            set_limit('SELECT * FROM test \n\tLIMIT  \t 10, 2', 4),
            'SELECT * FROM test LIMIT 4'
        )