# coding: utf-8
"""settings.py --- settings for particle visualizer.
"""
import copy

import default_settings
import particle_default_settings


class Settings(object):

    "Visualization setting class for Visualizer"

    def __init__(self, user_settings_dict = None):

        settings_dict = default_settings.__dict__.copy()

        if user_settings_dict is not None:
            if type(user_settings_dict) != type({}):
                print 'Illegal argument type for constructor of Settings class'
                sys.exit()
            settings_dict.update(user_settings_dict)

        for key, val in settings_dict.items():
            if key[0] != '_': # Data skip for private variables in setting_dict.
                if type(val) == type({}) or type(val) == type([]):
                    copy_val = copy.deepcopy(val)
                else:
                    copy_val = val
                setattr(self, key, copy_val)

    def _set_data(self, key, val):
        if val != None:
            setattr(self, key, val)

    def set_image(self,
                  height = None,
                  width = None,
                  background_color = None,
                  file_name_format = None
                  ):

        self._set_data('image_height', height)
        self._set_data('image_width', width)
        self._set_data('image_background_color', background_color)
        self._set_data('image_file_name_format', file_name_format)

    def set_movie(self,
                  frame_start_time = None,
                  frame_end_time = None,
                  frame_interval = None,
                  exposure_time = None
                  ):
        self.exposure_time = None
        self._set_data('frame_start_time', frame_start_time)
        self._set_data('frame_end_time', frame_end_time)
        self._set_data('frame_interval', frame_interval)
        self._set_data('exposure_time', exposure_time)
        if self.exposure_time is None:
            self.exposure_time = self.frame_interval

    def set_ffmpeg(self,
                   bin_path = None,
                   additional_options = None,
                   movie_fps = None
                   ):
        self._set_data('ffmpeg_bin_path', bin_path)
        self._set_data('ffmpeg_additional_options', additional_options)
        self._set_data('ffmpeg_movie_fps', movie_fps)

    def set_camera(self,
                   focal_point = None,
                   base_position = None,
                   azimuth = None,
                   elevation = None,
                   view_angle = None,
                   zoom = None,
                   parallel_projection = None
                   ):
        self._set_data('camera_focal_point', focal_point)
        self._set_data('camera_base_position', base_position)
        self._set_data('camera_azimuth', azimuth)
        self._set_data('camera_elevation', elevation)
        self._set_data('camera_view_angle', view_angle)
        self._set_data('camera_zoom', zoom)
        self._set_data('camera_parallel_projection', parallel_projection)

    def set_light(self,
                  intensity = None
                  ):
        self._set_data('light_intensity', intensity)

    def set_species_legend(self,
                           display = None,
                           border_display = None,
                           location = None,
                           height = None,
                           width = None,
                           offset = None
                           ):
        self._set_data('species_legend_display', display)
        self._set_data('species_legend_border_display', border_display)
        self._set_data('species_legend_location', location)
        self._set_data('species_legend_height', height)
        self._set_data('species_legend_width', width)
        self._set_data('species_legend_offset', offset)

    def set_time_legend(self,
                        display = None,
                        border_display = None,
                        format = None,
                        location = None,
                        height = None,
                        width = None,
                        offset = None
                        ):
        self._set_data('time_legend_display', display)
        self._set_data('time_legend_border_display', border_display)
        self._set_data('time_legend_format', format)
        self._set_data('time_legend_location', location)
        self._set_data('time_legend_height', height)
        self._set_data('time_legend_width', width)
        self._set_data('time_legend_offset', offset)

    def set_wireframed_cube(self,
                            display = None
                            ):
        self._set_data('wireframed_cube_diplay', display)

    def set_axis_annotation(self,
                            display = None,
                            color = None
                            ):
        self._set_data('axis_annotation_display', display)
        self._set_data('axis_annotation_color', color)

    def set_fluorimetry2d(self,
                          view_direction=None,
                          depth=None,
                          point=None,
                          normal_direction=None,
                          cutoff=None,
                          psf_range=None,
                          file_name_format=None
                          ):
        self._set_data('fluori2d_view_direction', view_direction)
        self._set_data('fluori2d_depth', depth)
        self._set_data('fluori2d_point', point)
        self._set_data('fluori2d_normal_direction', normal_direction)
        self._set_data('fluori2d_cutoff', cutoff)
        self._set_data('fluori2d_psf_range', psf_range)
        self._set_data('fluori2d_file_name_format', file_name_format)


    def add_plane_surface(self,
                         color = None,
                         opacity = None,
                         origin = None,
                         axis1 = None,
                         axis2 = None
                         ):

        color_ = self.plane_surface_color
        opacity_ = self.plane_surface_opacity
        origin_ = self.plane_surface_origin
        axis1_ = self.plane_surface_axis_1
        axis2_ = self.plane_surface_axis_2

        if color != None: color_ = color
        if opacity != None: opacity_ = opacity
        if origin != None: origin_ = origin
        if axis1 != None: axis1_ = axis1
        if axis2 != None: axis2_ = axis2

        self.plane_surface_list.append({'color':color_,
                                        'opacity':opacity_,
                                        'origin':origin_,
                                        'axis1':axis1_,
                                        'axis2':axis2_})

    def dump(self):
        dump_list = []
        for key in self.__dict__:
            dump_list.append((key, getattr(self, key, None)))

        dump_list.sort(lambda a, b:cmp(a[0], b[0]))

        print '>>>>>>> Settings >>>>>>>'
        for x in dump_list:
            print x[0], ':', x[1]
        print '<<<<<<<<<<<<<<<<<<<<<<<<'


class ParticleSettings(Settings):
    """
    Visualization setting class for ParticleVisualizer

    Taken from pd_visualizer/particle_visualizer.py.
    """
    
    def __init__(self, user_settings_dict = None):
        # default setting
        settings_dict = default_settings.__dict__.copy()
        settings_dict_lattice = particle_default_settings.__dict__.copy()
        settings_dict.update(settings_dict_lattice)
        
        # user setting
        if user_settings_dict is not None:
            if type(user_settings_dict) != type({}):
                print 'Illegal argument type for constructor of Settings class'
                sys.exit()
            settings_dict.update(user_settings_dict)

        for key, val in settings_dict.items():
            if key[0] != '_': # Data skip for private variables in setting_dict.
                if type(val) == type({}) or type(val) == type([]):
                    copy_val = copy.deepcopy(val)
                else:
                    copy_val = val
                setattr(self, key, copy_val)

    def set_fluorimetry(self,
                         display = None,
                         axial_voxel_number = None,
                         background_color = None,
                         shadow_display = None,
                         accumulation_mode = None,
                         ):
        self._set_data('fluorimetry_display', display)
        self._set_data('fluorimetry_axial_voxel_number', axial_voxel_number)
        self._set_data('fluorimetry_background_color', background_color)
        self._set_data('fluorimetry_shadow_display', shadow_display)
        self._set_data('fluorimetry_accumulation_mode', accumulation_mode)
        
    def pfilter_func_direct(self, particle, display_species_id, pattr):
        return pattr
    
    def pfilter_func(self, particle, display_species_id, pattr):
        return pattr

    def pfilter_sid_map_func(self, species_id):
        return species_id

    def pfilter_sid_to_pattr_func(self, display_species_id):
        return self.particle_attrs.get(display_species_id,
                                       self.default_particle_attr)


if __name__=='__main__':
    pass
