__import__("pkg_resources").declare_namespace(__name__)

import sys
import os
import logging
import nose
import mock
import traceback
import linecache
import types
import mock

logger = logging.getLogger(__name__)

class TracebackPlugin(nose.plugins.Plugin):
    name = 'infi-nose-traceback'

    def configure(self, options, conf):
        super(TracebackPlugin, self).configure(options, conf)
        self.enabled = True

    def prepareTestResult(self, result):
        result.addError = TracebackFormatter(result.addError)
        result.addFailure = TracebackFormatter(result.addFailure)
        return result

class TracebackFormatter(object):
    def __init__(self, func):
        self._func = func

    def _side_effect(self, *args, **kwargs):
        return_value = format_tb(*args, **kwargs)
        return return_value

    def __call__(self, err, test):
        with mock.patch("traceback.format_tb") as patch:
            patch.side_effect = self._side_effect
            return self._func(err, test)

# Taken from Python 2.7.2 traceback module

def format_tb(tb, limit = None):
    """A shorthand for 'format_list(extract_stack(f, limit))."""
    return format_list(extract_tb(tb, limit))

def extract_tb(tb, limit = None):
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
        n = n+1
    return list

def format_list(extracted_list):
    list = []
    for filename, lineno, name, line, _locals in extracted_list:
        item = '  File "%s", line %d, in %s\n' % (filename,lineno,name)
        if line:
            item = item + '    %s\n' % line.strip()
        if _locals:
            item = item + '  Local variables:\n'
            for key,value in _locals.items():
                item = item + '    %r: %r\n' % (key, value)
        list.append(item)
    return list

