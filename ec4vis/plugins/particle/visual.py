# coding: utf-8

import numpy, vtk
from ec4vis import rgb_colors
from ec4vis.visual import ActorsVisual, StaticActorsVisual, MappedActorsVisual, VolumesVisual


class LegacyStaticVisual(StaticActorsVisual):
    """Static visual with legacy settings.
    """
    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop('settings')
        StaticActorsVisual.__init__(self, *args, **kwargs)


class LegacyLegend(LegacyStaticVisual):
    """Legacy legend visual.
    """
    def _get_legend_position(self, location, height, width, offset):
        if location == 0:
            return (offset, offset)
        elif location == 1:
            return (1.0 - width - offset, offset)
        elif location == 2:
            return (offset, 1.0 - height - offset)
        elif location == 3:
            return (1.0 - width - offset, 1.0 - height - offset)
        else:
            raise VisualizerError('Illegal legend position: %d' % location)


class SpeciesLegend(LegacyLegend):
    """Visual for species legend.
    """
    def __init__(self, *args, **kwargs):
        LegacyLegend.__init__(self, *args, **kwargs)
        self.particle_attrs = getattr(self.settings, 'particle_attrs', {})

    @property
    def _pattrs(self):
        return self.particle_attrs

    @property
    def _mapped_species_idset(self):
        return self._pattrs.keys()
    
    def _create_actors(self):
        legend_box = vtk.vtkLegendBoxActor()
        # Get number of lines
        legend_line_numbers = len(self._mapped_species_idset)
        # Create legend actor
        legend_box.SetNumberOfEntries(legend_line_numbers)
        legend_box.SetPosition(
            self._get_legend_position(
                self.settings.species_legend_location,
                self.settings.species_legend_height,
                self.settings.species_legend_width,
                self.settings.species_legend_offset))
        legend_box.SetWidth(self.settings.species_legend_width)
        legend_box.SetHeight(self.settings.species_legend_height)
        tprop = vtk.vtkTextProperty()
        tprop.SetColor(rgb_colors.RGB_WHITE)
        tprop.SetVerticalJustificationToCentered()
        legend_box.SetEntryTextProperty(tprop)
        if self.settings.species_legend_border_display:
            legend_box.BorderOn()
        else:
            legend_box.BorderOff()
        # Entry legend string to the actor
        sphere = vtk.vtkSphereSource()

        # Create legends of particle speices
        count = 0
        for species_id in self._mapped_species_idset:
            legend_box.SetEntryColor \
                (count, self._pattrs[species_id]['color'])
            legend_box.SetEntryString \
                (count, str(species_id))
            legend_box.SetEntrySymbol(count, sphere.GetOutput())
            count += 1
        self._actors['Legend Box'] = legend_box


class TimeLegend(LegacyLegend):

    def _create_actors(self):
        """Creates time legend actors.
        """
        legend_box = vtk.vtkLegendBoxActor()

        # Create legend actor
        legend_box.SetNumberOfEntries(1)
        legend_box.SetPosition(
            *self._get_legend_position(
                self.settings.time_legend_location,
                self.settings.time_legend_height,
                self.settings.time_legend_width,
                self.settings.time_legend_offset))

        legend_box.SetWidth(self.settings.time_legend_width)
        legend_box.SetHeight(self.settings.time_legend_height)

        tprop = vtk.vtkTextProperty()
        tprop.SetColor(rgb_colors.RGB_WHITE)
        tprop.SetVerticalJustificationToCentered()
        legend_box.SetEntryTextProperty(tprop)

        if self.settings.time_legend_border_display:
            legend_box.BorderOn()
        else:
            legend_box.BorderOff()
        legend_box.SetEntryString(0, '0.00')
        self._actors['Legend Box'] = legend_box


class WireFrameCube(LegacyStaticVisual):

    def _create_actors(self):
        """Creates time legend actors.
        """
        cube = vtk.vtkCubeSource()
        scaling = self.settings.scaling
        cube.SetBounds(numpy.array([0.0, 1.0, 0.0, 1.0, 0.0, 1.0])*scaling)
        cube.SetCenter(numpy.array([0.5, 0.5, 0.5])*scaling)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetRepresentationToWireframe()
        self._actors['Wireframe Cube'] = actor
        

class Axes(LegacyStaticVisual):

    def __init__(self, *args, **kwargs):
        self.world_size = kwargs.get('world_size', 1.0)
        LegacyStaticVisual.__init__(self, *args, **kwargs)

    def _create_actors(self):
        """Creates axes actors.
        """
        axes = vtk.vtkCubeAxesActor2D()
        axes.SetBounds(
            numpy.array([0.0, 1.0, 0.0, 1.0, 0.0, 1.0])*self.settings.scaling)
        axes.SetRanges(0.0, self.world_size,
                       0.0, self.world_size,
                       0.0, self.world_size)
        axes.SetLabelFormat('%g')
        axes.SetFontFactor(1.5)
        tprop = vtk.vtkTextProperty()
        tprop.SetColor(self.settings.axis_annotation_color)
        tprop.ShadowOn()
        axes.SetAxisTitleTextProperty(tprop)
        axes.SetAxisLabelTextProperty(tprop)
        axes.UseRangesOn()
        axes.SetCornerOffset(0.0)
        axes.SetCamera(self._renderer.GetActiveCamera())
        self._actors['Axes'] = axes

    def update(self, data, *args, **kwargs):
        axes = self._actors.get('Axes', None)
        if axes:
            axes.SetRanges(0.0, self.world_size,
                           0.0, self.world_size,
                           0.0, self.world_size)


