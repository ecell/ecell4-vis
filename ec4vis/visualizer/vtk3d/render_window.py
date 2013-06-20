# coding: utf-8
"""render_window.py -- Wrapping panel for wxVTKRenderWindowInteractor.
"""

import numpy
import vtk
import wx

from wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from ec4vis.logger import debug, log_call, warning


class RenderWindowMixin(object):
    
    """A panel containing wxVTKRenderWindowInteractor.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        self._aspect_ratio = kwargs.get('aspect_ratio', (4, 3))
        self.render_window = wxVTKRenderWindowInteractor(self, -1)
        # disable widget (to avoid rendering)
        self.render_window.Enable(False)
        # Hook exit event.
        self.render_window.AddObserver('ExitEvent', self.ObserverExitEventHandler)
        self.renderers = []
        # events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # set up the window

    def ObserverExitEventHandler(self, observer, event, fromobj):
        fromobj.Close()
        
    def finalize(self):
        """Finalizer.
        """
        # stop interaction
        self.render_window.Enable(False)
        # purge all renderer from the window.
        for renderer in self.renderers:
            self.render_window.GetRenderWindow().RemoveRenderer(renderer)
        
    def _get_aspect_ratio(self):
        """Property getter for aspect_ratio.
        """
        return self._aspect_ratio

    def _set_aspect_ratio(self, aspect_ratio):
        """Property setter for aspect_ratio.
        """
        self._aspect_ratio = aspect_ratio
        self.force_aspect_ratio(*self.GetSize())

    aspect_ratio = property(_get_aspect_ratio, _set_aspect_ratio)

    def add_renderer(self, renderer):
        """Register and add a renderer to the window.
        """
        # Register renderer
        if renderer not in self.renderers:
            self.renderers.append(renderer)
            self.render_window.GetRenderWindow().AddRenderer(renderer)
        if self.renderers:
            # Enable widget.
            self.render_window.Enable(True)

    def remove_renderer(self, renderer):
        """Unregister and remove specified renderer from the window.
        """
        # Disable widget first.
        self.render_window.Enable(False)
        if renderer not in self.renderers:
            self.renderers.remove(renderer)
            self.render_window.GetRenderWindow().RemoveRenderer(renderer)
        if self.renderers:
            # Enable widget again
            self.render_window.Enable(True)

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

    def render(self):
        """Do real rendering action.
        """
        self.render_window.Render()

    @log_call
    def update(self):
        """Updates content of the rendering window.
        """
        self.render()


class RenderWindowPanel(wx.Panel, RenderWindowMixin):
    """Mixin for panel containing wxVTKRenderWindowInteractor.

    Attributes:
    aspect_ratio --- aspect ratio of render_window. (w, h)-tuple.

    """
    def __init__(self, *args, **kwargs):
        # mixin should be call after any widget's __init__.
        # extract aspect ratio, defaulting 4:3.
        aspect_ratio = kwargs.pop('aspect_ratio', (4, 3))
        super(RenderWindowPanel, self).__init__(*args, **kwargs)
        RenderWindowMixin.__init__(self, aspect_ratio=aspect_ratio)


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
            self.render_window_panel = render_window_panel
            self.SetTopWindow(frame)
            renderer = vtk.vtkRenderer()
            # stuff to be rendererd
            source = vtk.vtkConeSource()
            source.SetResolution(8)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            renderer.AddActor(actor)
            render_window_panel.add_renderer(renderer)
            return True

    app = DemoApp(0)
    app.MainLoop()


if __name__=='__main__':
    pass
