# coding=utf-8

import unittest
import sys

sys.path.append ("../UI")
import UI
from page import Page
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
        display.run_method_in_thread (display.app.Exit)
        time.sleep (0.1)
        assert not display.gui_thread.is_alive ()
        
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
        display.run_method_in_thread (display.app.Exit)
        time.sleep (0.1)
        assert not display.gui_thread.is_alive ()

class ReadingScreenTestCase (unittest.TestCase):

    
    def testDisplayEmptyBookpage (self):
        display = UI.UI ()
        assert display.gui_thread.is_alive ()

        display.display_bookpage ()
        
        time.sleep (0.1)
        assert display.gui_thread.is_alive ()

        display.run_method_in_thread (display.app.Exit)
        time.sleep (0.1)
        assert not display.gui_thread.is_alive ()

    def testSomethingFail (self):
        display = UI.UI ()
        assert display.gui_thread.is_alive ()

        display.add_bookpage_word ("Word")

        time.sleep (0.1)
        assert display.gui_thread.is_alive ()

    def testMakePage (self):
        display = UI.UI ()
        testpages = ["Testpage1", "Testpage2"]
        
        prevpage_callback = lambda: 4
        nextpage_callback = lambda: 5

        page = Page (display, testpages[0], "test_bookpage.png", prevpage_callback, nextpage_callback)

        assert(page)
        


def suite ():
    suite = unittest.TestSuite ()
    suite.addTest (OpenUITestCase ())
    suite.addTest (LibraryScreenTestCase ())
    suite.addTest (ReadingScreenTestCase ())
    return suite


if __name__ == "__main__":
    unittest.main()

