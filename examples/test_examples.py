import unittest

class TestCase(unittest.TestCase):
    def test_that_fails(self):
        self.fail()

    def test_that_raises_exception(self):
        raise Exception()

    def test_nested_exception(self):
        this = self
        self._nested_call()

    def _nested_call(self):
        raise Exception()

