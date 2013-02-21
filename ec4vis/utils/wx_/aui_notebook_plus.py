# coding: utf-8
"""utils.wx --- Various wx-related utility classes
"""
import os, glob
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call


class AuiNotebookPlus(wx.aui.AuiNotebook):
    """Notebook with plus.
    """
    @property
    def selected_page(self):
        """Returns currently selected page in the notebook.
        """
        selected_page_index = self.GetSelection()
        found = None
        if selected_page_index is not wx.NOT_FOUND:
            found = self.GetPage(selected_page_index)
        return found

    def finalize(self):
        """Finalize notebook (and its pages).
        """
        # deletion of pages will cause reorder of page_indices!
        while self.GetPageCount():
            self.destroy_page(0)

    def create_page(self, page_class, page_name, **kwargs):
        """Create a page instance of page_class and add it into the notebook with page_name.
        """
        page_instance = page_class(self, -1, **kwargs)
        # select=True because it should generate page change event.
        page_index = self.AddPage(page_instance, page_name, select=True)
        return page_index, page_instance

    def destroy_page(self, page_index):
        """Remove page of page_index from the notebok and destroy it.

        For symmetry, pages added by create_page should removed with this method.
        """
        page = self.GetPage(page_index)
        page.finalize()
        self.DeletePage(page_index)

    def destroy_selected_page(self):
        """Destroy page instance from the notebook.
        """
        selected_page_index = self.GetSelection()
        if selected_page_index is not wx.NOT_FOUND:
            # this implies page change event.
            self.destroy_page(selected_page_index)
        return selected_page_index

    # Future features
    def save_state(self):
        """Experimental: save page info.
        """
        info_dict = {}
        for i in range(self.GetPageCount()):
            name = self.GetPageText(i)
            page = self.GetPage(i)
            class_name = page.__class__.__name__
            module_name = page.__class__.__module__
            state = None
            if hasattr(page, 'state'):
                state = page.state
            info_dict[name] = dict(class_name=class_name, module_name=module_name, state=state)
        return info_dict

    def restore_state(self, info_dict):
        """Experimental: restore page info.
        """
        for name, info in info_dict.items():
            module_name = info['module_name']
            mod, cls = None, None
            try:
                mod = __import__(module_name)
                class_name = info['class_name']
                cls = getattr(mod, class_name, None)
            except ImportError:
                debug('Unable to load %s' %module_name)
            if cls:
                page = cls(self, -1)
                if hasattr(page, 'state'):
                    page.state = info['state']
                self.AddPage(page, name)


class AuiNotebookPlusWithTargetBindingPage(AuiNotebookPlus):
    """AuiNotebookPlus for target-binding pages
    """
    def __init__(self, *args, **kwargs):
        AuiNotebookPlus.__init__(self, *args, **kwargs)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnPageClose)
    
    def find_page_for_target(self, target):
        """Finds page which binds given target
        """
        found_page_index, found_page_instance = None, None
        if target is None:
            debug('Cannot find page for target=None')
        else:
            for page_index in range(self.GetPageCount()):
                page_instance = self.GetPage(page_index)
                if getattr(page_instance, 'target', None)==target:
                    found_page_index = page_index
                    found_page_instance = page_instance
        return found_page_index, found_page_instance

    def destroy_page_for_target(self, target):
        """Destroys page which binds given target
        """
        page_index_to_delete, page_instance_to_delete = self.find_page_for_target(target)
        if page_index_to_delete is None:
            return
        else:
            if target:
                target.remove_observer(page_instance_to_delete)
            self.destroy_page(page_index_to_delete)

    def OnPageClose(self, event):
        """On page close, the page should be removed from the observers list.
        """
        page_index = event.GetSelection()
        if not (page_index is wx.NOT_FOUND):
            self.GetPage(page_index).finalize()


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
