# coding: utf-8
"""pipeline.py --- Represents pipeline.
"""
import sys


# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, log_call, logger, DEBUG


# pipeline node registry
PIPELINE_NODE_REGISTRY = {}

@log_call
def register_pipeline_node(node_class, name=None):
    """Registers new pipeline node class to registry.
    """
    if bool(name)==False:
        name = node_class.__name__
    PIPELINE_NODE_REGISTRY[name] = node_class
    debug('registered pipeline node %s as %s' %(name, node_class))


class PipelineEvent(object):
    """Represents an event passed throught pipeline.
    """
    def __init__(self, data):
        """Initializer.
        """
        # event data
        self.data = data
        # visitor note for pipeline nodes.
        self.visited = []

    def note_visited(self, node):
        """Log a visit note. Returns false if node has already visited.
        """
        if node in self.visited:
            return False
        self.visited.append(node)
        return True

    def get_data_digest(self):
        """Returns digest of event data. Subclass should override.
        """
        return str(self.data)

    def __repr__(self):
        """Representation of event object.
        """
        return '<%s: %s>' %(self.__class__.__name__, self.get_data_digest())


class UpdateEvent(PipelineEvent):
    """Event indicating any updates.
    """
    pass


class PipelineSpecMetaClass(type):
    """A metaclass for pipeline specification classes.

    >>> PipelineSpec
    <PipelineSpec>
    
    """
    def __repr__(self):
        """Simply returns classname in triangle brakets.
        """
        return '<%s>' %(self.__name__)


class PipelineSpec(object):
    """Represents a data specification. Should not be instanciated.
    """
    __metaclass__ = PipelineSpecMetaClass


class UriSpec(PipelineSpec):
    """Data spec for URI string.
    """
    pass


class DatasourceSpec(PipelineSpec):
    """Data spec for Datasource object.
    """
    pass


class Observer(object):
    """Abstract base class for observers.
    """
    def __init__(self, target):
        self.target = None
        self.bind_target(target)

    def bind_target(self, target):
        self.target = target
        if self.target:
            self.target.add_observer(self)

    def unbind_target(self):
        if self.target:
            self.target.remove_observer(self)
            self.target = None
        
    def update(self):
        """Called on any changes on target object.

        Subclass should override this method to reflect target changes on the observer.
        """
        return NotImplemented


