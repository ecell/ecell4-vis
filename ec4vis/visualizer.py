# coding: utf-8
"""browser.py -- Browser window in visualizer application, by Yasushi Masuda (ymasuda@accense.com)
"""

import wx, vtk
from wx.lib.scrolledpanel import ScrolledPanel

from ec4vis.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor # as VRWI


class VisualizerFrame(wx.Frame):
    """Visualizer window.
    """

    def __init__(self, responder, world, visualizer, *args, **kwargs):
        """Initializer.
        """
        super(VisualizerFrame, self).__init__(*args, **kwargs)
        self.responder = responder
        self.world = world
        self.visualizer = visualizer
        self.SetSize((600, 600))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        render_window = wxVTKRenderWindowInteractor(self, -1)
        sizer.Add(render_window, 1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Layout()

        render_window.Enable(1)
        ren = vtk.vtkRenderer()
        render_window.GetRenderWindow().AddRenderer(ren)

        cone = vtk.vtkConeSource()
        cone.SetResolution(8)
        
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInput(cone.GetInput())

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)

        ren.AddActor(coneActor)
        self.render_window = render_window
        
        
