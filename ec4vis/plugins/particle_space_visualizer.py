# coding: utf-8
"""ec4vis.plugins.particle_space_visualizer --- ParticleSpace visualizer.
"""
import wx, wx.aui
import vtk
import numpy
import colorsys

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[: p.rindex(os.sep + 'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec

from ec4vis.plugins.particle_csv_loader import ParticleSpaceSpec
from ec4vis.visualizer.page import register_visualizer_page
from ec4vis.visualizer.vtk3d import Vtk3dVisualizerNode
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage
from ec4vis.visualizer.vtk3d.visual import ActorsVisual

# def create_axes(minpos, maxpos, **params):
def create_axes(bounds, **params):
    # bounds = (minpos[0], maxpos[0], minpos[1],
    #           maxpos[1], minpos[2], maxpos[2])
    ranges = bounds

    axes = vtk.vtkCubeAxesActor2D()
    axes.SetBounds(bounds)
    axes.SetRanges(ranges)
    axes.SetLabelFormat('%g')
    # axes.SetFontFactor(1.5)
    axes.UseRangesOn()
    # axes.SetCornerOffset(0.0)

    tprop = vtk.vtkTextProperty()
    if 'color' in params.keys():
        tprop.SetColor(params['color'])
    # tprop.ShadowOn()
    axes.SetAxisTitleTextProperty(tprop)
    axes.SetAxisLabelTextProperty(tprop)

    return axes

def get_new_color(idx):
    if idx < 0:
        raise ValueError
    elif idx < 6:
        return colorsys.hsv_to_rgb(idx / 6.0, 1.0, 1.0)
    elif idx < 12:
        return colorsys.hsv_to_rgb(
            (idx - 6) / 6.0 + 1.0 / 12.0, 1.0, 1.0)
    elif idx < 18:
        return colorsys.hsv_to_rgb(
            (idx - 12) / 6.0, 0.5, 1.0)
    elif idx < 24:
        return colorsys.hsv_to_rgb(
            (idx - 18) / 6.0 + 1.0 / 12.0, 0.5, 1.0)
    # else:
    return (1, 1, 1)

class ParticlesVisual(ActorsVisual):

    def __init__(self, *args, **kwargs):
        ActorsVisual.__init__(self, *args, **kwargs)

        self.particle_space = None
        self.view_scale = 1e-6
        self.color_map = {}
        self._axes = None
        self._actors_cache = {}

    def _get_actors(self):
        """override a base-class member function
        """
        for sid, actor in self._actors_cache.items():
            self._renderer.RemoveActor(actor)
        self._actors_cache.clear()

        if self.particle_space is not None:
            bounds = [numpy.inf, 0.0, numpy.inf, 0.0, numpy.inf, 0.0]
            # cmap = create_color_map(len(self.particle_space.species))
            # for i, sid in enumerate(self.particle_space.species):
            #     color = cmap[i]
            for sid in self.particle_space.species:
                if sid not in self.color_map.keys():
                    continue
                color = self.color_map[sid]

                particles = self.particle_space.list_particles(sid)
                if len(particles) == 0:
                    continue

                points = vtk.vtkPoints()
                radius = 0.0
                for pid, particle in particles:
                    points.InsertNextPoint(
                        numpy.asarray(particle.position) / self.view_scale)
                    radius = max(particle.radius / self.view_scale, radius)

                points.ComputeBounds()
                b = points.GetBounds()
                bounds = [
                    min(bounds[0], b[0]), max(bounds[1], b[1]),
                    min(bounds[2], b[2]), max(bounds[3], b[3]),
                    min(bounds[4], b[4]), max(bounds[5], b[5])]

                poly_data = vtk.vtkPolyData()
                poly_data.SetPoints(points)

                # source = vtk.vtkPointSource()
                # source.SetRadius(radius)
                source = vtk.vtkSphereSource()
                source.SetRadius(radius)

                mapper = vtk.vtkGlyph3DMapper()
                mapper.SetSourceConnection(source.GetOutputPort())
                mapper.SetInputConnection(poly_data.GetProducerPort())
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(color)
                self._actors_cache[sid] = actor

            # self._renderer.ResetCamera(bounds)
            # if self._axes is not None:
            #     self._renderer.RemoveViewProp(self._axes)
            # self._axes = create_axes(bounds)
            # self._axes.SetCamera(self._renderer.GetActiveCamera())
            # self._renderer.AddViewProp(self._axes)

        debug('actors: %s' % self._actors_cache)
        return self._actors_cache

    def reset_actors(self, data):
        for actor in self._actors_cache.values():
            self._renderer.RemoveActor(actor)
        self._actors_cache = {}

        self.particle_space = data['particle_space']
        self.view_scale = data['view_scale']
        self.color_map = data['color_map']

class ParticleSpaceVisualizerNode(Vtk3dVisualizerNode):
    """
    """
    INPUT_SPEC = [ParticleSpaceSpec]
    OUTPUT_SPEC = []

    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        Vtk3dVisualizerNode.__init__(self, *args, **kwargs)
        self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.particles_visual = ParticlesVisual(
            renderer=self.renderer, name='particles')

        self.view_scale = 1e-6
        self.sid_color_map = None

    @log_call
    def internal_update(self):
        """Reset cached particles
        """
        # self.view_scale = 1e-6
        # self.sid_color_map = None

        ps = self.fetch_particle_space()
        self.particles_visual.reset_actors(
            dict(particle_space = ps,
                 view_scale = self.view_scale,
                 color_map = self.sid_color_map))
        self.particles_visual.enable()

    @log_call
    def fetch_particle_space(self, **kwargs):
        ps = self.parent.request_data(ParticleSpaceSpec, **kwargs)
        if ps is not None:
            self.update_list(**kwargs)
        return ps

    @log_call
    def update_list(self, **kwargs):
        ps = self.parent.request_data(ParticleSpaceSpec, **kwargs)
        if ps is None:
            return

        if self.sid_color_map is None:
            self.sid_color_map = {}

        for sp in ps.species:
            if sp not in self.sid_color_map.keys():
                self.sid_color_map[sp] = get_new_color(len(self.sid_color_map))

register_pipeline_node(ParticleSpaceVisualizerNode)

class ParticleSpaceVisualizer(Vtk3dVisualizerPage):

    @log_call
    def update(self):
        self.render()

register_visualizer_page('ParticleSpaceVisualizerNode', ParticleSpaceVisualizer)

class ParticleSpaceVisualizerInspector(InspectorPage):
    """Inspector page for ParticleSpaceVisualizer.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)

        widgets = []

        self.view_scale_entry = wx.TextCtrl(
            self, wx.ID_ANY, "1e-6", style=wx.TE_PROCESS_ENTER)
        self.view_scale_entry.Bind(wx.EVT_TEXT_ENTER, self.view_scale_entry_updated)
        widgets.extend([
            (wx.StaticText(self, -1, 'Scale :'), 0, wx.ALL | wx.EXPAND),
            (self.view_scale_entry, 1, wx.ALL | wx.EXPAND)])

        element_array = []
        self.listbox = wx.CheckListBox(
            self, wx.ID_ANY, choices=element_array,
            # style=wx.LB_HSCROLL | wx.LB_NEEDED_SB | wx.LB_SORT)
            style=wx.LB_MULTIPLE | wx.LB_HSCROLL | wx.LB_NEEDED_SB | wx.LB_SORT)
        self.listbox.Bind(wx.EVT_CHECKLISTBOX, self.listbox_select)
        self.listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.doubleclick)
        # self.refresh_button = wx.Button(self, wx.ID_ANY, "Refresh")
        # self.refresh_button.Bind(wx.EVT_BUTTON, self.refresh_button_pressed)
        widgets.extend([
            (wx.StaticText(self, -1, 'Species'), 0, wx.ALL | wx.EXPAND),
            # (self.refresh_button_pressed, 0, wx.ALL | wx.EXPAND),
            (self.listbox, 1, wx.ALL | wx.EXPAND)])

        self.listbox.Bind(wx.EVT_RIGHT_DOWN, self.listbox_right_down)

        self.button = wx.Button(self, wx.ID_ANY, "save png")
        widgets.extend([
                        (self.button, 1, wx.ALL | wx.EXPAND)])
        self.button.Bind(wx.EVT_BUTTON, self.button_click)

        # pack in FlexGridSizer.
        fx_sizer = wx.FlexGridSizer(cols=2, vgap=9, hgap=25)
        fx_sizer.AddMany(widgets)
        fx_sizer.AddGrowableCol(1)
        self.sizer.Add(fx_sizer, 1, wx.EXPAND | wx.ALL, 10)

    @log_call
    def view_scale_entry_updated(self, event):
        raw_value = self.view_scale_entry.GetValue().strip()
        value = 0.0
        try:
            value = float(raw_value)
        except ValueError:
            value = 0.0

        if value > 0:
            self.view_scale_entry.ChangeValue(str(value))
            self.target.view_scale = value
            # self.target.internal_update()
            self.target.status_changed()
            for child in self.target.children:
                child.propagate_down(UpdateEvent(None))
        else:
            self.view_scale_entry.ChangeValue(str(self.target.view_scale))

    @log_call
    def refresh_button_pressed(self, event):
        self.target.sid_color_map = None
        self.target.update_list()
        self.target.status_changed()
        for child in self.target.children:
            child.propagate_down(UpdateEvent(None))

    @log_call
    def listbox_select(self, event):
        pass

    def listbox_right_down(self, event):
        popupmenu = wx.Menu()
        item1 = popupmenu.Append(-1, 'refresh')
        self.listbox.Bind(wx.EVT_MENU, self.refresh_button_pressed, item1)
        item2 = popupmenu.Append(-1, 'change colors')
        self.listbox.Bind(wx.EVT_MENU, self.doubleclick, item2)

        self.listbox.PopupMenu(popupmenu, event.GetPosition())
        popupmenu.Destroy()

    @log_call
    def doubleclick(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            newcolor = tuple(
                [float(x) / 255 for x in data.GetColour().Get()])

            # idx = event.GetInt()
            # sid = self.listbox.GetString(idx)
            for idx in self.listbox.GetSelections():
                sid = self.listbox.GetString(idx)
                self.target.sid_color_map[sid] = newcolor

            self.target.status_changed()
            for child in self.target.children:
                child.propagate_down(UpdateEvent(None))
        dlg.Destroy()

    @log_call
    def button_click(self, event):
        w2if = vtk.vtkWindowToImageFilter()
        import pdb; pdb.set_trace()
        w2if.SetInput(self.particles_visual.render)
        w2if.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName("screenshot.png")
        writer.SetInput(w2if.GetOutput())
        writer.Write()
        print "hogehoge"

    #@log_call
    def update(self):
        """Update UI.
        """
        if self.target.sid_color_map is not None:
            sp_list = self.target.sid_color_map.keys()
            sp_list.sort()
            self.listbox.Clear()
            self.listbox.SetItems(sp_list)
            for i, sid in enumerate(sp_list):
                self.listbox.Check(i, True)
                c = tuple([int(x * 255) for x in self.target.sid_color_map[sid]])
                self.listbox.SetItemForegroundColour(i, c)

register_inspector_page('ParticleSpaceVisualizerNode', ParticleSpaceVisualizerInspector)