class PipelineNode(object):
    """Represents an item in pipeline.

    # basic behaviour
    >>> node = PipelineNode()
    >>> node.CLASS_NAME
    >>> node.class_name
    'PipelineNode'
    >>> node.name
    'pipelinenode'
    >>> node
    <PipelineNode: pipelinenode>

    # filliality logics
    >>> grandparent = PipelineNode(name='grandmom')
    >>> parent = PipelineNode(name='mom')
    >>> child = PipelineNode(name='boy')
    >>> [node.is_root for node in (grandparent, parent, child)]
    [True, True, True]
    >>> parent.connect(grandparent)
    >>> [node.is_root for node in (grandparent, parent, child)]
    [True, False, True]
    >>> parent.parent
    <PipelineNode: grandmom>
    >>> grandparent.children
    [<PipelineNode: mom>]
    >>> grandparent.connect(parent) # this should fail
    Traceback (most recent call last):
    ...
    ValueError: Cyclic filliation detected.
    >>> child.connect(parent)
    >>> [node.is_root for node in (grandparent, parent, child)]
    [True, False, False]
    >>> grandparent.connect(child) # again, this should fail
    Traceback (most recent call last):
    ...
    ValueError: Cyclic filliation detected.
    >>> grandparent.parent, grandparent.children 
    (None, [<PipelineNode: mom>])
    >>> parent.parent, parent.children 
    (<PipelineNode: grandmom>, [<PipelineNode: boy>])
    >>> child.parent, child.children 
    (<PipelineNode: mom>, [])
    >>> child.connect(grandparent) # switches parent from mom to grandmom
    >>> [node.is_root for node in (grandparent, parent, child)]
    [True, False, False]
    >>> grandparent.parent, grandparent.children 
    (None, [<PipelineNode: mom>, <PipelineNode: boy>])
    >>> parent.parent, parent.children 
    (<PipelineNode: grandmom>, [])
    >>> child.parent, child.children 
    (<PipelineNode: grandmom>, [])

    # pipeline specs
    >>> root = RootPipelineNode()
    >>> class LatticeSpec(PipelineSpec): pass
    >>> class SpeciesSpec(PipelineSpec): pass
    >>> class ParticleSpec(PipelineSpec): pass
    >>> class LatticeProviderNode(PipelineNode):
    ...     def get_output_spec(self):
    ...         return [LatticeSpec, SpeciesSpec]
    >>> class ParticleProviderNode(PipelineNode):
    ...     def get_output_spec(self):
    ...         return [ParticleSpec, SpeciesSpec]
    >>> class LatticeConsumerNode(PipelineNode):
    ...     def get_input_spec(self):
    ...         return [LatticeSpec, SpeciesSpec]
    >>> lat_prov = LatticeProviderNode()
    >>> pat_prov = ParticleProviderNode()
    >>> lat_prov.connect(root)
    >>> pat_prov.connect(root)
    >>> lat_cons = LatticeConsumerNode()
    >>> lat_cons.connect(lat_prov)
    >>> lat_cons.connect(pat_prov) # this should fail
    Traceback (most recent call last):
    ...
    ValueError: Parent item does not provide LatticeSpec
    
    """
    CLASS_NAME = None # subclass may override this
    INPUT_SPEC = []
    OUTPUT_SPEC = []
    
    def __init__(self, name=None):
        """Initializer.
        """
        if name is None:
            name = self.class_name.lower()
        self.name = name
        self.parent = None
        self.children = []
        self.upward_event_handlers = {}
        self.downward_event_handlers = {}
        self.observers = []

    def __repr__(self):
        """Retrurns in <class_name: instance_name> format.
        """
        return '<%s: %r>' %(self.class_name, self.name)

    def finalize(self):
        """Finalizer.
        """
        pass

    @property
    def class_name(self):
        """Returns human-friendly class name.
        """
        return self.CLASS_NAME or self.__class__.__name__

    # spec-related interfaces
    @classmethod
    def class_input_spec(cls):
        """Returns input specification. Subclass may override this.
        """
        return cls.INPUT_SPEC

    @classmethod
    def class_output_spec(cls):
        """Returns output specification. Subclass may override this.
        """
        return cls.OUTPUT_SPEC

    def get_input_spec(self):
        """Returns input specification. Subclass may override this.
        """
        return self.class_input_spec()

    def get_output_spec(self):
        """Returns output specification. Subclass may override this.
        """
        return self.class_output_spec()

    @property
    def input_spec(self):
        return self.get_input_spec()

    @property
    def output_spec(self):
        return self.get_output_spec()

    # tree node management interfaces

    @property
    def is_root(self):
        """Returns if instance is the root (has no parent). 
        """
        return self.parent is None

    @property
    def ancestors(self):
        """Returns list of all ancestors, including self.
        """
        ret = [self]
        if self.parent:
            ret.extend(self.parent.ancestors)
        return ret

    @property
    def descendants(self):
        """Returns list of all descendants, including self.
        """
        ret = [self]
        for child in self.children:
            ret.extend(child.descendants)
        return ret

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
        # **implicitly** bind child's parent
        child.parent = self
        self.children.append(child)

    def unbind_child(self, child):
        """Un-bind child from a member of children.
        """
        if child in self.children:
            # **implicitly** unbind child's parent
            child.parent = None
            self.children.remove(child)

    def connect(self, parent):
        """Connect to parent item.
        """
        # check if parent is a valid PipelineNode
        if not isinstance(parent, PipelineNode):
            raise ValueError('Cannot connect to non-PipelineNode instance.')
        # check if parent can provide appropreate data except in case
        # parent is root which should determine output spec dinamically
        if parent.is_root==False:
            for spec in self.input_spec:
                if spec not in parent.output_spec:
                    raise ValueError('Parent item does not provide %s'
                                     %(spec.__name__))
        # if already connected, disconnect first
        if self.parent:
            self.disconnect()
        parent.bind_child(self) # implicitly set self.parent

    def disconnect(self):
        """Disconnect from parent item.
        """
        if self.parent:
            self.parent.unbind_child(self) # implicitly delete self.parent

    def request_data(self, spec, **params):
        """Request parent for given spec data.
        """
        return None

    # event handling interfaces

    def handle_upward_event(self, pipeline_event):
        """Handles upstreaming pipeline event. Subclass may override.
        """
        pass # empty!

    def handle_downward_event(self, pipeline_event):
        """Handles downstreaming pipeline event. Subclass may override.
        """
        pass # empty!

    def propagate_up(self, pipeline_event):
        """Propagates event upward.
        """
        debug('%s propagating up %s' %(self.__class__.__name__, pipeline_event))
        if pipeline_event.note_visited(self):
            self.handle_upward_event(pipeline_event)
            # call for extra event handlers
            event_handlers = self.upward_event_handlers.get(pipeline_event.__class__, [])
            for event_handler in event_handlers:
                event_handler(self, pipeline_event)
        if self.parent:
            self.parent.propagate_up(pipeline_event)

    def propagate_down(self, pipeline_event):
        """Propagates event downward.
        """
        debug('%s propagating down %s' %(self.__class__.__name__, pipeline_event))
        if pipeline_event.note_visited(self):
            self.handle_downward_event(pipeline_event)
            # call for extra event handlers
            event_handlers = self.downward_event_handlers.get(pipeline_event.__class__, [])
            for event_handler in event_handlers:
                event_handler(self, pipeline_event)
            for child in self.children:
                child.propagate_down(pipeline_event)

    # observer interfaces

    def add_observer(self, observer):
        """Add an observer.
        """
        if observer not in self.observers:
            self.observers.append(observer)
            debug('>>>>> ADD: observers are now %s' %self.observers)

    def remove_observer(self, observer):
        """Remove inspector from the node.
        """
        if observer in self.observers:
            self.observers.remove(observer)
            debug('>>>>> REMOVE: observers are now %s' %self.observers)

    def internal_update(self):
        """Update internal status.
        """

    @log_call
    def status_changed(self):
        """Notifies status change (to inspectors).
        """
        self.internal_update()
        debug('%s' %self.observers)
        for observer in self.observers:
            observer.update()


