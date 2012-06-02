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

