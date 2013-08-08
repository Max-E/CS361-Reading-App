

import wx, wx.lib.scrolledpanel, wx.lib.newevent
import threading, time


#
# Library Screen
#

COLUMN_WIDTH = 150
ROW_HEIGHT = COLUMN_WIDTH*0.75
CELL_PAD = 5

class BookThumbnail (wx.BitmapButton):
    
    def __init__ (self, parent, bookname, bookcover):
        
        self.name = bookname
        
        img = wx.Image (bookcover)
        img.Rescale (COLUMN_WIDTH, ROW_HEIGHT)
        
        super(BookThumbnail, self).__init__(parent, wx.ID_ANY, img.ConvertToBitmap())
        
        self.Bind (wx.EVT_BUTTON, self.onClick, self)
    
    def onClick (self, evt):
        
        print "CLICKED BOOK \""+self.name+"\""

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
        
        self.SetupScrolling(scroll_x = False)
        
        self.Bind (wx.EVT_SIZE, self.onResize)
        
    def setSize (self):
        
        (w, h) = self.GetSizeTuple ()
        self.sizer.SetCols (width_to_numcolumns(w))
        self.sizer.CalcRowsCols ()
    
    def onResize (self, evt):
        
        self.setSize()
        
        evt.Skip ()
    
    def Show (self):
        
        self.parent.SetSize ((numcolumns_to_width (4), numrows_to_height (4)))
        self.parent.SetMinSize ((numcolumns_to_width (2), numrows_to_height (2)))
        
        self.setSize()
        
        self.sizer.Layout ()
        
        super(LibraryScreen, self).Show()
    
    def add_book (self, bookname, bookcover):
        
        thumbnail = BookThumbnail (self, bookname, bookcover)
        self.sizer.Add (thumbnail, 1, wx.FIXED_MINSIZE)


#
# Main Window
#
        
class MainWindow (wx.Frame):
    
    def __init__(self, title):
    
        super(MainWindow, self).__init__(None, title = title)
        
        self.sizer = wx.BoxSizer (wx.VERTICAL)
        
        self.allscreens = []
        
        self.SetSizer (self.sizer)
        
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
        
        self.mainloop_thread = threading.Thread (target = self.thread_toplevel)
        self.mainloop_thread.daemon = True
        self.mainloop_thread.start ()
        
        time.sleep (0.5) # let initialization finish
        
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
        
        app.MainLoop ()
    
    # Begin methods intended to be public:
    
    def display_library (self):
        
        self.run_method_in_thread (lambda: self.window.SwitchToScreen (self.libraryscreen))
    
    def add_book_to_library (self, bookname, bookcover):
        
        self.run_method_in_thread (lambda: self.libraryscreen.add_book (bookname, bookcover))
            
