# coding: utf-8
"""ec4vis.console.panel --- Console panel in visualizer application.
"""
import wx


# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG, StreamHandler


class ConsoleLogStream(object):

    def __init__(self, text_ctrl):
        self.text_ctrl = text_ctrl

    def write(self, bytes):
        try:
            wx.CallAfter(self.text_ctrl.AppendText, bytes)
        except:
            pass # prevent failure on app exit.
    
    def flush(self):
        pass


class ConsolePanel(wx.Panel):
    """Console panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        text_ctrl = wx.TextCtrl(
            self, -1, '',
            style=wx.TE_READONLY|wx.TE_BESTWRAP|wx.TE_MULTILINE)
        console_stream_handler = StreamHandler(stream=ConsoleLogStream(text_ctrl))
        logger.addHandler(console_stream_handler)
        sizer = wx.BoxSizer()
        sizer.Add(text_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)
        # bindings
        self.console_stream_handler = console_stream_handler

    def finalize(self):
        """Finalizer.
        """
        # actually this is not necesally...
        logger.removeHandler(self.console_stream_handler)



if __name__=='__main__':

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """wxApp Initializer.
            """
            frame = wx.Frame(None, -1, u'ConsolePanel demo')
            console_panel = ConsolePanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(console_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    logger.setLevel(DEBUG)
    debug('foo bar baz')
    app.MainLoop()
