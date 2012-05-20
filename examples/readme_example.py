import traceback
from infi.traceback import traceback_context, traceback_decorator

def call():
    text = 'some text'
    boolean = True
    obj = object()
    raise RuntimeError()

@traceback_decorator
def test_decorator():
    try:
        call()
    except:
       traceback.print_exc()

def test_context():
    with traceback_context():
        try:
            call()
        except:
           traceback.print_exc()

test_decorator()
test_context()
