

import wx, wx.lib.scrolledpanel, wx.lib.newevent
import threading


#
# Library Screen
#

COLUMN_WIDTH = 150
ROW_HEIGHT = COLUMN_WIDTH*0.75
CELL_PAD = 5

class BookThumbnail (wx.BitmapButton):
    
    def __init__ (self, parent, bookcallback, bookcover):
        
        self.callback = bookcallback
        
        img = wx.Image (bookcover)
        img.Rescale (COLUMN_WIDTH, ROW_HEIGHT)
        
        super(BookThumbnail, self).__init__(parent, wx.ID_ANY, img.ConvertToBitmap())
        
        self.Bind (wx.EVT_BUTTON, self.onClick, self)
    
    def onClick (self, evt):
        
        self.callback ()

def width_to_numcolumns (width):
    return (width-wx.SystemSettings.GetMetric (wx.SYS_VSCROLL_X))/(COLUMN_WIDTH+2*CELL_PAD)

def numcolumns_to_width (numcolumns):
    return numcolumns*(COLUMN_WIDTH+2*CELL_PAD)+wx.SystemSettings.GetMetric (wx.SYS_VSCROLL_X)

def height_to_numrows (height):
    return height/(ROW_HEIGHT+2*CELL_PAD)

def numrows_to_height (numrows):
    return numrows*(ROW_HEIGHT+2*CELL_PAD)

class LibraryScreen (wx.lib.scrolledpanel.ScrolledPanel):
    
    def __init__ (self, parent):
        
        super(LibraryScreen, self).__init__ (parent)
        
        self.parent = parent
        
        self.sizer = wx.GridSizer (vgap = CELL_PAD, hgap = CELL_PAD)
        self.SetSizer (self.sizer)
        
        self.Bind (wx.EVT_SIZE, self.onResize)
        
    def setSize (self):
        
        (w, h) = self.GetSizeTuple ()
        self.sizer.SetCols (width_to_numcolumns(w))
        self.sizer.CalcRowsCols ()
        self.SetupScrolling(scroll_x = False, scrollToTop = False)
        self.sizer.Layout ()
    
    def onResize (self, evt):
        
        self.setSize()
        
        evt.Skip ()
    
    def Show (self):
        
        self.parent.SetSize ((numcolumns_to_width (4), numrows_to_height (4)))
        self.parent.SetMinSize ((numcolumns_to_width (2), numrows_to_height (2)))
        
        self.setSize()
        
        self.sizer.Layout ()
        
        super(LibraryScreen, self).Show()
    
    def add_book (self, bookcallback, bookcover):
        
        thumbnail = BookThumbnail (self, bookcallback, bookcover)
        self.sizer.Add (thumbnail, 1, wx.FIXED_MINSIZE)
        
        self.setSize()


#
# Main Window
#
        
class MainWindow (wx.Frame):
    
    def __init__(self, title):
    
        super(MainWindow, self).__init__(None, title = title)
        
        self.sizer = wx.BoxSizer (wx.VERTICAL)
        self.SetSizer (self.sizer)
        
        self.allscreens = []
        
    def AddScreen (self, screen):
        
        self.sizer.Add (screen, 1, wx.EXPAND)
        screen.Hide ()
        
        self.allscreens += [screen]
    
    def SwitchToScreen (self, screen):
        
        for otherscreen in self.allscreens:
            otherscreen.Hide ()
        
        screen.Show ()
        
        self.Layout ()
        
        self.Show ()


#
# UI Interface
#

class UI:
    
    def __init__ (self):
        
        self.callback_queue_lock = threading.Lock ()
        self.callback_queue = []
        
        self.init_lock = threading.Lock ()
        
        self.init_lock.acquire ()
        
        self.gui_thread = threading.Thread (target = self.thread_toplevel)
        self.gui_thread.daemon = True
        self.gui_thread.start ()
        
        self.init_lock.acquire ()
        
    # Called from the same thread as the rest of the program. Used to run 
    # an arbitrary method in the GUI thread.
    def run_method_in_thread (self, callback):
        
        evt = self.RunMethodEvent (callback = callback)
        
        #PostEvent is explicitly supposed to be thread-safe.
        wx.PostEvent (self.window, evt) 
    
    # runs in the GUI thread
    def onRunMethod (self, evt):
        
        evt.callback ()
    
    # GUI thread main loop
    def thread_toplevel (self):
        
        app = wx.App()
        
        self.RunMethodEvent, self.EVT_RUN_METHOD = wx.lib.newevent.NewEvent ()
        
        self.window = MainWindow(title = 'Reading App')
        
        self.libraryscreen = LibraryScreen (self.window)
        self.window.AddScreen (self.libraryscreen)
        
        self.window.Bind (self.EVT_RUN_METHOD, self.onRunMethod)
        self.window.Bind (wx.EVT_CLOSE, self.onClose)
        
        self.init_lock.release ()
        
        app.MainLoop ()
    
    # runs in either thread, makes callbacks which will run in GUI thread
    def make_add_callback_callback (self, callback):
        
        def callback_callback ():
            with self.callback_queue_lock:
                self.callback_queue += [callback]
        
        return callback_callback
    
    # runs in GUI thread
    def onClose (self, evt):
        
        with self.callback_queue_lock:
            self.callback_queue += [lambda: exit (0)]
    
    # Begin methods intended to be public:
    
    def display_library (self):
        
        self.run_method_in_thread (lambda: self.window.SwitchToScreen (self.libraryscreen))
    
    def add_book_to_library (self, bookcallback, bookcover):
        
        callback_callback = self.make_add_callback_callback (bookcallback)
        self.run_method_in_thread (lambda: self.libraryscreen.add_book (callback_callback, bookcover))
    
    def flush_callback_queue (self):
        
        old_callback_queue = None
        with self.callback_queue_lock:
            old_callback_queue = self.callback_queue
            self.callback_queue = []
        
        for old_callback in old_callback_queue:
            old_callback ()
    
