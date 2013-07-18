# coding: utf-8
"""ec4vis.plugins.timecourse_visualizer --- 2D plot of time course values.
"""
import matplotlib
import wx

try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])
from ec4vis.logger import debug, warning, error
from ec4vis.pipeline import PipelineNode, PipelineSpec, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec
from ec4vis.visualizer.page import VisualizerPage, register_visualizer_page

# Initialize matplotlib/wx backends
matplotlib.use('WXAgg')
try:
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
    from matplotlib.backends.backend_wx import NavigationToolbar2Wx
    from matplotlib.figure import Figure
except ImportError, e:
    error('Unable to initialize matplotlib: %s' %(str(e)))

class TimecourseVisualizerNode(PipelineNode):
    """Node representing a simple matplotlib-based timecourse plotter.
    """
    INPUT_SPEC = [Hdf5DataSpec, NumberOfItemsSpec]
    OUTPUT_SPEC = []
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        PipelineNode.__init__(self, *args, **kwargs)
        self._plot_species = {}

    @property
    def time_course(self):
        """Returns dictionary of species_name->number-of-particles.
        """
        n_items = self.parent.request_data(NumberOfItemsSpec)
        populations = {}
        for i in range(n_items):
            chunk = self.parent.request_data(Hdf5DataSpec, index=i)
            if chunk==None:
                warning('No data available for index=%d.' %(i))
            data_section = chunk.get('/data')
            if data_section==None or len(data_section.values())<1:
                warning('Invalid Data section for index=%d.' %(i))
                continue
            data = data_section.values()[0]
            ts = data.attrs.get('t')
            particles = data.get('particles')
            if ts==None or particles==None:
                warning('Invalid timestamp/particles')
            species_section = chunk.get('/species')
            if species_section==None:
                warning('No species table for index=%d' %(i))
                continue
            # iterate for species...
            for id, name, radius, dvalue in species_section:
                # count number of particles
                n_particles = sum(particles['species_id']==id)
                bin_ = populations.setdefault(name, [])
                bin_.append((ts, n_particles))
        print populations
        return populations

register_pipeline_node(TimecourseVisualizerNode)


class TimecourseVisualizer(VisualizerPage):
    """Simple timecourse visualizer.
    """
    def __init__(self, *args, **kwargs):
        """
        """
        VisualizerPage.__init__(self, *args, **kwargs)
        figure = Figure()
        figure.add_subplot('111')
        canvas = FigureCanvasWxAgg(self, -1, figure)
        self.sizer.Add(canvas, 1, wx.ALL|wx.EXPAND, 5)
        self.figure = figure
        self.canvas = canvas

    def update(self):
        """Observer's update handler
        """
        self.figure.clear()
        axes = self.figure.add_subplot('111')
        populations = self.target.time_course
        xys = []
        names = []
        for name, xy in populations.items():
            xys.extend(zip(*xy)+['o-'])
            names.append(name)
        axes.plot(*xys)
        axes.legend(names)
        self.canvas.draw()

register_visualizer_page('TimecourseVisualizerNode', TimecourseVisualizer)


if __name__=='__main__':
    # TBD
    app = wx.App()
    frame = wx.Frame(None, -1, '')
    node = TimecourseVisualizerNode()
    page = TimecourseVisualizer(frame, -1, target=node)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(page)
    frame.SetSizer(sizer)
    frame.Show(True)
    app.MainLoop()
