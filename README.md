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

A common is use-case is to have a pretty traceback when an un-caught exeption is raised by a console script entry point. For that, you can use:

```python
from infi.traceback import pretty_traceback_and_exit_decorator

@pretty_traceback_and_exit_decorator
def entrypoint():
    pass
```

By default, local vars will truncate at 500 characters.  This can be changed in one of two ways.

Globally:

```python
from infi.traceback import set_truncation_limit

set_truncation_limit(100)
```

and will affect any tracebacks that are hit and if you call it again in different places, both calls will affect the global value for everywhere else.

Per call:

```python
from infi.traceback import traceback_context, traceback_decorator, pretty_traceback_and_exit_decorator


@traceback_decorator(300)
def test_decorator():
    import traceback
    try:
        call()
    except:
       traceback.print_exc()

def test_context():
    with traceback_context(None):
        import traceback
        try:
            call()
        except:
           traceback.print_exc()

@pretty_traceback_and_exit_decorator(100)
def entrypoint():
    call()
```

This gives much more fine grained control when you might want differnt outputs for differnt parts of the code.  None means nothing will be truncated.

Checking out the code
=====================

Run the following:

    easy_install -U infi.projector
    projector devenv build
