# coding: utf-8
"""
ec4vis.plugins --- Plugin related utilities.

Plugin is a simple module which may contain arbitrary set of classes.
You may define Visualizer to be registered, patch existing module(s),
extend UI or whatever you want...

"""
from glob import glob
from os.path import dirname, join, splitext, isdir, exists

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, log_call, logger, DEBUG


class PluginLoader(object):
    """Plugins loader.
    """
    def __init__(self, prefix=dirname(__file__)):
        modules_info = []
        for filepath in glob(join(prefix, '*')):
            if filepath.endswith('.py'):
                if not filepath.endswith('__init__.py'):
                    modname, ext = splitext(filepath[len(prefix)+1:])
                    modules_info.append(('ec4vis.plugins', modname))
            elif isdir(filepath) and exists(join(filepath, '__init__.py')):
                modname = filepath[len(prefix)+1:]
                modules_info.append(('ec4vis.plugins', modname))
        self.modules_info = modules_info

    def load_iterative(self):
        for mod_path, modname in self.modules_info:
            try:
                mod_fullpath = mod_path+'.'+modname
                __import__(mod_fullpath)
                yield (mod_fullpath, True)
            except Exception, e:
                debug('**FAILED**: %s' %str(e))
                yield (mod_fullpath, False)
        return


if __name__=='__main__':
    pass
