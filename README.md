Overview
========
Python's traceback module does pretty formatting and printing of tracebacks, but does not add the local variable of each frame.
This module adds this capacbility to the traceback module by monkeypatching.

Usage
-----

```python
from infi.traceback import traceback_context, traceback_decorator

def call():
    text = 'some text'
    boolean = True
    obj = object()
    raise RuntimeError()

@traceback_decorator
def test_decorator():
    import traceback
    try:
        call()
    except:
       traceback.print_exc()

def test_context():
    with traceback_context():
        import traceback
        try:
            call()
        except:
           traceback.print_exc()

test_decorator()
test_context()
```

Checking out the code
=====================

This project uses buildout, and git to generate setup.py and __version__.py.
In order to generate these, run:

    python -S bootstrap.py -d -t
    bin/buildout -c buildout-version.cfg
    python setup.py develop

In our development environment, we use isolated python builds, by running the following instead of the last command:

   bin/buildout install development-scripts

