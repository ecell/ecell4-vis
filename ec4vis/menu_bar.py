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
    #('Workspace', (
    #    ('set_root', 'Set Root Directory...', 'Ctrl-O', 'Set Root Directory for Workspace.'),
        #('save', 'Save Workspace', 'Ctrl-S', 'Save current workspace state.'),
        #('save_as', 'Save Workspace As...', 'Ctrl-Shift-S', 'Save current workspace state with given filename.'),
        #('load', 'Load Workspace...', 'Ctrl-O', 'Load current workspace state.'),
        #('remove', 'Remove Selected Item', '', 'Remove item in selection.'),
        #('add_file', 'Add Data Files...', '', 'Add data file(s).'),
        #('add_loader', 'Add Loader...', '', 'Add a loader.'),
        #('add_visualizer', 'Add Visualizer...', '', 'Add a visualizer.'),
        #('add_filter', 'Add Filter...', '', 'Add a filter.'),
    #    )),
    #('Visual', (
    #    ('toggle', 'Toggle Visibility', '', 'Toggle visivility.'),
    #    )),
    #('Parameter', (
    #    ('import', 'Import Parameters...', '', 'Import parameters.'),
    #    )),
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
            self.ExitMainLoop()
        
    app = App(0)
    app.MainLoop()
