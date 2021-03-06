# coding: utf-8
"""ec4vis.plugins.particle_space_filter --- ParticleSpace filter plugin.
"""
import os.path
import csv
import re
import glob
import copy
from urlparse import urlparse
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[: p.rindex(os.sep + 'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import NumberOfItemsSpec
from ec4vis.plugins.particle_csv_loader import ParticleSpaceSpec
from ec4vis.plugins.particle_space import Particle, ParticleSpace

class ParticleSpaceFilterNode(PipelineNode):
    """ParticleSpace filter.
    """
    INPUT_SPEC = [ParticleSpaceSpec, NumberOfItemsSpec]
    OUTPUT_SPEC = [ParticleSpaceSpec, NumberOfItemsSpec]

    def __init__(self, *args, **kwargs):
        PipelineNode.__init__(self, *args, **kwargs)

        self.sid_list = None
        self.kwargs_cache = {}
        self.ignore_list = []
        self.max_num_particles = 10000

    @log_call
    def internal_update(self):
        """Reset cached csv data.
        """
        self.sid_list = None

    def fetch_particle_space(self, **kwargs):
        """Property getter for particle_space
        """
        self.kwargs_cache = kwargs
        particle_space = self.parent.request_data(ParticleSpaceSpec, **kwargs)

        if particle_space is None:
            return None

        if self.sid_list is None:
            self.update_list(**kwargs)

        sids = set(particle_space.species) - set(self.ignore_list)
        if len(sids) == 0:
            return None

        filtered = ParticleSpace()
        for sid in sids:
            stride = particle_space.num_particles(sid) // self.max_num_particles + 1
            for pid, particle in particle_space.list_particles(sid)[: : stride]:
                filtered.add_particle(pid, particle)
        return filtered

    def update_list(self, **kwargs):
        if self.sid_list:
            pass
        else:
            # donot refer self.particle_space here
            particle_space = self.parent.request_data(ParticleSpaceSpec, **kwargs)
            if particle_space is not None:
                self.sid_list = particle_space.species

    @log_call
    def request_data(self, spec, **kwargs):
        """Provides particle data.
        """
        if spec == NumberOfItemsSpec:
            debug('Serving NumberOfItemsSpec')
            return self.parent.request_data(NumberOfItemsSpec, **kwargs)
        elif spec == ParticleSpaceSpec:
            debug('Serving ParticleSpaceSpec')
            return self.fetch_particle_space(**kwargs)
        return None

register_pipeline_node(ParticleSpaceFilterNode)

class ParticleSpaceFilterInspector(InspectorPage):
    """Inspector page for ParticleSpaceFilter.
    """
    # PROP_NAMES = ['filename', 'mode', 'driver', 'libver', 'userblock_size',
    #               'name', 'id', 'ref', 'attrs']
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)

        widgets = []

        self.max_num_entry = wx.TextCtrl(
            self, wx.ID_ANY, "10000", style=wx.TE_PROCESS_ENTER)
        self.max_num_entry.Bind(wx.EVT_TEXT_ENTER, self.max_num_entry_updated)
        widgets.extend([
            (wx.StaticText(self, -1, 'Max #'), 0, wx.ALL | wx.EXPAND),
            (self.max_num_entry, 1, wx.ALL | wx.EXPAND)])

        element_array = []
        self.listbox = wx.CheckListBox(
            self, wx.ID_ANY, choices=element_array,
            style=wx.LB_MULTIPLE | wx.LB_HSCROLL | wx.LB_NEEDED_SB | wx.LB_SORT)
        self.listbox.Bind(wx.EVT_CHECKLISTBOX, self.listbox_select)
        widgets.extend([
            (wx.StaticText(self, -1, 'Species'), 0, wx.ALL | wx.EXPAND),
            (self.listbox, 1, wx.ALL | wx.EXPAND)])

        # pack in FlexGridSizer.
        fx_sizer = wx.FlexGridSizer(cols=2, vgap=9, hgap=25)
        fx_sizer.AddMany(widgets)
        fx_sizer.AddGrowableCol(1)
        self.sizer.Add(fx_sizer, 1, wx.EXPAND | wx.ALL, 10)

    # @log_call
    def max_num_entry_updated(self, event):
        raw_value = self.max_num_entry.GetValue().strip()
        if all(x in '0123456789' for x in raw_value):
            # convert to float and limit to 2 decimals
            value = int(raw_value)
            if value > 0:
                self.max_num_entry.ChangeValue(str(value))
                self.target.max_num_particles = value
                self.target.internal_update()
                for child in self.target.children:
                    child.propagate_down(UpdateEvent(None))
            else:
                self.max_num_entry.ChangeValue(str(self.target.max_num_particles))
        else:
            self.max_num_entry.ChangeValue(str(self.target.max_num_particles))

    @log_call
    def listbox_select(self, event):
        particle_space = self.target.parent.request_data(
            ParticleSpaceSpec, **self.target.kwargs_cache)
        if particle_space is not None:
            idx = event.GetInt()
            sid = self.listbox.GetString(idx)
            if self.listbox.IsChecked(idx):
                if sid in self.target.ignore_list:
                    self.target.ignore_list.remove(sid)
            else:
                if sid not in self.target.ignore_list:
                    self.target.ignore_list.append(sid)

            self.target.internal_update()
            for child in self.target.children:
                child.propagate_down(UpdateEvent(None))

    @log_call
    def update(self):
        """Update UI.
        """
        self.target.update_list(**self.target.kwargs_cache)
        if self.target.sid_list is not None:
            self.listbox.SetItems(self.target.sid_list)
            for i, sid in enumerate(self.target.sid_list):
                if sid not in self.target.ignore_list:
                    self.listbox.Check(i, True)

register_inspector_page('ParticleSpaceFilterNode', ParticleSpaceFilterInspector)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags = ELLIPSIS)
