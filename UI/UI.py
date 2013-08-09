

import wx, wx.lib.scrolledpanel, wx.lib.newevent
import threading


#
# Library Screen
#

COLUMN_WIDTH = 150
ROW_HEIGHT = COLUMN_WIDTH*0.75
CELL_PAD = 5

class BookThumbnail (wx.BitmapButton):
    
    def __init__ (self, parent, enqueue_callback, bookcover):
        
        self.enqueue_callback = enqueue_callback
        
        img = wx.Image (bookcover)
        img.Rescale (COLUMN_WIDTH, ROW_HEIGHT)
        
        super(BookThumbnail, self).__init__(parent, wx.ID_ANY, img.ConvertToBitmap(), size = (COLUMN_WIDTH, ROW_HEIGHT))
        
        self.Bind (wx.EVT_BUTTON, self.onClick, self)
    
    def onClick (self, evt):
        
        self.enqueue_callback ()

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
    
    def add_book (self, enqueue_callback, bookcover):
        
        thumbnail = BookThumbnail (self, enqueue_callback, bookcover)
        self.sizer.Add (thumbnail, 1, wx.FIXED_MINSIZE)
        
        self.setSize()


#
# Book Page Screen
#

ICON_WIDTH = 100
ICON_HEIGHT = 75

class PageButton (wx.BitmapButton):
    
    def __init__ (self, parent, iconpath):
        
        img = wx.Image (iconpath)
        img.Rescale (ICON_WIDTH, ICON_HEIGHT)
        
        super(PageButton, self).__init__(parent, wx.ID_ANY, img.ConvertToBitmap())
        
