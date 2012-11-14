# coding: utf-8
"""Various wx-related utility classes
"""
import wx


class TreeCtrlPlus(wx.TreeCtrl):
    
    BINDINGS = (
        ('BEGIN_DRAG', 'OnBeginDrag'),
        ('BEGIN_RDRAG', 'OnBeginRDrag'),
        ('END_DRAG', 'OnEndDrag'),
        ('BEGIN_LABEL_EDIT', 'OnBeginLabelEdit'),
        ('END_LABEL_EDIT', 'OnEndLabelEdit'),
        ('DELETE_ITEM', 'OnDeleteItem'),
        ('GET_INFO', 'OnGetInfo'),
        ('SET_INFO', 'OnSetInfo'),
        ('ITEM_ACTIVATED', 'OnItemActivated'),
        ('ITEM_COLLAPSED', 'OnItemCollapsed'),
        ('ITEM_COLLAPSING', 'OnItemCollapsing'),
        ('ITEM_EXPANDED', 'OnItemExpanded'),
        ('ITEM_EXPANDING', 'OnItemExpanding'),
        ('ITEM_RIGHT_CLICK', 'OnItemRightClick'),
        ('ITEM_MIDDLE_CLICK', 'OnItemMiddleClick'),
        ('SEL_CHANGED', 'OnSelChanged'),
        ('SEL_CHANGING', 'OnSelChanging'),
        ('KEY_DOWN', 'OnKeyDown'),
        ('ITEM_GETTOOLTIP', 'OnItemGetToolTip'),
        ('ITEM_MENU', 'OnItemMenu'),
        ('STATE_IMAGE_CLICK', 'OnStateImageClick'),
        )    


    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        for evt_name, handler_name in self.BINDINGS:
            macro = getattr(wx, 'EVT_TREE_'+evt_name)
            handler = getattr(self, handler_name, None)
            if handler:
                self.Bind(macro, handler, self)
        
    def OnBeginDrag(self, evt):
        """Handler called on begin item dragging.
        """
        pass # do nothing atm

    def OnBeginRDrag(self, evt):
        """Handler called on begin item dragging with right button.
        """
        pass # do nothing atm

    def OnEndDrag(self, evt):
        """Handler called on end item dragging.
        """
        pass # do nothing atm

    def OnBeginLabelEdit(self, evt):
        """Handler called on begin editing label on an item.
        """
        pass # do nothing atm

    def OnEndLabelEdit(self, evt):
        """Handler called on end editing label on an item.
        """
        pass # do nothing atm

    def OnDeleteItem(self, evt):
        """Handler called on deleting item.
        """
        pass # do nothing atm

    def OnGetInfo(self, evt):
        """Handler called on getting node info.
        """
        pass # do nothing atm

    def OnSetInfo(self, evt):
        """Handler called on getting node info.
        """
        pass # do nothing atm

    def OnItemActivated(self, evt):
        """Handler called on activating item.
        """
        pass # do nothing atm

    def OnItemCollapsed(self, evt):
        """Handler called on an item has collapsed.
        """
        pass # do nothing atm

    def OnItemCollapsing(self, evt):
        """Handler called on collapsing an item.
        """
        pass # do nothing atm

    def OnItemExpanded(self, evt):
        """Handler called on an item has expanded.
        """
        pass # do nothing atm
        
    def OnItemExpanding(self, evt):
        """Handler called on expanding item.
        """
        pass # do nothing atm

    def OnItemRightClick(self, evt):
        """Handler called on right-clicking item.
        """
        pass # do nothing atm

    def OnItemMiddleClick(self, evt):
        """Handler called on middle-clicking item.
        """
        pass # do nothing atm

    def OnSelChanged(self, evt):
        """Handler called on user has changed item selection.
        """
        pass # do nothing atm

    def OnSelChanging(self, evt):
        """Handler called on changing selection.
        """
        pass # do nothing atm

    def OnKeyDown(self, evt):
        """Handler called on key down.
        """
        pass # do nothing atm

    def OnItemGetToolTip(self, evt):
        """Handler called on getting tooltip
        """
        pass # do nothing atm

    def OnItemMenu(self, evt):
        """Handler called on requiring context menu.
        """
        pass # do nothing atm

    def OnStateImageClick(self, evt):
        """Handler called on clicing state image.
        """
        pass # do nothing atm

if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
