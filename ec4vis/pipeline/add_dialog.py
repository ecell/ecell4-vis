# coding: utf-8
import wx

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG


class AddPipelineNodeDialog(wx.Dialog):
    """Dialog used for 'Add Pipeline Node' operation.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        caption = kwargs.pop('caption', 'Choose Node Type')
        pn_choices = kwargs.pop('choices', [])
        style=kwargs.setdefault('style', wx.CAPTION|wx.CLOSE_BOX)
        kwargs.setdefault('title', 'Node Types')
        wx.Dialog.__init__(self, *args, **kwargs)
        caption_label = wx.StaticText(self, -1, label=caption)
        type_listbox = wx.ListBox(self, -1, style=wx.LB_SINGLE|wx.LB_SORT|wx.SUNKEN_BORDER, choices=pn_choices)
        # 'Name:' text entry
        name_label = wx.StaticText(self, -1, label='Name: ')
        name_text = wx.TextCtrl(self, -1, 'MyPipelineNode')
        # sizer for text entry
        text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer.Add(name_label, 0, wx.ALL|wx.EXPAND, 0)
        text_sizer.Add(name_text, 1, wx.ALL|wx.EXPAND, 0)
        # sizer for OK/Cancel buttons
        button_sizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        # populate dialog's root sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(caption_label, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(type_listbox, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(text_sizer, 0, wx.ALL|wx.EXPAND, 10)
        sizer.Add(button_sizer, 0, wx.ALL|wx.EXPAND, 0)
        # memorize OK/Cancel button for Enable/Disable control
        ok_button, cancel_button = None, None
        # This is a small hack to disable OK button at default.
        for sizer_item in button_sizer.GetChildren():
            window = sizer_item.GetWindow()
            if window:
                if window.GetId()==wx.ID_OK:
                    ok_button = window
                    ok_button.Disable()
                elif window.GetId()==wx.ID_CANCEL:
                    cancel_button = window
        # bindings
        self.pipeline_node_choices = pn_choices
        self.name_text = name_text
        self.type_listbox = type_listbox
        self.ok_button = ok_button
        self.cancel_button = cancel_button
        # event bindings
        self.Bind(wx.EVT_LISTBOX, self.OnListBox)
        self.Bind(wx.EVT_TEXT, self.OnNameText)
        self.SetSizer(sizer)

    def OnListBox(self, evt):
        """If no entry in list box is selected, disable OK button.
        """
        if self.node_name is None:
            return
        self.name_text.SetValue(self.node_name)
        self.ok_button.Enable()
        
    def OnNameText(self, evt):
        """If value of the name text is zero, disable OK button.
        """
        text = self.name_text.GetValue()
        self.ok_button.Enable(bool(len(text)))

    @property
    def label_name(self):
        return self.name_text.GetValue()

    @property
    def node_name(self):
        selected_row_index = self.type_listbox.GetSelection()
        if selected_row_index is wx.NOT_FOUND:
            self.ok_button.Disable()
            return None
        return self.type_listbox.GetString(selected_row_index)


if __name__=='__main__':

    class DemoApp(wx.App):

        def OnInit(self):
            frame = wx.Frame(None, -1)
            self.frame = frame
            sizer = wx.BoxSizer()
            button = wx.Button(frame, -1, 'Pop dialog')
            button.Bind(wx.EVT_BUTTON, self.OnButton)
            sizer.Add(button, 0, wx.ALL|wx.EXPAND, 30)
            frame.SetSizer(sizer)
            frame.Fit()
            self.SetTopWindow(frame)
            frame.Show(True)
            return True

        def OnButton(self, evt):
            dlg = AddPipelineNodeDialog(self.frame, choices=['Lancelot', 'Garahad', 'Robin', 'Arthur'])
            ret = dlg.ShowModal()

    app = DemoApp(0)
    app.MainLoop()
