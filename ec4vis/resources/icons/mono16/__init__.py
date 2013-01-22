# coding: utf-8
"""ec4vis.resources.icons.mono16 --- monochromat 16x16 icons
"""
import os.path, glob
import wx

IMAGE_SIZE = (16, 16)
image_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def image_list():
image_list = wx.ImageList(*image_size)

for fn in glob.glob(os.path.join(image_data_path, '*.png')):
    print fn



if __name__=='__main__':
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Mono16 icons Demo')
            sizer = wx.BoxSizer(wx.VERTICAL)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    #app.MainLoop()
