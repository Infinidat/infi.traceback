import unittest

class RaisingRepr(object):
    def __repr__(self):
        raise Exception()

class TestCase(unittest.TestCase):
    def test_safe_repr(self):
        from infi.traceback import safe_repr
        obj = RaisingRepr()
        string = safe_repr(obj)

