# coding: utf-8
"""ec4vis.plugins.particle_visualizer --- Particle visualizer.
"""
import json
import numpy
import os

import wx, wx.aui
import vtk

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec

from ec4vis.plugins.particle_constructor import ParticlesSpec, SpeciesTableSpec, WorldSizeSpec
from ec4vis.visualizer.page import register_visualizer_page
from ec4vis.visualizer.vtk3d import Vtk3dVisualizerNode
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage
from ec4vis.visualizer.vtk3d.visual import ActorsVisual


class ParticlesVisual(ActorsVisual):
    """Represents a group of particles.
    """

    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        ActorsVisual.__init__(self, *args, **kwargs)
        self.world_size = None
        self.species_table = None
        self.particles = None
        self.scaling = 1.0
        self._actors_cache = {}

    def _get_actors(self):
        """Property getter for self.actors.
        """
        if (bool(self._actors_cache)==False and
            self.species_table and self.world_size and self.particles):
            for sp_id, info in self.species_table.items():
                name = info['name']
                radius = info['radius']
                D = info['D']
                points = vtk.vtkPoints()
                for p_id, p_info in self.particles.items():
                    if p_info['species_id']==sp_id:
                        points.InsertNextPoint(p_info['position']*self.scaling/self.world_size)
                poly_data = vtk.vtkPolyData()
                poly_data.SetPoints(points)
                source = vtk.vtkSphereSource()
                source.SetRadius(radius*self.scaling/self.world_size)
                # XXX
                # XXX There've been several PolyDataSource tries...
                # XXX
                # source = vtk.vtkPointSource() 
                # source = vtk.vtkGlyphSource2D()
                # source.SetRadius(radius*self.scaling/self.world_size)
                # source = vtk.vtkDiskSource() 
                # source.SetOuterRadius(radius*self.scaling/self.world_size)
                # source.SetGlyphTypeToCircle()
                # source.SetScale(2*radius*self.scaling/self.world_size)
                mapper = vtk.vtkGlyph3DMapper()
                mapper.SetSourceConnection(source.GetOutputPort())
                mapper.SetInputConnection(poly_data.GetProducerPort())
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                self._actors_cache[sp_id] = actor
        return self._actors_cache

    def update(self, data):
        for actor in self._actors_cache.values():
            self._renderer.RemoveActor(actor)
        self._actors_cache = {}
        self.world_size = data['world_size']
        self.species_table = data['species_table']
        self.particles = data['particles']


class ParticleVisualizerNode(Vtk3dVisualizerNode):
    """
    """
    INPUT_SPEC = [ParticlesSpec, SpeciesTableSpec, WorldSizeSpec]
    OUTPUT_SPEC = []
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        Vtk3dVisualizerNode.__init__(self, *args, **kwargs)
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.particles_visual = ParticlesVisual(
            renderer = self.renderer,
            name = 'particles')

    @log_call
    def internal_update(self):
        """Reset cached particles
        """
        self.particles_visual.update(
            dict(world_size = self.parent.world_size,
                 species_table = self.parent.species_table,
                 particles = self.parent.particles))
        self.particles_visual.enable()

register_pipeline_node(ParticleVisualizerNode)


class ParticleVisualizer(Vtk3dVisualizerPage):
    """Visualizer.
    """
    @log_call
    def update(self):
        """Updates content of the rendering window.

        TODO: this method call should be handled in superclass...
        """
        self.render()

register_visualizer_page('ParticleVisualizerNode', ParticleVisualizer)


