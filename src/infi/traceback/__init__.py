__import__("pkg_resources").declare_namespace(__name__)

import sys
import nose
import mock
import linecache
import types
import traceback
import mock
import infi.pyutils.contexts
import infi.pyutils.patch
import infi.exceptools

truncate_repr = None

class NosePlugin(nose.plugins.Plugin):
    """better tracebacks"""
    name = 'infi-traceback'

    def __init__(self):
        super(NosePlugin, self).__init__()
        self.active_context = None

    def help(self):
        return "Print better tracebacks"

    def startContext(self, context):
        if self.active_context is not None:
            return
        self.active_context = context
        self.traceback_context = traceback_context()
        self.traceback_context.__enter__()

    def stopContext(self, context):
        if not self.active_context is context:
            return
        self.active_context = None
        self.traceback_context.__exit__(None, None, None)

@infi.pyutils.contexts.contextmanager
def traceback_context():
    with infi.pyutils.patch.patch(traceback, "format_tb", format_tb), \
         infi.pyutils.patch.patch(traceback, "print_tb", print_tb), \
         infi.pyutils.patch.patch(traceback, "format_exception", format_exception), \
         infi.pyutils.patch.patch(traceback, "print_exception", print_exception):
        yield

def traceback_decorator(func):
    @infi.pyutils.contexts.wraps(func)
    def callee(*args, **kwargs):
        with traceback_context():
            return func(*args, **kwargs)
    return callee

def pretty_traceback_and_exit_decorator(func):
    @infi.pyutils.contexts.wraps(func)
    def callee(*args, **kwargs):
        with traceback_context():
            import traceback
            try:
                return func(*args, **kwargs)
            except SystemExit:
                traceback.print_exc()
                raise
            except:
                traceback.print_exc()
                raise infi.exceptools.chain(SystemExit(1))
    return callee

# Taken from Python 2.7.2 traceback module

def format_tb(tb, limit=None):
    """A shorthand for 'format_list(extract_stack(f, limit))."""
    return format_list(extract_tb(tb, limit))

def print_tb(tb, limit=None, file=None):
    """Print up to 'limit' stack trace entries from the traceback 'tb'.

    If 'limit' is omitted or None, all entries are printed.  If 'file'
    is omitted or None, the output goes to sys.stderr; otherwise
    'file' should be an open file or file-like object with a write()
    method.
    """
    if file is None:
        file = sys.stderr
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    file.write('\n'.join(format_tb(tb, limit)) + '\n')

def extract_tb(tb, limit=None):
    if limit is None:
        if hasattr(sys, 'tracebacklimit'):
            limit = sys.tracebacklimit
    list = []
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        _locals = tb. tb_frame.f_locals
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        if line: line = line.strip()
        else: line = None
        list.append((filename, lineno, name, line, _locals))
        tb = tb.tb_next
        n = n + 1
    return list

def set_truncation_limit(limit):
    global truncate_repr
    assert limit is None or (isinstance(limit, int) and limit > 0)
    truncate_repr = limit

def safe_repr(obj):
    try:
        res = repr(obj)
        if truncate_repr is not None and len(res) > truncate_repr:
            res = "<repr truncated: %s>" % (object.__repr__(obj), )
    except:
        res = "<repr fallback: %s>" % (object.__repr__(obj), )
    return res

def format_list(extracted_list):
    list = []
    for filename, lineno, name, line, _locals in extracted_list:
        item = '  File "%s", line %d, in %s\n' % (filename, lineno, name)
        if line:
            item = item + '    %s\n' % line.strip()
        if _locals:
            item = item + '  Local variables:\n'
            for key, value in _locals.items():
                item = item + '    %r: %s\n' % (key, safe_repr(value))
        list.append(item)
    return list

def format_exception(etype, value, tb, limit = None):
    """Format a stack trace and the exception information.

    The arguments have the same meaning as the corresponding arguments
    to print_exception().  The return value is a list of strings, each
    ending in a newline and some containing internal newlines.  When
    these lines are concatenated and printed, exactly the same text is
    printed as does print_exception().
    """
    import traceback
    if tb:
        list = ['Traceback (most recent call last):\n']
        list = list + format_tb(tb, limit)
    else:
        list = []
    list = list + traceback.format_exception_only(etype, value)
    return list


def print_exception(etype, value, tb, limit=None, file=None, chain=True):
    """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

    This differs from print_tb() in the following ways: (1) if
    traceback is not None, it prints a header "Traceback (most recent
    call last):"; (2) it prints the exception type and value after the
    stack trace; (3) if type is SyntaxError and value has the
    appropriate format, it prints the line where the syntax error
    occurred with a caret on the next line indicating the approximate
    position of the error.
    """
    import traceback
    if file is None:
        file = sys.stderr
    if tb:
        file.write('Traceback (most recent call last):\n')
        print_tb(tb, limit, file)
    lines = traceback.format_exception_only(etype, value)
    for line in lines:
        file.write(line)