class RootPipelineNode(PipelineNode):
    """Special pipeline item intended to be a root of pipeline tree.

    >>> r = RootPipelineNode()
    >>> p = PipelineNode()
    >>> r.datasource # None
    >>> r.connect(p)
    Traceback (most recent call last):
    ...
    ValueError: RootPipelineNode should always be root.
    
    """
    def __init__(self, name=None, datasource=None):
        """Initializer.
        """
        PipelineNode.__init__(self, name=name)
        self._datasource = datasource

    def get_datasource(self):
        """Property getter for datasource
        """
        return self._datasource

    def set_datasource(self, datasource):
        """Property setter for datasource
        """
        self._datasource = datasource
        debug('RootPipelineNode::datasource set to %s' %datasource)

    datasource = property(get_datasource, set_datasource)

    #def get_output_spec(self):
    @staticmethod
    def get_output_spec():
        """Returns output specification. Subclass may override this.
        """
        return [DatasourceSpec, UriSpec]

    def request_data(self, spec):
        """Returns datasource or uri
        """
        if spec is DatasourceSpec:
            return self.datasource
        elif spec is UriSpec:
            return self.datasource.uri # datasource must support this
        else:
            raise ValueError(
                '%s does not support %s'
                %(self.__class__.__name__, spec.__name__))

    def connect(self, parent):
        """RootPipelineNode denies connect().
        """
        raise ValueError('%s should always be root.' %self.__class__.__name__)

    def handle_downward_event(self, pipeline_event):
        if isinstance(pipeline_event, UpdateEvent):
            self.status_changed()


class PipelineTree(object):
    """Represents a pipeline.
    
    >>> p = PipelineTree()
    >>> p
    <PipelineTree>
    >>> p.root
    <RootPipelineNode: Root>

    """
    def __init__(self, name='Pipeline', root_name='Root', datasource=None):
        """Initializer.
        """
        self.name = name
        self.root = RootPipelineNode(name=root_name, datasource=datasource)

    def __repr__(self):
        """Returns representation.
        """
        return '<PipelineTree>'

    def propagate(self, pipeline_event):
        """Propagate down event.
        """
        self.root.propagate_down(pipeline_event)


def print_pipeline_item_tree(pipeline_item, prefix, indent):
    """Utility for printing (a part of) pipeline item tree.

    >>> foo = PipelineNode('Foo')
    >>> bar = PipelineNode('Bar')
    >>> baz = PipelineNode('Baz')
    >>> qux = PipelineNode('Qux')
    >>> bar.connect(foo)
    >>> baz.connect(bar)
    >>> qux.connect(foo)
    >>> print_pipeline_item_tree(foo, '', '  ')
    <PipelineNode: Foo>
      <PipelineNode: Bar>
        <PipelineNode: Baz>
      <PipelineNode: Qux>

    """
    print(prefix+str(pipeline_item))
    for child in pipeline_item.children:
        print_pipeline_item_tree(child, prefix+indent, indent)


def print_pipeline(pipeline, prefix='', indent='  '):
    """Utility for printing pipeline(and itspipeline item tree).

    >>> tree = PipelineTree()
    >>> foo = PipelineNode('Foo')
    >>> bar = PipelineNode('Bar')
    >>> baz = PipelineNode('Baz')
    >>> qux = PipelineNode('Qux')
    >>> quux = PipelineNode('Quux')
    >>> foo.connect(tree.root)
    >>> bar.connect(foo)
    >>> baz.connect(bar)
    >>> qux.connect(foo)
    >>> quux.connect(tree.root)
    >>> print_pipeline(tree)
    <PipelineTree>
      <RootPipelineNode: Root>
        <PipelineNode: Foo>
          <PipelineNode: Bar>
            <PipelineNode: Baz>
          <PipelineNode: Qux>
        <PipelineNode: Quux>
    
    """
    print(prefix+str(pipeline))
    print_pipeline_item_tree(pipeline.root, indent, indent)


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
