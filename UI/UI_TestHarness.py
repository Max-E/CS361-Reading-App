from UI import UI
from page import Page
import time

display = UI ()

illustrations = [
    "test_bookpage1.png",
    "test_bookpage2.png",
    "test_bookpage3.png",
    "test_bookpage4.png"
]

raw_pages = [
    "One fish",
    "two fish",
    "red fish",
    "blue fish",
    "Hello, this is some test text.",
    "This is some more text.",
    "This is some more text.",
    "This is some more text.",
    "This is some more text.",
    "This is the last page."
]



page_callbacks = []

def make_page_callback (i):
    
    def ret ():
        
        prevpage_callback = None
        nextpage_callback = None
        if i != 0:
            prevpage_callback = page_callbacks[i-1]
        if i+1 != len (raw_pages):
            nextpage_callback = page_callbacks[i+1]
        
        illustration_path = "test_bookpage.png"
        if i < len(illustrations):
            illustration_path = illustrations[i]
        
        page = Page (display, raw_pages[i], illustration_path, prevpage_callback, nextpage_callback)
        
        if i != 0:
            page.set_confidences ([1-float(i)/float(len(raw_pages)-1)]*page.numwords)
        
        page.show ()
        
    return ret

for i in xrange (len (raw_pages)):
    page_callbacks += [make_page_callback (i)]

for i in xrange (16):
    display.add_book_to_library (page_callbacks[0], "test_bookcover.png")

display.display_library ()

while True:
    display.flush_callback_queue ()
    time.sleep (0.1)
