Overview
========
Python's traceback module does pretty formatting and printing of tracebacks, but does not add the local variable of each frame.
This module adds this capacbility to the traceback module by monkeypatching.

Usage
-----

Here's an example on how to use this module:

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

This prints:
```python
    Traceback (most recent call last):
      File "examples/readme_example.py", line 14, in test_decorator
        call()

      File "examples/readme_example.py", line 9, in call
        raise RuntimeError()
      Local variables:
        'text': 'some text'
        'boolean': True
        'obj': <object object at 0x100283200>

    RuntimeError
    Traceback (most recent call last):
      File "examples/readme_example.py", line 21, in test_context
        call()

      File "examples/readme_example.py", line 9, in call
        raise RuntimeError()
      Local variables:
        'text': 'some text'
        'boolean': True
        'obj': <object object at 0x100283210>

    RuntimeError
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

