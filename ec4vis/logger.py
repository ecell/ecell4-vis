# coding: utf-8
"""ec4vis.logger -- Logger.
"""
from logging import *
from functools import wraps

# default loglevel is set to DEBUG.
basicConfig(
    level=DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logger = getLogger()

LOG_CALL_LOGLEVEL = DEBUG


def log_call(func):
    """Decorator to emit debug log on calling/exiting the wrapped function.

    >>> import sys
    >>> logger.addHandler(StreamHandler(sys.stdout))
    >>> def foo():
    ...   debug('I am in foo()')
    >>> foo()
    I am in foo()
    >>> wrapped_foo = log_call(foo)
    >>> wrapped_foo()
    Entering __main__.foo
    I am in foo()
    Exited __main__.foo
    
    """
    bits = []
    for attr in ['__module__', '__name__']:
        if hasattr(func, attr):
            bits.append(getattr(func, attr))
    func_id = '.'.join(bits)
    @wraps(func)
    def wrapped(*args, **kwargs):
        log(LOG_CALL_LOGLEVEL, 'Entering '+func_id)
        ret = func(*args, **kwargs)
        log(LOG_CALL_LOGLEVEL, 'Exited '+func_id)
        return ret
    return wrapped


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
