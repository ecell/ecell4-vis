# coding: utf-8
"""settings.py --- settings for vizualizer application.
"""

class Settings(object):
    """Simple settings container.
    """

    def __init__(self, **kwargs):
        """Initializer.
        """
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Updates current setting attributs with given kwargs.
        """
        for k, v in kwargs.items():
            if not k.startswith('_'):
                setattr(self, k, v)


# built-in settings
import default_settings
settings = Settings(**default_settings.__dict__)
del default_settings


def configure(**kwargs):
    """Overrides settings
    """
    settings.configure(**kwargs)


if __name__=='__main__':
    # TBD: unittest
    from doctest import *
    testmod(optionflags=ELLIPSIS)

