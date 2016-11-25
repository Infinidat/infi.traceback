import os
import sys


def _canonic(filename):
    if filename == "<" + filename[1:-1] + ">":
        return filename
    canonic = os.path.abspath(filename)
    canonic = os.path.normcase(canonic)
    return canonic


def _runscript(filename):
    # The script has to run in __main__ namespace (or imports from
    # __main__ will break).
    #
    # So we clear up the __main__ and set several special variables
    # (this gets rid of pdb's globals and cleans old variables on restarts).
    import __main__
    __main__.__dict__.clear()
    __main__.__dict__.update({"__name__"    : "__main__",
                              "__file__"    : filename,
                              "__builtins__": __builtins__,
                             })

    mainpyfile = _canonic(filename)
    statement = 'execfile(%r)' % filename

    globals = __main__.__dict__
    locals = globals

    exec statement in globals, locals


def main():
    from . import traceback_context

    if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
        print "usage: python -m infi.traceback scriptfile [arg] ..."
        sys.exit(2)

    mainpyfile =  sys.argv[1]     # Get script filename
    if not os.path.exists(mainpyfile):
        print 'Error:', mainpyfile, 'does not exist'
        sys.exit(1)

    del sys.argv[0]         # Hide "infi/traceback/__main__.py" from argument list

    sys.path[0] = os.path.dirname(mainpyfile)

    import traceback
    with traceback_context():
        try:
            return _runscript(mainpyfile)
        except SystemExit:
            raise
        except:
            traceback.print_exc()
            return 1


# When invoked as main program, invoke the debugger on a script
if __name__ == '__main__':
    sys.exit(main())