class Planes(LegacyStaticVisual):

    def _create_actors(self):
        """Creates plane actors.
        """
        scaling = self.settings.scaling
        for i, x in enumerate(self.settings.plane_surface_list):
            actor = vtk.vtkActor()
            plane = vtk.vtkPlaneSource()
            plane.SetOrigin(x['origin']*scaling)
            plane.SetPoint1(x['axis1']*scaling)
            plane.SetPoint2(x['axis2']*scaling)

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(plane.GetOutput())

            actor.SetMapper(mapper)
            prop = actor.GetProperty()
            prop.SetColor(x['color'])
            prop.SetOpacity(x['opacity'])
            plane_list.append(actor)
            self._actors['Plane #%d' %i] = actor


class BlurryParticlesVolume(VolumesVisual):

    def _get_volumes(self):
        if not hasattr(self, '_volumes'):
            self._volumes = {}
            self._create_volumes()
        return self._volumes.values()

    def _initialize(self):
        self._pipeline_objs = {}
        self.world_size = 1.0

    def _create_volumes(self):
        settings = self._settings
        world_size = self.world_size
        scaling = settings.scaling
        particle_attrs = settings.particle_attrs

        nx = ny = nz = settings.fluorimetry_axial_voxel_number

        for sid, pattr in particle_attrs.items():
            points = vtk.vtkPoints()
            poly_data = vtk.vtkPolyData()
            poly_data.SetPoints(points)
            poly_data.ComputeBounds()
            # Calc standard deviation of gauss distribution function
            wave_length = pattr['fluorimetry_wave_length']
            sigma = scaling * 0.5 * wave_length / world_size
            # Create guassian splatter
            gs = vtk.vtkGaussianSplatter()
            gs.SetInput(poly_data)
            gs.SetSampleDimensions(nx, ny, nz)
            gs.SetRadius(sigma)
            gs.SetExponentFactor(-.5)
            gs.ScalarWarpingOff()
            # gs.SetModelBounds([-sigma, scaling + sigma] * 3)
            gs.SetAccumulationModeToMax()
            # Create filter for volume rendering
            filter_ = vtk.vtkImageShiftScale()
            # Scales to unsigned char
            filter_.SetScale(255. * pattr['fluorimetry_brightness'])
            filter_.ClampOverflowOn()
            filter_.SetOutputScalarTypeToUnsignedChar()
            filter_.SetInputConnection(gs.GetOutputPort())
            mapper = vtk.vtkFixedPointVolumeRayCastMapper()
            mapper.SetInputConnection(filter_.GetOutputPort())
            volume = vtk.vtkVolume()
            property = volume.GetProperty() # vtk.vtkVolumeProperty()
            color = pattr['fluorimetry_luminescence_color']
            color_tfunc = vtk.vtkColorTransferFunction()
            color_tfunc.AddRGBPoint(0, color[0], color[1], color[2])
            property.SetColor(color_tfunc)
            opacity_tfunc = vtk.vtkPiecewiseFunction()
            opacity_tfunc.AddPoint(0, 0.0)
            opacity_tfunc.AddPoint(255., 1.0)
            property.SetScalarOpacity(opacity_tfunc)
            property.SetInterpolationTypeToLinear()
            if settings.fluorimetry_shadow_display:
                property.ShadeOn()
            else:
                property.ShadeOff()
            volume.SetMapper(mapper)
            volume.VisibilityOff()
            # XXX dirty hack: memorize pipeline objects
            self._pipeline_objs[sid] = dict(
                poly_data=poly_data, gaussian_splatter=gs)
            self._volumes[sid] = volume

    def update(self, data, *args, **kwargs):
        """Updates volume data
        """
        settings = self._settings
        scaling = settings.scaling
        world_size = self.world_size
        for sid, points in data.items():
            # pipeline objects
            pipeline_objs = self._pipeline_objs[sid]
            poly_data = pipeline_objs['poly_data']
            gs = pipeline_objs['gaussian_splatter']
            # update points
            """
            # hacked for performance
            old_points = poly_data.GetPoints()
            new_points = vtk.vtkPoints()
            for pos in coords:
                ret = new_points.InsertNextPoint(pos * scaling / world_size)
            poly_data.SetPoints(new_points)
            #del old_points
            """
            poly_data.SetPoints(points)
            # update pipeline
            poly_data.ComputeBounds()
            volume = self._volumes[sid]
            pattr = settings.particle_attrs[sid]
            wave_length = pattr['fluorimetry_wave_length']
            sigma = scaling * 0.5 * wave_length / world_size
            gs.SetRadius(sigma)
            # gs.SetModelBounds([-sigma, scaling + sigma] * 3)
            gs.Update()
            volume.Update()
            volume.VisibilityOn()
