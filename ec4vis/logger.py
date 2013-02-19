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


def log_call(func):
    """Decorator to emit debug log on calling/exiting the wrapped function.
    """
    bits = []
    for attr in ['__module__', '__name__']:
        if hasattr(func, attr):
            bits.append(getattr(func, attr))
    func_id = '.'.join(bits)
    @wraps(func)
    def wrapped(*args, **kwargs):
        log(DEBUG-1, 'Entering '+func_id)
        ret = func(*args, **kwargs)
        log(DEBUG-1, 'Exited '+func_id)
        return ret
    return wrapped

