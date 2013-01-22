__init__.py
----------------------
=======================
app.py
----------------------
# coding: utf-8
"""app.py -- Visualizer Application.
"""
from logging import debug
from os import getcwd

import wx

from ec4vis.browser import BrowserFrame
from ec4vis.plugins import PluginLoader
from ec4vis.settings import settings
from ec4vis.visualizer import VISUALIZER_CLASSES, VisualizerEventResponder

VERSION = (0, 0, 1)
APP_TITLE_NAME = 'E-Cell 4 Data Browser Version %d.%d.%d' %VERSION


class BrowserApp(wx.App, VisualizerEventResponder):
    """Application object for browser.
    """
    def __init__(self, *args, **kwargs):
        
        # application status
        self.visualizer = None # current visualizer
        self.settings = kwargs.pop('settings', None)
        wx.App.__init__(self, *args, **kwargs)

    def OnInit(self):
        """Integrated initialization hook.
        """
        # initialize plugins
        self.init_plugins()
        # initialize UI stuff
        self.init_ui()
        self.render_window.Render()
        return True

    def init_plugins(self):
        """Initialize plugins
        """
        # load plugins
        plugin_loader = PluginLoader()
        for i, (modpath, status) in enumerate(plugin_loader.load_iterative()):
            message = '%s ... %s' %(modpath, 'OK' if status else 'FAILED')
            # pass

    def init_ui(self):
        """Initialize UI.
        """
        # browser
        browser = BrowserFrame(None, -1, APP_TITLE_NAME, size=(1000, 600))
        workspace_panel = browser.workspace_panel
        renderer_panel = browser.renderer_panel
        render_window = renderer_panel.render_window
        # inspector_panel = browser.inspector_panel # TBD

        # outlet bindings
        self.browser = browser
        self.workspace_panel = workspace_panel
        self.workspace_tree = workspace_panel.tree_ctrl
        self.renderer_panel = renderer_panel
        if self.settings:
            render_window_panel.configure_renderer(self.settings)
        self.render_window = render_window
        self.renderer = renderer_panel.renderer

        # self.inspector_panel = inspector_panel
        
        # # outlet configurations
        # self.sources = []
        # source_model = SourceDataViewModel(self.sources)
        # # data_model = DataDataViewModel([])
        # self.update_visualizer_buttons_status()
        # # self.source_list.AssociateModel(source_model)
        # self.update_source_remove_ui_status()
        # # self.data_list.AssociateModel(data_model)
        # self.update_data_list_buttons_status()

        # menu event bindings
        menu_bar = browser.menu_bar
        app_about = menu_bar.app_about
        app_quit = menu_bar.app_quit
        workspace_set_root = menu_bar.workspace_set_root
        #workspace_save = menu_bar.workspace_save
        #workspace_save_as = menu_bar.workspace_save_as
        #workspace_load = menu_bar.workspace_load
        #workspace_remove = menu_bar.workspace_remove
        #workspace_add_file = menu_bar.workspace_add_file
        #workspace_add_loader = menu_bar.workspace_add_loader
        #workspace_add_visualizer = menu_bar.workspace_add_visualizer
        #workspace_add_filter = menu_bar.workspace_add_filter

        # menu commands
        def menu_bind(handler, menu):
            browser.Bind(wx.EVT_MENU, handler, menu)
        menu_bind(self.OnAppAboutMenu, app_about)
        menu_bind(self.OnAppQuitMenu, app_quit)
        menu_bind(self.OnWorkspaceSetRootMenu, workspace_set_root)
        #menu_bind(self.OnWorkspaceLoadMenu, workspace_load)
        #menu_bind(self.OnWorkspaceSaveMenu, workspace_save)
        #menu_bind(self.OnWorkspaceSaveAsMenu, workspace_save_as)
        #menu_bind(self.OnWorkspaceAddFileMenu, workspace_add_file)
        #menu_bind(self.OnWorkspaceAddFileMenu, workspace_add_file)

        # renderer event binding --- this is a bad hack
        def render_window_render_observer(o, e, f=renderer_panel):
            # hasattr() is to prevent AttributeError.
            """ # This is kept for demonstration use.
            if hasattr(self, 'visualizer'):
                if self.visualizer:
                    self.visualizer.update()"""
            pass
        self.render_window.AddObserver(
            "RenderEvent", render_window_render_observer)

        # assign and show top window
        self.SetTopWindow(browser)
        self.browser.Show(True)

    def finalize(self):
        """Finalizer.
        """
        pass # just a placeholder now.

    def OnAppAboutMenu(self, event):
        """Called on 'App'->'About' menu.
        """
        dlg = wx.MessageDialog(self.browser, APP_TITLE_NAME,
                               'About this application...', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAppQuitMenu(self, event):
        """Called on 'App'->'Quit' menu.
        """
        self.finalize()
        self.ExitMainLoop()

    def OnWorkspaceSetRootMenu(self, evt):
        """Called on 'Workspace'->'Set Root Direcotry...' menu.
        """
        # TBD: save current workspace to file.
        dlg = wx.DirDialog(
            self.browser,
            u'Choose root directory for workspace',
            style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST|wx.DD_CHANGE_DIR)
        ret = dlg.ShowModal()
        if ret==wx.ID_OK:
            dirname = dlg.GetPath()
            # TBD: set directory
            self.workspace_tree.set_root_directory(dirname)
            

#     def OnWorkspaceLoadMenu(self, evt):
#         """Called on 'Workspace'->'Load workspace' menu.
#         """
#         # TBD: save current workspace to file.
#         dlg = wx.FileDialog(
#             self.browser,
#             u'Choose workspace file to load',
#             style=wx.OPEN, defaultDir=getcwd())
#         ret = dlg.ShowModal()
#         if ret==wx.ID_OK:
#             filename = dlg.GetPath()
#         # TBD: saving mechanism
            
#     def OnWorkspaceSaveMenu(self, evt):
#         """Called on 'Workspace'->'Save workspace' menu.
#         """
#         # TBD: save current workspace to file.
            
#     def OnWorkspaceSaveAsMenu(self, evt):
#         """Called on 'Workspace'->'Save workspace as...' menu.
#         """
#         # TBD: save current workspace to file.
#         dlg = wx.FileDialog(
#             self.browser,
#             u'Choose workspace file to save',
#             style=wx.SAVE, defaultDir=getcwd())
#         ret = dlg.ShowModal()
#         if ret==wx.ID_OK:
#             filename = dlg.GetPath()
#         # TBD: saving mechanism
            
#     def OnWorkspaceAddFileMenu(self, evt):
#         """Called on 'Workspace'->'Add file...' menu.
#         """
#         dlg = wx.DirDialog(
#             self.browser,
#             u'Choose data directory',
#             style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST|wx.DD_CHANGE_DIR)
#         ret = dlg.ShowModal()
#         if ret==wx.ID_OK:
#             dirname = dlg.GetPath()
            

    def update_visualizer_buttons_status(self):
        """Updates enable/disable status of Reset/Configure buttons.
        """
        visualizer = self.visualizer
        can_reset = not (visualizer is None)
        has_config_ui = bool(visualizer) and visualizer.has_configuration_ui
        # self.visualizer_reset_button.Enable(can_reset)
        self.visualizer_configure_button.Enable(has_config_ui)

    def update_source_remove_ui_status(self):
        """Updates enable/disable status of UIs related removing source.
        """
        if False:
            selected = self.source_list.GetSelection()
            self.source_remove_button.Enable(bool(selected))

    def update_data_list_buttons_status(self):
        """Updates enable/disable status of UIs related removing source.
        """
        data_list = self.data_list 
        model = data_list.GetModel()
        selected = data_list.GetSelection()
        # this is hack: wxPython's DVLC lacks way-to-count-rows or something.
        n_rows = 0
        selected_row = wx.NOT_FOUND
        if selected and self.visualizer:
            # this is dirty because DVLC lacks functionality to count rows.
            selected_data_id = model.GetValue(selected, 0)
            data_objects = self.visualizer.data_objects
            n_rows = len(data_objects)
            for row_id, info in enumerate(data_objects):
                if selected_data_id==info[0]:
                    selected_row = row_id
                    break
        self.data_up_button.Enable(bool(selected and selected_row>0))
        self.data_down_button.Enable(bool(selected and (0<=selected_row<(n_rows-1))))

    def do_process_sources(self):
        self.visualizer.process_sources([uri for use, uri in self.sources])
        data_objects = self.visualizer.data_objects
        data_list = self.data_list
        new_data_model = DataDataViewModel(data_objects)
        new_data_model.AfterReset()
        old_data_model = data_list.GetModel()
        data_list.AssociateModel(new_data_model)
        del old_data_model

    def OnVisualizerResetButton(self, event):
        """Handles visualizer 'Reset' button.
        """
        if self.visualizer is None:
            return
        self.visualizer.reset()
        self.do_process_sources()

    def OnVisualizerConfigureButton(self, event):
        """Handles visualizer 'Configure' button.
        """
        self.visualizer.load_configuration_ui()

    def OnSourceAddButton(self, event):
        """Called on Add source boutton.
        """
        self.add_file_source()

    def OnSourceRemoveButton(self, event):
        """Called on Add source boutton.
        """
        selected = self.source_list.GetSelection()
        if selected:
            selected_uri = self.source_list.GetModel().GetValue(selected, 1)
            popped = None
            for i, (use, uri) in enumerate(self.sources):
                if uri==selected_uri:
                    popped = self.sources.pop(i)
                    break
            if popped:
                # this is required for yielding
                self.source_list.GetModel().AfterReset()
        self.update_source_remove_ui_status()

    def OnVisualizerChoice(self, event):
        """Called on selection of visualizer_choice changed.
        """
        selected_idx = event.GetSelection()
        if selected_idx: # not 'Select Visualizer'
            key = event.GetString()
            visualizer_class = VISUALIZER_CLASSES[key]
        else:
            visualizer_class = None
        if self.visualizer.__class__==visualizer_class:
            # do nothing if visualizer class not chaged
            return
        # detach old visualizer from application
        old_visualizer, self.visualizer = self.visualizer, None
        if old_visualizer:
            old_visualizer.finalize()
            del old_visualizer
        if visualizer_class:
            # attach new visualizer to application
            new_visualizer = visualizer_class(self, self.renderer)
            new_visualizer.initialize() # implies show()
            self.visualizer = new_visualizer
            self.do_process_sources()
            self.render_window.Render()
        self.update_visualizer_buttons_status()
        
    def OnSourceListSelectionChanged(self, event):
        """Called on selection of soruce list changed.
        """
        self.update_source_remove_ui_status()

    def OnDataListSelectionChanged(self, event):
        """Called on selection of data list changed.
        """
        model = self.data_list.GetModel()
        if model is None:
            return
        selected = self.data_list.GetSelection()
        data_id = model.GetValue(selected, 0)
        if self.visualizer is None:
            return
        self.visualizer.update(data_id)
        self.render_window.Render()
        self.update_data_list_buttons_status()

    def move_current_data(self, offset):
        """Do real job for OnDataUp/DownButton.
        """
        model = self.data_list.GetModel()
        if model is None:
            return
        selected = self.data_list.GetSelection()
        if selected is None:
            return
        if self.visualizer is None:
            return
        data_id = model.GetValue(selected, 0)
        self.visualizer.move_data_ordering(data_id, offset)
        # model.ValueChanged()
        model.AfterReset() # yield
            
    def OnDataUpButton(self, event):
        """Called on data list up button.
        """
        self.move_current_data(-1)
        
    def OnDataDownButton(self, event):
        """Called on data list down button.
        """
        self.move_current_data(+1)

    # Visualizer Event Responder methods
    def get_ui_root(self):
        # just returns browser as toplevel window
        return self.browser

    def process_sources_start(self, sender, sources):
        # show data-loading dialog
        if self.data_loader_dialog is None:
            self.data_loader_dialog = wx.ProgressDialog(
                u'Loading data...',
                u'',
                maximum=len(sources),
                parent=self.browser,
            style=wx.PD_AUTO_HIDE)
    
    def process_sources_done(self, sender, sources):
        # withdraw data-loading dialog
        if self.data_loader_dialog:
            self.data_loader_dialog.Destroy()
            wx.Yield()
            self.data_loader_dialog = None

    def process_source_done(self, sender, source, error):
        # update data-loading dialog
        print error
        if self.data_loader_dialog is None:
            return
        sources = [uri for use, uri in self.sources]
        if source in sources:
            index = sources.index(source)
            message = 'Processing %s ... %s' %(source, 'OK' if (error is None) else 'FAILED')
            self.data_loader_dialog.Update(index, message)
        

if __name__=='__main__':
    app = BrowserApp(0)
    app.MainLoop()
=======================
attic.py
----------------------
# from ecell4.utils import find_hdf5
# from ecell4.world import World
# from ecell4.particle import ParticleSpace
# from ecell4.lattice import LatticeSpace

# this is a hack
# class ParticleWorld(World):
#     SPACE_REGISTRY = (('ParticleSpace', ParticleSpace),)
# class LatticeWorld(World): 
#     SPACE_REGISTRY = (('LatticeSpace', LatticeSpace),)

# SUPPORTED_WORLDS = dict(
#     world=World, particleworld=ParticleWorld, latticeworld=LatticeWorld)


        
            
            #try:
                # h5data = find_hdf5(path, new=False)
                # format_ = h5data.attrs.get('format', '(nonexistent)')
                # WorldClass = SUPPORTED_WORLDS[format_]
                # world = WorldClass.Load(path)
                # name = world.name
                # self.browser.control_panel.data_list.Append(name, world)
            #    psss
            #except Exception, e:
            #wx.MessageBox(
            #        'Failed to load %s: %s' %(path, str(e)),
            # 'Oops!', wx.OK)


# """visualizer.py -- core visualization functionality, by Yasushi Masuda (ymasuda@accense.com)

# Taken from pd_visualizer/visualizer.py:

#     Visialization module of particles and shells
#      in HDF5 file outputed from E-Cell simulator

#     Revision 0 (2010/1/25 released)
#         First release of this module.
     
#     Revision 1 (2010/2/26 released)
#         New features:
#             - Blurry effect of particles is available.
#             - Exception class is added for visualizer.
#         Bug fixes:
#             - Fixed a bug caused that newly created Settings object has history
#               of the old objects.

#     This module uses following third-party libraries:
#       - VTK (Visualization Tool Kit)
#       - h5py (Python biding to HDF5 library)
#       - numpy (Numerical Python)
#       - FFmpeg (To make a movie from outputed snapshots)

#     Please install above libraries before use this module.

# """

# import os
# import sys
# import tempfile
# import math
# import time

# import h5py
# import vtk
# import numpy

# import domain_kind_constants
# import rgb_colors
# import default_settings
# import copy


# class VisualizerError(Exception):

#     "Exception class for visualizer"

#     def __init__(self, info):
#         self.__info = info

#     def __repr__(self):
#         return self.__info

#     def __str__(self):
#         return self.__info


# class Settings(object):

#     "Visualization setting class for Visualizer"

#     def __init__(self, user_settings_dict = None):

#         settings_dict = default_settings.__dict__.copy()

#         if user_settings_dict is not None:
#             if type(user_settings_dict) != type({}):
#                 print 'Illegal argument type for constructor of Settings class'
#                 sys.exit()
#             settings_dict.update(user_settings_dict)

#         for key, val in settings_dict.items():
#             if key[0] != '_': # Data skip for private variables in setting_dict.
#                 if type(val) == type({}) or type(val) == type([]):
#                     copy_val = copy.deepcopy(val)
#                 else:
#                     copy_val = val
#                 setattr(self, key, copy_val)

#     def __set_data(self, key, val):
#         if val != None:
#             setattr(self, key, val)

#     def set_image(self,
#                   height = None,
#                   width = None,
#                   background_color = None,
#                   file_name_format = None
#                   ):

#         self.__set_data('image_height', height)
#         self.__set_data('image_width', width)
#         self.__set_data('image_background_color', background_color)
#         self.__set_data('image_file_name_format', file_name_format)

#     def set_ffmpeg(self,
#                    movie_file_name = None,
#                    bin_path = None,
#                    additional_options = None
#                    ):
#         self.__set_data('ffmpeg_movie_file_name', movie_file_name)
#         self.__set_data('ffmpeg_bin_path', bin_path)
#         self.__set_data('ffmpeg_additional_options', additional_options)

#     def set_camera(self,
#                    forcal_point = None,
#                    base_position = None,
#                    azimuth = None,
#                    elevation = None,
#                    view_angle = None
#                    ):
#         self.__set_data('camera_forcal_point', forcal_point)
#         self.__set_data('camera_base_position', base_position)
#         self.__set_data('camera_azimuth', azimuth)
#         self.__set_data('camera_elevation', elevation)
#         self.__set_data('camera_view_angle', view_angle)

#     def set_light(self,
#                   intensity = None
#                   ):
#         self.__set_data('light_intensity', intensity)

#     def set_species_legend(self,
#                            display = None,
#                            border_display = None,
#                            location = None,
#                            height = None,
#                            width = None,
#                            offset = None
#                            ):
#         self.__set_data('species_legend_display', display)
#         self.__set_data('species_legend_border_display', border_display)
#         self.__set_data('species_legend_location', location)
#         self.__set_data('species_legend_height', height)
#         self.__set_data('species_legend_width', width)
#         self.__set_data('species_legend_offset', offset)

#     def set_time_legend(self,
#                         display = None,
#                         border_display = None,
#                         format = None,
#                         location = None,
#                         height = None,
#                         width = None,
#                         offset = None
#                         ):
#         self.__set_data('time_legend_display', display)
#         self.__set_data('time_legend_border_display', border_display)
#         self.__set_data('time_legend_format', format)
#         self.__set_data('time_legend_location', location)
#         self.__set_data('time_legend_height', height)
#         self.__set_data('time_legend_width', width)
#         self.__set_data('time_legend_offset', offset)

#     def set_wireframed_cube(self,
#                             display = None
#                             ):
#         self.__set_data('wireframed_cube_diplay', display)

#     def set_axis_annotation(self,
#                             display = None,
#                             color = None
#                             ):
#         self.__set_data('axis_annotation_display', display)
#         self.__set_data('axis_annotation_color', color)

#     def set_fluorimetry(self,
#                          display = None,
#                          axial_voxel_number = None,
#                          background_color = None,
#                          shadow_display = None,
#                          accumulation_mode = None,
#                          ):
#         self.__set_data('fluorimetry_display', display)
#         self.__set_data('fluorimetry_axial_voxel_number', axial_voxel_number)
#         self.__set_data('fluorimetry_background_color', background_color)
#         self.__set_data('fluorimetry_shadow_display', shadow_display)
#         self.__set_data('fluorimetry_accumulation_mode', accumulation_mode)

#     def add_plane_surface(self,
#                          color = None,
#                          opacity = None,
#                          origin = None,
#                          axis1 = None,
#                          axis2 = None
#                          ):

#         color_ = self.plane_surface_color
#         opacity_ = self.plane_surface_opacity
#         origin_ = self.plane_surface_origin
#         axis1_ = self.plane_surface_axis_1
#         axis2_ = self.plane_surface_axis_2

#         if color != None: color_ = color
#         if opacity != None: opacity_ = opacity
#         if origin != None: origin_ = origin
#         if axis1 != None: axis1_ = axis1
#         if axis2 != None: axis2_ = axis2

#         self.plane_surface_list.append({'color':color_,
#                                         'opacity':opacity_,
#                                         'origin':origin_,
#                                         'axis1':axis1_,
#                                         'axis2':axis2_})

#     def pfilter_func(self, particle, display_species_id, pattr):
#         return pattr

#     def pfilter_sid_map_func(self, species_id):
#         return species_id

#     def pfilter_sid_to_pattr_func(self, display_species_id):
#         return self.particle_attrs.get(display_species_id,
#                                        self.default_particle_attr)

#     def dump(self):
#         dump_list = []
#         for key in self.__slots__:
#             dump_list.append((key, getattr(self, key, None)))

#         dump_list.sort(lambda a, b:cmp(a[0], b[0]))

#         print '>>>>>>> Settings >>>>>>>'
#         for x in dump_list:
#             print x[0], ':', x[1]
#         print '<<<<<<<<<<<<<<<<<<<<<<<<'


# class Visualizer(object):

#     def __init__(self, renderer, settings, species_list, world_size):
#         assert  isinstance(settings, Settings)
#         assert world_size is not None
#         self.settings = settings
#         self.__world_size = world_size

#         self.__build_particle_attrs(species_list)
#         self.__build_domain_attrs()
#         self.renderer = renderer
#         self.__setup_renderer()

#         self.__axes = None
#         self.__cube = None
#         self.__species_legend = None
#         self.__time_legend = None
#         self.__plane_list = self.__create_planes()

#         # Create axis annotation
#         if self.settings.axis_annotation_display:
#             self.__axes = self.__create_axes()
#             self.__axes.SetCamera(self.renderer.GetActiveCamera())

#         # Create a wireframed cube
#         if self.settings.wireframed_cube_display:
#             self.__cube = self.__create_wireframe_cube()

#         # Create species legend box
#         if self.settings.species_legend_display:
#             self.__species_legend = self.__create_species_legend()

#         # Create time legend box
#         if self.settings.time_legend_display:
#             self.__time_legend = self.__create_time_legend()

#     def __get_domain_color(self, domain_kind):
#         return self.__dattrs.get \
#                 (domain_kind, self.settings.default_domain_attr)['color']

#     def __get_domain_opacity(self, domain_kind):
#         return self.__dattrs.get \
#                 (domain_kind, self.settings.default_domain_attr)['opacity']

#     def __get_legend_position(self, location, height, width, offset):
#         if location == 0:
#             return (offset, offset)
#         elif location == 1:
#             return (1.0 - width - offset, offset)
#         elif location == 2:
#             return (offset, 1.0 - height - offset)
#         elif location == 3:
#             return (1.0 - width - offset, 1.0 - height - offset)
#         else:
#             raise VisualizerError('Illegal legend position: %d' % location)

#     def __create_planes(self):
#         plane_list = []
#         scaling = self.settings.scaling
#         for x in self.settings.plane_surface_list:
#             actor = vtk.vtkActor()
#             plane = vtk.vtkPlaneSource()
#             plane.SetOrigin(x['origin'] * scaling)
#             plane.SetPoint1(x['axis1'] * scaling)
#             plane.SetPoint2(x['axis2'] * scaling)

#             mapper = vtk.vtkPolyDataMapper()
#             mapper.SetInput(plane.GetOutput())

#             actor.SetMapper(mapper)
#             prop = actor.GetProperty()
#             prop.SetColor(x['color'])
#             prop.SetOpacity(x['opacity'])
#             plane_list.append(actor)

#         return plane_list

#     def __build_particle_attrs(self, species_list):
#         # Data transfer of species dataset to the dictionary
#         species_dict = {}
#         species_idmap = {}
#         for species in species_list:
#             species_id = species['id']
#             display_species_id = self.settings.pfilter_sid_map_func(species_id)
#             if display_species_id is not None:
#                 species_idmap[species_id] = display_species_id
#                 species_dict[species_id] = dict((species.dtype.names[i], v) for i, v in enumerate(species))

#         # Delete duplicated numbers by set constructor
#         self.__species_idmap = species_idmap
#         self.__reverse_species_idmap = dict((v, k) for k, v in species_idmap.iteritems())

#         # Set particle attributes
#         self.__pattrs = {}
#         nondisplay_species_idset = set()

#         for species_id, display_species_id in self.__reverse_species_idmap.iteritems():
#             # Get default color and opacity from default_settings
#             _def_attr = self.settings.pfilter_sid_to_pattr_func(display_species_id)
#             if _def_attr is not None:
#                 def_attr = dict(_def_attr)
#                 def_attr.update(species_dict[species_id])
#                 self.__pattrs[display_species_id] = def_attr

#         self.__mapped_species_idset = self.__pattrs.keys()

#     def __build_domain_attrs(self):
#         self.__dattrs = self.settings.domain_attrs

#     def __create_camera(self):
#         # Create a camera
#         camera = vtk.vtkCamera()

#         camera.SetFocalPoint(
#             numpy.array(self.settings.camera_focal_point) *
#             self.settings.scaling)
#         camera.SetPosition(numpy.array(self.settings.camera_base_position) *
#             self.settings.scaling)

#         camera.Azimuth(self.settings.camera_azimuth)
#         camera.Elevation(self.settings.camera_elevation)
#         camera.SetViewAngle(self.settings.camera_view_angle)
#         return camera

#     def __add_lights_to_renderer(self, renderer):
#         # Create a automatic light kit
#         light_kit = vtk.vtkLightKit()
#         light_kit.SetKeyLightIntensity(self.settings.light_intensity)
#         light_kit.AddLightsToRenderer(renderer)

#     def __setup_renderer(self):
#         self.renderer.SetViewport(0.0, 0.0, 1., 1.)
#         self.renderer.SetActiveCamera(self.__create_camera())
#         self.renderer.SetBackground(self.settings.image_background_color)
#         self.__add_lights_to_renderer(self.renderer)

#     def __create_axes(self):
#         axes = vtk.vtkCubeAxesActor2D()
#         axes.SetBounds(numpy.array([0.0, 1.0, 0.0, 1.0, 0.0, 1.0]) * self.settings.scaling)
#         axes.SetRanges(0.0, self.__world_size,
#                               0.0, self.__world_size,
#                               0.0, self.__world_size)
#         axes.SetLabelFormat('%g')
#         axes.SetFontFactor(1.5)
#         tprop = vtk.vtkTextProperty()
#         tprop.SetColor(self.settings.axis_annotation_color)
#         tprop.ShadowOn()
#         axes.SetAxisTitleTextProperty(tprop)
#         axes.SetAxisLabelTextProperty(tprop)
#         axes.UseRangesOn()
#         axes.SetCornerOffset(0.0)

#         return axes

#     def __create_wireframe_cube(self):
#         cube = vtk.vtkCubeSource()
#         scaling = self.settings.scaling
#         cube.SetBounds(numpy.array([0.0, 1.0, 0.0, 1.0, 0.0, 1.0]) * scaling)
#         cube.SetCenter(numpy.array([0.5, 0.5, 0.5]) * scaling)

#         mapper = vtk.vtkPolyDataMapper()
#         mapper.SetInputConnection(cube.GetOutputPort())

#         actor = vtk.vtkActor()
#         actor.SetMapper(mapper)
#         actor.GetProperty().SetRepresentationToWireframe()
#         return actor

#     def __create_time_legend(self):
#         time_legend = vtk.vtkLegendBoxActor()

#         # Create legend actor
#         time_legend.SetNumberOfEntries(1)
#         time_legend.SetPosition(
#             self.__get_legend_position(
#                 self.settings.time_legend_location,
#                 self.settings.time_legend_height,
#                 self.settings.time_legend_width,
#                 self.settings.time_legend_offset))

#         time_legend.SetWidth(self.settings.time_legend_width)
#         time_legend.SetHeight(self.settings.time_legend_height)

#         tprop = vtk.vtkTextProperty()
#         tprop.SetColor(rgb_colors.RGB_WHITE)
#         tprop.SetVerticalJustificationToCentered()
#         time_legend.SetEntryTextProperty(tprop)

#         if self.settings.time_legend_border_display:
#             time_legend.BorderOn()
#         else:
#             time_legend.BorderOff()
#         return time_legend

#     def __create_species_legend(self):
#         species_legend = vtk.vtkLegendBoxActor()
#         # Get number of lines
#         legend_line_numbers = len(self.__mapped_species_idset) \
#                             + len(domain_kind_constants.DOMAIN_KIND_NAME)

#         # Create legend actor
#         species_legend.SetNumberOfEntries(legend_line_numbers)
#         species_legend.SetPosition(
#             self.__get_legend_position(
#                 self.settings.species_legend_location,
#                 self.settings.species_legend_height,
#                 self.settings.species_legend_width,
#                 self.settings.species_legend_offset))
#         species_legend.SetWidth(self.settings.species_legend_width)
#         species_legend.SetHeight(self.settings.species_legend_height)

#         tprop = vtk.vtkTextProperty()
#         tprop.SetColor(rgb_colors.RGB_WHITE)
#         tprop.SetVerticalJustificationToCentered()

#         species_legend.SetEntryTextProperty(tprop)

#         if self.settings.species_legend_border_display:
#             species_legend.BorderOn()
#         else:
#             species_legend.BorderOff()

#         # Entry legend string to the actor
#         sphere = vtk.vtkSphereSource()

#         # Create legends of particle speices
#         count = 0
#         for species_id in self.__mapped_species_idset:
#             species_legend.SetEntryColor \
#                 (count, self.__pattrs[species_id]['color'])
#             species_legend.SetEntryString \
#                 (count, self.__pattrs[species_id]['name'])
#             species_legend.SetEntrySymbol(count, sphere.GetOutput())
#             count += 1

#         # Create legends of shell spesies
#         offset = count
#         count = 0
#         for kind, name in domain_kind_constants.DOMAIN_KIND_NAME.items():
#             species_legend.SetEntryColor \
#                 (offset + count, self.__get_domain_color(kind))
#             species_legend.SetEntrySymbol \
#                 (offset + count, sphere.GetOutput())
#             species_legend.SetEntryString(offset + count, name)
#             count += 1
#         return species_legend

#     def __render_particles(self, particles_dataset):
#         # Data transfer from HDF5 dataset to numpy array for fast access
#         scaling = self.settings.scaling
#         species_id_idx = particles_dataset.dtype.names.index('species_id')
#         position_idx = particles_dataset.dtype.names.index('position')

#         for x in particles_dataset:
#             display_species_id = self.__species_idmap.get(x[species_id_idx])
#             if display_species_id is None:
#                 continue
#             pattr = self.__pattrs.get(display_species_id)
#             if pattr is None:
#                 continue
#             pattr = self.settings.pfilter_func(x, display_species_id, pattr)
#             if pattr is not None:
#                 sphere = vtk.vtkSphereSource()
#                 sphere.SetRadius(scaling * pattr['radius'] / self.__world_size)
#                 sphere.SetCenter(scaling * x[position_idx] / self.__world_size)

#                 mapper = vtk.vtkPolyDataMapper()
#                 mapper.SetInput(sphere.GetOutput())

#                 sphere_actor = vtk.vtkActor()
#                 sphere_actor.SetMapper(mapper)
#                 sphere_actor.GetProperty().SetColor(pattr['color'])
#                 sphere_actor.GetProperty().SetOpacity(pattr['opacity'])

#                 self.renderer.AddActor(sphere_actor)

#     def __render_blurry_particles(self, particles_dataset):
#         particles_per_species = dict((k, vtk.vtkPoints()) for k in self.__species_idmap.iterkeys())

#         scaling = self.settings.scaling

#         position_idx = particles_dataset.dtype.names.index('position')
#         species_id_idx = particles_dataset.dtype.names.index('species_id')
#         for p in particles_dataset:
#             pos = p[position_idx]
#             display_species_id = self.__species_idmap.get(p[species_id_idx])
#             if display_species_id is None:
#                 continue
#             particles_per_species[display_species_id].InsertNextPoint(
#                 pos * scaling / self.__world_size)

#         nx = ny = nz = self.settings.fluorimetry_axial_voxel_number

#         for display_species_id, points in particles_per_species.iteritems():
#             poly_data = vtk.vtkPolyData()
#             poly_data.SetPoints(points)
#             poly_data.ComputeBounds()

#             pattr = self.__pattrs[display_species_id]
#             # Calc standard deviation of gauss distribution function
#             wave_length = pattr['fluorimetry_wave_length']
#             sigma = scaling * 0.5 * wave_length / self.__world_size

#             # Create guassian splatter
#             gs = vtk.vtkGaussianSplatter()
#             gs.SetInput(poly_data)
#             gs.SetSampleDimensions(nx, ny, nz)
#             gs.SetRadius(sigma)
#             gs.SetExponentFactor(-.5)
#             gs.ScalarWarpingOff()
#             gs.SetModelBounds([-sigma, scaling + sigma] * 3)
#             gs.SetAccumulationModeToMax()

#             # Create filter for volume rendering
#             filter = vtk.vtkImageShiftScale()
#             # Scales to unsigned char
#             filter.SetScale(255. * pattr['fluorimetry_brightness'])
#             filter.ClampOverflowOn()
#             filter.SetOutputScalarTypeToUnsignedChar()
#             filter.SetInputConnection(gs.GetOutputPort())

#             mapper = vtk.vtkFixedPointVolumeRayCastMapper()
#             mapper.SetInputConnection(filter.GetOutputPort())

#             volume = vtk.vtkVolume()
#             property = volume.GetProperty() # vtk.vtkVolumeProperty()
#             color = pattr['fluorimetry_luminescence_color']
#             color_tfunc = vtk.vtkColorTransferFunction()
#             color_tfunc.AddRGBPoint(0, color[0], color[1], color[2])
#             property.SetColor(color_tfunc)
#             opacity_tfunc = vtk.vtkPiecewiseFunction()
#             opacity_tfunc.AddPoint(0, 0.0)
#             opacity_tfunc.AddPoint(255., 1.0)
#             property.SetScalarOpacity(opacity_tfunc)
#             property.SetInterpolationTypeToLinear()

#             if self.settings.fluorimetry_shadow_display:
#                 property.ShadeOn()
#             else:
#                 property.ShadeOff()

#             volume.SetMapper(mapper)

#             self.renderer.AddVolume(volume)

#     def __render_shells(self,
#                         shells_dataset,
#                         domain_shell_assoc,
#                         domains_dataset):

#         # Data transfer from HDF5 dataset to numpy array for fast access
#         shells_array = numpy.zeros(shape = shells_dataset.shape,
#                                    dtype = shells_dataset.dtype)

#         shells_dataset.read_direct(shells_array)

#         # Construct assosiaction dictionary
#         domain_shell_assoc_array = numpy.zeros(shape = domain_shell_assoc.shape,
#                                                dtype = domain_shell_assoc.dtype)

#         domain_shell_assoc.read_direct(domain_shell_assoc_array)
#         domain_shell_assoc_dict = dict(domain_shell_assoc_array)

#         # Construct domains dictionary
#         domains_array = numpy.zeros(shape = domains_dataset.shape,
#                                     dtype = domains_dataset.dtype)

#         domains_dataset.read_direct(domains_array)
#         domains_dict = dict(domains_array)

#         # Add shell actors
#         for x in shells_array:

#             shell_id = x['id']

#             try:
#                 domain_id = domain_shell_assoc_dict[shell_id]
#             except KeyError:
#                 raise VisualizerError \
#                     ('Illegal shell_id is found in dataset of domain_shell_association!')

#             try:
#                 domain_kind = domains_dict[domain_id]
#             except KeyError:
#                 raise VisualizerError \
#                     ('Illegal domain_id is found in domains dataset!')

#             if self.__get_domain_opacity(domain_kind) > 0.0:

#                 sphere = vtk.vtkSphereSource()
#                 sphere.SetRadius(x['radius'] / self.__world_size)
#                 sphere.SetCenter(x['position'][0] / self.__world_size,
#                                  x['position'][1] / self.__world_size,
#                                  x['position'][2] / self.__world_size)

#                 mapper = vtk.vtkPolyDataMapper()
#                 mapper.SetInput(sphere.GetOutput())

#                 sphere_actor = vtk.vtkActor()
#                 sphere_actor.SetMapper(mapper)
#                 sphere_actor.GetProperty().SetColor \
#                     (self.__get_domain_color(domain_kind))
#                 sphere_actor.GetProperty().SetRepresentationToWireframe()
#                 sphere_actor.GetProperty().SetOpacity \
#                     (self.__get_domain_opacity(domain_kind))

#                 self.renderer.AddActor(sphere_actor)

#     def __reset_actors(self):
#         self.renderer.RemoveAllViewProps()

#         if self.__axes is not None:
#             self.renderer.AddViewProp(self.__axes)

#         if self.__cube is not None:
#             self.renderer.AddActor(self.__cube)

#         if self.__species_legend is not None:
#             self.renderer.AddActor(self.__species_legend)

#         if self.__time_legend is not None:
#             self.renderer.AddActor(self.__time_legend)

#         for plane in self.__plane_list:
#             self.renderer.AddActor(plane)

#     def render(self, t, particles_dataset, shells_dataset=None,
#                domain_shell_assoc=None, domains_dataset=None):
#         self.__reset_actors()
#         if self.__time_legend is not None:
#             self.__time_legend.SetEntryString(0,
#                 self.settings.time_legend_format % t)

#         if self.settings.fluorimetry_display:
#             self.__render_blurry_particles(particles_dataset)
#         else:
#             if self.settings.render_particles:
#                 self.__render_particles(particles_dataset)

#             if self.settings.render_shells and shells_dataset is not None:
#                 self.__render_shells(shells_dataset,
#                                      domain_shell_assoc,
#                                      domains_dataset)


# # coding: utf-8
# """settings.py --- Settings classes.
# """

# class SettingsError(Exception):
#     """Settings related error.
#     """
#     pass


# class Field(object):
#     """Descriptor field.
#     """
#     def __init__(self, default=None, *args, **kwargs):
#         """Initializer.
#         """
#         self.value = default
    
#     def __get__(self):
#         """Descriptor __get__.
#         """
#         return self.value

#     def __set__(self, value):
#         """Descriptor __set__.
#         """
#         self.value = self.safe_cast(value)

#     def safe_cast(self, value):
#         """Cast value to field's storage type. Subclass should override.
#         """
#         return value

#     def from_string(self, svalue):
#         """Value from string. Subclass may override.
#         """
#         return self.safe_cast(svalue)

#     def to_string(self):
#         """Value to string. Subclass may override.
#         """
#         return str(self.value)


# class Settings(object):
#     """Settings.
#     """
#     def __init__(self, **kwargs):
#         """Initializer.
#         """
#         self.update(kwargs)

#     def save(self, filepath):
#         """Save settings to a file.
#         """
#         settings_file = None
#         try:
#             settings_file = open(filepath, 'wb')
            
#         except IOError:
#             raise
#         finally:
#             settings_file.close()

#     def load(self, filepath):
#         """Load settings from a file.
#         """
#         settings_file = None
#         try:
#             settings_file = open(filepath, 'rb')
#         except IOError:
#             raise
#         finally:
#             settings_file.close()

#     def update(self, settings):
#         """Update fields with given dictionary.
#         """
#         for key, value in settings:
#             field = getattr(self, key, None)
#             if field:
#                 field.__set__(value)


# if __name__=='__main__':
#     from doctest import testmod, ELLIPSIS
#     testmod(optionflags=ELLIPSIS)

# from wx.lib.mixins import treemixin


# class WorkspaceTreeModel(object):
#     ''' TreeModel holds the domain objects that are shown in the different
#     tree controls. Each domain object is simply a two-tuple consisting of
#     a label and a list of child tuples, i.e. (label, [list of child tuples]). 
#     '''
#     def __init__(self, *args, **kwargs):
#         self.items = []
#         self.itemCounter = 0
#         super(WorkspaceTreeModel, self).__init__(*args, **kwargs)

#     def GetItem(self, indices):
#         text, children = 'Hidden root', self.items
#         for index in indices:
#             text, children = children[index]
#         return text, children

#     def GetText(self, indices):
#         return self.GetItem(indices)[0]

#     def GetChildren(self, indices):
#         return self.GetItem(indices)[1]

#     def GetChildrenCount(self, indices):
#         return len(self.GetChildren(indices))

#     def SetChildrenCount(self, indices, count):
#         children = self.GetChildren(indices)
#         while len(children) > count:
#             children.pop()
#         while len(children) < count:
#             children.append(('item %d'%self.itemCounter, []))
#             self.itemCounter += 1

#     def MoveItem(self, itemToMoveIndex, newParentIndex):
#         itemToMove = self.GetItem(itemToMoveIndex)
#         newParentChildren = self.GetChildren(newParentIndex)
#         newParentChildren.append(itemToMove)
#         oldParentChildren = self.GetChildren(itemToMoveIndex[:-1])
#         oldParentChildren.remove(itemToMove)


# class WorkspaceTreeMixin(treemixin.VirtualTree, treemixin.DragAndDrop, 
#                     treemixin.ExpansionState):
#     """Tree Mixin.
#     """
#     def __init__(self, *args, **kwargs):
#         self.model = kwargs.pop('treemodel')
#         self.log = kwargs.pop('log')
#         super(WorksspaceTreeMixin, self).__init__(*args, **kwargs)
#         self.CreateImageList()

#     def CreateImageList(self):
#         size = (16, 16)
#         self.imageList = wx.ImageList(*size)
#         for art in wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE:
#             self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER, 
#                                                         size))
#         self.AssignImageList(self.imageList)

#     def OnGetItemText(self, indices):
#         return self.model.GetText(indices)

#     def OnGetChildrenCount(self, indices):
#         return self.model.GetChildrenCount(indices)

#     def OnGetItemFont(self, indices):
#         # Show how to change the item font. Here we use a small font for
#         # items that have children and the default font otherwise.
#         if self.model.GetChildrenCount(indices) > 0:
#             return wx.SMALL_FONT
#         else:
#             return super(DemoTreeMixin, self).OnGetItemFont(indices)

#     def OnGetItemTextColour(self, indices):
#         # Show how to change the item text colour. In this case second level
#         # items are coloured red and third level items are blue. All other
#         # items have the default text colour.
#         if len(indices) % 2 == 0:
#             return wx.RED
#         elif len(indices) % 3 == 0:
#             return wx.BLUE
#         else:
#             return super(DemoTreeMixin, self).OnGetItemTextColour(indices)

#     def OnGetItemBackgroundColour(self, indices):
#         # Show how to change the item background colour. In this case the
#         # background colour of each third item is green.
#         if indices[-1] == 2:
#             return wx.GREEN
#         else: 
#             return super(DemoTreeMixin, 
#                          self).OnGetItemBackgroundColour(indices)

#     def OnGetItemImage(self, indices, which):
#         # Return the right icon depending on whether the item has children.
#         if which in [wx.TreeItemIcon_Normal, wx.TreeItemIcon_Selected]:
#             if self.model.GetChildrenCount(indices):
#                 return 0
#             else:
#                 return 2
#         else:
#             return 1

#     def OnDrop(self, dropTarget, dragItem):
#         dropIndex = self.GetIndexOfItem(dropTarget)
#         dropText = self.model.GetText(dropIndex)
#         dragIndex = self.GetIndexOfItem(dragItem)
#         dragText = self.model.GetText(dragIndex)
#         """self.log.write('drop %s %s on %s %s'%(dragText, dragIndex,
#             dropText, dropIndex))"""
#         self.model.MoveItem(dragIndex, dropIndex)
#         self.GetParent().RefreshItems()


# # WorkspaceTree uses WorkspaceModel instance as an internal data model.
# # See workspace.py for details.


# class WorkspaceTree(WorkspaceTreeMixin, wx.TreeCtrl):
#     """TreeCtrl for workspace.
#     """
    
#     def __init__(self, *args, **kwargs):
#         wx.TreeCtrl.__init__(self, *args, **kwargs)
#         self.AddRoot(os.getcwd())
#         self._model = None

#     def set_root_directory(self, path):
#         """Set root directory path.
#         """
#         self.DeleteAllItems()
#         self.AddRoot(path)

#     def set_model(self, model):
#         """Bind model to the tree.
#         """
#         self._model = model
#         self.refresh()

#     def get_model(self):
#         return self._model

#     model = property(get_model, set_model)

#     def refresh(self):
#         """Refresh tree content to reflect given model.
#         """
#         for node_type in ['file', 'loader', 'filter', 'visualizer',
#                           'visual', 'parameter', 'frame']:
#             parent_node = getattr(self, node_type+'_node', None)
#             node_add_handler = getattr(self, 'add_'+node_type+'_node')
#             if parent_node and node_add_handler:
#                 self.DeleteChildren(parent_node)
#                 for subnode_info in getattr(self._model, node_type, []):
#                     node_add_handler(subnode_info)

=======================
attic_settings.py
----------------------
#-----------------------------
# Species legend settings
#-----------------------------
species_legend_display = True
species_legend_border_display = True
species_legend_location = 0 # 0:left botttom, 1:right bottom, 2:left top, 3:right top
species_legend_height = 0.2 # This is normalized to image height.
species_legend_width = 0.1 # This is normalized to image width.
species_legend_offset = 0.005

#-----------------------------
# Time legend settings
#-----------------------------
time_legend_display = True
time_legend_border_display = True
time_legend_format = 'time = %g'
time_legend_location = 1  # 0:left botttom, 1:right bottom, 2:left top, 3:right top
time_legend_height = 0.05 # This is normalized to image height.
time_legend_width = 0.15 # This is normalized to image width.
time_legend_offset = 0.005

#-----------------------------
# Wireframed cube
#-----------------------------
wireframed_cube_display = True

#-----------------------------
# Axis annotation
#-----------------------------
axis_annotation_display = True
axis_annotation_color = RGB_WHITE

#-----------------------------
# Surface object: plane
#-----------------------------
plane_surface_color = RGB_WHITE
plane_surface_opacity = 1.0
# Original point of plane  (This unit is world_size)
plane_surface_origin = (0, 0, 0)
# Axis 1 of plane (This unit is world_size)
plane_surface_axis_1 = (1, 0, 0)
# Axis 2 of plane (This unit is world_size)
plane_surface_axis_2 = (0, 1, 0)

plane_surface_list = []

#-----------------------------
# Fluorimetry 2D settings
#-----------------------------
# View direction from camera position
fluori2d_view_direction=(0.0, 0.0, 0.0)

# Focus depth form camera position
fluori2d_depth=1.0

# Focus plane point
fluori2d_point=(0.0, 0.0, 0.0)

# Normal vector of focus plane
fluori2d_normal_direction=(1.0, 0.0, 0.0)

# Cut off distance
fluori2d_cutoff=1.0e-10

# Range of point spreading function
fluori2d_psf_range=1.0e-10

# Base time length for evaluating strength.
#fluori2d_base_time=1.0e-7

# Image file name
fluori2d_file_name_format='fluori2d_%04d.png'



=======================
browser.py
----------------------
# coding: utf-8
"""browser.py -- Browser window in visualizer application
"""
from logging import debug

import wx
import wx.aui
from ec4vis import *

from renderer_panel import RendererPanel
from workspace_panel import WorkspacePanel
from pipeline_panel import PipelinePanel
from inspector_panel import InspectorPanel
from menu_bar import AppMenuBar
        

class BrowserFrame(wx.Frame):
    """Browser window.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Frame.__init__(self, *args, **kwargs)
        # workspace panel
        workspace_panel = WorkspacePanel(self, -1)
        # pipeline panel
        pipeline_panel = PipelinePanel(self, -1)
        # renderer panel
        renderer_panel = RendererPanel(self, -1)
        # inspector panel
        inspector_panel = InspectorPanel(self, -1)
        # menu
        menu_bar = AppMenuBar(self)
        # aui manager
        aui_manager = wx.aui.AuiManager()
        aui_manager.SetManagedWindow(self)
        aui_manager.AddPane(pipeline_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('pipeline')
                            .Caption('Pipeline')
                            .BestSize((200, -1))
                            .Left())
        aui_manager.AddPane(workspace_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('workspace')
                            .Caption('Workspace')
                            .Left())
        aui_manager.AddPane(wx.Panel(self, -1),
                            wx.aui.AuiPaneInfo()
                            .Name('console')
                            .Caption('Console')
                            .BestSize((-1, 100))
                            .Bottom())
        aui_manager.AddPane(renderer_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('vtk window')
                            .Caption('Particles preview')
                            .Center())
        aui_manager.AddPane(inspector_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('inspector')
                            .Caption('Inspector')
                            .BestSize((200, -1))
                            .Right())
        aui_manager.Update()
        # bindings
        self.aui_manager = aui_manager
        self.workspace_panel = workspace_panel
        self.renderer_panel = renderer_panel
        # self.inspector_panel = inspector_panel
        self.menu_bar = menu_bar

    def OnClose(self, evt):
        self.aui_manager.UnInit()
        del self.aui_manager
        self.Destroy()


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = BrowserFrame(None, -1, u'Browser Frame Demo')
            frame.Show(True)
            # frame.aui_manager.Upodate()
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
=======================
control_panel.py
----------------------
# coding: utf-8
"""control_panel.py --- Control panel in visualizer application.
"""
import wx
from visualizer_panel import VisualizerPanel


class ControlPanel(wx.Panel):
    """Control panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # visualizer control
        visualizer_panel = VisualizerPanel(self, -1)
        # name bindings
        self.visualizer_panel = visualizer_panel
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.SetMinSize((300, -1))
        self.SetSize((300, 600))
        self.SetSizer(root_sizer)
        self.Layout()


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visual Panel Demo')
            control_panel = ControlPanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(control_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
=======================
data_panel.py
----------------------
# coding: utf-8
"""data_panel.py --- Control panel in visualizer application.
"""
import wx
from visualizer_panel import VisualizerPanel


class DataPanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # visualizer control
        tree_panel = wx.TreeCtrl(self, -1, style=wx.SUNKEN_BORDER)
        tree_panel.AddRoot("WorkSpace")
        # name bindings
        self.tree_panel = tree_panel
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(tree_panel, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.SetMinSize((300, -1))
        self.SetSize((300, 600))
        self.SetSizer(root_sizer)
        self.Layout()


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visual Panel Demo')
            data_panel = DataPanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(data_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
=======================
default_settings.py
----------------------
# coding: utf-8
"""default_settings.py --- default settings for vizualizer application.
"""
from rgb_colors import *

#-----------------------------
# General settings
#-----------------------------
ignore_open_errors = False
offscreen_rendering = False
scaling = 1

#-----------------------------
# Output image settings
#-----------------------------
image_height = 640
image_width = 640
image_background_color = RGB_LIGHT_SLATE_GRAY
image_file_name_format = 'image_%04d.png' # Must be compatible with FFmpeg's input-file notation

#-----------------------------
# FFMPEG command settings
#-----------------------------
# FFMPEG binary path (ex.'/usr/local/bin/ffmpeg')
# For empty string, trace back to $PATH.
ffmpeg_bin_path = 'ffmpeg'

#FFMPEG FPS
ffmpeg_movie_fps = 5 #5-30

#FFMPEG option (over write value of default_setting module)
#(Please specify FFMPEG's options except FPS and IO-filename option.)
ffmpeg_additional_options = '-sameq '

#-----------------------------
# movie time setting
#-----------------------------
frame_start_time = 0.0
frame_end_time = None
frame_interval = 1.0e-7
exposure_time = frame_interval

#-----------------------------
# Camera settings
#-----------------------------
# Focal point of x,y,z (This unit is world_size)
camera_focal_point = (0.5, 0.5, 0.5)

# Base position of x,y,z (This unit is world_size)
camera_base_position = (-2.0, 0.5, 0.5)

# Movement along azimuth direction from base position [degree]
camera_azimuth = 0.0

# Elevation from base position [degree]
camera_elevation = 0.0

# View angle [degree]
camera_view_angle = 45.0

# Zoom Zoom-in > 1.0 > Zoom-out
camera_zoom = 1.0

# Set Projection, Perspective=False or Parallel=True
camera_parallel_projection = False

#-----------------------------
# Light settings
#-----------------------------
light_intensity = 1.0

# attic
render_particles = True
render_shells = True

=======================
file_group.py
----------------------
# coding: utf-8
"""file_group.py --- represents a group of file (in a directory).
"""
from glob import glob
from os.path import exists

from workspace import WorkspaceEntity


class FileGroup(WorkspaceEntity):
    """Represents a group of file (in a directory).

    >>> fg = FileGroup()
    >>> fg.label
    u'FileGroup'
    >>> fg.directory # returns None
    >>> fg.props
    {'directory': None}
    >>> fg.is_valid
    False
    >>> from os.path import abspath, dirname
    >>> fg.directory = dirname(abspath('.')) # this directory should exist
    >>> fg.is_valid
    True
    
    """
    def __init__(self, label='FileGroup', **props):
        """Initializer.
        """
        WorkspaceEntity.__init__(self, label, **props)
        self.props.setdefault('directory', None)

    def _get_directory(self):
        return self.props['directory']

    def _set_directory(self, directory):
        self.props['directory'] = directory

    directory = property(_get_directory, _set_directory)
    
    def do_is_valid(self):
        return (bool(self.directory) and exists(self.directory))

    def list_files(self):
        return glob(self.directory)


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
=======================
inspector_panel.py
----------------------
# coding: utf-8
"""inspector_panel.py --- Inspector panel in visualizer application.
"""
import wx


class InspectorPanel(wx.Panel):
    """Inspector panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Inspector Panel Demo')
            inspector_panel = InspectorPanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(inspector_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
=======================
loader.py
----------------------
# coding: utf-8
"""loader.py --- represents a file laader.
"""
from workspace import WorkspaceEntity


class Loader(WorkspaceEntity):
    """Represents a file loader.
    """
    def __init__(self, label='Loader', **props):
        """Initializer.
        """
        WorkspaceEntity.__init__(self, label, **props)
        self.props.setdefault('input', None)

    def do_is_valid(self):
        return (bool(self.directory) and exists(self.directory))

    def list_files(self):
        return glob(self.directory)


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
=======================
menu_bar.py
----------------------
# coding: utf-8
"""menubar.py --- Application menubar.
"""
import wx


MENU_STRUCTURE = (
    # section_name, section_info
    ('App', (
        # attr_bit, label, accel_key, tip
        ('about', 'About', '', 'About this application.'),
        ('quit', 'Quit', 'Ctrl-Q', 'Quit application'),
        )),
    ('Workspace', (
        ('set_root', 'Set Root Directory...', 'Ctrl-O', 'Set Root Directory for Workspace.'),
        #('save', 'Save Workspace', 'Ctrl-S', 'Save current workspace state.'),
        #('save_as', 'Save Workspace As...', 'Ctrl-Shift-S', 'Save current workspace state with given filename.'),
        #('load', 'Load Workspace...', 'Ctrl-O', 'Load current workspace state.'),
        #('remove', 'Remove Selected Item', '', 'Remove item in selection.'),
        #('add_file', 'Add Data Files...', '', 'Add data file(s).'),
        #('add_loader', 'Add Loader...', '', 'Add a loader.'),
        #('add_visualizer', 'Add Visualizer...', '', 'Add a visualizer.'),
        #('add_filter', 'Add Filter...', '', 'Add a filter.'),
        )),
    ('Visual', (
        ('toggle', 'Toggle Visibility', '', 'Toggle visivility.'),
        )),
    ('Parameter', (
        ('import', 'Import Parameters...', '', 'Import parameters.'),
        )),
    )


class AppMenuBar(wx.MenuBar):
    """Application menubar.
    """
    def __init__(self, parent, *args, **kwargs):
        """Initializer.
        """
        wx.MenuBar.__init__(self, *args, **kwargs)

        # Build menu from MENU_STRUCTURE
        for section_name, section_info in MENU_STRUCTURE:
            # create section
            menu = wx.Menu()
            self.Append(menu, '&'+section_name)
            # bind as self.<section_name>_menu
            setattr(self, section_name.lower()+'_menu', menu)
            for attr_bit, label, accel_key, tip in section_info:
                # create menuitem for the section
                if accel_key:
                    label += ('\t'+accel_key)
                menu_item = menu.Append(-1, label, tip)
                # bind as self.<section_name>_<attr_bit>
                setattr(self, section_name.lower()+'_'+attr_bit, menu_item)
        # associate menubar to parent.
        parent.SetMenuBar(self)


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Menu Demo')
            menubar = AppMenuBar(frame)
            frame.SetMenuBar(menubar)
            frame.Layout()
            frame.Bind(wx.EVT_MENU, self.OnQuitMenu, menubar.app_quit)
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

        def OnQuitMenu(self, evt):
            self.ExitMainLoop()
        
    app = App(0)
    app.MainLoop()
=======================
pipeline.py
----------------------
# coding: utf-8
"""pipeline.py --- Represents pipeline.
"""
import sys


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
        """Returns output specification. Subclass may override this.
        """
        return []

    @property
    def input_spec(self):
        return self.get_input_spec()

    @property
    def output_spec(self):
        return self.get_output_spec()

    @property
    def is_root(self):
        """Returns if instance is the root (has no parent). 
        """
        return self.parent is None

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

    def request_data(self, spec):
        """Request parent for given spec data.
        """
        return None


class RootPipelineNode(PipelineNode):
    """Special pipeline item intended to be a root of pipeline tree.

    >>> r = RootPipelineNode()
    >>> p = PipelineNode()
    >>> r.connect(p)
    Traceback (most recent call last):
    ...
    ValueError: RootPipelineNode should always be root.
    
    """
    def connect(self, parent):
        raise ValueError('%s should always be root.' %self.__class__.__name__)


class PipelineTree(object):
    """Represents a pipeline.
    
    >>> p = PipelineTree()
    >>> p
    <PipelineTree>
    >>> p.root
    <RootPipelineNode: Root>

    """
    def __init__(self):
        """Initializer.
        """
        self.root = RootPipelineNode(name='Root')

    def __repr__(self):
        """Returns representation.
        """
        return '<PipelineTree>'


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
=======================
pipeline_panel.py
----------------------
# coding: utf-8
"""pipeline_panel.py --- Workspace panel in visualizer application.
"""
import wx
from wx.lib.mixins import treemixin

from utils_wx import TreeCtrlPlus
from pipeline import PipelineTree, PipelineNode


class PipelineTree(TreeCtrlPlus):
    """TreeCtrl for workspace.
    """    
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        style = kwargs.pop('style', 0)|wx.TR_NO_BUTTONS
        pipeline = kwargs.pop('pipeline', None)
        kwargs['style'] = style
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        # root/toplevel nodes
        self.root_item_id = None # will provided in rebuild_root()
        self.pipeline = pipeline # will invoke rebuild_root()

    def set_pipeline(self, pipeline):
        """Bind model to the tree.
        """
        self._pipeline = pipeline
        self.rebuild_root()

    def get_pipeline(self):
        return self._pipeline

    pipeline = property(get_pipeline, set_pipeline)

    def rebuild_root(self):
        """Rebuild tree from the toplevel.
        """
        self.DeleteAllItems()
        root_item_id = self.AddRoot("<<Data>>")
        root_object = None
        if self.pipeline:
            root_object = self.pipeline.root
        self.root_item_id = root_item_id
        self.SetPyData(root_item_id, root_object)
        self.rebuild_tree(root_item_id)

    def rebuild_tree(self, item_id):
        """Rebuild subtree beneath the given item_id.
        """
        node_data = self.GetPyData(item_id)
        if node_data is None:
            return
        for child in node_data.children:
            child_id = self.AppendItem(item_id, '%s::%s' %(child.class_name, child.name))
            self.SetPyData(child_id, child)
            self.rebuild_tree(child_id)


class PipelinePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = PipelineTree(self, -1, style=wx.SUNKEN_BORDER)
        # buttons
        add_button = wx.Button(self, -1, '+')
        del_button = wx.Button(self, -1, '-')
        # name bindings
        self.tree_ctrl = tree_ctrl
        # sizer
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(add_button, 0, wx.ALL, 0)
        button_sizer.Add(del_button, 0, wx.ALL, 0)
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.Add(button_sizer, 0, wx.ALL, 5)
        root_sizer.SetMinSize((200, -1))
        self.SetSize((200, 600))
        self.SetSizer(root_sizer)
        self.Layout()


if __name__=='__main__':

    pipeline = Pipeline()
    filter1 = PipelineNode('Filter 1')
    filter2 = PipelineNode('Filter 2')
    filter3 = PipelineNode('Filter 3')
    renderer1 = PipelineNode('Renderer 1')
    renderer2 = PipelineNode('Renderer 2')
    renderer3 = PipelineNode('Renderer 3')
    filter1.connect(pipeline.root)
    filter2.connect(filter1)
    filter3.connect(filter2)
    renderer1.connect(filter1)
    renderer2.connect(filter2)
    renderer3.connect(filter3)
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Pipeline Panel Demo')
            pipeline_panel = PipelinePanel(frame, -1)
            tree = pipeline_panel.tree_ctrl
            tree.pipeline = pipeline
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(pipeline_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
=======================
render_window.py
----------------------
# coding: utf-8
"""render_window.py -- Wrapping panel for wxVTKRenderWindowInteractor.
"""

import numpy
import vtk
import wx

from wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor


class RenderWindowPanel(wx.Panel):
    """A panel containing wxVTKRenderWindowInteractor.

    Attributes:
    render_window --- wxVTKRenderWindowInteractor instance.
    aspect_ratio --- aspect ratio of render_window. (w, h)-tuple.

    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # extract aspect ratio, defaulting 4:3.
        self._aspect_ratio = kwargs.pop('aspect_ratio', (4, 3))
        super(RenderWindowPanel, self).__init__(*args, **kwargs)
        render_window = wxVTKRenderWindowInteractor(self, -1)
        # binding
        self.render_window = render_window
        # events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.setup_renderer()
        settings = kwargs.get('settings', None)
        if settings:
            self.configure_renderer(settings)

    def _get_aspect_ratio(self):
        return self._aspect_ratio

    def _set_aspect_ratio(self, aspect_ratio):
        self._aspect_ratio = aspect_ratio
        self.force_aspect_ratio(*self.GetSize())

    aspect_ratio = property(_get_aspect_ratio, _set_aspect_ratio)

    def configure_renderer(self, settings):
        """Configure rendering environment.
        """
        renderer = self.renderer
        # configure camera
        camera = renderer.GetActiveCamera()
        camera.SetFocalPoint(
            numpy.array(settings.camera_focal_point)*settings.scaling)
        camera.SetPosition(
            numpy.array(settings.camera_base_position)*settings.scaling)
        camera.Azimuth(settings.camera_azimuth)
        camera.Elevation(settings.camera_elevation)
        camera.SetViewAngle(settings.camera_view_angle)
        camera.SetParallelProjection(settings.camera_parallel_projection)
        camera.Zoom(settings.camera_zoom)
        # configure background
        renderer.SetBackground(settings.image_background_color)
        # configure lighting
        light_kit = vtk.vtkLightKit()
        light_kit.SetKeyLightIntensity(settings.light_intensity)
        light_kit.AddLightsToRenderer(renderer)

    def setup_renderer(self):
        """Set up vtk renderers.
        """
        # Enable rendering
        self.render_window.Enable(1)
        # Hook exit event.
        self.render_window.AddObserver(
            'ExitEvent', lambda o,e,f=self: f.Close())
        # create renderer
        renderer = vtk.vtkRenderer()
        renderer.SetViewport(0.0, 0.0, 1.0, 1.0)
        # Register renderer
        self.render_window.GetRenderWindow().AddRenderer(renderer)
        self.renderer = renderer

    def force_aspect_ratio(self, width, height):
        """
        Force size of render_window to follow aspect ratio.

        Arguments:
        width --- preferred width of the window.
        height --- preferred height of the window.
        
        """
        aw, ah = self.aspect_ratio
        width = int(min(width, height*aw/float(ah)))
        height = int(min(height, width*ah/float(aw)))
        self.render_window.SetSize((width, height))
        
    def OnSize(self, event):
        """Resize handler.
        """
        self.force_aspect_ratio(*event.GetSize())


if __name__=='__main__':
    # Run a demo application.
    class DemoApp(wx.App):
        """Demonstrative application.
        """
        ASPECT_RATIOS = [(4, 3), (16, 8)]
        def OnRadioSelect(self, event):
            aspect_ratio = self.ASPECT_RATIOS[event.GetInt()]
            self.render_window_panel.aspect_ratio = aspect_ratio

        def OnInit(self):
            frame = wx.Frame(None, -1, u'RenderWindowPanel demo',
                             size=(400, 400))
            aspect_radio = wx.RadioBox(
                frame, -1,
                choices=['%s:%s' %ar for ar in self.ASPECT_RATIOS])
            render_window_panel = RenderWindowPanel(frame, -1)
            frame.Bind(wx.EVT_RADIOBOX, self.OnRadioSelect)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(aspect_radio, 0, wx.ALL|wx.EXPAND, 5)
            sizer.Add(render_window_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            renderer = render_window_panel.renderer
            # stuff to be rendererd
            source = vtk.vtkConeSource()
            source.SetResolution(8)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            renderer.AddActor(actor)
            return True

    app = DemoApp(0)
    app.MainLoop()


if __name__=='__main__':
    pass
=======================
renderer_panel.py
----------------------
# coding: utf-8
"""renderer_panel.py -- Panel to wrap wxVTKRenderWindowInteractor.
"""

import numpy
import vtk
import wx

from wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor


class RendererPanel(wx.Panel):
    """A panel containing wxVTKRenderWindowInteractor.

    Attributes:
    render_window --- wxVTKRenderWindowInteractor instance.
    aspect_ratio --- aspect ratio of render_window. (w, h)-tuple.

    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # extract aspect ratio, defaulting 4:3.
        self._aspect_ratio = kwargs.pop('aspect_ratio', (4, 3))
        super(RendererPanel, self).__init__(*args, **kwargs)
        render_window = wxVTKRenderWindowInteractor(self, -1)
        # binding
        self.render_window = render_window
        # events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.setup_renderer()
        settings = kwargs.get('settings', None)
        if settings:
            self.configure_renderer(settings)

    def _get_aspect_ratio(self):
        return self._aspect_ratio

    def _set_aspect_ratio(self, aspect_ratio):
        self._aspect_ratio = aspect_ratio
        self.force_aspect_ratio(*self.GetSize())

    aspect_ratio = property(_get_aspect_ratio, _set_aspect_ratio)

    def configure_renderer(self, settings):
        """Configure rendering environment.
        """
        renderer = self.renderer
        # configure camera
        camera = renderer.GetActiveCamera()
        camera.SetFocalPoint(
            numpy.array(settings.camera_focal_point)*settings.scaling)
        camera.SetPosition(
            numpy.array(settings.camera_base_position)*settings.scaling)
        camera.Azimuth(settings.camera_azimuth)
        camera.Elevation(settings.camera_elevation)
        camera.SetViewAngle(settings.camera_view_angle)
        camera.SetParallelProjection(settings.camera_parallel_projection)
        camera.Zoom(settings.camera_zoom)
        # configure background
        renderer.SetBackground(settings.image_background_color)
        # configure lighting
        light_kit = vtk.vtkLightKit()
        light_kit.SetKeyLightIntensity(settings.light_intensity)
        light_kit.AddLightsToRenderer(renderer)

    def setup_renderer(self):
        """Set up vtk renderers.
        """
        # Enable rendering
        self.render_window.Enable(1)
        # Hook exit event.
        self.render_window.AddObserver(
            'ExitEvent', lambda o,e,f=self: f.Close())
        # create renderer
        renderer = vtk.vtkRenderer()
        renderer.SetViewport(0.0, 0.0, 1.0, 1.0)
        # Register renderer
        self.render_window.GetRenderWindow().AddRenderer(renderer)
        self.renderer = renderer

    def force_aspect_ratio(self, width, height):
        """
        Force size of render_window to follow aspect ratio.

        Arguments:
        width --- preferred width of the window.
        height --- preferred height of the window.
        
        """
        aw, ah = self.aspect_ratio
        width = int(min(width, height*aw/float(ah)))
        height = int(min(height, width*ah/float(aw)))
        self.render_window.SetSize((width, height))
        
    def OnSize(self, event):
        """Resize handler.
        """
        self.force_aspect_ratio(*event.GetSize())


if __name__=='__main__':
    # Run a demo application.
    class DemoApp(wx.App):
        """Demonstrative application.
        """
        ASPECT_RATIOS = [(4, 3), (16, 8)]
        def OnRadioSelect(self, event):
            aspect_ratio = self.ASPECT_RATIOS[event.GetInt()]
            self.render_window_panel.aspect_ratio = aspect_ratio

        def OnInit(self):
            frame = wx.Frame(None, -1, u'RendererPanel demo',
                             size=(400, 400))
            aspect_radio = wx.RadioBox(
                frame, -1,
                choices=['%s:%s' %ar for ar in self.ASPECT_RATIOS])
            renderer_panel = RendererPanel(frame, -1)
            frame.Bind(wx.EVT_RADIOBOX, self.OnRadioSelect)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(aspect_radio, 0, wx.ALL|wx.EXPAND, 5)
            sizer.Add(renderer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            renderer = renderer_panel.renderer
            # stuff to be rendererd
            source = vtk.vtkConeSource()
            source.SetResolution(8)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            renderer.AddActor(actor)
            return True

    app = DemoApp(0)
    app.MainLoop()
=======================
rgb_colors.py
----------------------
# coding: utf-8
"""
rgb_colors.py --- RGB color list for visualizer.

Color names and values are taken from X11's rgb.txt
You can see the color at:
http://www.w3.org/TR/css3-color/#svg-color, or related pages.

Note: RGB values are ranged in [0, 1] instead of [0,255].

"""

RGB_SNOW                      = (1.000, 0.980, 0.980)
RGB_GHOST_WHITE               = (0.973, 0.973, 1.000)
RGB_GHOSTWHITE                = (0.973, 0.973, 1.000)
RGB_WHITE_SMOKE               = (0.961, 0.961, 0.961)
RGB_WHITESMOKE                = (0.961, 0.961, 0.961)
RGB_GAINSBORO                 = (0.863, 0.863, 0.863)
RGB_FLORAL_WHITE              = (1.000, 0.980, 0.941)
RGB_FLORALWHITE               = (1.000, 0.980, 0.941)
RGB_OLD_LACE                  = (0.992, 0.961, 0.902)
RGB_OLDLACE                   = (0.992, 0.961, 0.902)
RGB_LINEN                     = (0.980, 0.941, 0.902)
RGB_ANTIQUE_WHITE             = (0.980, 0.922, 0.843)
RGB_ANTIQUEWHITE              = (0.980, 0.922, 0.843)
RGB_PAPAYA_WHIP               = (1.000, 0.937, 0.835)
RGB_PAPAYAWHIP                = (1.000, 0.937, 0.835)
RGB_BLANCHED_ALMOND           = (1.000, 0.922, 0.804)
RGB_BLANCHEDALMOND            = (1.000, 0.922, 0.804)
RGB_BISQUE                    = (1.000, 0.894, 0.769)
RGB_PEACH_PUFF                = (1.000, 0.855, 0.725)
RGB_PEACHPUFF                 = (1.000, 0.855, 0.725)
RGB_NAVAJO_WHITE              = (1.000, 0.871, 0.678)
RGB_NAVAJOWHITE               = (1.000, 0.871, 0.678)
RGB_MOCCASIN                  = (1.000, 0.894, 0.710)
RGB_CORNSILK                  = (1.000, 0.973, 0.863)
RGB_IVORY                     = (1.000, 1.000, 0.941)
RGB_LEMON_CHIFFON             = (1.000, 0.980, 0.804)
RGB_LEMONCHIFFON              = (1.000, 0.980, 0.804)
RGB_SEASHELL                  = (1.000, 0.961, 0.933)
RGB_HONEYDEW                  = (0.941, 1.000, 0.941)
RGB_MINT_CREAM                = (0.961, 1.000, 0.980)
RGB_MINTCREAM                 = (0.961, 1.000, 0.980)
RGB_AZURE                     = (0.941, 1.000, 1.000)
RGB_ALICE_BLUE                = (0.941, 0.973, 1.000)
RGB_ALICEBLUE                 = (0.941, 0.973, 1.000)
RGB_LAVENDER                  = (0.902, 0.902, 0.980)
RGB_LAVENDER_BLUSH            = (1.000, 0.941, 0.961)
RGB_LAVENDERBLUSH             = (1.000, 0.941, 0.961)
RGB_MISTY_ROSE                = (1.000, 0.894, 0.882)
RGB_MISTYROSE                 = (1.000, 0.894, 0.882)
RGB_WHITE                     = (1.000, 1.000, 1.000)
RGB_BLACK                     = (0.000, 0.000, 0.000)
RGB_DARK_SLATE_GRAY           = (0.184, 0.310, 0.310)
RGB_DARKSLATEGRAY             = (0.184, 0.310, 0.310)
RGB_DARK_SLATE_GREY           = (0.184, 0.310, 0.310)
RGB_DARKSLATEGREY             = (0.184, 0.310, 0.310)
RGB_DIM_GRAY                  = (0.412, 0.412, 0.412)
RGB_DIMGRAY                   = (0.412, 0.412, 0.412)
RGB_DIM_GREY                  = (0.412, 0.412, 0.412)
RGB_DIMGREY                   = (0.412, 0.412, 0.412)
RGB_SLATE_GRAY                = (0.439, 0.502, 0.565)
RGB_SLATEGRAY                 = (0.439, 0.502, 0.565)
RGB_SLATE_GREY                = (0.439, 0.502, 0.565)
RGB_SLATEGREY                 = (0.439, 0.502, 0.565)
RGB_LIGHT_SLATE_GRAY          = (0.467, 0.533, 0.600)
RGB_LIGHTSLATEGRAY            = (0.467, 0.533, 0.600)
RGB_LIGHT_SLATE_GREY          = (0.467, 0.533, 0.600)
RGB_LIGHTSLATEGREY            = (0.467, 0.533, 0.600)
RGB_GRAY                      = (0.745, 0.745, 0.745)
RGB_GREY                      = (0.745, 0.745, 0.745)
RGB_LIGHT_GREY                = (0.827, 0.827, 0.827)
RGB_LIGHTGREY                 = (0.827, 0.827, 0.827)
RGB_LIGHT_GRAY                = (0.827, 0.827, 0.827)
RGB_LIGHTGRAY                 = (0.827, 0.827, 0.827)
RGB_MIDNIGHT_BLUE             = (0.098, 0.098, 0.439)
RGB_MIDNIGHTBLUE              = (0.098, 0.098, 0.439)
RGB_NAVY                      = (0.000, 0.000, 0.502)
RGB_NAVY_BLUE                 = (0.000, 0.000, 0.502)
RGB_NAVYBLUE                  = (0.000, 0.000, 0.502)
RGB_CORNFLOWER_BLUE           = (0.392, 0.584, 0.929)
RGB_CORNFLOWERBLUE            = (0.392, 0.584, 0.929)
RGB_DARK_SLATE_BLUE           = (0.282, 0.239, 0.545)
RGB_DARKSLATEBLUE             = (0.282, 0.239, 0.545)
RGB_SLATE_BLUE                = (0.416, 0.353, 0.804)
RGB_SLATEBLUE                 = (0.416, 0.353, 0.804)
RGB_MEDIUM_SLATE_BLUE         = (0.482, 0.408, 0.933)
RGB_MEDIUMSLATEBLUE           = (0.482, 0.408, 0.933)
RGB_LIGHT_SLATE_BLUE          = (0.518, 0.439, 1.000)
RGB_LIGHTSLATEBLUE            = (0.518, 0.439, 1.000)
RGB_MEDIUM_BLUE               = (0.000, 0.000, 0.804)
RGB_MEDIUMBLUE                = (0.000, 0.000, 0.804)
RGB_ROYAL_BLUE                = (0.255, 0.412, 0.882)
RGB_ROYALBLUE                 = (0.255, 0.412, 0.882)
RGB_BLUE                      = (0.000, 0.000, 1.000)
RGB_DODGER_BLUE               = (0.118, 0.565, 1.000)
RGB_DODGERBLUE                = (0.118, 0.565, 1.000)
RGB_DEEP_SKY_BLUE             = (0.000, 0.749, 1.000)
RGB_DEEPSKYBLUE               = (0.000, 0.749, 1.000)
RGB_SKY_BLUE                  = (0.529, 0.808, 0.922)
RGB_SKYBLUE                   = (0.529, 0.808, 0.922)
RGB_LIGHT_SKY_BLUE            = (0.529, 0.808, 0.980)
RGB_LIGHTSKYBLUE              = (0.529, 0.808, 0.980)
RGB_STEEL_BLUE                = (0.275, 0.510, 0.706)
RGB_STEELBLUE                 = (0.275, 0.510, 0.706)
RGB_LIGHT_STEEL_BLUE          = (0.690, 0.769, 0.871)
RGB_LIGHTSTEELBLUE            = (0.690, 0.769, 0.871)
RGB_LIGHT_BLUE                = (0.678, 0.847, 0.902)
RGB_LIGHTBLUE                 = (0.678, 0.847, 0.902)
RGB_POWDER_BLUE               = (0.690, 0.878, 0.902)
RGB_POWDERBLUE                = (0.690, 0.878, 0.902)
RGB_PALE_TURQUOISE            = (0.686, 0.933, 0.933)
RGB_PALETURQUOISE             = (0.686, 0.933, 0.933)
RGB_DARK_TURQUOISE            = (0.000, 0.808, 0.820)
RGB_DARKTURQUOISE             = (0.000, 0.808, 0.820)
RGB_MEDIUM_TURQUOISE          = (0.282, 0.820, 0.800)
RGB_MEDIUMTURQUOISE           = (0.282, 0.820, 0.800)
RGB_TURQUOISE                 = (0.251, 0.878, 0.816)
RGB_CYAN                      = (0.000, 1.000, 1.000)
RGB_LIGHT_CYAN                = (0.878, 1.000, 1.000)
RGB_LIGHTCYAN                 = (0.878, 1.000, 1.000)
RGB_CADET_BLUE                = (0.373, 0.620, 0.627)
RGB_CADETBLUE                 = (0.373, 0.620, 0.627)
RGB_MEDIUM_AQUAMARINE         = (0.400, 0.804, 0.667)
RGB_MEDIUMAQUAMARINE          = (0.400, 0.804, 0.667)
RGB_AQUAMARINE                = (0.498, 1.000, 0.831)
RGB_DARK_GREEN                = (0.000, 0.392, 0.000)
RGB_DARKGREEN                 = (0.000, 0.392, 0.000)
RGB_DARK_OLIVE_GREEN          = (0.333, 0.420, 0.184)
RGB_DARKOLIVEGREEN            = (0.333, 0.420, 0.184)
RGB_DARK_SEA_GREEN            = (0.561, 0.737, 0.561)
RGB_DARKSEAGREEN              = (0.561, 0.737, 0.561)
RGB_SEA_GREEN                 = (0.180, 0.545, 0.341)
RGB_SEAGREEN                  = (0.180, 0.545, 0.341)
RGB_MEDIUM_SEA_GREEN          = (0.235, 0.702, 0.443)
RGB_MEDIUMSEAGREEN            = (0.235, 0.702, 0.443)
RGB_LIGHT_SEA_GREEN           = (0.125, 0.698, 0.667)
RGB_LIGHTSEAGREEN             = (0.125, 0.698, 0.667)
RGB_PALE_GREEN                = (0.596, 0.984, 0.596)
RGB_PALEGREEN                 = (0.596, 0.984, 0.596)
RGB_SPRING_GREEN              = (0.000, 1.000, 0.498)
RGB_SPRINGGREEN               = (0.000, 1.000, 0.498)
RGB_LAWN_GREEN                = (0.486, 0.988, 0.000)
RGB_LAWNGREEN                 = (0.486, 0.988, 0.000)
RGB_GREEN                     = (0.000, 1.000, 0.000)
RGB_CHARTREUSE                = (0.498, 1.000, 0.000)
RGB_MEDIUM_SPRING_GREEN       = (0.000, 0.980, 0.604)
RGB_MEDIUMSPRINGGREEN         = (0.000, 0.980, 0.604)
RGB_GREEN_YELLOW              = (0.678, 1.000, 0.184)
RGB_GREENYELLOW               = (0.678, 1.000, 0.184)
RGB_LIME_GREEN                = (0.196, 0.804, 0.196)
RGB_LIMEGREEN                 = (0.196, 0.804, 0.196)
RGB_YELLOW_GREEN              = (0.604, 0.804, 0.196)
RGB_YELLOWGREEN               = (0.604, 0.804, 0.196)
RGB_FOREST_GREEN              = (0.133, 0.545, 0.133)
RGB_FORESTGREEN               = (0.133, 0.545, 0.133)
RGB_OLIVE_DRAB                = (0.420, 0.557, 0.137)
RGB_OLIVEDRAB                 = (0.420, 0.557, 0.137)
RGB_DARK_KHAKI                = (0.741, 0.718, 0.420)
RGB_DARKKHAKI                 = (0.741, 0.718, 0.420)
RGB_KHAKI                     = (0.941, 0.902, 0.549)
RGB_PALE_GOLDENROD            = (0.933, 0.910, 0.667)
RGB_PALEGOLDENROD             = (0.933, 0.910, 0.667)
RGB_LIGHT_GOLDENROD_YELLOW    = (0.980, 0.980, 0.824)
RGB_LIGHTGOLDENRODYELLOW      = (0.980, 0.980, 0.824)
RGB_LIGHT_YELLOW              = (1.000, 1.000, 0.878)
RGB_LIGHTYELLOW               = (1.000, 1.000, 0.878)
RGB_YELLOW                    = (1.000, 1.000, 0.000)
RGB_GOLD                      = (1.000, 0.843, 0.000)
RGB_LIGHT_GOLDENROD           = (0.933, 0.867, 0.510)
RGB_LIGHTGOLDENROD            = (0.933, 0.867, 0.510)
RGB_GOLDENROD                 = (0.855, 0.647, 0.125)
RGB_DARK_GOLDENROD            = (0.722, 0.525, 0.043)
RGB_DARKGOLDENROD             = (0.722, 0.525, 0.043)
RGB_ROSY_BROWN                = (0.737, 0.561, 0.561)
RGB_ROSYBROWN                 = (0.737, 0.561, 0.561)
RGB_INDIAN_RED                = (0.804, 0.361, 0.361)
RGB_INDIANRED                 = (0.804, 0.361, 0.361)
RGB_SADDLE_BROWN              = (0.545, 0.271, 0.075)
RGB_SADDLEBROWN               = (0.545, 0.271, 0.075)
RGB_SIENNA                    = (0.627, 0.322, 0.176)
RGB_PERU                      = (0.804, 0.522, 0.247)
RGB_BURLYWOOD                 = (0.871, 0.722, 0.529)
RGB_BEIGE                     = (0.961, 0.961, 0.863)
RGB_WHEAT                     = (0.961, 0.871, 0.702)
RGB_SANDY_BROWN               = (0.957, 0.643, 0.376)
RGB_SANDYBROWN                = (0.957, 0.643, 0.376)
RGB_TAN                       = (0.824, 0.706, 0.549)
RGB_CHOCOLATE                 = (0.824, 0.412, 0.118)
RGB_FIREBRICK                 = (0.698, 0.133, 0.133)
RGB_BROWN                     = (0.647, 0.165, 0.165)
RGB_DARK_SALMON               = (0.914, 0.588, 0.478)
RGB_DARKSALMON                = (0.914, 0.588, 0.478)
RGB_SALMON                    = (0.980, 0.502, 0.447)
RGB_LIGHT_SALMON              = (1.000, 0.627, 0.478)
RGB_LIGHTSALMON               = (1.000, 0.627, 0.478)
RGB_ORANGE                    = (1.000, 0.647, 0.000)
RGB_DARK_ORANGE               = (1.000, 0.549, 0.000)
RGB_DARKORANGE                = (1.000, 0.549, 0.000)
RGB_CORAL                     = (1.000, 0.498, 0.314)
RGB_LIGHT_CORAL               = (0.941, 0.502, 0.502)
RGB_LIGHTCORAL                = (0.941, 0.502, 0.502)
RGB_TOMATO                    = (1.000, 0.388, 0.278)
RGB_ORANGE_RED                = (1.000, 0.271, 0.000)
RGB_ORANGERED                 = (1.000, 0.271, 0.000)
RGB_RED                       = (1.000, 0.000, 0.000)
RGB_HOT_PINK                  = (1.000, 0.412, 0.706)
RGB_HOTPINK                   = (1.000, 0.412, 0.706)
RGB_DEEP_PINK                 = (1.000, 0.078, 0.576)
RGB_DEEPPINK                  = (1.000, 0.078, 0.576)
RGB_PINK                      = (1.000, 0.753, 0.796)
RGB_LIGHT_PINK                = (1.000, 0.714, 0.757)
RGB_LIGHTPINK                 = (1.000, 0.714, 0.757)
RGB_PALE_VIOLET_RED           = (0.859, 0.439, 0.576)
RGB_PALEVIOLETRED             = (0.859, 0.439, 0.576)
RGB_MAROON                    = (0.690, 0.188, 0.376)
RGB_MEDIUM_VIOLET_RED         = (0.780, 0.082, 0.522)
RGB_MEDIUMVIOLETRED           = (0.780, 0.082, 0.522)
RGB_VIOLET_RED                = (0.816, 0.125, 0.565)
RGB_VIOLETRED                 = (0.816, 0.125, 0.565)
RGB_MAGENTA                   = (1.000, 0.000, 1.000)
RGB_VIOLET                    = (0.933, 0.510, 0.933)
RGB_PLUM                      = (0.867, 0.627, 0.867)
RGB_ORCHID                    = (0.855, 0.439, 0.839)
RGB_MEDIUM_ORCHID             = (0.729, 0.333, 0.827)
RGB_MEDIUMORCHID              = (0.729, 0.333, 0.827)
RGB_DARK_ORCHID               = (0.600, 0.196, 0.800)
RGB_DARKORCHID                = (0.600, 0.196, 0.800)
RGB_DARK_VIOLET               = (0.580, 0.000, 0.827)
RGB_DARKVIOLET                = (0.580, 0.000, 0.827)
RGB_BLUE_VIOLET               = (0.541, 0.169, 0.886)
RGB_BLUEVIOLET                = (0.541, 0.169, 0.886)
RGB_PURPLE                    = (0.627, 0.125, 0.941)
RGB_MEDIUM_PURPLE             = (0.576, 0.439, 0.859)
RGB_MEDIUMPURPLE              = (0.576, 0.439, 0.859)
RGB_THISTLE                   = (0.847, 0.749, 0.847)
RGB_SNOW1                     = (1.000, 0.980, 0.980)
RGB_SNOW2                     = (0.933, 0.914, 0.914)
RGB_SNOW3                     = (0.804, 0.788, 0.788)
RGB_SNOW4                     = (0.545, 0.537, 0.537)
RGB_SEASHELL1                 = (1.000, 0.961, 0.933)
RGB_SEASHELL2                 = (0.933, 0.898, 0.871)
RGB_SEASHELL3                 = (0.804, 0.773, 0.749)
RGB_SEASHELL4                 = (0.545, 0.525, 0.510)
RGB_ANTIQUEWHITE1             = (1.000, 0.937, 0.859)
RGB_ANTIQUEWHITE2             = (0.933, 0.875, 0.800)
RGB_ANTIQUEWHITE3             = (0.804, 0.753, 0.690)
RGB_ANTIQUEWHITE4             = (0.545, 0.514, 0.471)
RGB_BISQUE1                   = (1.000, 0.894, 0.769)
RGB_BISQUE2                   = (0.933, 0.835, 0.718)
RGB_BISQUE3                   = (0.804, 0.718, 0.620)
RGB_BISQUE4                   = (0.545, 0.490, 0.420)
RGB_PEACHPUFF1                = (1.000, 0.855, 0.725)
RGB_PEACHPUFF2                = (0.933, 0.796, 0.678)
RGB_PEACHPUFF3                = (0.804, 0.686, 0.584)
RGB_PEACHPUFF4                = (0.545, 0.467, 0.396)
RGB_NAVAJOWHITE1              = (1.000, 0.871, 0.678)
RGB_NAVAJOWHITE2              = (0.933, 0.812, 0.631)
RGB_NAVAJOWHITE3              = (0.804, 0.702, 0.545)
RGB_NAVAJOWHITE4              = (0.545, 0.475, 0.369)
RGB_LEMONCHIFFON1             = (1.000, 0.980, 0.804)
RGB_LEMONCHIFFON2             = (0.933, 0.914, 0.749)
RGB_LEMONCHIFFON3             = (0.804, 0.788, 0.647)
RGB_LEMONCHIFFON4             = (0.545, 0.537, 0.439)
RGB_CORNSILK1                 = (1.000, 0.973, 0.863)
RGB_CORNSILK2                 = (0.933, 0.910, 0.804)
RGB_CORNSILK3                 = (0.804, 0.784, 0.694)
RGB_CORNSILK4                 = (0.545, 0.533, 0.471)
RGB_IVORY1                    = (1.000, 1.000, 0.941)
RGB_IVORY2                    = (0.933, 0.933, 0.878)
RGB_IVORY3                    = (0.804, 0.804, 0.757)
RGB_IVORY4                    = (0.545, 0.545, 0.514)
RGB_HONEYDEW1                 = (0.941, 1.000, 0.941)
RGB_HONEYDEW2                 = (0.878, 0.933, 0.878)
RGB_HONEYDEW3                 = (0.757, 0.804, 0.757)
RGB_HONEYDEW4                 = (0.514, 0.545, 0.514)
RGB_LAVENDERBLUSH1            = (1.000, 0.941, 0.961)
RGB_LAVENDERBLUSH2            = (0.933, 0.878, 0.898)
RGB_LAVENDERBLUSH3            = (0.804, 0.757, 0.773)
RGB_LAVENDERBLUSH4            = (0.545, 0.514, 0.525)
RGB_MISTYROSE1                = (1.000, 0.894, 0.882)
RGB_MISTYROSE2                = (0.933, 0.835, 0.824)
RGB_MISTYROSE3                = (0.804, 0.718, 0.710)
RGB_MISTYROSE4                = (0.545, 0.490, 0.482)
RGB_AZURE1                    = (0.941, 1.000, 1.000)
RGB_AZURE2                    = (0.878, 0.933, 0.933)
RGB_AZURE3                    = (0.757, 0.804, 0.804)
RGB_AZURE4                    = (0.514, 0.545, 0.545)
RGB_SLATEBLUE1                = (0.514, 0.435, 1.000)
RGB_SLATEBLUE2                = (0.478, 0.404, 0.933)
RGB_SLATEBLUE3                = (0.412, 0.349, 0.804)
RGB_SLATEBLUE4                = (0.278, 0.235, 0.545)
RGB_ROYALBLUE1                = (0.282, 0.463, 1.000)
RGB_ROYALBLUE2                = (0.263, 0.431, 0.933)
RGB_ROYALBLUE3                = (0.227, 0.373, 0.804)
RGB_ROYALBLUE4                = (0.153, 0.251, 0.545)
RGB_BLUE1                     = (0.000, 0.000, 1.000)
RGB_BLUE2                     = (0.000, 0.000, 0.933)
RGB_BLUE3                     = (0.000, 0.000, 0.804)
RGB_BLUE4                     = (0.000, 0.000, 0.545)
RGB_DODGERBLUE1               = (0.118, 0.565, 1.000)
RGB_DODGERBLUE2               = (0.110, 0.525, 0.933)
RGB_DODGERBLUE3               = (0.094, 0.455, 0.804)
RGB_DODGERBLUE4               = (0.063, 0.306, 0.545)
RGB_STEELBLUE1                = (0.388, 0.722, 1.000)
RGB_STEELBLUE2                = (0.361, 0.675, 0.933)
RGB_STEELBLUE3                = (0.310, 0.580, 0.804)
RGB_STEELBLUE4                = (0.212, 0.392, 0.545)
RGB_DEEPSKYBLUE1              = (0.000, 0.749, 1.000)
RGB_DEEPSKYBLUE2              = (0.000, 0.698, 0.933)
RGB_DEEPSKYBLUE3              = (0.000, 0.604, 0.804)
RGB_DEEPSKYBLUE4              = (0.000, 0.408, 0.545)
RGB_SKYBLUE1                  = (0.529, 0.808, 1.000)
RGB_SKYBLUE2                  = (0.494, 0.753, 0.933)
RGB_SKYBLUE3                  = (0.424, 0.651, 0.804)
RGB_SKYBLUE4                  = (0.290, 0.439, 0.545)
RGB_LIGHTSKYBLUE1             = (0.690, 0.886, 1.000)
RGB_LIGHTSKYBLUE2             = (0.643, 0.827, 0.933)
RGB_LIGHTSKYBLUE3             = (0.553, 0.714, 0.804)
RGB_LIGHTSKYBLUE4             = (0.376, 0.482, 0.545)
RGB_SLATEGRAY1                = (0.776, 0.886, 1.000)
RGB_SLATEGRAY2                = (0.725, 0.827, 0.933)
RGB_SLATEGRAY3                = (0.624, 0.714, 0.804)
RGB_SLATEGRAY4                = (0.424, 0.482, 0.545)
RGB_LIGHTSTEELBLUE1           = (0.792, 0.882, 1.000)
RGB_LIGHTSTEELBLUE2           = (0.737, 0.824, 0.933)
RGB_LIGHTSTEELBLUE3           = (0.635, 0.710, 0.804)
RGB_LIGHTSTEELBLUE4           = (0.431, 0.482, 0.545)
RGB_LIGHTBLUE1                = (0.749, 0.937, 1.000)
RGB_LIGHTBLUE2                = (0.698, 0.875, 0.933)
RGB_LIGHTBLUE3                = (0.604, 0.753, 0.804)
RGB_LIGHTBLUE4                = (0.408, 0.514, 0.545)
RGB_LIGHTCYAN1                = (0.878, 1.000, 1.000)
RGB_LIGHTCYAN2                = (0.820, 0.933, 0.933)
RGB_LIGHTCYAN3                = (0.706, 0.804, 0.804)
RGB_LIGHTCYAN4                = (0.478, 0.545, 0.545)
RGB_PALETURQUOISE1            = (0.733, 1.000, 1.000)
RGB_PALETURQUOISE2            = (0.682, 0.933, 0.933)
RGB_PALETURQUOISE3            = (0.588, 0.804, 0.804)
RGB_PALETURQUOISE4            = (0.400, 0.545, 0.545)
RGB_CADETBLUE1                = (0.596, 0.961, 1.000)
RGB_CADETBLUE2                = (0.557, 0.898, 0.933)
RGB_CADETBLUE3                = (0.478, 0.773, 0.804)
RGB_CADETBLUE4                = (0.325, 0.525, 0.545)
RGB_TURQUOISE1                = (0.000, 0.961, 1.000)
RGB_TURQUOISE2                = (0.000, 0.898, 0.933)
RGB_TURQUOISE3                = (0.000, 0.773, 0.804)
RGB_TURQUOISE4                = (0.000, 0.525, 0.545)
RGB_CYAN1                     = (0.000, 1.000, 1.000)
RGB_CYAN2                     = (0.000, 0.933, 0.933)
RGB_CYAN3                     = (0.000, 0.804, 0.804)
RGB_CYAN4                     = (0.000, 0.545, 0.545)
RGB_DARKSLATEGRAY1            = (0.592, 1.000, 1.000)
RGB_DARKSLATEGRAY2            = (0.553, 0.933, 0.933)
RGB_DARKSLATEGRAY3            = (0.475, 0.804, 0.804)
RGB_DARKSLATEGRAY4            = (0.322, 0.545, 0.545)
RGB_AQUAMARINE1               = (0.498, 1.000, 0.831)
RGB_AQUAMARINE2               = (0.463, 0.933, 0.776)
RGB_AQUAMARINE3               = (0.400, 0.804, 0.667)
RGB_AQUAMARINE4               = (0.271, 0.545, 0.455)
RGB_DARKSEAGREEN1             = (0.757, 1.000, 0.757)
RGB_DARKSEAGREEN2             = (0.706, 0.933, 0.706)
RGB_DARKSEAGREEN3             = (0.608, 0.804, 0.608)
RGB_DARKSEAGREEN4             = (0.412, 0.545, 0.412)
RGB_SEAGREEN1                 = (0.329, 1.000, 0.624)
RGB_SEAGREEN2                 = (0.306, 0.933, 0.580)
RGB_SEAGREEN3                 = (0.263, 0.804, 0.502)
RGB_SEAGREEN4                 = (0.180, 0.545, 0.341)
RGB_PALEGREEN1                = (0.604, 1.000, 0.604)
RGB_PALEGREEN2                = (0.565, 0.933, 0.565)
RGB_PALEGREEN3                = (0.486, 0.804, 0.486)
RGB_PALEGREEN4                = (0.329, 0.545, 0.329)
RGB_SPRINGGREEN1              = (0.000, 1.000, 0.498)
RGB_SPRINGGREEN2              = (0.000, 0.933, 0.463)
RGB_SPRINGGREEN3              = (0.000, 0.804, 0.400)
RGB_SPRINGGREEN4              = (0.000, 0.545, 0.271)
RGB_GREEN1                    = (0.000, 1.000, 0.000)
RGB_GREEN2                    = (0.000, 0.933, 0.000)
RGB_GREEN3                    = (0.000, 0.804, 0.000)
RGB_GREEN4                    = (0.000, 0.545, 0.000)
RGB_CHARTREUSE1               = (0.498, 1.000, 0.000)
RGB_CHARTREUSE2               = (0.463, 0.933, 0.000)
RGB_CHARTREUSE3               = (0.400, 0.804, 0.000)
RGB_CHARTREUSE4               = (0.271, 0.545, 0.000)
RGB_OLIVEDRAB1                = (0.753, 1.000, 0.243)
RGB_OLIVEDRAB2                = (0.702, 0.933, 0.227)
RGB_OLIVEDRAB3                = (0.604, 0.804, 0.196)
RGB_OLIVEDRAB4                = (0.412, 0.545, 0.133)
RGB_DARKOLIVEGREEN1           = (0.792, 1.000, 0.439)
RGB_DARKOLIVEGREEN2           = (0.737, 0.933, 0.408)
RGB_DARKOLIVEGREEN3           = (0.635, 0.804, 0.353)
RGB_DARKOLIVEGREEN4           = (0.431, 0.545, 0.239)
RGB_KHAKI1                    = (1.000, 0.965, 0.561)
RGB_KHAKI2                    = (0.933, 0.902, 0.522)
RGB_KHAKI3                    = (0.804, 0.776, 0.451)
RGB_KHAKI4                    = (0.545, 0.525, 0.306)
RGB_LIGHTGOLDENROD1           = (1.000, 0.925, 0.545)
RGB_LIGHTGOLDENROD2           = (0.933, 0.863, 0.510)
RGB_LIGHTGOLDENROD3           = (0.804, 0.745, 0.439)
RGB_LIGHTGOLDENROD4           = (0.545, 0.506, 0.298)
RGB_LIGHTYELLOW1              = (1.000, 1.000, 0.878)
RGB_LIGHTYELLOW2              = (0.933, 0.933, 0.820)
RGB_LIGHTYELLOW3              = (0.804, 0.804, 0.706)
RGB_LIGHTYELLOW4              = (0.545, 0.545, 0.478)
RGB_YELLOW1                   = (1.000, 1.000, 0.000)
RGB_YELLOW2                   = (0.933, 0.933, 0.000)
RGB_YELLOW3                   = (0.804, 0.804, 0.000)
RGB_YELLOW4                   = (0.545, 0.545, 0.000)
RGB_GOLD1                     = (1.000, 0.843, 0.000)
RGB_GOLD2                     = (0.933, 0.788, 0.000)
RGB_GOLD3                     = (0.804, 0.678, 0.000)
RGB_GOLD4                     = (0.545, 0.459, 0.000)
RGB_GOLDENROD1                = (1.000, 0.757, 0.145)
RGB_GOLDENROD2                = (0.933, 0.706, 0.133)
RGB_GOLDENROD3                = (0.804, 0.608, 0.114)
RGB_GOLDENROD4                = (0.545, 0.412, 0.078)
RGB_DARKGOLDENROD1            = (1.000, 0.725, 0.059)
RGB_DARKGOLDENROD2            = (0.933, 0.678, 0.055)
RGB_DARKGOLDENROD3            = (0.804, 0.584, 0.047)
RGB_DARKGOLDENROD4            = (0.545, 0.396, 0.031)
RGB_ROSYBROWN1                = (1.000, 0.757, 0.757)
RGB_ROSYBROWN2                = (0.933, 0.706, 0.706)
RGB_ROSYBROWN3                = (0.804, 0.608, 0.608)
RGB_ROSYBROWN4                = (0.545, 0.412, 0.412)
RGB_INDIANRED1                = (1.000, 0.416, 0.416)
RGB_INDIANRED2                = (0.933, 0.388, 0.388)
RGB_INDIANRED3                = (0.804, 0.333, 0.333)
RGB_INDIANRED4                = (0.545, 0.227, 0.227)
RGB_SIENNA1                   = (1.000, 0.510, 0.278)
RGB_SIENNA2                   = (0.933, 0.475, 0.259)
RGB_SIENNA3                   = (0.804, 0.408, 0.224)
RGB_SIENNA4                   = (0.545, 0.278, 0.149)
RGB_BURLYWOOD1                = (1.000, 0.827, 0.608)
RGB_BURLYWOOD2                = (0.933, 0.773, 0.569)
RGB_BURLYWOOD3                = (0.804, 0.667, 0.490)
RGB_BURLYWOOD4                = (0.545, 0.451, 0.333)
RGB_WHEAT1                    = (1.000, 0.906, 0.729)
RGB_WHEAT2                    = (0.933, 0.847, 0.682)
RGB_WHEAT3                    = (0.804, 0.729, 0.588)
RGB_WHEAT4                    = (0.545, 0.494, 0.400)
RGB_TAN1                      = (1.000, 0.647, 0.310)
RGB_TAN2                      = (0.933, 0.604, 0.286)
RGB_TAN3                      = (0.804, 0.522, 0.247)
RGB_TAN4                      = (0.545, 0.353, 0.169)
RGB_CHOCOLATE1                = (1.000, 0.498, 0.141)
RGB_CHOCOLATE2                = (0.933, 0.463, 0.129)
RGB_CHOCOLATE3                = (0.804, 0.400, 0.114)
RGB_CHOCOLATE4                = (0.545, 0.271, 0.075)
RGB_FIREBRICK1                = (1.000, 0.188, 0.188)
RGB_FIREBRICK2                = (0.933, 0.173, 0.173)
RGB_FIREBRICK3                = (0.804, 0.149, 0.149)
RGB_FIREBRICK4                = (0.545, 0.102, 0.102)
RGB_BROWN1                    = (1.000, 0.251, 0.251)
RGB_BROWN2                    = (0.933, 0.231, 0.231)
RGB_BROWN3                    = (0.804, 0.200, 0.200)
RGB_BROWN4                    = (0.545, 0.137, 0.137)
RGB_SALMON1                   = (1.000, 0.549, 0.412)
RGB_SALMON2                   = (0.933, 0.510, 0.384)
RGB_SALMON3                   = (0.804, 0.439, 0.329)
RGB_SALMON4                   = (0.545, 0.298, 0.224)
RGB_LIGHTSALMON1              = (1.000, 0.627, 0.478)
RGB_LIGHTSALMON2              = (0.933, 0.584, 0.447)
RGB_LIGHTSALMON3              = (0.804, 0.506, 0.384)
RGB_LIGHTSALMON4              = (0.545, 0.341, 0.259)
RGB_ORANGE1                   = (1.000, 0.647, 0.000)
RGB_ORANGE2                   = (0.933, 0.604, 0.000)
RGB_ORANGE3                   = (0.804, 0.522, 0.000)
RGB_ORANGE4                   = (0.545, 0.353, 0.000)
RGB_DARKORANGE1               = (1.000, 0.498, 0.000)
RGB_DARKORANGE2               = (0.933, 0.463, 0.000)
RGB_DARKORANGE3               = (0.804, 0.400, 0.000)
RGB_DARKORANGE4               = (0.545, 0.271, 0.000)
RGB_CORAL1                    = (1.000, 0.447, 0.337)
RGB_CORAL2                    = (0.933, 0.416, 0.314)
RGB_CORAL3                    = (0.804, 0.357, 0.271)
RGB_CORAL4                    = (0.545, 0.243, 0.184)
RGB_TOMATO1                   = (1.000, 0.388, 0.278)
RGB_TOMATO2                   = (0.933, 0.361, 0.259)
RGB_TOMATO3                   = (0.804, 0.310, 0.224)
RGB_TOMATO4                   = (0.545, 0.212, 0.149)
RGB_ORANGERED1                = (1.000, 0.271, 0.000)
RGB_ORANGERED2                = (0.933, 0.251, 0.000)
RGB_ORANGERED3                = (0.804, 0.216, 0.000)
RGB_ORANGERED4                = (0.545, 0.145, 0.000)
RGB_RED1                      = (1.000, 0.000, 0.000)
RGB_RED2                      = (0.933, 0.000, 0.000)
RGB_RED3                      = (0.804, 0.000, 0.000)
RGB_RED4                      = (0.545, 0.000, 0.000)
RGB_DEEPPINK1                 = (1.000, 0.078, 0.576)
RGB_DEEPPINK2                 = (0.933, 0.071, 0.537)
RGB_DEEPPINK3                 = (0.804, 0.063, 0.463)
RGB_DEEPPINK4                 = (0.545, 0.039, 0.314)
RGB_HOTPINK1                  = (1.000, 0.431, 0.706)
RGB_HOTPINK2                  = (0.933, 0.416, 0.655)
RGB_HOTPINK3                  = (0.804, 0.376, 0.565)
RGB_HOTPINK4                  = (0.545, 0.227, 0.384)
RGB_PINK1                     = (1.000, 0.710, 0.773)
RGB_PINK2                     = (0.933, 0.663, 0.722)
RGB_PINK3                     = (0.804, 0.569, 0.620)
RGB_PINK4                     = (0.545, 0.388, 0.424)
RGB_LIGHTPINK1                = (1.000, 0.682, 0.725)
RGB_LIGHTPINK2                = (0.933, 0.635, 0.678)
RGB_LIGHTPINK3                = (0.804, 0.549, 0.584)
RGB_LIGHTPINK4                = (0.545, 0.373, 0.396)
RGB_PALEVIOLETRED1            = (1.000, 0.510, 0.671)
RGB_PALEVIOLETRED2            = (0.933, 0.475, 0.624)
RGB_PALEVIOLETRED3            = (0.804, 0.408, 0.537)
RGB_PALEVIOLETRED4            = (0.545, 0.278, 0.365)
RGB_MAROON1                   = (1.000, 0.204, 0.702)
RGB_MAROON2                   = (0.933, 0.188, 0.655)
RGB_MAROON3                   = (0.804, 0.161, 0.565)
RGB_MAROON4                   = (0.545, 0.110, 0.384)
RGB_VIOLETRED1                = (1.000, 0.243, 0.588)
RGB_VIOLETRED2                = (0.933, 0.227, 0.549)
RGB_VIOLETRED3                = (0.804, 0.196, 0.471)
RGB_VIOLETRED4                = (0.545, 0.133, 0.322)
RGB_MAGENTA1                  = (1.000, 0.000, 1.000)
RGB_MAGENTA2                  = (0.933, 0.000, 0.933)
RGB_MAGENTA3                  = (0.804, 0.000, 0.804)
RGB_MAGENTA4                  = (0.545, 0.000, 0.545)
RGB_ORCHID1                   = (1.000, 0.514, 0.980)
RGB_ORCHID2                   = (0.933, 0.478, 0.914)
RGB_ORCHID3                   = (0.804, 0.412, 0.788)
RGB_ORCHID4                   = (0.545, 0.278, 0.537)
RGB_PLUM1                     = (1.000, 0.733, 1.000)
RGB_PLUM2                     = (0.933, 0.682, 0.933)
RGB_PLUM3                     = (0.804, 0.588, 0.804)
RGB_PLUM4                     = (0.545, 0.400, 0.545)
RGB_MEDIUMORCHID1             = (0.878, 0.400, 1.000)
RGB_MEDIUMORCHID2             = (0.820, 0.373, 0.933)
RGB_MEDIUMORCHID3             = (0.706, 0.322, 0.804)
RGB_MEDIUMORCHID4             = (0.478, 0.216, 0.545)
RGB_DARKORCHID1               = (0.749, 0.243, 1.000)
RGB_DARKORCHID2               = (0.698, 0.227, 0.933)
RGB_DARKORCHID3               = (0.604, 0.196, 0.804)
RGB_DARKORCHID4               = (0.408, 0.133, 0.545)
RGB_PURPLE1                   = (0.608, 0.188, 1.000)
RGB_PURPLE2                   = (0.569, 0.173, 0.933)
RGB_PURPLE3                   = (0.490, 0.149, 0.804)
RGB_PURPLE4                   = (0.333, 0.102, 0.545)
RGB_MEDIUMPURPLE1             = (0.671, 0.510, 1.000)
RGB_MEDIUMPURPLE2             = (0.624, 0.475, 0.933)
RGB_MEDIUMPURPLE3             = (0.537, 0.408, 0.804)
RGB_MEDIUMPURPLE4             = (0.365, 0.278, 0.545)
RGB_THISTLE1                  = (1.000, 0.882, 1.000)
RGB_THISTLE2                  = (0.933, 0.824, 0.933)
RGB_THISTLE3                  = (0.804, 0.710, 0.804)
RGB_THISTLE4                  = (0.545, 0.482, 0.545)
RGB_GRAY0                     = (0.000, 0.000, 0.000)
RGB_GREY0                     = (0.000, 0.000, 0.000)
RGB_GRAY1                     = (0.012, 0.012, 0.012)
RGB_GREY1                     = (0.012, 0.012, 0.012)
RGB_GRAY2                     = (0.020, 0.020, 0.020)
RGB_GREY2                     = (0.020, 0.020, 0.020)
RGB_GRAY3                     = (0.031, 0.031, 0.031)
RGB_GREY3                     = (0.031, 0.031, 0.031)
RGB_GRAY4                     = (0.039, 0.039, 0.039)
RGB_GREY4                     = (0.039, 0.039, 0.039)
RGB_GRAY5                     = (0.051, 0.051, 0.051)
RGB_GREY5                     = (0.051, 0.051, 0.051)
RGB_GRAY6                     = (0.059, 0.059, 0.059)
RGB_GREY6                     = (0.059, 0.059, 0.059)
RGB_GRAY7                     = (0.071, 0.071, 0.071)
RGB_GREY7                     = (0.071, 0.071, 0.071)
RGB_GRAY8                     = (0.078, 0.078, 0.078)
RGB_GREY8                     = (0.078, 0.078, 0.078)
RGB_GRAY9                     = (0.090, 0.090, 0.090)
RGB_GREY9                     = (0.090, 0.090, 0.090)
RGB_GRAY10                    = (0.102, 0.102, 0.102)
RGB_GREY10                    = (0.102, 0.102, 0.102)
RGB_GRAY11                    = (0.110, 0.110, 0.110)
RGB_GREY11                    = (0.110, 0.110, 0.110)
RGB_GRAY12                    = (0.122, 0.122, 0.122)
RGB_GREY12                    = (0.122, 0.122, 0.122)
RGB_GRAY13                    = (0.129, 0.129, 0.129)
RGB_GREY13                    = (0.129, 0.129, 0.129)
RGB_GRAY14                    = (0.141, 0.141, 0.141)
RGB_GREY14                    = (0.141, 0.141, 0.141)
RGB_GRAY15                    = (0.149, 0.149, 0.149)
RGB_GREY15                    = (0.149, 0.149, 0.149)
RGB_GRAY16                    = (0.161, 0.161, 0.161)
RGB_GREY16                    = (0.161, 0.161, 0.161)
RGB_GRAY17                    = (0.169, 0.169, 0.169)
RGB_GREY17                    = (0.169, 0.169, 0.169)
RGB_GRAY18                    = (0.180, 0.180, 0.180)
RGB_GREY18                    = (0.180, 0.180, 0.180)
RGB_GRAY19                    = (0.188, 0.188, 0.188)
RGB_GREY19                    = (0.188, 0.188, 0.188)
RGB_GRAY20                    = (0.200, 0.200, 0.200)
RGB_GREY20                    = (0.200, 0.200, 0.200)
RGB_GRAY21                    = (0.212, 0.212, 0.212)
RGB_GREY21                    = (0.212, 0.212, 0.212)
RGB_GRAY22                    = (0.220, 0.220, 0.220)
RGB_GREY22                    = (0.220, 0.220, 0.220)
RGB_GRAY23                    = (0.231, 0.231, 0.231)
RGB_GREY23                    = (0.231, 0.231, 0.231)
RGB_GRAY24                    = (0.239, 0.239, 0.239)
RGB_GREY24                    = (0.239, 0.239, 0.239)
RGB_GRAY25                    = (0.251, 0.251, 0.251)
RGB_GREY25                    = (0.251, 0.251, 0.251)
RGB_GRAY26                    = (0.259, 0.259, 0.259)
RGB_GREY26                    = (0.259, 0.259, 0.259)
RGB_GRAY27                    = (0.271, 0.271, 0.271)
RGB_GREY27                    = (0.271, 0.271, 0.271)
RGB_GRAY28                    = (0.278, 0.278, 0.278)
RGB_GREY28                    = (0.278, 0.278, 0.278)
RGB_GRAY29                    = (0.290, 0.290, 0.290)
RGB_GREY29                    = (0.290, 0.290, 0.290)
RGB_GRAY30                    = (0.302, 0.302, 0.302)
RGB_GREY30                    = (0.302, 0.302, 0.302)
RGB_GRAY31                    = (0.310, 0.310, 0.310)
RGB_GREY31                    = (0.310, 0.310, 0.310)
RGB_GRAY32                    = (0.322, 0.322, 0.322)
RGB_GREY32                    = (0.322, 0.322, 0.322)
RGB_GRAY33                    = (0.329, 0.329, 0.329)
RGB_GREY33                    = (0.329, 0.329, 0.329)
RGB_GRAY34                    = (0.341, 0.341, 0.341)
RGB_GREY34                    = (0.341, 0.341, 0.341)
RGB_GRAY35                    = (0.349, 0.349, 0.349)
RGB_GREY35                    = (0.349, 0.349, 0.349)
RGB_GRAY36                    = (0.361, 0.361, 0.361)
RGB_GREY36                    = (0.361, 0.361, 0.361)
RGB_GRAY37                    = (0.369, 0.369, 0.369)
RGB_GREY37                    = (0.369, 0.369, 0.369)
RGB_GRAY38                    = (0.380, 0.380, 0.380)
RGB_GREY38                    = (0.380, 0.380, 0.380)
RGB_GRAY39                    = (0.388, 0.388, 0.388)
RGB_GREY39                    = (0.388, 0.388, 0.388)
RGB_GRAY40                    = (0.400, 0.400, 0.400)
RGB_GREY40                    = (0.400, 0.400, 0.400)
RGB_GRAY41                    = (0.412, 0.412, 0.412)
RGB_GREY41                    = (0.412, 0.412, 0.412)
RGB_GRAY42                    = (0.420, 0.420, 0.420)
RGB_GREY42                    = (0.420, 0.420, 0.420)
RGB_GRAY43                    = (0.431, 0.431, 0.431)
RGB_GREY43                    = (0.431, 0.431, 0.431)
RGB_GRAY44                    = (0.439, 0.439, 0.439)
RGB_GREY44                    = (0.439, 0.439, 0.439)
RGB_GRAY45                    = (0.451, 0.451, 0.451)
RGB_GREY45                    = (0.451, 0.451, 0.451)
RGB_GRAY46                    = (0.459, 0.459, 0.459)
RGB_GREY46                    = (0.459, 0.459, 0.459)
RGB_GRAY47                    = (0.471, 0.471, 0.471)
RGB_GREY47                    = (0.471, 0.471, 0.471)
RGB_GRAY48                    = (0.478, 0.478, 0.478)
RGB_GREY48                    = (0.478, 0.478, 0.478)
RGB_GRAY49                    = (0.490, 0.490, 0.490)
RGB_GREY49                    = (0.490, 0.490, 0.490)
RGB_GRAY50                    = (0.498, 0.498, 0.498)
RGB_GREY50                    = (0.498, 0.498, 0.498)
RGB_GRAY51                    = (0.510, 0.510, 0.510)
RGB_GREY51                    = (0.510, 0.510, 0.510)
RGB_GRAY52                    = (0.522, 0.522, 0.522)
RGB_GREY52                    = (0.522, 0.522, 0.522)
RGB_GRAY53                    = (0.529, 0.529, 0.529)
RGB_GREY53                    = (0.529, 0.529, 0.529)
RGB_GRAY54                    = (0.541, 0.541, 0.541)
RGB_GREY54                    = (0.541, 0.541, 0.541)
RGB_GRAY55                    = (0.549, 0.549, 0.549)
RGB_GREY55                    = (0.549, 0.549, 0.549)
RGB_GRAY56                    = (0.561, 0.561, 0.561)
RGB_GREY56                    = (0.561, 0.561, 0.561)
RGB_GRAY57                    = (0.569, 0.569, 0.569)
RGB_GREY57                    = (0.569, 0.569, 0.569)
RGB_GRAY58                    = (0.580, 0.580, 0.580)
RGB_GREY58                    = (0.580, 0.580, 0.580)
RGB_GRAY59                    = (0.588, 0.588, 0.588)
RGB_GREY59                    = (0.588, 0.588, 0.588)
RGB_GRAY60                    = (0.600, 0.600, 0.600)
RGB_GREY60                    = (0.600, 0.600, 0.600)
RGB_GRAY61                    = (0.612, 0.612, 0.612)
RGB_GREY61                    = (0.612, 0.612, 0.612)
RGB_GRAY62                    = (0.620, 0.620, 0.620)
RGB_GREY62                    = (0.620, 0.620, 0.620)
RGB_GRAY63                    = (0.631, 0.631, 0.631)
RGB_GREY63                    = (0.631, 0.631, 0.631)
RGB_GRAY64                    = (0.639, 0.639, 0.639)
RGB_GREY64                    = (0.639, 0.639, 0.639)
RGB_GRAY65                    = (0.651, 0.651, 0.651)
RGB_GREY65                    = (0.651, 0.651, 0.651)
RGB_GRAY66                    = (0.659, 0.659, 0.659)
RGB_GREY66                    = (0.659, 0.659, 0.659)
RGB_GRAY67                    = (0.671, 0.671, 0.671)
RGB_GREY67                    = (0.671, 0.671, 0.671)
RGB_GRAY68                    = (0.678, 0.678, 0.678)
RGB_GREY68                    = (0.678, 0.678, 0.678)
RGB_GRAY69                    = (0.690, 0.690, 0.690)
RGB_GREY69                    = (0.690, 0.690, 0.690)
RGB_GRAY70                    = (0.702, 0.702, 0.702)
RGB_GREY70                    = (0.702, 0.702, 0.702)
RGB_GRAY71                    = (0.710, 0.710, 0.710)
RGB_GREY71                    = (0.710, 0.710, 0.710)
RGB_GRAY72                    = (0.722, 0.722, 0.722)
RGB_GREY72                    = (0.722, 0.722, 0.722)
RGB_GRAY73                    = (0.729, 0.729, 0.729)
RGB_GREY73                    = (0.729, 0.729, 0.729)
RGB_GRAY74                    = (0.741, 0.741, 0.741)
RGB_GREY74                    = (0.741, 0.741, 0.741)
RGB_GRAY75                    = (0.749, 0.749, 0.749)
RGB_GREY75                    = (0.749, 0.749, 0.749)
RGB_GRAY76                    = (0.761, 0.761, 0.761)
RGB_GREY76                    = (0.761, 0.761, 0.761)
RGB_GRAY77                    = (0.769, 0.769, 0.769)
RGB_GREY77                    = (0.769, 0.769, 0.769)
RGB_GRAY78                    = (0.780, 0.780, 0.780)
RGB_GREY78                    = (0.780, 0.780, 0.780)
RGB_GRAY79                    = (0.788, 0.788, 0.788)
RGB_GREY79                    = (0.788, 0.788, 0.788)
RGB_GRAY80                    = (0.800, 0.800, 0.800)
RGB_GREY80                    = (0.800, 0.800, 0.800)
RGB_GRAY81                    = (0.812, 0.812, 0.812)
RGB_GREY81                    = (0.812, 0.812, 0.812)
RGB_GRAY82                    = (0.820, 0.820, 0.820)
RGB_GREY82                    = (0.820, 0.820, 0.820)
RGB_GRAY83                    = (0.831, 0.831, 0.831)
RGB_GREY83                    = (0.831, 0.831, 0.831)
RGB_GRAY84                    = (0.839, 0.839, 0.839)
RGB_GREY84                    = (0.839, 0.839, 0.839)
RGB_GRAY85                    = (0.851, 0.851, 0.851)
RGB_GREY85                    = (0.851, 0.851, 0.851)
RGB_GRAY86                    = (0.859, 0.859, 0.859)
RGB_GREY86                    = (0.859, 0.859, 0.859)
RGB_GRAY87                    = (0.871, 0.871, 0.871)
RGB_GREY87                    = (0.871, 0.871, 0.871)
RGB_GRAY88                    = (0.878, 0.878, 0.878)
RGB_GREY88                    = (0.878, 0.878, 0.878)
RGB_GRAY89                    = (0.890, 0.890, 0.890)
RGB_GREY89                    = (0.890, 0.890, 0.890)
RGB_GRAY90                    = (0.898, 0.898, 0.898)
RGB_GREY90                    = (0.898, 0.898, 0.898)
RGB_GRAY91                    = (0.910, 0.910, 0.910)
RGB_GREY91                    = (0.910, 0.910, 0.910)
RGB_GRAY92                    = (0.922, 0.922, 0.922)
RGB_GREY92                    = (0.922, 0.922, 0.922)
RGB_GRAY93                    = (0.929, 0.929, 0.929)
RGB_GREY93                    = (0.929, 0.929, 0.929)
RGB_GRAY94                    = (0.941, 0.941, 0.941)
RGB_GREY94                    = (0.941, 0.941, 0.941)
RGB_GRAY95                    = (0.949, 0.949, 0.949)
RGB_GREY95                    = (0.949, 0.949, 0.949)
RGB_GRAY96                    = (0.961, 0.961, 0.961)
RGB_GREY96                    = (0.961, 0.961, 0.961)
RGB_GRAY97                    = (0.969, 0.969, 0.969)
RGB_GREY97                    = (0.969, 0.969, 0.969)
RGB_GRAY98                    = (0.980, 0.980, 0.980)
RGB_GREY98                    = (0.980, 0.980, 0.980)
RGB_GRAY99                    = (0.988, 0.988, 0.988)
RGB_GREY99                    = (0.988, 0.988, 0.988)
RGB_GRAY100                   = (1.000, 1.000, 1.000)
RGB_GREY100                   = (1.000, 1.000, 1.000)
RGB_DARK_GREY                 = (0.663, 0.663, 0.663)
RGB_DARKGREY                  = (0.663, 0.663, 0.663)
RGB_DARK_GRAY                 = (0.663, 0.663, 0.663)
RGB_DARKGRAY                  = (0.663, 0.663, 0.663)
RGB_DARK_BLUE                 = (0.000, 0.000, 0.545)
RGB_DARKBLUE                  = (0.000, 0.000, 0.545)
RGB_DARK_CYAN                 = (0.000, 0.545, 0.545)
RGB_DARKCYAN                  = (0.000, 0.545, 0.545)
RGB_DARK_MAGENTA              = (0.545, 0.000, 0.545)
RGB_DARKMAGENTA               = (0.545, 0.000, 0.545)
RGB_DARK_RED                  = (0.545, 0.000, 0.000)
RGB_DARKRED                   = (0.545, 0.000, 0.000)
RGB_LIGHT_GREEN               = (0.565, 0.933, 0.565)
RGB_LIGHTGREEN                = (0.565, 0.933, 0.565)
=======================
settings.py
----------------------
# coding: utf-8
"""settings.py --- settings for vizualizer application.
"""

class Settings(object):
    """Simple settings container.
    """

    def __init__(self, **kwargs):
        """Initializer.
        """
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Updates current setting attributs with given kwargs.
        """
        for k, v in kwargs.items():
            if not k.startswith('_'):
                setattr(self, k, v)


# built-in settings
import default_settings
settings = Settings(**default_settings.__dict__)
del default_settings


def configure(**kwargs):
    """Overrides settings
    """
    settings.configure(**kwargs)


if __name__=='__main__':
    # TBD: unittest
    from doctest import *
    testmod(optionflags=ELLIPSIS)

=======================
utils.py
----------------------
# coding: utf-8
"""Various utility classes.
"""
=======================
utils_wx.py
----------------------
# coding: utf-8
"""Various wx-related utility classes
"""
import wx


class TreeCtrlPlus(wx.TreeCtrl):
    
    BINDINGS = (
        ('BEGIN_DRAG', 'OnBeginDrag'),
        ('BEGIN_RDRAG', 'OnBeginRDrag'),
        ('END_DRAG', 'OnEndDrag'),
        ('BEGIN_LABEL_EDIT', 'OnBeginLabelEdit'),
        ('END_LABEL_EDIT', 'OnEndLabelEdit'),
        ('DELETE_ITEM', 'OnDeleteItem'),
        ('GET_INFO', 'OnGetInfo'),
        ('SET_INFO', 'OnSetInfo'),
        ('ITEM_ACTIVATED', 'OnItemActivated'),
        ('ITEM_COLLAPSED', 'OnItemCollapsed'),
        ('ITEM_COLLAPSING', 'OnItemCollapsing'),
        ('ITEM_EXPANDED', 'OnItemExpanded'),
        ('ITEM_EXPANDING', 'OnItemExpanding'),
        ('ITEM_RIGHT_CLICK', 'OnItemRightClick'),
        ('ITEM_MIDDLE_CLICK', 'OnItemMiddleClick'),
        ('SEL_CHANGED', 'OnSelChanged'),
        ('SEL_CHANGING', 'OnSelChanging'),
        ('KEY_DOWN', 'OnKeyDown'),
        ('ITEM_GETTOOLTIP', 'OnItemGetToolTip'),
        ('ITEM_MENU', 'OnItemMenu'),
        ('STATE_IMAGE_CLICK', 'OnStateImageClick'),
        )    


    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        for evt_name, handler_name in self.BINDINGS:
            macro = getattr(wx, 'EVT_TREE_'+evt_name)
            handler = getattr(self, handler_name, None)
            if handler:
                self.Bind(macro, handler, self)
        
    def OnBeginDrag(self, evt):
        """Handler called on begin item dragging.
        """
        pass # do nothing atm

    def OnBeginRDrag(self, evt):
        """Handler called on begin item dragging with right button.
        """
        pass # do nothing atm

    def OnEndDrag(self, evt):
        """Handler called on end item dragging.
        """
        pass # do nothing atm

    def OnBeginLabelEdit(self, evt):
        """Handler called on begin editing label on an item.
        """
        pass # do nothing atm

    def OnEndLabelEdit(self, evt):
        """Handler called on end editing label on an item.
        """
        pass # do nothing atm

    def OnDeleteItem(self, evt):
        """Handler called on deleting item.
        """
        pass # do nothing atm

    def OnGetInfo(self, evt):
        """Handler called on getting node info.
        """
        pass # do nothing atm

    def OnSetInfo(self, evt):
        """Handler called on getting node info.
        """
        pass # do nothing atm

    def OnItemActivated(self, evt):
        """Handler called on activating item.
        """
        pass # do nothing atm

    def OnItemCollapsed(self, evt):
        """Handler called on an item has collapsed.
        """
        pass # do nothing atm

    def OnItemCollapsing(self, evt):
        """Handler called on collapsing an item.
        """
        pass # do nothing atm

    def OnItemExpanded(self, evt):
        """Handler called on an item has expanded.
        """
        pass # do nothing atm
        
    def OnItemExpanding(self, evt):
        """Handler called on expanding item.
        """
        pass # do nothing atm

    def OnItemRightClick(self, evt):
        """Handler called on right-clicking item.
        """
        pass # do nothing atm

    def OnItemMiddleClick(self, evt):
        """Handler called on middle-clicking item.
        """
        pass # do nothing atm

    def OnSelChanged(self, evt):
        """Handler called on user has changed item selection.
        """
        pass # do nothing atm

    def OnSelChanging(self, evt):
        """Handler called on changing selection.
        """
        pass # do nothing atm

    def OnKeyDown(self, evt):
        """Handler called on key down.
        """
        pass # do nothing atm

    def OnItemGetToolTip(self, evt):
        """Handler called on getting tooltip
        """
        pass # do nothing atm

    def OnItemMenu(self, evt):
        """Handler called on requiring context menu.
        """
        pass # do nothing atm

    def OnStateImageClick(self, evt):
        """Handler called on clicing state image.
        """
        pass # do nothing atm

if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
=======================
visual.py
----------------------
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
=======================
visual_panel.py
----------------------
# coding: utf-8
"""visual_panel.py --- Visual inspector panel in control panel.
"""
import wx
from wx.dataview import (
    DataViewListCtrl, PyDataViewModel, NullDataViewItem)


class VisualDataViewModel(PyDataViewModel):
    """Data model for VisualDataViewListCtrl.
    """
    # almost same as FileDataViewModel.
    def __init__(self, data, *args, **kwargs):
        """Initializer.
        """
        PyDataViewModel.__init__(self, *args, **kwargs)
        self.data = data

    def GetColumnCount(self):
        return 2

    def GetColumnType(self, col):
        return ['bool', 'string'][col]

    def GetChildren(self, parent, children):
        n_children = 0
        if not parent:
            for obj in self.data:
                children.append(self.ObjectToItem(obj))
            n_children = len(self.data)
        return n_children

    def IsContainer(self, item):
        if not item:
            return True
        return False

    def GetParent(self, item):
        return NullDataViewItem

    def GetValue(self, item, col):
        node = self.ItemToObject(item)
        if node:
            """
            if col==0:
                return node.checked
            else:
                return node.path"""
            return node[col]

    def SetValue(self, value, item, col):
        node = self.ItemToObject(item)
        if node:
            """
            if col==0:
                node.checked = value
            else:
                node.path = value"""
            node[col] = value


class VisualDataViewListCtrl(DataViewListCtrl):
    """DataViewListCtrl for visual list.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        DataViewListCtrl.__init__(self, *args, **kwargs)
        visible_column = self.AppendToggleColumn('Visible', width=40)
        name_column = self.AppendTextColumn('Name')
        # for auto-column-width hack
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.visible_column = visible_column
        self.name_column = name_column

    def AssociateModel(self, model):
        """Overriden method to fix unaware-prepopulated-items bug.
        """
        DataViewListCtrl.AssociateModel(self, model)
        # this is called to fix errornours behaviour
        # that DVLC does not refresh rows when
        # AssociateModel() is called with a populated model.
        model.AfterReset()

    def OnSize(self, event):
        """Adjusts file column width.
        """
        width = self.GetClientSize()[0]-10
        self.name_column.SetWidth(width-self.visible_column.GetWidth())
        

class VisualPanel(wx.Panel):
    """Visual controlls panel.
    """
    def __init__(self, *args, **kwargs):
        kwargs['style'] = kwargs.get('style', 0)|wx.BORDER_SUNKEN
        wx.Panel.__init__(self, *args, **kwargs)
        visual_list = VisualDataViewListCtrl(self, -1, style=wx.BORDER_SUNKEN)
        # name bindings
        self.visual_list = visual_list
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(wx.StaticText(self, -1, u'Visuals'), 0, wx.ALL, 5)
        root_sizer.Add(visual_list, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(root_sizer)


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visual Panel Demo')
            visual_panel = VisualPanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(visual_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
=======================
visualizer.py
----------------------
# coding: utf-8
from collections import OrderedDict

import wx

# exception
class VisualizerError(Exception):
    """Exception class for visualizer
    """
    pass


# Visualizer registry
VISUALIZER_CLASSES = {}
def register(visualizer_class, name=None):
    """Registers a visualizer class into VISUALIZER_CLASSES registry.
    """
    # if no name is given, use name of the class.
    if name is None:
        name = visualizer_class.__name__
    VISUALIZER_CLASSES[name] = visualizer_class


class VisualizerEventResponder(object):
    """Null responder implemnentation.
    """
    def get_ui_root(self):
        """Returns root window for visualizer configuration UI.
        """
        return wx.GetApp().GetTopWindow()

    def process_source_done(self, sender, source, error=None):
        """Hook called on process_source() finished.
        """
        pass

    def process_sources_start(self, sender, sources):
        """Hook called on process_sources() begins. Note sources plural.
        """
        pass

    def process_sources_done(self, sender, sources):
        """Hook called on process_sources() finished. Note sources plural.
        """
        pass

        
class Visualizer(object):
    """
    Base class for visualizers.

    Lifecycle:
    v = Visualizer()               # instantiate
    v.configure()                  # update configuration
    v.initialize()                 # subclass-specific initialization
    for bit in bits:
      data_id = v.register_data(bits)  # register data frame
    for data_id in data_ids:
      v.select_data(data_id)       # select data to render
      # some Render() action.
    v.finalize()                   # finalize.
      
    """
    CONFIGURATION_UI_CLASS = None # Set this if your subclass supports configuration UI.
    
    def __init__(self, responder, renderer, *args, **kwargs):
        """
        Initializer.

        Arguments:
        responder --- Action responder.
        renderer --- VTK renderer.
        
        Attributes:
        responder --- Action responder. Usually an wxApp instance.
        renderer --- VTK renderer.
        visuals --- Dictionary of name => (visual, enabled)
        data_registry --- (Ordered) dictionary of data_id => validated_data
        current_data_id --- Currently selected data's id
        
        """
        if responder is None: # fallback to Null implementation.
            responder = VisualizerEventResponder()
        self.responder = responder
        self.renderer = renderer
        self.visuals = OrderedDict()
        self.data_objects = []
        self.current_data_id = None
        self.configuration_ui = None

    # lifecycle methods
    def initialize(self):
        """
        Visualizer-specific initializer.

        This method is called from application just *before* a visualizer
        is being attached to an application. Any configuration or
        preparation can be done in this method.
        
        """
        # In subclasses, you should update visuals first, then call
        # Visualizer.initialize() to make show(True) called for all visuals.
        self.show(True)

    def reset(self):
        """Reset visualizer. Subclass should override.
        """
        self.initialize()

    def finalize(self):
        """
        Visualizer-specific finalizer.

        This method is called from application just *after* a visualizer
        has been detached from an application. Saving changes,
        releasing resources or any other finalization process can be
        done in this method.

        """
        for visual in self.visuals.values():
            if visual.enabled:
                visual.disable()
        # force clearing all props
        self.renderer.RemoveAllViewProps()
                

    def show(self, status=True):
        """Show/hide all visuals.
        """
        for visual in self.visuals.values():
            visual.show(status)

    def update_visuals(self):
        """Update visuals to current state. Subclass may override.
        """
        current_data = None
        if self.current_data_id:
            # search for info having exact data_id
            for info in self.data_objects:
                if info[0]==self.current_data_id:
                    # assuming last item of the info points data
                    current_data = info[-1]
        for visual in self.visuals.values():
            visual.update(current_data)

    def update(self, data_id=None):
        """Update internal status of the visualizer.
        """
        self.current_data_id = data_id
        self.update_visuals()

    # source handling methods
    def process_source(self, source):
        """
        Process individual source to update data registry.

        You may want to update self.data_objects with generated data.
        Note that each item of data_objects should be a *list* of
        [id, Type, Name, data_object].
        
        """
        pass
    
    def process_sources(self, sources):
        """Process souce to update data registry.
        """
        self.data_objects = []
        self.responder.process_sources_start(self, sources)
        for source in sources:
            error = None
            try:
                self.process_source(source)
            except Exception, e:
                error = e
                pass
            self.responder.process_source_done(self, source, error)
        self.responder.process_sources_done(self, sources)
        # reset current data cursor
        if len(self.data_objects):
            self.current_data_index = 0
        else:
            self.current_data_index = None

    # Configuration-UI-related methods
    @property
    def has_configuration_ui(self):
        """Returns True if visualizer has configuration ui.
        """
        return bool(getattr(self, 'CONFIGURATION_UI_CLASS'))

    def load_configuration_ui(self):
        """Loads configuration ui.
        """
        if self.has_configuration_ui==False:
            return
        ui_root = None
        if self.configuration_ui is None:
            self.ui_root = self.responder.get_ui_root()
        configuration_ui = self.CONFIGURATION_UI_CLASS(self, ui_root)
        configuration_ui.Show(True)
        self.configuration_ui = configuration_ui

    def configure(self, configuration):
        """Configure visualizer.
        """
        pass

    # misc
    def move_data_ordering(self, data_id, offset):
        """Move data in data-object list.
        """
        data_objects = self.data_objects
        for index, record in enumerate(data_objects):
            if data_id==record[0]:
                if 0<=index+offset<len(data_objects):
                    index_from = min(index, index+offset)
                    index_to = max(index, index+offset)+1
                    data_objects[index_from:index_to] = data_objects[index_from:index_to][::-1]
                    break
                

# XXX These interfaces are prepared for future development.
#
#
#     def clear_data(self):
#         """Clears all data registered so far.
#         """
#         self.current_data = None
#         self.data_registry.clear()
#         self.update_visuals()

#     def validate_data(self, data):
#         """Validate data and return validated result. Otherwise raise exception.
#         """
#         return data

#     def unregister_data(self, data_id):
#         """Unregister data and return.
#         """
#         if (self.current_data and
#             self.data_registry.get(data_id, None)==self.current_data):
#             self.current_data = None
#             self.update_visuals()
#         return self.data_registry.pop(data_id, None)

#     def register_data(self, data_id, data):
#         """Register data to internal registry. May raise exception in error.
#         """
#         self.data_registry[data_id] = self.validate_data(data)
#         self.update_visuals()

#     def select_data(self, data_id):
#         """Select data frame to reflect current visual state.
#         """
#         self.current_data = self.data_registry.get(data_id, None)
#         self.update_visuals()


class VisualizerConfigurationUi(wx.Frame):
    """Base class for configuration panel.
    """
    def __init__(self, visualizer, *args, **kwargs):
        """Initializer.
        """
        self.visualizer = visualizer
        wx.Frame.__init__(self, *args, **kwargs)


if __name__=='__main__':
    """Demonstrative app.
    """
    import vtk
    from render_window import RenderWindowPanel
    from visual import StaticActorsVisual

    class DemoVisual(StaticActorsVisual):
        def _create_actors(self):
            """Creates demo cone actors.
            """
            cone = vtk.vtkConeSource()
            cone.SetResolution(8)
            coneMapper = vtk.vtkPolyDataMapper()
            coneMapper.SetInput(cone.GetOutput())
            coneActor = vtk.vtkActor()
            coneActor.SetMapper(coneMapper)
            self._actors['Cone'] = coneActor

    class DemoVisualizer(Visualizer):
        def initialize(self):
            Visualizer.initialize(self)
            self.visuals = {'Cone': DemoVisual(self.renderer)}

    class VisualizerDemoApp(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            frame = wx.Frame(None, -1, u'RenderWindowPanel demo',
                             size=(400, 400))
            render_window_panel = RenderWindowPanel(frame, -1)
            self.renderer = render_window_panel.renderer
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(render_window_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            visualizer = DemoVisualizer(self, self.renderer)
            visualizer.initialize()
            visualizer.show()
            self.SetTopWindow(frame)
            return True

    app = VisualizerDemoApp(0)
    app.MainLoop()
=======================
visualizer_panel.py
----------------------
# coding: utf-8
"""visualizer_panel.py --- visualizer panel
"""
import wx
from wx.dataview import (
    DataViewListCtrl, PyDataViewModel, NullDataViewItem)


class DataViewModelPlus(PyDataViewModel):
    """Enhanced DataViewModel.
    """
    def __init__(self, data, *args, **kwargs):
        """Initialzer.
        """
        PyDataViewModel.__init__(self, *args, **kwargs)
        self.data = data

    def GetChildren(self, parent, children):
        n_children = 0
        if not parent:
            for obj in self.data:
                children.append(self.ObjectToItem(obj))
            n_children = len(self.data)
        return n_children

    def IsContainer(self, item):
        if item is None:
            return True
        return False

    def GetParent(self, item):
        return NullDataViewItem

    def GetValue(self, item, col):
        node = self.ItemToObject(item)
        if node:
            return node[col]

    def SetValue(self, value, item, col):
        node = self.ItemToObject(item)
        if node:
            node[col] = value


class DataViewListCtrlPlus(DataViewListCtrl):
    """Enhanced DataViewListCtrl for source list.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        DataViewListCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self._columns = [] # (columns, width_ratio)
        self._populate_columns()

    def _populate_columns(self):
        """Subclass should override to poplulate columns.
        """
        return NotImplemented

    def AssociateModel(self, model):
        """Overriden method to fix unaware-prepopulated-items bug.
        """
        DataViewListCtrl.AssociateModel(self, model)
        # this is called to fix errornours behaviour
        # that DVLC does not refresh rows when
        # AssociateModel() is called with a populated model.
        model.AfterReset()

    def OnSize(self, event):
        """Adjusts source column width.
        """
        width = self.GetClientSize()[0]-10
        fixed_columns_width = sum(
            col.GetWidth() for col, w_ratio in self._columns if w_ratio==0)
        auto_width_sum = sum(
            w_ratio for col, w_ratio in self._columns if w_ratio)
        auto_width = width-fixed_columns_width
        for col, w_ratio in self._columns:
            if w_ratio:
                if auto_width<0:
                    col.SetWidth(0)
                else:
                    col.SetWidth(int(auto_width*w_ratio/float(auto_width_sum)))


class SourceDataViewModel(DataViewModelPlus):
    """Data model for SourceDataViewListCtrl.
    """

    def GetColumnCount(self):
        return 2

    def GetColumnType(self, col):
        return ['bool', 'string'][col]


class SourceDataViewListCtrl(DataViewListCtrlPlus):
    """DataViewListCtrl for source list.
    """
    def _populate_columns(self):
        use_column = self.AppendToggleColumn('Use', width=30)
        source_column = self.AppendTextColumn('Source')
        self._columns.append((use_column, 0))
        self._columns.append((source_column, 1))
        self.use_column = use_column
        self.source_column = source_column


class DataDataViewModel(DataViewModelPlus):
    """Data model for DataDataViewListCtrl.
    """
    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        # id, type, name
        return ['string', 'string', 'string'][col]


class DataDataViewListCtrl(DataViewListCtrlPlus):
    """DataViewListCtrl for data list.
    """
    def _populate_columns(self):
        id_column = self.AppendTextColumn('Id', width=30)
        type_column = self.AppendTextColumn('Type', width=100)
        name_column = self.AppendTextColumn('Name')
        self._columns.append((id_column, 0))
        self._columns.append((type_column, 0))
        self._columns.append((name_column, 1))
        self.id_column = type_column
        self.type_column = type_column
        self.name_column = name_column


class VisualizerPanel(wx.Panel):
    """Visualizer configuration panel.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        kwargs['style'] = kwargs.get('style', 0)|wx.BORDER_SUNKEN
        wx.Panel.__init__(self, *args, **kwargs)
        visualizer_choice = wx.Choice(self, -1)
        # controls
        reset_button = wx.Button(self, -1, u'Reset/Update')
        configure_button = wx.Button(self, -1, u'Configure')
        # source_list = SourceDataViewListCtrl(self, -1, style=wx.BORDER_SUNKEN)
        # add_button = wx.Button(self, -1, u'Add')
        # remove_button = wx.Button(self, -1, u'Delete')
        data_list = DataDataViewListCtrl(self, -1, style=wx.BORDER_SUNKEN)
        up_button = wx.Button(self, -1, u'Up')
        down_button = wx.Button(self, -1, u'Down')
        """
        interval_spin = wx.SpinCtrlDouble(self, -1, value='0.064', min=0.032, max=2.048, inc=0.016)
        frame_id_text = wx.StaticText(self, -1, u'')
        frame_pos_slider = wx.Slider(self, -1, value=0, minValue=0, maxValue=1)
        start_button = wx.Button(self, -1, '|<')
        end_button = wx.Button(self, -1, '>|')
        play_button = wx.Button(self, -1, u'>')
        """
        # sizers
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer1.Add(reset_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer1.Add(configure_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        # button_sizer2.Add(add_button, 1, wx.EXPAND|wx.ALL, 0)
        # button_sizer2.Add(remove_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer3.Add(up_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer3.Add(down_button, 1, wx.EXPAND|wx.ALL, 0)
        """
        player_sizer = wx.BoxSizer(wx.VERTICAL)
        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        status_sizer.Add(wx.StaticText(self, -1, u'Interval'), 0, wx.ALL, 0)
        status_sizer.Add(interval_spin, 0, wx.ALL, 0)
        button_sizer4.Add(start_button, 0, wx.ALL|wx.EXPAND, 0)
        button_sizer4.Add(play_button, 0, wx.ALL|wx.EXPAND, 0)
        button_sizer4.Add(end_button, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(status_sizer, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(frame_id_text, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(frame_pos_slider, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(button_sizer4, 0, wx.ALL|wx.EXPAND, 0)
        """
        root_sizer.Add(wx.StaticText(self, -1, u'Visualizer'), 0, wx.ALL, 5)
        root_sizer.Add(visualizer_choice, 0, wx.ALL, 5)
        root_sizer.Add(button_sizer1, 0, wx.ALL, 5)
        root_sizer.Add(wx.StaticText(self, -1, u'Sources'), 0, wx.ALL, 5)
        # root_sizer.Add(source_list, 1, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(button_sizer2, 0, wx.ALL, 5)
        root_sizer.Add(wx.StaticText(self, -1, u'Data'), 0, wx.ALL, 5)
        root_sizer.Add(data_list, 1, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(button_sizer3, 0, wx.ALL, 5)
        """
        root_sizer.Add(wx.StaticText(self, -1, u'Animation'), 0, wx.ALL, 5)
        root_sizer.Add(player_sizer, 0, wx.ALL, 5)
        """
        # name bindings
        self.reset_button = reset_button
        self.configure_button = configure_button
        self.visualizer_choice = visualizer_choice
        # self.source_list = source_list
        self.data_list = data_list
        # self.add_button = add_button
        # self.remove_button = remove_button
        self.up_button = up_button
        self.down_button = down_button
        """
        self.interval_spin = interval_spin
        self.frame_id_text = frame_id_text
        self.frame_pos_slider = frame_pos_slider
        self.start_button = start_button
        self.end_button = end_button
        self.play_button = play_button
        """
        # bind sizer
        self.SetSizer(root_sizer)

    def set_visualizer_choices(self, choices):
        """Set visualizer choices.
        """
        self.visualizer_choice.Clear()
        self.visualizer_choice.AppendItems(choices)


if __name__=='__main__':
    VISUALIZERS = ['Particle', 'Lattice', 'Compartment']
    sources = [[True, '/foo/bar/baz.data'],
               [False, '/foo/bar/qux.data']]
    data = [['SomeType', 'some-typed-data'],
            ['AnotherType', 'another-typed-data']]
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visualizer Panel Demo', size=(-1, 600))
            visualizer_panel = VisualizerPanel(frame, -1)
            visualizer_panel.set_visualizer_choices(VISUALIZERS)
            source_model = SourceDataViewModel(sources)
            data_model = DataDataViewModel(data)
            # visualizer_panel.source_list.AssociateModel(source_model)
            visualizer_panel.data_list.AssociateModel(data_model)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
=======================
workspace.py
----------------------
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
    
=======================
workspace_panel.py
----------------------
# coding: utf-8
"""workspace_panel.py --- Workspace panel in visualizer application.
"""
import glob, os, os.path
import wx
from wx.lib import filebrowsebutton

from utils_wx import TreeCtrlPlus

icons_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'resources', 'icons')


class Ec4DirectoryScanner(object):

    def is_directory(self, path):
        """Determines if path 'should be treated as' directory.
        """
        if self.is_data_bundle(path):
            return False
        if os.path.isdir(path):
            return True

    def is_data_bundle(self, path):
        """Determines if path is a data (or data bundle)
        """
        # actual algorithm is TBD
        pass


class WorkspaceTree(TreeCtrlPlus):

    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        TreeCtrlPlus.__init__(self, *args, **kwargs)
        image_size = (16, 16)
        self.image_list = wx.ImageList(*image_size)
        self.folder_image_id = self.image_list.Add(
            wx.Image(os.path.join(icons_path, 'folder_open.png'),
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.file_image_id = self.image_list.Add(
            wx.Image(os.path.join(icons_path, 'document_default.png'),
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.bundle_image_id = self.image_list.Add(
            wx.Image(os.path.join(icons_path, 'draw_layer.png'),
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.SetImageList(self.image_list)
        self._root_path = os.getcwd()
        self.rebuild_root()

    def get_root_path(self):
        """Getter for root_path
        """
        return self._root_path

    def set_root_path(self, root_path):
        """Setter for root_path
        """
        self._root_path = root_path
        self.rebuild_root()

    root_path = property(get_root_path, set_root_path)

    def rebuild_root(self):
        """Rebuild tree from root.
        """
        root_item_id = self.GetRootItem()
        if root_item_id and root_item_id.IsOk():
            if self.GetItemText(root_item_id)!=self._root_path:
                self.DeleteAllItems()
                self.AddRoot(self._root_path)
        else:
            self.AddRoot(self._root_path)
        root_item_id = self.GetRootItem()
        self.SetItemHasChildren(root_item_id, os.path.isdir(self._root_path))
        self.SetItemImage(root_item_id, self.folder_image_id, wx.TreeItemIcon_Normal)
        self.SetItemImage(root_item_id, self.folder_image_id, wx.TreeItemIcon_Expanded)
        if self.ItemHasChildren(root_item_id) and self.IsExpanded(root_item_id):
            self.rebuild_tree(root_item_id)

    def get_node_path(self, item_id):
        """Resolve path of the node (with recursion).
        """
        parent_id = self.GetItemParent(item_id)
        if parent_id:
            parent_node_path = self.get_node_path(parent_id)
            return os.path.join(parent_node_path, self.GetItemText(item_id))
        else:
            return self.GetItemText(item_id)

    def rebuild_tree(self, item_id):
        """Rebuilds a subtree.
        """
        node_path = self.get_node_path(item_id)
        node_names = os.listdir(node_path)
        child_id, cookie = self.GetFirstChild(item_id)
        id_to_delete = []
        # phase 1: update children, marking candidates for deletion
        while child_id:
            child_text = self.GetItemText(child_id)
            if child_text not in node_names:
                # mark nonexistent children to delete
                id_to_delete.append(child_id)
            else:
                node_names.remove(child_text)
                child_path = os.path.join(node_path, child_text)
                if os.path.isdir(child_path):
                    image_id = self.folder_image_id
                    if glob.glob(os.path.join(child_path, '*.h5')):
                        image_id = self.bundle_image_id
                    self.SetItemImage(
                        child_id, self.image_id, wx.TreeItemIcon_Normal)
                    self.SetItemHasChildren(child_id, True)
                    if self.IsExpanded(child_id):
                        self.rebuild_tree(child_id)
                else:
                    self.SetItemImage(child_id, self.file_image_id, wx.TreeItemIcon_Normal)
                    self.SetItemHasChildren(child_id, False)
            child_id, cookie = self.GetNextChild(child_id, cookie)
        # phase 2: delete nonexistent nodes
        for del_id in id_to_delete:
            self.Delete(del_id)
        # phase 3: populate newly introduced nodes
        for node_name in node_names:
            child_path = os.path.join(node_path, node_name)
            child_id = self.AppendItem(item_id, node_name)
            is_dir = os.path.isdir(child_path)
            self.SetItemHasChildren(child_id, is_dir)
            if is_dir:
                image_id = self.folder_image_id
                if glob.glob(os.path.join(child_path, '*.h5')):
                    image_id = self.bundle_image_id
                self.SetItemImage(child_id, image_id, wx.TreeItemIcon_Normal)
                self.SetItemImage(child_id, image_id, wx.TreeItemIcon_Expanded)
            else:
                image_id = self.file_image_id
                self.SetItemImage(child_id, image_id, wx.TreeItemIcon_Normal)
        return

    def OnItemCollapsed(self, evt):
        """Handler called on an item has collapsed.
        """
        item_id = evt.GetItem()
        self.DeleteChildren(item_id)

    def OnItemExpanding(self, evt):
        """Handler called on expanding item.
        """
        item_id = evt.GetItem()
        self.rebuild_tree(item_id)


class WorkspacePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = WorkspaceTree(
            self, -1, style=wx.SUNKEN_BORDER|wx.TR_HAS_BUTTONS)
        self.tree_ctrl = tree_ctrl
        # root_directory browse button
        directory_browse_button = filebrowsebutton.DirBrowseButton(
            self, -1, changeCallback=self.directory_browse_callback,
            labelText='Data Root:', 
            )
        directory_browse_button.SetValue(tree_ctrl.root_path)
        # name bindings
        self.directory_browse_button = directory_browse_button
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(directory_browse_button, 0, wx.ALL|wx.EXPAND, 0)
        root_sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.SetMinSize((200, -1))
        self.SetSize((200, 600))
        self.SetSizer(root_sizer)
        self.Layout()

    def directory_browse_callback(self, evt):
        self.tree_ctrl.root_path = evt.GetString()
        


if __name__=='__main__':
    
    class DummyNode(object):

        def __init__(self, label):
            self.label = label

        def __unicode__(self):
            return self.label

    class DummyModel(object):

        def __init__(self):
            self.file = [DummyNode('FooFile'), DummyNode('BarFile')]
            self.filter = [DummyNode('BazFilter'), DummyNode('QuxFilter')]
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Workspace Panel Demo')
            workspace_panel = WorkspacePanel(frame, -1)
            tree = workspace_panel.tree_ctrl
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(workspace_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
=======================
wxVTKRenderWindowInteractor.py
----------------------
# coding: utf-8

# Taken from yet-another-wx-vtk project, which is BSD licensed:
#   http://sourceforge.net/projects/wxvtk/
# The reason to use this variant is that original
# wxVTKRenderWindowInteractor bundled with VTK5.8 seems to be
# somewhat broken.

"""

A VTK RenderWindowInteractor widget for wxPython.

Find wxPython info at http://wxPython.org

Created by Prabhu Ramachandran, April 2002
Based on wxVTKRenderWindow.py

Fixes and updates by Charl P. Botha 2003-2008

Updated to new wx namespace and some cleaning up by Andrea Gavana,
December 2006
"""

"""
Please see the example at the end of this file.

----------------------------------------
Creation:

 wxVTKRenderWindowInteractor(parent, ID, stereo=0, [wx keywords]):

 You should create a wx.PySimpleApp() or some other wx**App before
 creating the window.

Behaviour:

 Uses __getattr__ to make the wxVTKRenderWindowInteractor behave just
 like a vtkGenericRenderWindowInteractor.

----------------------------------------

"""

# import usual libraries
import math, os, sys
import wx
import vtk

# wxPython 2.4.0.4 and newer prefers the use of True and False, standard
# booleans in Python 2.2 but not earlier.  Here we define these values if
# they don't exist so that we can use True and False in the rest of the
# code.  At the time of this writing, that happens exactly ONCE in
# CreateTimer()
try:
    True
except NameError:
    True = 1
    False = 0

# a few configuration items, see what works best on your system

# Use GLCanvas as base class instead of wx.Window.
# This is sometimes necessary under wxGTK or the image is blank.
# (in wxWindows 2.3.1 and earlier, the GLCanvas had scroll bars)
baseClass = wx.Window
if wx.Platform == "__WXGTK__":
    import wx.glcanvas
    baseClass = wx.glcanvas.GLCanvas

# Keep capturing mouse after mouse is dragged out of window
# (in wxGTK 2.3.2 there is a bug that keeps this from working,
# but it is only relevant in wxGTK if there are multiple windows)
_useCapture = (wx.Platform == "__WXMSW__")

# end of configuration items


class EventTimer(wx.Timer):
    """Simple wx.Timer class.
    """

    def __init__(self, iren):
        """Default class constructor.
        @param iren: current render window
        """
        wx.Timer.__init__(self)
        self.iren = iren


    def Notify(self):
        """ The timer has expired.
        """
        self.iren.TimerEvent()


class wxVTKRenderWindowInteractor(baseClass):
    """
    A wxRenderWindow for wxPython.
    Use GetRenderWindow() to get the vtkRenderWindow.
    Create with the keyword stereo=1 in order to
    generate a stereo-capable window.
    """

    # class variable that can also be used to request instances that use
    # stereo; this is overridden by the stereo=1/0 parameter.  If you set
    # it to True, the NEXT instantiated object will attempt to allocate a
    # stereo visual.  E.g.:
    # wxVTKRenderWindowInteractor.USE_STEREO = True
    # myRWI = wxVTKRenderWindowInteractor(parent, -1)
    USE_STEREO = False

    def __init__(self, parent, ID, *args, **kw):
        """Default class constructor.
        @param parent: parent window
        @param ID: window id
        @param **kw: wxPython keywords (position, size, style) plus the
        'stereo' keyword
        """
        # private attributes
        self.__RenderWhenDisabled = 0

        # First do special handling of some keywords:
        # stereo, position, size, style

        stereo = 0

        if kw.has_key('stereo'):
            if kw['stereo']:
                stereo = 1
            del kw['stereo']

        elif self.USE_STEREO:
            stereo = 1

        position, size = wx.DefaultPosition, wx.DefaultSize

        if kw.has_key('position'):
            position = kw['position']
            del kw['position']

        if kw.has_key('size'):
            size = kw['size']
            del kw['size']

        # wx.WANTS_CHARS says to give us e.g. TAB
        # wx.NO_FULL_REPAINT_ON_RESIZE cuts down resize flicker under GTK
        style = wx.WANTS_CHARS | wx.NO_FULL_REPAINT_ON_RESIZE

        if kw.has_key('style'):
            style = style | kw['style']
            del kw['style']

        # the enclosing frame must be shown under GTK or the windows
        #  don't connect together properly
        if wx.Platform != '__WXMSW__':
            l = []
            p = parent
            while p: # make a list of all parents
                l.append(p)
                p = p.GetParent()
            l.reverse() # sort list into descending order
            for p in l:
                p.Show(1)

        if baseClass.__name__ == 'GLCanvas':
            # code added by cpbotha to enable stereo and double
            # buffering correctly where the user requests this; remember
            # that the glXContext in this case is NOT allocated by VTK,
            # but by WX, hence all of this.

            # Initialize GLCanvas with correct attriblist
            attribList = [wx.glcanvas.WX_GL_RGBA,
                          wx.glcanvas.WX_GL_MIN_RED, 1,
                          wx.glcanvas.WX_GL_MIN_GREEN, 1,
                          wx.glcanvas.WX_GL_MIN_BLUE, 1,
                          wx.glcanvas.WX_GL_DEPTH_SIZE, 16,
                          wx.glcanvas.WX_GL_DOUBLEBUFFER]
            if stereo:
                attribList.append(wx.glcanvas.WX_GL_STEREO)

            try:
                baseClass.__init__(self, parent, ID, position, size, style,
                                   attribList=attribList)
            except wx.PyAssertionError:
                # visual couldn't be allocated, so we go back to default
                baseClass.__init__(self, parent, ID, position, size, style)
                if stereo:
                    # and make sure everyone knows that the stereo
                    # visual wasn't set.
                    stereo = 0

        else:
            baseClass.__init__(self, parent, ID, position, size, style)

        # create the RenderWindow and initialize it
        self._Iren = vtk.vtkGenericRenderWindowInteractor()
        self._Iren.SetRenderWindow( vtk.vtkRenderWindow() )
        self._Iren.AddObserver('CreateTimerEvent', self.CreateTimer)
        self._Iren.AddObserver('DestroyTimerEvent', self.DestroyTimer)
        self._Iren.GetRenderWindow().AddObserver('CursorChangedEvent',
                                                 self.CursorChangedEvent)

        try:
            self._Iren.GetRenderWindow().SetSize(size.width, size.height)
        except AttributeError:
            self._Iren.GetRenderWindow().SetSize(size[0], size[1])

        if stereo:
            self._Iren.GetRenderWindow().StereoCapableWindowOn()
            self._Iren.GetRenderWindow().SetStereoTypeToCrystalEyes()

        self.__handle = None

        self.BindEvents()

        # with this, we can make sure that the reparenting logic in
        # Render() isn't called before the first OnPaint() has
        # successfully been run (and set up the VTK/WX display links)
        self.__has_painted = False

        # set when we have captured the mouse.
        self._own_mouse = False
        # used to store WHICH mouse button led to mouse capture
        self._mouse_capture_button = 0

        # A mapping for cursor changes.
        self._cursor_map = {0: wx.CURSOR_ARROW, # VTK_CURSOR_DEFAULT
                            1: wx.CURSOR_ARROW, # VTK_CURSOR_ARROW
                            2: wx.CURSOR_SIZENESW, # VTK_CURSOR_SIZENE
                            3: wx.CURSOR_SIZENWSE, # VTK_CURSOR_SIZENWSE
                            4: wx.CURSOR_SIZENESW, # VTK_CURSOR_SIZESW
                            5: wx.CURSOR_SIZENWSE, # VTK_CURSOR_SIZESE
                            6: wx.CURSOR_SIZENS, # VTK_CURSOR_SIZENS
                            7: wx.CURSOR_SIZEWE, # VTK_CURSOR_SIZEWE
                            8: wx.CURSOR_SIZING, # VTK_CURSOR_SIZEALL
                            9: wx.CURSOR_HAND, # VTK_CURSOR_HAND
                            10: wx.CURSOR_CROSS, # VTK_CURSOR_CROSSHAIR
                           }

    def BindEvents(self):
        """Binds all the necessary events for navigation, sizing,
        drawing.
        """
        # refresh window by doing a Render
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # turn off background erase to reduce flicker
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda e: None)

        # Bind the events to the event converters
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnButtonDown)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnButtonDown)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnButtonDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnButtonUp)
        self.Bind(wx.EVT_LEFT_UP, self.OnButtonUp)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnButtonUp)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        # If we use EVT_KEY_DOWN instead of EVT_CHAR, capital versions
        # of all characters are always returned.  EVT_CHAR also performs
        # other necessary keyboard-dependent translations.
        self.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

        self.Bind(wx.EVT_SIZE, self.OnSize)

        # the wx 2.8.7.1 documentation states that you HAVE to handle
        # this event if you make use of CaptureMouse, which we do.
        if _useCapture and hasattr(wx, 'EVT_MOUSE_CAPTURE_LOST'):
            self.Bind(wx.EVT_MOUSE_CAPTURE_LOST,
                    self.OnMouseCaptureLost)


    def __getattr__(self, attr):
        """Makes the object behave like a
        vtkGenericRenderWindowInteractor.
        """
        if attr == '__vtk__':
            return lambda t=self._Iren: t
        elif hasattr(self._Iren, attr):
            return getattr(self._Iren, attr)
        else:
            raise AttributeError, self.__class__.__name__ + \
                  " has no attribute named " + attr

    def CreateTimer(self, obj, evt):
        """ Creates a timer.
        """
        self._timer = EventTimer(self)
        self._timer.Start(10, True)

    def DestroyTimer(self, obj, evt):
        """The timer is a one shot timer so will expire automatically.
        """
        return 1

    def _CursorChangedEvent(self, obj, evt):
        """Change the wx cursor if the renderwindow's cursor was
        changed.
        """
        cur = self._cursor_map[obj.GetCurrentCursor()]
        c = wx.StockCursor(cur)
        self.SetCursor(c)

    def CursorChangedEvent(self, obj, evt):
        """Called when the CursorChangedEvent fires on the render
        window."""
        # This indirection is needed since when the event fires, the
        # current cursor is not yet set so we defer this by which time
        # the current cursor should have been set.
        wx.CallAfter(self._CursorChangedEvent, obj, evt)

    def HideCursor(self):
        """Hides the cursor."""
        c = wx.StockCursor(wx.CURSOR_BLANK)
        self.SetCursor(c)

    def ShowCursor(self):
        """Shows the cursor."""
        rw = self._Iren.GetRenderWindow()
        cur = self._cursor_map[rw.GetCurrentCursor()]
        c = wx.StockCursor(cur)
        self.SetCursor(c)

    def GetDisplayId(self):
        """Function to get X11 Display ID from WX and return it in a format
        that can be used by VTK Python.

        We query the X11 Display with a new call that was added in wxPython
        2.6.0.1.  The call returns a SWIG object which we can query for the
        address and subsequently turn into an old-style SWIG-mangled string
        representation to pass to VTK.
        """
        d = None

        try:
            d = wx.GetXDisplay()

        except NameError:
            # wx.GetXDisplay was added by Robin Dunn in wxPython 2.6.0.1
            # if it's not available, we can't pass it.  In general,
            # things will still work; on some setups, it'll break.
            pass

        else:
            # wx returns None on platforms where wx.GetXDisplay is not relevant
            if d:
                d = hex(d)
                # On wxPython-2.6.3.2 and above there is no leading '0x'.
                if not d.startswith('0x'):
                    d = '0x' + d

                # we now have 0xdeadbeef
                # VTK wants it as: _deadbeef_void_p (pre-SWIG-1.3 style)
                d = '_%s_%s\0' % (d[2:], 'void_p')

        return d

    def OnMouseCaptureLost(self, event):
        """This is signalled when we lose mouse capture due to an
        external event, such as when a dialog box is shown.  See the
        wx documentation.
        """

        # the documentation seems to imply that by this time we've
        # already lost capture.  I have to assume that we don't need
        # to call ReleaseMouse ourselves.
        if _useCapture and self._own_mouse:
            self._own_mouse = False

    def OnPaint(self,event):
        """Handles the wx.EVT_PAINT event for
        wxVTKRenderWindowInteractor.
        """

        # wx should continue event processing after this handler.
        # We call this BEFORE Render(), so that if Render() raises
        # an exception, wx doesn't re-call OnPaint repeatedly.
        event.Skip()

        dc = wx.PaintDC(self)

        # make sure the RenderWindow is sized correctly
        self._Iren.GetRenderWindow().SetSize(*self.GetSizeTuple())

        # Tell the RenderWindow to render inside the wx.Window.
        if not self.__handle:

            # on relevant platforms, set the X11 Display ID
            d = self.GetDisplayId()
            if d and self.__has_painted:
                self._Iren.GetRenderWindow().SetDisplayId(d)

            # store the handle
            self.__handle = self.GetHandle()
            # and give it to VTK
            self._Iren.GetRenderWindow().SetWindowInfo(str(self.__handle))

            # now that we've painted once, the Render() reparenting logic
            # is safe
            self.__has_painted = True

        self.Render()

    def OnSize(self,event):
        """Handles the wx.EVT_SIZE event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue (we call this before the
        # Render(), in case it raises an exception)
        event.Skip()

        try:
            width, height = event.GetSize()
        except:
            width = event.GetSize().width
            height = event.GetSize().height
        self._Iren.SetSize(width, height)
        self._Iren.ConfigureEvent()

        # this will check for __handle
        self.Render()

    def OnMotion(self,event):
        """Handles the wx.EVT_MOTION event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        # we call this early in case any of the VTK code raises an
        # exception.
        event.Skip()

        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            event.ControlDown(),
                                            event.ShiftDown(),
                                            chr(0), 0, None)
        self._Iren.MouseMoveEvent()

    def OnEnter(self,event):
        """Handles the wx.EVT_ENTER_WINDOW event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        event.Skip()

        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            event.ControlDown(),
              event.ShiftDown(),
              chr(0), 0, None)
        self._Iren.EnterEvent()


    def OnLeave(self,event):
        """Handles the wx.EVT_LEAVE_WINDOW event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        event.Skip()

        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            event.ControlDown(),
              event.ShiftDown(),
              chr(0), 0, None)
        self._Iren.LeaveEvent()


    def OnButtonDown(self,event):
        """Handles the wx.EVT_LEFT/RIGHT/MIDDLE_DOWN events for
        wxVTKRenderWindowInteractor.
        """

        # allow wx event processing to continue
        # on wxPython 2.6.0.1, omitting this will cause problems with
        # the initial focus, resulting in the wxVTKRWI ignoring keypresses
        # until we focus elsewhere and then refocus the wxVTKRWI frame
        # we do it this early in case any of the following VTK code
        # raises an exception.
        event.Skip()

        ctrl, shift = event.ControlDown(), event.ShiftDown()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            ctrl, shift, chr(0), 0, None)

        button = 0
        if event.RightDown():
            self._Iren.RightButtonPressEvent()
            button = 'Right'
        elif event.LeftDown():
            self._Iren.LeftButtonPressEvent()
            button = 'Left'
        elif event.MiddleDown():
            self._Iren.MiddleButtonPressEvent()
            button = 'Middle'

        # save the button and capture mouse until the button is released
        # we only capture the mouse if it hasn't already been captured
        if _useCapture and not self._own_mouse:
            self._own_mouse = True
            self._mouse_capture_button = button
            self.CaptureMouse()


    def OnButtonUp(self,event):
        """Handles the wx.EVT_LEFT/RIGHT/MIDDLE_UP events for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        event.Skip()

        button = 0
        if event.RightUp():
            button = 'Right'
        elif event.LeftUp():
            button = 'Left'
        elif event.MiddleUp():
            button = 'Middle'

        # if the same button is released that captured the mouse, and
        # we have the mouse, release it.
        # (we need to get rid of this as soon as possible; if we don't
        #  and one of the event handlers raises an exception, mouse
        #  is never released.)
        if _useCapture and self._own_mouse and \
                button==self._mouse_capture_button:
            self.ReleaseMouse()
            self._own_mouse = False

        ctrl, shift = event.ControlDown(), event.ShiftDown()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            ctrl, shift, chr(0), 0, None)

        if button == 'Right':
            self._Iren.RightButtonReleaseEvent()
        elif button == 'Left':
            self._Iren.LeftButtonReleaseEvent()
        elif button == 'Middle':
            self._Iren.MiddleButtonReleaseEvent()


    def OnMouseWheel(self,event):
        """Handles the wx.EVT_MOUSEWHEEL event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        event.Skip()

        ctrl, shift = event.ControlDown(), event.ShiftDown()
        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            ctrl, shift, chr(0), 0, None)
        if event.GetWheelRotation() > 0:
            self._Iren.MouseWheelForwardEvent()
        else:
            self._Iren.MouseWheelBackwardEvent()


    def OnKeyDown(self,event):
        """Handles the wx.EVT_KEY_DOWN event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        event.Skip()

        ctrl, shift = event.ControlDown(), event.ShiftDown()
        keycode, keysym = event.GetKeyCode(), None
        key = chr(0)
        if keycode < 256:
            key = chr(keycode)

        # wxPython 2.6.0.1 does not return a valid event.Get{X,Y}()
        # for this event, so we use the cached position.
        (x,y)= self._Iren.GetEventPosition()
        self._Iren.SetEventInformation(x, y,
                                       ctrl, shift, key, 0,
                                       keysym)

        self._Iren.KeyPressEvent()
        self._Iren.CharEvent()


    def OnKeyUp(self,event):
        """Handles the wx.EVT_KEY_UP event for
        wxVTKRenderWindowInteractor.
        """

        # event processing should continue
        event.Skip()

        ctrl, shift = event.ControlDown(), event.ShiftDown()
        keycode, keysym = event.GetKeyCode(), None
        key = chr(0)
        if keycode < 256:
            key = chr(keycode)

        self._Iren.SetEventInformationFlipY(event.GetX(), event.GetY(),
                                            ctrl, shift, key, 0,
                                            keysym)
        self._Iren.KeyReleaseEvent()


    def GetRenderWindow(self):
        """Returns the render window (vtkRenderWindow).
        """
        return self._Iren.GetRenderWindow()

    def Render(self):
        """Actually renders the VTK scene on screen.
        """
        RenderAllowed = 1

        if not self.__RenderWhenDisabled:
            # the user doesn't want us to render when the toplevel frame
            # is disabled - first find the top level parent
            topParent = wx.GetTopLevelParent(self)
            if topParent:
                # if it exists, check whether it's enabled
                # if it's not enabeld, RenderAllowed will be false
                RenderAllowed = topParent.IsEnabled()

        if RenderAllowed:
            if self.__handle and self.__handle == self.GetHandle():
                self._Iren.GetRenderWindow().Render()

            elif self.GetHandle() and self.__has_painted:
                # this means the user has reparented us; let's adapt to the
                # new situation by doing the WindowRemap dance
                self._Iren.GetRenderWindow().SetNextWindowInfo(
                    str(self.GetHandle()))

                # make sure the DisplayId is also set correctly
                d = self.GetDisplayId()
                if d:
                    self._Iren.GetRenderWindow().SetDisplayId(d)

                # do the actual remap with the new parent information
                self._Iren.GetRenderWindow().WindowRemap()

                # store the new situation
                self.__handle = self.GetHandle()
                self._Iren.GetRenderWindow().Render()

    def SetRenderWhenDisabled(self, newValue):
        """Change value of __RenderWhenDisabled ivar.

        If __RenderWhenDisabled is false (the default), this widget will not
        call Render() on the RenderWindow if the top level frame (i.e. the
        containing frame) has been disabled.

        This prevents recursive rendering during wx.SafeYield() calls.
        wx.SafeYield() can be called during the ProgressMethod() callback of
        a VTK object to have progress bars and other GUI elements updated -
        it does this by disabling all windows (disallowing user-input to
        prevent re-entrancy of code) and then handling all outstanding
        GUI events.

        However, this often triggers an OnPaint() method for wxVTKRWIs,
        resulting in a Render(), resulting in Update() being called whilst
        still in progress.
        """
        self.__RenderWhenDisabled = bool(newValue)


#--------------------------------------------------------------------
def wxVTKRenderWindowInteractorConeExample():
    """Like it says, just a simple example
    """
    # every wx app needs an app
    app = wx.PySimpleApp()

    # create the top-level frame, sizer and wxVTKRWI
    frame = wx.Frame(None, -1, "wxVTKRenderWindowInteractor", size=(400,400))
    widget = wxVTKRenderWindowInteractor(frame, -1)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(widget, 1, wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Layout()

    # It would be more correct (API-wise) to call widget.Initialize() and
    # widget.Start() here, but Initialize() calls RenderWindow.Render().
    # That Render() call will get through before we can setup the
    # RenderWindow() to render via the wxWidgets-created context; this
    # causes flashing on some platforms and downright breaks things on
    # other platforms.  Instead, we call widget.Enable().  This means
    # that the RWI::Initialized ivar is not set, but in THIS SPECIFIC CASE,
    # that doesn't matter.
    widget.Enable(1)

    widget.AddObserver("ExitEvent", lambda o,e,f=frame: f.Close())

    ren = vtk.vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)

    cone = vtk.vtkConeSource()
    cone.SetResolution(8)

    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInput(cone.GetOutput())

    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)

    ren.AddActor(coneActor)

    # show the window
    frame.Show()

    app.MainLoop()

if __name__ == "__main__":
    wxVTKRenderWindowInteractorConeExample()

=======================
