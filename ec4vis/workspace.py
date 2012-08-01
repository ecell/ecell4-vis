# coding: utf-8
"""workspace.py --- Workspace data model.
"""
import pickle


class WorkspaceEntity(object):
    """Represents an entity in a workspace.

    >>> we = WorkspaceEntity('foo')
    >>> unicode(we)
    u'foo'
    >>> we.label
    u'foo'
    >>> we.props
    {}
    
    """
    def __init__(self, label='Entity', **props):
        """Initializer.
        """
        self.label = unicode(label)
        self.props = props

    def __unicode__(self):
        """Simply returns label.
        """
        return self.label

    @property
    def is_valid(self):
        """Returns true if the object is valid.
        """
        return self.do_is_valid()

    def do_is_valid(self):
        """Do real computation for is_valid.
        """
        return False


class Workspace(object):
    """Workspace data model.
    """
    def __init__(self):
        self.file = []
        self.loader = []
        self.filter = []
        self.visualizer = []
        self.visual = []
        self.parameter = []
        self.frame = []

    @classmethod
    def Loads(self, buf):
        """Class method. Loads workspace properties from buffer.
        """
        return pickle.loads(buf)
        
    def dumps(self):
        """Dumps workspace as a string.
        """
        return pickle.dumps(self)

    def add_entity(self, type, obj):
        """Add an object of given type to collection in the workspace.
        """
        # find collection according to type
        collection = getattr(self, type, None)
        if collection:
            labels = [unicode(entry) for entry in collection]
            suffix, sfx_count = '', 0
            obj_label = unicode(obj)
            # shift suffix until obj's label gets unique in the collection.
            while obj_label+suffix in labels:
                if sfx_count:
                    suffix = '_%d' %(sfx_count)
                sfx_count+=1
            # tweak suffix and add
            obj.label = obj_label+suffix
            collection.append(obj)
        # always returns nothing.
        return

    def delete_entity(self, type, label):
        """Delete object of given type/label from collection in the workspace.
        """
        # find collection according to type
        collection = getattr(self, type, None)
        if collection:
            for idx, entry in enumerate(collection):
                if unicode(entry)==label:
                    collection.pop(idx)
                    return
        # omits silently if entry not found here.
        return

    def lookup(self, type, label):
        """Looks up entity of given type and label.
        """
        # find collection according to type
        collection = getattr(self, type, None)
        if collection:
            for entry in collection:
                if unicode(entry)==label:
                    return entry
        # omits silently if entry not found here.
        return None


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
