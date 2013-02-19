# coding: utf-8
"""Shelve-based registry.
"""
import os, shelve

REGISTRY_DIRNAME = '.ec4vis'

class Registry(object):
    """Simple shelve-based registry.
    """

    def __init__(self, home_path=None, create=False):
        """Initializer.
        """
        # check if home_path and registry path exist.
        if home_path is None:
            home_path = os.getenv('HOME', os.getcwd())
        if os.path.exists(home_path)==False:
            raise ValueError('Home path (%s) does not exist.' %home_path)
        registry_path = os.path.join(home_path, REGISTRY_DIRNAME)
        if os.path.exists(registry_path)==False:
            if create:
                os.mkdir(registry_path)
        if os.path.exists(registry_path)==False:
            raise ValueError('Registry path (%s) does not exist.' %registry_path)
        self.registry_path = registry_path
        self.sections_cache = {}

    def get_section_path(self, section_name):
        """Returns section path.
        """
        return os.path.join(self.registry_path, '%s.shelve' %section_name)

    def load_section(self, section_name):
        """Load shelved section data for given name.
        """
        section = self.sections_cache.get(
            section_name,
            shelve.open(self.get_section_path(section_name)))
        if section:
            self.sections_cache[section_name] = section
        return section

    def unload_section(self, section_name):
        """Unload section (remove from cache).
        """
        cached = self.sections_cache.pop(section_name, None)
        if cached:
            cached.close()

    def sync(self):
        """Force sync for all sections.
        """
        for section_name, shelf in self.sections_cache.items():
            shelf.sync()

    def close(self):
        """Force close fro all sections.
        """
        while self.sections_cache.keys():
            section_name, shelf = self.sections_cache.popitem()
            shelf.close()


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
