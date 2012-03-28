# coding: utf-8
"""app.py -- Visualizer Application implementation by Yasushi Masuda (ymasuda@accense.com)
"""
from logging import debug

import wx

from browser import BrowserFrame
from ecell4.world import World


VERSION = (0, 0, 1)
APP_TITLE_NAME = 'E-Cell 4 Visualization Browser Version (%d.%d.%d)' %VERSION


class BrowserApp(wx.App):
    """Application object for browser.
    """

    def OnInit(self):
        """Integrated initialization hook.
        """
        # UI stuff
        browser = BrowserFrame(self, None, -1, APP_TITLE_NAME)
        self.SetTopWindow(browser)
        browser.Show(True)
        self.browser = browser

        # application status
        self.world = None
        self.visualizer = None
        
        return True

    def OnOpenWorldMenu(self, evt):
        """Handler for 'File'->'Open World File' menu.
        """
        dlg = wx.FileDialog(
            self.browser, message='Select world datafile',
            style=wx.OPEN)
        path = None
        if dlg.ShowModal()==wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if path:
            pass
            # if valid worldtype, load it
            # try:
            #     world = load_world(path)
            # except:
            #     pass # error
            # look for available visualizer
            # available_visualizers = find_visializers(world)
            # visualizer_class = None
            # if len(available_visualizers)==1: # found exact
            #     visualizer_class_name = available_visualizers[0]
            # elif len(available_visualizers)>1:
            #     # show selection dialog
            #     visualizer_class_name = dlg.GetValue()
            # VizualizerClass = load_visualizer_class(visualizer_class_name)
            # self.visualizer = VisualizerClass(self.renderer, world)
            # add to browser
        #self.browser.Fit()

    def OnQuitMenu(self, evt):
        """Handler for 'File'->'Quit' menu.
        """
        self.ExitMainLoop()

    def DummyHandler(self, evt):
        """Dummy Handler.
        """
        pass
