# coding: utf-8
"""ec4vis.plugins.demo_cone_visualizer --- Demonstrative vtkCone visualizer.
"""
import vtk
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

# from ec4vis.logger import debug, log_call
from ec4vis.visualizer.page import register_visualizer_page
from ec4vis.visualizer.vtk3d import Vtk3dVisualizerNode, register_pipeline_node
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage


# Define node which is used as visualizer page target.
class DemoConeVisualizerNode(Vtk3dVisualizerNode):

    def __init__(self, *args, **kwargs):
        super(DemoConeVisualizerNode, self).__init__(*args, **kwargs)
        self.renderer
        source = vtk.vtkConeSource()
        source.SetResolution(64)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(source.GetOutput())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.renderer.AddActor(self.actor)
        self.renderer


# Register pipleline node
register_pipeline_node(DemoConeVisualizerNode)

# Define visualizer
class DemoConeVisualizerPage(Vtk3dVisualizerPage):
    """Abstract superclass for pages in a visualizer notebook.
    """
    pass
        
# Register visualizer page to registry.
register_visualizer_page('DemoConeVisualizerNode', DemoConeVisualizerPage)


# You may write demonstrative app code here...
if __name__=='__main__':
    pass
