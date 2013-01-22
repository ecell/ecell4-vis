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