class ParticleVisualizerInspector(InspectorPage):
    """Inspector.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        """Sets UI up.
        """
        widgets = []
        # x/y/z controls
        for attr_name in ['Position', 'Focal point', 'View Up']:
            widgets.extend([wx.StaticText(self, -1, attr_name), (0, 0)])
            for i, axis_name in enumerate(['x', 'y', 'z']):
                prop_name = attr_name.lower().replace(' ', '_')+'_'+axis_name
                label = wx.StaticText(self, -1, axis_name)
                text_ctrl = wx.TextCtrl(self, -1, '', style=wx.TE_PROCESS_ENTER)
                setattr(self, prop_name+'_text', text_ctrl)
                widgets.extend([label, text_ctrl])
        # parallel scale
        self.parallel_scale_text = wx.TextCtrl(self, -1, '', style=wx.TE_PROCESS_ENTER)
        widgets.extend([
            wx.StaticText(self, -1, 'Scale'), self.parallel_scale_text])
        # event bindings for text_ctrls
        for widget in widgets:
            if isinstance(widget, wx.TextCtrl):
                self.Bind(wx.EVT_TEXT_ENTER, self.OnCameraParameterText, widget)
        # import/export buttons
        self.import_button = wx.Button(self, -1, label='Import...')
        self.export_button = wx.Button(self, -1, label='Export...')
        self.Bind(wx.EVT_BUTTON, self.OnImportButton, self.import_button)
        self.Bind(wx.EVT_BUTTON, self.OnExportButton, self.export_button)
        widgets.extend([
            wx.StaticText(self, -1, 'Import/Export'), (0, 0),
            self.import_button, self.export_button])
        # pack in FlexGridSizer.
        fx_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        fx_sizer.AddMany(widgets)
        fx_sizer.AddGrowableCol(1)
        self.sizer.Add(fx_sizer, 1, wx.EXPAND|wx.ALL, 10)
        self.update()

    def params_from_camera(self):
        """Reflects camera parameters from current active camera.
        """
        camera = self.target.renderer.GetActiveCamera()
        if camera:
            for prefix, parameter in (
                ('position_', camera.GetPosition()),
                ('focal_point_', camera.GetFocalPoint()),
                ('view_up_', camera.GetViewUp())):
                for i, axis_name in enumerate(['x', 'y', 'z']):
                    getattr(self, prefix+axis_name+'_text').SetValue(str(parameter[i]))
            self.parallel_scale_text.SetValue(str(camera.GetParallelScale()))

    @log_call
    def update(self):
        """Called on any status_change() on PipelineNode.
        """
        self.params_from_camera()
        
    @log_call
    def OnCameraParameterText(self, evt):
        """Called on TextCtrl edits.
        """
        try:
            camera = self.target.renderer.GetActiveCamera()
            # x/y/z controls
            for prefix, handler in (
                ('position_', camera.SetPosition),
                ('focal_point_', camera.SetFocalPoint),
                ('view_up_', camera.SetViewUp)):
                handler(*[
                    float(getattr(self, prefix+axis_name+'_text').GetValue())
                    for i, axis_name in enumerate(['x', 'y', 'z'])])
            # parallel scale
            camera.SetParallelScale(float(self.parallel_scale_text.GetValue()))
            self.target.status_changed(exclude_observers=[self])
        except Exception, e:
            debug('OnCameraParameterText failed due to %s' %(e))
            self.params_from_camera()

    @log_call
    def OnImportButton(self, evt):
        """Called on Import... button
        """
        dlg = wx.FileDialog(
            self, message="Open camera parameters ...", defaultDir=os.getcwd(),
            defaultFile="camera_params.json", wildcard="Json (*.json)|*.json|")
        ret = dlg.ShowModal()
        if ret==wx.ID_OK:
            path = dlg.GetPath()
            try:
                infile = open(path, 'r')
                data = json.loads(infile.read())
                infile.close()
                camera = self.target.renderer.GetActiveCamera()
                camera.SetPosition(data['position'])
                camera.SetFocalPoint(data['focal_point'])
                camera.SetViewUp(data['view_up'])
                camera.SetParallelScale(data['parallel_scale'])
                self.params_from_camera()
            except Exception, e:
                debug('Import failed due to %s' %(str(e)))

    @log_call
    def OnExportButton(self, evt):
        """Called on Export... button
        """
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="camera_params.json", wildcard="Json (*.json)|*.json|",
            style=wx.SAVE)
        ret = dlg.ShowModal()
        if ret==wx.ID_OK:
            path = dlg.GetPath()
            try:
                camera = self.target.renderer.GetActiveCamera()
                data = dict(
                    position=tuple(camera.GetPosition()),
                    focal_point=tuple(camera.GetFocalPoint()),
                    view_up=tuple(camera.GetViewUp()),
                    parallel_scale=camera.GetParallelScale())
                ofile = open(path, 'w')
                ofile.write(json.dumps(data))
                ofile.close()
            except Exception, e:
                debug('Export failed due to %s' %(str(e)))
                

register_inspector_page('ParticleVisualizerNode', ParticleVisualizerInspector)
