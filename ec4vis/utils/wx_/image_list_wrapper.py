# coding: utf-8
"""utils.wx_.image_list_wrapper --- convenient ImageList wrapper.
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
from ec4vis.utils import RESOURCES_PATH


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


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