class BookPageScreen (wx.Panel):
    
    def __init__ (self, parent, quitcallback):
        
        super(BookPageScreen, self).__init__ (parent)
        
        self.parent = parent
        
        self.sizer = wx.BoxSizer (wx.VERTICAL)
        self.SetSizer (self.sizer)
        
        self.onQuit = lambda evt: quitcallback ()
        
        self.topbar_panel = wx.Panel (self)
        self.topbar_sizer = wx.BoxSizer (wx.HORIZONTAL)
        self.topbar_panel.SetSizer (self.topbar_sizer)
        self.page_title = wx.StaticText (self.topbar_panel, wx.ID_ANY, "insert title here, if any")
        self.topbar_sizer.AddStretchSpacer ()
        self.topbar_sizer.Add (self.page_title, proportion = 1, flag = wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        self.quit_button = PageButton (self.topbar_panel, "test_bookquit.png")
        self.quit_button.Bind (wx.EVT_BUTTON, self.onQuit)
        self.topbar_sizer.Add (self.quit_button, proportion = 0, flag = wx.ALIGN_RIGHT)
        self.sizer.Add (self.topbar_panel, proportion = 0, flag = wx.ALIGN_TOP | wx.EXPAND)

        self.main_panel = wx.Panel (self)        
        self.main_sizer = wx.BoxSizer (wx.HORIZONTAL)
        self.main_panel.SetSizer (self.main_sizer)
        self.back_button = PageButton (self.main_panel, "test_bookprev.png")
        self.main_sizer.Add (self.back_button, proportion = 0, flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        self.illustration = wx.StaticBitmap (self.main_panel, wx.ID_ANY)
        self.main_sizer.Add (self.illustration, proportion = 1, flag = wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        self.forward_button = PageButton (self.main_panel, "test_booknext.png")
        self.main_sizer.Add (self.forward_button, proportion = 0, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add (self.main_panel, proportion = 1, flag = wx.EXPAND)
        
        self.text_panel = wx.Panel (self)
        self.text_sizer = wx.BoxSizer (wx.HORIZONTAL)
        self.text_panel.SetSizer (self.text_sizer)
        self.sizer.Add (self.text_panel, proportion = 0, flag = wx.ALIGN_BOTTOM | wx.EXPAND)
        
        self.bottombar_panel = wx.Panel (self)
        self.bottombar_sizer = wx.BoxSizer (wx.HORIZONTAL)
        self.bottombar_panel.SetSizer (self.bottombar_sizer)
        self.speak_button = PageButton (self.bottombar_panel, "test_speakicon.png")
        self.bottombar_sizer.Add (self.speak_button, proportion = 0, flag = wx.ALIGN_LEFT)
        self.sizer.Add (self.bottombar_panel, proportion = 0, flag = wx.ALIGN_BOTTOM | wx.EXPAND)
        
        self.Bind (wx.EVT_SIZE, self.onResize)
        
        self.clear ()
    
    def setBitmap (self):
        
        (w, h) = self.main_sizer.GetSizeTuple ()
        
        img = wx.Image ("test_bookpage.png")
        
        old_w = img.GetWidth ()
        old_h = img.GetHeight ()
        
        new_w = w
        if self.forward_button.IsShown ():
            new_w -= ICON_WIDTH
        if self.back_button.IsShown ():
            new_w -= ICON_WIDTH
        new_h = (new_w*old_h)/old_w
        if new_h > h:
            new_h = h
            new_w = (new_h*old_w)/old_h
        
        img.Rescale (new_w, new_h)
        
        self.illustration.SetBitmap (img.ConvertToBitmap())
        self.Layout ()
    
    def onResize (self, evt):
        
        self.setBitmap ()
        
        evt.Skip ()
    
    
    def Show (self):
        
        self.parent.SetSize ((700, 600))
        
        self.setBitmap()
        
        self.sizer.Layout ()
        
        super(BookPageScreen, self).Show()
    
    def clear (self):
        
        self.text_sizer.Clear (True)
        self.text_sizer.AddStretchSpacer ()
        self.text_sizer.Add (wx.StaticText (self.text_panel, wx.ID_ANY, ""), flag = wx.ALIGN_LEFT)
        
        self.back_button.Hide ()
        self.forward_button.Hide ()
        self.Layout ()
    
    def add_word (self, word_text, word_color):
        
        text = wx.StaticText (self.text_panel, wx.ID_ANY, word_text)
        text.SetForegroundColour (word_color)
        text.SetFont (wx.Font (20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        
        self.text_sizer.Add (text, wx.ALIGN_CENTER_HORIZONTAL | wx.FIXED_MINSIZE)
        
        self.Layout ()
    
    def set_back (self, enqueue_callback):
        
        self.back_button.Bind (wx.EVT_BUTTON, lambda evt: enqueue_callback())
        self.back_button.Show ()
        self.Layout ()
    
    def set_forward (self, enqueue_callback):
        
        self.forward_button.Bind (wx.EVT_BUTTON, lambda evt: enqueue_callback())
        self.forward_button.Show ()
        self.Layout ()
    


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
        
        self.bookpagescreen = BookPageScreen (self.window, self.make_add_callback_callback (self.display_library))
        self.window.AddScreen (self.bookpagescreen)
        
        self.window.Bind (self.EVT_RUN_METHOD, self.onRunMethod)
        self.window.Bind (wx.EVT_CLOSE, self.onClose)
        
        self.init_lock.release ()
        
        app.MainLoop ()
    
    # runs in either thread, makes callbacks which will run in GUI thread
    def make_add_callback_callback (self, callback):
        
        def enqueue_callback ():
            with self.callback_queue_lock:
                self.callback_queue += [callback]
        
        return enqueue_callback
    
    # runs in GUI thread
    def onClose (self, evt):
        
        with self.callback_queue_lock:
            self.callback_queue += [lambda: exit (0)]
    
    # Begin methods intended to be public:
    
    def display_library (self):
        
        self.run_method_in_thread (lambda: self.window.SwitchToScreen (self.libraryscreen))
    
    def add_book_to_library (self, bookcallback, bookcover):
        
        enqueue_callback = self.make_add_callback_callback (bookcallback)
        self.run_method_in_thread (lambda: self.libraryscreen.add_book (enqueue_callback, bookcover))
    
    def clear_bookpage (self):
        
        self.run_method_in_thread (lambda: self.bookpagescreen.clear ())
    
    def add_bookpage_word (self, word_text, word_color):
        
        self.run_method_in_thread (lambda: self.bookpagescreen.add_word (word_text, word_color))
    
    def set_bookpage_next (self, nextpage_callback):
        
        enqueue_callback = self.make_add_callback_callback (nextpage_callback)
        self.run_method_in_thread (lambda: self.bookpagescreen.set_forward (enqueue_callback))
    
    def set_bookpage_prev (self, prevpage_callback):
        
        enqueue_callback = self.make_add_callback_callback (prevpage_callback)
        self.run_method_in_thread (lambda: self.bookpagescreen.set_back (enqueue_callback))
    
    def display_bookpage (self):
        
        self.run_method_in_thread (lambda: self.window.SwitchToScreen (self.bookpagescreen))
    
    def flush_callback_queue (self):
        
        old_callback_queue = None
        with self.callback_queue_lock:
            old_callback_queue = self.callback_queue
            self.callback_queue = []
        
        for old_callback in old_callback_queue:
            old_callback ()
    
