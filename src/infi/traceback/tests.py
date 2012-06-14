import unittest
from infi.traceback import pretty_traceback_and_exit_decorator

@pretty_traceback_and_exit_decorator
def main():
    local_variable = None
    raise NotImplementedError()

class RaisingRepr(object):
    def __repr__(self):
        raise Exception()

class TestCase(unittest.TestCase):
    def test_safe_repr(self):
        from infi.traceback import safe_repr
        obj = RaisingRepr()
        string = safe_repr(obj)

    def test_main(self):
        with self.assertRaises(SystemExit):
            main()

if __name__ == "__main__":
    main()
    
