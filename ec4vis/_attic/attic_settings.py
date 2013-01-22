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



