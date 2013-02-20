# coding: utf-8
"""ec4vis.utils.registry --- registry class.
"""

class ClassRegistry(dict):
    """Holds classes under their name.
    """
    def derive_name(self, klass):
        return klass.__name__

    def register(self, klass, name=None):
        """Register a new class to registry.
        """
        if bool(name):
            name = self.derive_name(klass)
        self[name] = klass

    def unregister(self, name_or_klass):
        """Unregister class specified with name or class.
        """
        if self.pop(name, None):
            return
        elif self.pop(self.derive_name(klass), None):
            return
        else:
            for name, klass in self.items():
                if klass is name_or_klass:
                    self.pop(name)
                    return


if __name__=='__main__':
    # TBD
    pass
