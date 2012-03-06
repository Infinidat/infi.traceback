import unittest

class TestCase(unittest.TestCase):
    def test_that_fails(self):
        self.fail()

    def test_that_raises_exception(self):
        raise Exception()

