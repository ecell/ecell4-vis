# coding: utf-8
"""

The Visual class represents a set of actors in a visualized scene.
Visual objects can be enable()-ed or disable()-ed so that they are
added or removed from renderer.

Developers can derive Visual class to define custom visualized
entity such as raycast volumes or textured billboard particles,
accroding to specific visualization needs.

"""
from collections import OrderedDict
import vtk


class Visual(object):
    """Abstract base class for objects to be visualized.
    """

    def __init__(self, renderer=None, name=None, settings=None,
                 data=None, *args, **kwargs):
        """Initializer.
        """
        self._args = args
        self._kwargs = kwargs
        self._renderer = renderer
        self._enabled = False
        self._settings = settings
        if name is None:
            name = self.__class__.__name__
        self.name = name
        self._initialize()

    def _initialize(self):
        """Instant initializer for subclasses.
        """
        return

    def _get_enabled(self):
        """Returns if the visual is enabled."""
        return self._enabled
    def _set_enabled(self, flag):
        """Sets if the visual is enabled."""
        self._enabled = flag
    enabled = property(
        lambda self: self._get_enabled(),
        lambda self, f: self._set_enabled(f))

    def update(self, data, *args, **kwargs):
        """Updates actors. Override method, should return None.
        """
        return

    def enable(self):
        """Enable visual (registers vtk objects to renderer)"""
        return NotImplemented
                    
    def disable(self):
        """Disable visual (unregisters vtk objects on renderer)"""
        return NotImplemented

    def show(self, flag):
        """Switches display status of the visual.
        """
        if flag==self._enabled:
            return
        try:
            if flag==True:
                self.enable()
            else:
                self.disable()
        finally:
            self._enabled = flag


class ActorsVisual(Visual):
    """Visual consists of actors.
    """
    def __init__(self, *args, **kwargs):
        Visual.__init__(self, *args, **kwargs)
        
    # make sure to call subclass's _get_set(), while
    # property(_get_set) points Visual._get_set.
    def _get_actors(self):
        """Returns iterable of actors. Should return dictionary."""
        return NotImplemented
    actors = property(
        lambda self: self._get_actors())

    def enable(self):
        """Performs AddActor() for all actors within.
        """
        for actor in self.actors.values():
            try:
                self._renderer.AddActor(actor)
            except Exception, e:
                print 'EnableActor', str(e)
                pass # TBD: any error logging.

    def disable(self):
        """Performs RemoveActor() for all actors within.
        """
        for actor in self.actors.values():
            try:
                self._renderer.RemoveActor(actor)
            except:
                print 'DisableActor', str(e)
                pass # TBD: any error logging.


class StaticActorsVisual(ActorsVisual):
    """ActorsVisual with cacheing pre-generated actors.
    """
    def __init__(self, *args, **kwargs):
        ActorsVisual.__init__(self, *args, **kwargs)
        self._actors = None

    def _create_actors(self):
        """Do creation of actors."""
        return NotImplemented

    def _get_actors(self):
        if self._actors is None:
            self._actors = OrderedDict()
            self._create_actors()
        return self._actors


class MappedActorsVisual(ActorsVisual):
    """Visual of multiple actors mapped by id.
    """
    def __init__(self, *args, **kwargs):
        Visual.__init__(self, *args, **kwargs)
        # attributes common among actors.
        self._common_attributes = None
        # maps 'id' to actor
        self._actors_map = {}

    def _get_actors(self):
        return self._actors_map.values()

    def _iter_actor_attributes(self):
        """
        Generates (id, actor attributes) tuples over data.

        Subclass should override this as a generator.
        
        """
        return NotImplemented

    def _new_actor(self, **kwargs):
        """Creates new actor with given attributes.
        """
        return NotImplemented

    def _update_actor(self, actor, **kwargs):
        """Returns updated actor with given attributes.
        """
        return actor

    def _withdraw_actor(self, actor):
        """
        Withdraws actor and returns it, or None if it is deleted.

        You may 'withdraw' actor either by just deleting it,
        or by VisibilityOff(). Anyway you should always
        assume that the actor can be removed after
        calling this method.

        MappedActorVisual withdraws actor by VisibilityOff(),
        returning (invisible) actor.
        
        """
        actor.VisibilityOff()
        return actor

    def update(self, data):
        """Updates mapped actors.
        """
        visited_ids = []
        for id_, attrs in self._iter_actor_attributes():
            visited_ids.append(id_)
            actor = self._actors_map.pop(id_, None)
            if actor:
                actor = self._update_actor(actor, **attrs)
            else:
                actor = self._new_actor(**attrs)
            # update implies making it visible.
            actor.VisibilityOn()
            self._actors_map[id_] = actor
        # find unvisited actors to disable.
        for id_ in self._actors_map.keys():
            if id_ not in visited_ids:
                actor = self._actors_map.pop(id_, None)
                if actor:
                    actor = self._disable_actor(actor)
                    self._actors_map[id_] = actor


class VolumesVisual(Visual):
    """Visual containing a volumes.
    """
    def __init__(self, *args, **kwargs):
        Visual.__init__(self, *args, **kwargs)

    def _get_volumes(self):
        """Returns iterable of volumes."""
        return NotImplemented
    
    volumes = property(
        lambda self: self._get_volumes())

    def enable(self):
        """Performs AddVolume() for all actors within.
        """
        for volume in self.volumes:
            try:
                self._renderer.AddVolume(volume)
            except:
                pass # TBD: any error logging.

    def disable(self):
        """Performs RemoveVolume() for all actors within.
        """
        for volume in self.volumes:
            try:
                self._renderer.RemoveVolume(volume)
            except:
                pass # TBD: any error logging.


if __name__=='__main__':
    from doctest import *
    testmod(optionflags=ELLIPSIS)
