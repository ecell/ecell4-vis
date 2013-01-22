# coding: utf-8
"""visual_panel.py --- Visual inspector panel in control panel.
"""
import wx
from wx.dataview import (
    DataViewListCtrl, PyDataViewModel, NullDataViewItem)


class VisualDataViewModel(PyDataViewModel):
    """Data model for VisualDataViewListCtrl.
    """
    # almost same as FileDataViewModel.
    def __init__(self, data, *args, **kwargs):
        """Initializer.
        """
        PyDataViewModel.__init__(self, *args, **kwargs)
        self.data = data

    def GetColumnCount(self):
        return 2

    def GetColumnType(self, col):
        return ['bool', 'string'][col]

    def GetChildren(self, parent, children):
        n_children = 0
        if not parent:
            for obj in self.data:
                children.append(self.ObjectToItem(obj))
            n_children = len(self.data)
        return n_children

    def IsContainer(self, item):
        if not item:
            return True
        return False

    def GetParent(self, item):
        return NullDataViewItem

    def GetValue(self, item, col):
        node = self.ItemToObject(item)
        if node:
            """
            if col==0:
                return node.checked
            else:
                return node.path"""
            return node[col]

    def SetValue(self, value, item, col):
        node = self.ItemToObject(item)
        if node:
            """
            if col==0:
                node.checked = value
            else:
                node.path = value"""
            node[col] = value


class VisualDataViewListCtrl(DataViewListCtrl):
    """DataViewListCtrl for visual list.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        DataViewListCtrl.__init__(self, *args, **kwargs)
        visible_column = self.AppendToggleColumn('Visible', width=40)
        name_column = self.AppendTextColumn('Name')
        # for auto-column-width hack
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.visible_column = visible_column
        self.name_column = name_column

    def AssociateModel(self, model):
        """Overriden method to fix unaware-prepopulated-items bug.
        """
        DataViewListCtrl.AssociateModel(self, model)
        # this is called to fix errornours behaviour
        # that DVLC does not refresh rows when
        # AssociateModel() is called with a populated model.
        model.AfterReset()

    def OnSize(self, event):
        """Adjusts file column width.
        """
        width = self.GetClientSize()[0]-10
        self.name_column.SetWidth(width-self.visible_column.GetWidth())
        

class VisualPanel(wx.Panel):
    """Visual controlls panel.
    """
    def __init__(self, *args, **kwargs):
        kwargs['style'] = kwargs.get('style', 0)|wx.BORDER_SUNKEN
        wx.Panel.__init__(self, *args, **kwargs)
        visual_list = VisualDataViewListCtrl(self, -1, style=wx.BORDER_SUNKEN)
        # name bindings
        self.visual_list = visual_list
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(wx.StaticText(self, -1, u'Visuals'), 0, wx.ALL, 5)
        root_sizer.Add(visual_list, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(root_sizer)


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visual Panel Demo')
            visual_panel = VisualPanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(visual_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
