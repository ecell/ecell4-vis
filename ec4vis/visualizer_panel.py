# coding: utf-8
"""visualizer_panel.py --- visualizer panel
"""
import wx
from wx.dataview import (
    DataViewListCtrl, PyDataViewModel, NullDataViewItem)


class DataViewModelPlus(PyDataViewModel):
    """Enhanced DataViewModel.
    """
    def __init__(self, data, *args, **kwargs):
        """Initialzer.
        """
        PyDataViewModel.__init__(self, *args, **kwargs)
        self.data = data

    def GetChildren(self, parent, children):
        n_children = 0
        if not parent:
            for obj in self.data:
                children.append(self.ObjectToItem(obj))
            n_children = len(self.data)
        return n_children

    def IsContainer(self, item):
        if item is None:
            return True
        return False

    def GetParent(self, item):
        return NullDataViewItem

    def GetValue(self, item, col):
        node = self.ItemToObject(item)
        if node:
            return node[col]

    def SetValue(self, value, item, col):
        node = self.ItemToObject(item)
        if node:
            node[col] = value


class DataViewListCtrlPlus(DataViewListCtrl):
    """Enhanced DataViewListCtrl for source list.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        DataViewListCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self._columns = [] # (columns, width_ratio)
        self._populate_columns()

    def _populate_columns(self):
        """Subclass should override to poplulate columns.
        """
        return NotImplemented

    def AssociateModel(self, model):
        """Overriden method to fix unaware-prepopulated-items bug.
        """
        DataViewListCtrl.AssociateModel(self, model)
        # this is called to fix errornours behaviour
        # that DVLC does not refresh rows when
        # AssociateModel() is called with a populated model.
        model.AfterReset()

    def OnSize(self, event):
        """Adjusts source column width.
        """
        width = self.GetClientSize()[0]-10
        fixed_columns_width = sum(
            col.GetWidth() for col, w_ratio in self._columns if w_ratio==0)
        auto_width_sum = sum(
            w_ratio for col, w_ratio in self._columns if w_ratio)
        auto_width = width-fixed_columns_width
        for col, w_ratio in self._columns:
            if w_ratio:
                if auto_width<0:
                    col.SetWidth(0)
                else:
                    col.SetWidth(int(auto_width*w_ratio/float(auto_width_sum)))


class SourceDataViewModel(DataViewModelPlus):
    """Data model for SourceDataViewListCtrl.
    """

    def GetColumnCount(self):
        return 2

    def GetColumnType(self, col):
        return ['bool', 'string'][col]


class SourceDataViewListCtrl(DataViewListCtrlPlus):
    """DataViewListCtrl for source list.
    """
    def _populate_columns(self):
        use_column = self.AppendToggleColumn('Use', width=30)
        source_column = self.AppendTextColumn('Source')
        self._columns.append((use_column, 0))
        self._columns.append((source_column, 1))
        self.use_column = use_column
        self.source_column = source_column


class DataDataViewModel(DataViewModelPlus):
    """Data model for DataDataViewListCtrl.
    """
    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        # id, type, name
        return ['string', 'string', 'string'][col]


class DataDataViewListCtrl(DataViewListCtrlPlus):
    """DataViewListCtrl for data list.
    """
    def _populate_columns(self):
        id_column = self.AppendTextColumn('Id', width=30)
        type_column = self.AppendTextColumn('Type', width=100)
        name_column = self.AppendTextColumn('Name')
        self._columns.append((id_column, 0))
        self._columns.append((type_column, 0))
        self._columns.append((name_column, 1))
        self.id_column = type_column
        self.type_column = type_column
        self.name_column = name_column


class VisualizerPanel(wx.Panel):
    """Visualizer configuration panel.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        kwargs['style'] = kwargs.get('style', 0)|wx.BORDER_SUNKEN
        wx.Panel.__init__(self, *args, **kwargs)
        visualizer_choice = wx.Choice(self, -1)
        # controls
        reset_button = wx.Button(self, -1, u'Reset/Update')
        configure_button = wx.Button(self, -1, u'Configure')
        # source_list = SourceDataViewListCtrl(self, -1, style=wx.BORDER_SUNKEN)
        # add_button = wx.Button(self, -1, u'Add')
        # remove_button = wx.Button(self, -1, u'Delete')
        data_list = DataDataViewListCtrl(self, -1, style=wx.BORDER_SUNKEN)
        up_button = wx.Button(self, -1, u'Up')
        down_button = wx.Button(self, -1, u'Down')
        """
        interval_spin = wx.SpinCtrlDouble(self, -1, value='0.064', min=0.032, max=2.048, inc=0.016)
        frame_id_text = wx.StaticText(self, -1, u'')
        frame_pos_slider = wx.Slider(self, -1, value=0, minValue=0, maxValue=1)
        start_button = wx.Button(self, -1, '|<')
        end_button = wx.Button(self, -1, '>|')
        play_button = wx.Button(self, -1, u'>')
        """
        # sizers
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer1.Add(reset_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer1.Add(configure_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        # button_sizer2.Add(add_button, 1, wx.EXPAND|wx.ALL, 0)
        # button_sizer2.Add(remove_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer3.Add(up_button, 1, wx.EXPAND|wx.ALL, 0)
        button_sizer3.Add(down_button, 1, wx.EXPAND|wx.ALL, 0)
        """
        player_sizer = wx.BoxSizer(wx.VERTICAL)
        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        status_sizer.Add(wx.StaticText(self, -1, u'Interval'), 0, wx.ALL, 0)
        status_sizer.Add(interval_spin, 0, wx.ALL, 0)
        button_sizer4.Add(start_button, 0, wx.ALL|wx.EXPAND, 0)
        button_sizer4.Add(play_button, 0, wx.ALL|wx.EXPAND, 0)
        button_sizer4.Add(end_button, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(status_sizer, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(frame_id_text, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(frame_pos_slider, 0, wx.ALL|wx.EXPAND, 0)
        player_sizer.Add(button_sizer4, 0, wx.ALL|wx.EXPAND, 0)
        """
        root_sizer.Add(wx.StaticText(self, -1, u'Visualizer'), 0, wx.ALL, 5)
        root_sizer.Add(visualizer_choice, 0, wx.ALL, 5)
        root_sizer.Add(button_sizer1, 0, wx.ALL, 5)
        root_sizer.Add(wx.StaticText(self, -1, u'Sources'), 0, wx.ALL, 5)
        # root_sizer.Add(source_list, 1, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(button_sizer2, 0, wx.ALL, 5)
        root_sizer.Add(wx.StaticText(self, -1, u'Data'), 0, wx.ALL, 5)
        root_sizer.Add(data_list, 1, wx.ALL|wx.EXPAND, 5)
        root_sizer.Add(button_sizer3, 0, wx.ALL, 5)
        """
        root_sizer.Add(wx.StaticText(self, -1, u'Animation'), 0, wx.ALL, 5)
        root_sizer.Add(player_sizer, 0, wx.ALL, 5)
        """
        # name bindings
        self.reset_button = reset_button
        self.configure_button = configure_button
        self.visualizer_choice = visualizer_choice
        # self.source_list = source_list
        self.data_list = data_list
        # self.add_button = add_button
        # self.remove_button = remove_button
        self.up_button = up_button
        self.down_button = down_button
        """
        self.interval_spin = interval_spin
        self.frame_id_text = frame_id_text
        self.frame_pos_slider = frame_pos_slider
        self.start_button = start_button
        self.end_button = end_button
        self.play_button = play_button
        """
        # bind sizer
        self.SetSizer(root_sizer)

    def set_visualizer_choices(self, choices):
        """Set visualizer choices.
        """
        self.visualizer_choice.Clear()
        self.visualizer_choice.AppendItems(choices)


if __name__=='__main__':
    VISUALIZERS = ['Particle', 'Lattice', 'Compartment']
    sources = [[True, '/foo/bar/baz.data'],
               [False, '/foo/bar/qux.data']]
    data = [['SomeType', 'some-typed-data'],
            ['AnotherType', 'another-typed-data']]
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Visualizer Panel Demo', size=(-1, 600))
            visualizer_panel = VisualizerPanel(frame, -1)
            visualizer_panel.set_visualizer_choices(VISUALIZERS)
            source_model = SourceDataViewModel(sources)
            data_model = DataDataViewModel(data)
            # visualizer_panel.source_list.AssociateModel(source_model)
            visualizer_panel.data_list.AssociateModel(data_model)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
