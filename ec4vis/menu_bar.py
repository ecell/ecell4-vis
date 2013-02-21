# coding: utf-8
"""ec4vis.menu_bar --- Application menubar.
"""
import wx


MENU_STRUCTURE = (
    # section_name, section_info
    ('App', (
        # attr_bit, label, accel_key, tip
        ('about', 'About', '', 'About this application.'),
        ('quit', 'Quit', 'Ctrl-Q', 'Quit application'),
        )),
    ('Datasource', (
        # attr_bit, label, accel_key, tip
        ('add', 'Add...', '', 'Add datasource page.'),
        ('remove', 'Remove', '', 'Remove datasource page.'),
        )),
    ('Pipeline', (
        # attr_bit, label, accel_key, tip
        ('add_node', 'Add Node...', '', 'Add pipeline node.'),
        )),
    )


class AppMenuBar(wx.MenuBar):
    """Application menubar.
    """
    def __init__(self, parent, *args, **kwargs):
        """Initializer.
        """
        wx.MenuBar.__init__(self, *args, **kwargs)

        # Build menu from MENU_STRUCTURE
        for section_name, section_info in MENU_STRUCTURE:
            # create section
            menu = wx.Menu()
            self.Append(menu, '&'+section_name)
            # bind as self.<section_name>_menu
            setattr(self, section_name.lower()+'_menu', menu)
            for attr_bit, label, accel_key, tip in section_info:
                # create menuitem for the section
                if accel_key:
                    label += ('\t'+accel_key)
                menu_item = menu.Append(-1, label, tip)
                # bind as self.<section_name>_<attr_bit>
                setattr(self, section_name.lower()+'_'+attr_bit, menu_item)
        # associate menubar to parent.
        parent.SetMenuBar(self)

    def finalize(self):
        """Finalizer.
        """
        # placeholder atm


if __name__=='__main__':

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Menu Demo')
            menubar = AppMenuBar(frame)
            frame.SetMenuBar(menubar)
            frame.Layout()
            frame.Bind(wx.EVT_MENU, self.OnQuitMenu, menubar.app_quit)
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

        def OnQuitMenu(self, evt):
            """Handler on Quit menu.
            """
            self.ExitMainLoop()
        
    app = App(0)
    app.MainLoop()
