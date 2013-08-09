# coding=utf-8

import unittest
import sys

sys.path.append ("../UI")
import UI
import time


# Things to test:
#   Creating a window
#
#
#
#
#   Closing the window

class OpenUITestCase (unittest.TestCase):
    def runTest (self):
        display = UI.UI ()
        assert display.gui_thread.is_alive ()

# Create Display Object
# Add Books
# Display Library

# Create Display Object
# Display Library
# Add Books

class LibraryScreenTestCase (unittest.TestCase):
    def _ABADL_Book (self, id, display):
        callback = lambda: -1
        
        display.add_book_to_library (callback, "res/test_bookcover.png")
        
        time.sleep (0.1)
        
        children = display.libraryscreen.sizer.GetChildren ()
        
        assert (len (children) == id + 1)
        
        children[id].Window.enqueue_callback ()
        with display.callback_queue_lock:
            assert (callback in display.callback_queue)
        
        assert (children[id].Window.IsShown ())
    
    def testAddBooksAndDisplayLibrary (self):
        display = UI.UI ()
        
        self._ABADL_Book (0, display)
        
        assert (not display.libraryscreen.IsShown ())
        display.display_library ()
        time.sleep (0.1)
        assert (display.libraryscreen.IsShown ())
        
        self._ABADL_Book(1, display)
        
        assert display.gui_thread.is_alive ()


if __name__ == "__main__":
    unittest.main()

