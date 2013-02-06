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

from ec4vis.logger import debug, log_call
from ec4vis.visualizer.page import register_visualizer_page
from ec4vis.visualizer.vtk3d import Vtk3dVisualizerNode, register_pipeline_node
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage


class DemoConeVisualizerNode(Vtk3dVisualizerNode):
    pass

register_pipeline_node(DemoConeVisualizerNode)


class DemoConeVisualizerPage(Vtk3dVisualizerPage):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        Vtk3dVisualizerPage.__init__(self, *args, **kwargs)
        self.actor = None

    def render(self):
        if self.actor is None:
            source = vtk.vtkConeSource()
            source.SetResolution(64)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            self.actor = vtk.vtkActor()
            self.actor.SetMapper(mapper)
            self.renderer.AddActor(self.actor)
            self.renderer.Render()
        Vtk3dVisualizerPage.render(self)
        

register_visualizer_page('DemoConeVisualizerNode', DemoConeVisualizerPage)


if __name__=='__main__':
    # TBD
    pass
