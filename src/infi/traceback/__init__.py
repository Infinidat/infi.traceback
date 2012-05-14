__import__("pkg_resources").declare_namespace(__name__)

import sys
import nose
import mock
import linecache
import types
import mock
import infi.pyutils.contexts

class NosePlugin(nose.plugins.Plugin):
    """better tracebacks"""
    name = 'infi-traceback'

    def help(self):
        return "Print better tracebacks"

    def prepareTestResult(self, result):
        result.addError = traceback_decorator(result.addError)
        result.addFailure = traceback_decorator(result.addFailure)
        return result

def traceback_decorator(func):
    @infi.pyutils.contexts.wraps(func)
    def callee(*args, **kwargs):
        with traceback_context():
            return func(*args, **kwargs)
    return callee

@infi.pyutils.contexts.contextmanager
def traceback_context():
    with mock.patch("traceback.format_tb") as patched_format_tb, mock.patch("traceback.print_tb") as patched_print_tb:
        patched_format_tb.side_effect = format_tb
        patched_print_tb.side_effect = print_tb
        yield

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

def safe_repr(obj):
    try:
        return repr(obj)
    except:
        return object.__repr__(obj)

def format_list(extracted_list):
    list = []
    for filename, lineno, name, line, _locals in extracted_list:
        item = '  File "%s", line %d, in %s\n' % (filename, lineno, name)
        if line:
            item = item + '    %s\n' % line.strip()
        if _locals:
            item = item + '  Local variables:\n'
            for key, value in _locals.items():
                item = item + '    %r: %r\n' % (key, safe_repr(value))
        list.append(item)
    return list

