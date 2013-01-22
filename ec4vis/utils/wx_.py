# coding: utf-8
"""utils.wx --- Various wx-related utility classes
"""
import os, glob
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.utils import RESOURCES_PATH


class AuiNotebookPlus(wx.aui.AuiNotebook):
    """Notebook with plus.
    """
    def find_page(self, caption):
        """Finds page with caption.
        """
        debug('%s::find_page finding "%s" ...' %(self.__class__.__name__, caption))
        for i in range(self.GetPageCount()):
            if caption == self.GetPageText(i):
                debug('found at #%d' %(i))
                return self.GetPage(i)
        debug('not found.' %(i))
        return None

    def finalize(self):
        """Finalize notebook (and its pages).
        """
        for i in range(self.GetPageCount()):
            page = self.GetPage(i)
            page.finalize()
        debug('finalized %s' %(self.__class__.__name__))


class ImageListWrapper(object):
    """Wrapper for ImageList for list/tree controls.
    """
    def __init__(self, resource_path, image_size=(16, 16), bitmap_type=wx.BITMAP_TYPE_PNG,
                 glob_pattern='*.png'):
        """Initializer.
        """
        self.resource_path = os.path.join(RESOURCES_PATH, resource_path.replace('/', os.path.sep))
        self.glob_pattern = glob_pattern
        self.image_size = image_size
        self.bitmap_type = bitmap_type
        self._image_list = None
        # 
        self.image_id_dict = {}

    @property
    def image_list(self):
        """
        Provides ImageList instance as lazy property.
        
        This is provided as a property, because ImageList cannot be used
        before wx.App is created.
        """
        if self._image_list == None:
            image_list = wx.ImageList(*self.image_size)
            glob_path = os.path.join(self.resource_path, self.glob_pattern)
            for path in glob.glob(glob_path):
                head, tail = os.path.split(path)
                name, ext = os.path.splitext(tail)
                src_image, bmp_image, image_id = None, None, None
                try:
                    src_image = wx.Image(path, self.bitmap_type)
                    bmp_image = src_image.ConvertToBitmap()
                    image_id = image_list.Add(bmp_image)
                except:
                    raise
                if src_image and bmp_image and (image_id is not None):
                    self.image_id_dict[name] = image_id
            self._image_list = image_list
        return self._image_list

    def __getitem__(self, key, default=None):
        """Returns id in wx.ImageList instance for specified image name.
        """
        _unused_ = self.image_list # force to build ImageList
        return self.image_id_dict.get(key, default)
            

class TreeCtrlPlus(wx.TreeCtrl):
    """TreeCtrl having predefined set of handlers (as empty stab).
    """
    
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
        """Initializer.
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        for evt_name, handler_name in self.BINDINGS:
            macro = getattr(wx, 'EVT_TREE_'+evt_name)
            handler = getattr(self, handler_name, None)
            if handler:
                self.Bind(macro, handler, self)

    # Below comments are template of handlers for use in subclass.
    # Handlers are sometimes defined in a subclass, sometimes in somewhere
    # outside of a subclass. Thus TreeCtrlPlus does not expect all handlers
    # are defined inside of a subclass.
    
    # def OnBeginDrag(self, evt):
    #     """Handler called on begin item dragging.
    #     """
    #     pass # do nothing atm

    # def OnBeginRDrag(self, evt):
    #     """Handler called on begin item dragging with right button.
    #     """
    #     pass # do nothing atm

    # def OnEndDrag(self, evt):
    #     """Handler called on end item dragging.
    #     """
    #     pass # do nothing atm

    # def OnBeginLabelEdit(self, evt):
    #     """Handler called on begin editing label on an item.
    #     """
    #     pass # do nothing atm

    # def OnEndLabelEdit(self, evt):
    #     """Handler called on end editing label on an item.
    #     """
    #     pass # do nothing atm

    # def OnDeleteItem(self, evt):
    #     """Handler called on deleting item.
    #     """
    #     pass # do nothing atm

    # def OnGetInfo(self, evt):
    #     """Handler called on getting node info.
    #     """
    #     pass # do nothing atm

    # def OnSetInfo(self, evt):
    #     """Handler called on getting node info.
    #     """
    #     pass # do nothing atm

    # def OnItemActivated(self, evt):
    #     """Handler called on activating item.
    #     """
    #     pass # do nothing atm

    # def OnItemCollapsed(self, evt):
    #     """Handler called on an item has collapsed.
    #     """
    #     pass # do nothing atm

    # def OnItemCollapsing(self, evt):
    #     """Handler called on collapsing an item.
    #     """
    #     pass # do nothing atm

    # def OnItemExpanded(self, evt):
    #     """Handler called on an item has expanded.
    #     """
    #     pass # do nothing atm

    # def OnItemExpanding(self, evt):
    #     """Handler called on expanding item.
    #     """
    #     pass # do nothing atm

    # def OnItemRightClick(self, evt):
    #     """Handler called on right-clicking item.
    #     """
    #     pass # do nothing atm

    # def OnItemMiddleClick(self, evt):
    #     """Handler called on middle-clicking item.
    #     """
    #     pass # do nothing atm

    # def OnSelChanged(self, evt):
    #     """Handler called on user has changed item selection.
    #     """
    #     pass # do nothing atm

    # def OnSelChanging(self, evt):
    #     """Handler called on changing selection.
    #     """
    #     pass # do nothing atm

    # def OnKeyDown(self, evt):
    #     """Handler called on key down.
    #     """
    #     pass # do nothing atm

    # def OnItemGetToolTip(self, evt):
    #     """Handler called on getting tooltip
    #     """
    #     pass # do nothing atm

    # def OnItemMenu(self, evt):
    #     """Handler called on requiring context menu.
    #     """
    #     pass # do nothing atm

    # def OnStateImageClick(self, evt):
    #     """Handler called on clicing state image.
    #     """
    #     pass # do nothing atm


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
