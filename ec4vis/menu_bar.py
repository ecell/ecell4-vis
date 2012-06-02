# coding: utf-8
"""menubar.py --- Application menubar.
"""
import wx


class AppMenuBar(wx.MenuBar):
    """Application menubar.
    """
    def __init__(self, parent, *args, **kwargs):
        """Initializer.
        """
        wx.MenuBar.__init__(self, *args, **kwargs)
        # file menu
        file_menu = wx.Menu()
        file_add = file_menu.Append(-1, '&Add source...\tCtrl-O', "Add a file source")
        file_quit = file_menu.Append(-1, '&Quit\tCtrl-Q', "Quit application")
        # populating menus
        self.Append(file_menu, '&File')
        # name bindings
        self.file_menu = file_menu
        self.file_add = file_add
        self.file_quit = file_quit
        # associate menubar to parent.
        parent.SetMenuBar(self)


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visual Panel Demo')
            menubar = AppMenuBar(frame)
            frame.SetMenuBar(menubar)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
