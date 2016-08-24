import sys
import unittest
from infi.traceback import pretty_traceback_and_exit_decorator
from infi.traceback import set_truncation_limit

PY3 = sys.version_info[0] == 3

@pretty_traceback_and_exit_decorator
def main():
    local_variable = None
    raise NotImplementedError()

@pretty_traceback_and_exit_decorator
def system_exit():
    raise SystemExit(3)

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

    def test_system_exit(self):
        try:
            system_exit()
        except SystemExit as error:
           self.assertEquals(error.args, (3, ))

    def test_truncated_repr(self):
        if PY3:
            from io import StringIO
        else:
            from StringIO import StringIO
        import sys
        @pretty_traceback_and_exit_decorator
        def func_with_variable():
            long_variable = "a very long string that we will truncate to 10 chars"
            raise Exception()
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        set_truncation_limit(10)
        try:
            with self.assertRaises(SystemExit):
                func_with_variable()
            sys.stderr.seek(0)
            output = sys.stderr.read()
        finally:
            sys.stderr = old_stderr
        self.assertIn("long_variable", output)
        self.assertIn("func_with_variable", output)
        self.assertIn("repr truncated", output)
        self.assertNotIn("10 chars", output)


if __name__ == "__main__":
    main()
    
