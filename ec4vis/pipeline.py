# coding: utf-8
"""pipeline.py --- Represents pipeline.
"""

class PipelineSpec(object):
    """Represents a data specification. Should not be instanciated.
    """
    pass


class PipelineItem(object):
    """Represents an item in pipeline.

    # basic behaviour
    >>> pi = PipelineItem()
    >>> pi.CLASS_NAME
    >>> pi.class_name
    'PipelineItem'
    >>> pi.name
    'pipelineitem'
    >>> pi
    <PipelineItem: pipelineitem>

    # filliality logics
    >>> grandparent = PipelineItem(name='grandmom')
    >>> parent = PipelineItem(name='mom')
    >>> child = PipelineItem(name='boy')
    >>> parent.connect(grandparent)
    >>> parent.parent
    <PipelineItem: grandmom>
    >>> grandparent.children
    [<PipelineItem: mom>]
    >>> grandparent.connect(parent) # this should fail
    Traceback (most recent call last):
    ...
    ValueError: Cyclic filliation detected.
    >>> child.connect(parent)
    >>> grandparent.connect(child) # again, this should fail
    Traceback (most recent call last):
    ...
    ValueError: Cyclic filliation detected.
    >>> grandparent.parent, grandparent.children 
    (None, [<PipelineItem: mom>])
    >>> parent.parent, parent.children 
    (<PipelineItem: grandmom>, [<PipelineItem: boy>])
    >>> child.parent, child.children 
    (<PipelineItem: mom>, [])
    >>> child.connect(grandparent) # switches parent from mom to grandmom
    >>> grandparent.parent, grandparent.children 
    (None, [<PipelineItem: mom>, <PipelineItem: boy>])
    >>> parent.parent, parent.children 
    (<PipelineItem: grandmom>, [])
    >>> child.parent, child.children 
    (<PipelineItem: grandmom>, [])

    # pipeline specs
    >>> class LatticeSpec(PipelineSpec): pass
    >>> class SpeciesSpec(PipelineSpec): pass
    >>> class ParticleSpec(PipelineSpec): pass
    >>> class LatticeProviderItem(PipelineItem):
    ...     def get_output_spec(self):
    ...         return [LatticeSpec, SpeciesSpec]
    >>> class ParticleProviderItem(PipelineItem):
    ...     def get_output_spec(self):
    ...         return [ParticleSpec, SpeciesSpec]
    >>> class LatticeConsumerItem(PipelineItem):
    ...     def get_input_spec(self):
    ...         return [LatticeSpec, SpeciesSpec]
    >>> lat_prov = LatticeProviderItem()
    >>> pat_prov = ParticleProviderItem()
    >>> lat_cons = LatticeConsumerItem()
    >>> lat_cons.connect(lat_prov)
    >>> lat_cons.connect(pat_prov) # this should fail
    Traceback (most recent call last):
    ...
    ValueError: Parent item does not provide LatticeSpec
    
    """
    INSTANCE_NAMES = []
    CLASS_NAME = None # subclass may override this
    
    def __init__(self, name=None):
        """Initializer.
        """
        if name is None:
            name = self.class_name.lower()
        self.name = name
        self.parent = None
        self.children = []

    def __repr__(self):
        """Retrurns in <class_name: instance_name> format.
        """
        return '<%s: %s>' %(self.class_name, self.name)

    @property
    def class_name(self):
        """Returns human-friendly class name.
        """
        return self.CLASS_NAME or self.__class__.__name__

    def get_input_spec(self):
        """Returns input specification. Subclass may override this.
        """
        return []

    def get_output_spec(self):
        """Retursn output specification. Subclass may override this.
        """
        return []

    @property
    def input_spec(self):
        return self.get_input_spec()

    @property
    def output_spec(self):
        return self.get_output_spec()

    def bind_child(self, child):
        """Bind child as a member of children.
        """
        # avoid duplicated population
        if child in self.children:
            return
        # check if child is not in my grandparents.
        cur = self
        while cur:
            if cur is child:
                raise ValueError('Cyclic filliation detected.')
            cur = cur.parent
        self.children.append(child)

    def unbind_child(self, child):
        """Un-bind child from a member of children.
        """
        if child in self.children:
            self.children.remove(child)

    def connect(self, parent):
        """Connect to parent item.
        """
        # check if parent is a valid PipelineItem
        if not isinstance(parent, PipelineItem):
            raise ValueError('Cannot connect to non-PipelineItem instance.')
        # check if parent can provide appropreate data
        for spec in self.input_spec:
            if parent.has_spec(spec)==False:
                raise ValueError('Parent item does not provide %s' %(spec.__name__))
        # if already connected, disconnect first
        if self.parent:
            self.disconnect()
        parent.bind_child(self)
        self.parent = parent

    def disconnect(self):
        """Disconnect from parent item.
        """
        if self.parent:
            self.parent.unbind_child(self)
        self.parent = None

    def has_spec(self, spec):
        """Checks if instance can provide given spec.
        """
        return spec in self.output_spec


class RootPipelineItem(PipelineItem):
    """Special pipeline item intended to be a root of pipeline tree.
    """
    def has_spec(self, spec):
        """Checks if instance can provide given spec.

        Pipeline class always returns True.
        """
        return spec in self.output_spec


class Pipeline(object):
    """Represents a pipeline.
    
    >>> p = Pipeline()
    >>> p
    <Pipeline>

    """
    def __init__(self):
        """Initializer.
        """
        self.root = RootPipelineItem(name='Root')

    def __repr__(self):
        """Returns representation.
        """
        return '<Pipeline>'

    def append(self, pipeline_item):
        """Append a pipeline item at end of 
        """


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
