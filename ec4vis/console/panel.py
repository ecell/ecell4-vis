# coding: utf-8
"""ec4vis.console.panel --- Console panel in visualizer application.
"""
import wx

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG, StreamHandler, Formatter


class ConsoleLogStream(object):
    """Pseudo stream object which redirects input to wx.TextCtrl.
    """

    def __init__(self, text_ctrl):
        """Initializer.
        """
        self.text_ctrl = text_ctrl

    def write(self, bytes):
        """Writes bytes (into wx.TextArea buffer).
        """
        try:
            # wx.CallAfter is used to avoid unexpected deadlock.
            wx.CallAfter(self.text_ctrl.AppendText, bytes)
        except:
            pass # prevent any failure on app exit.

    def flush(self):
        """Do nothing.
        """
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
        # prepare a hooked stream handler
        console_stream_handler = StreamHandler(stream=ConsoleLogStream(text_ctrl))
        console_stream_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S'))
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
            console_panel.Bind(wx.EVT_TIMER, self.OnTimer)
            self.timer = wx.Timer(console_panel)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(console_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            # timer
            return True

        def OnTimer(self, event):
            """Timer event handler.
            """
            debug('foo bar baz, I like ham, spam and bacon.')
        
    logger.setLevel(DEBUG)
    app = App(0)
    app.timer.Start(1000)
    app.MainLoop()
