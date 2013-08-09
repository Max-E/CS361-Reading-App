from UI import UI
import time

display = UI ()

raw_pages = [
    "Hello, this is some test text.".split(),
    "This is some more text.".split(),
    "This is the last page.".split()
]

page_callbacks = []

def make_page_callback (i):
    
    def ret ():
        
        display.clear_bookpage ()
        
        for wordnum in xrange (len (raw_pages[i])):
            color_factor = wordnum*(300/len(raw_pages[i]))
            color = None
            if i == 1:
                color = (255-color_factor, 255-color_factor, color_factor)
            elif i == 2 and wordnum == 2:
                color = (255, 0, 0)
            elif i == 2 and wordnum == 4:
                color = (255, 64, 0)
            display.add_bookpage_word (raw_pages[i][wordnum], color)
            if wordnum+1 != len(raw_pages[i]):
                display.add_bookpage_word (" ", None)
        
        if i == 0:
            display.set_bookpage_prev (display.display_library)
        else:
            display.set_bookpage_prev (page_callbacks[i-1])
        
        if i+1 == len(raw_pages):
            display.set_bookpage_next (display.display_library)
        else:
            display.set_bookpage_next (page_callbacks[i+1])
        
        display.display_bookpage ()
        
    return ret

for i in xrange (len (raw_pages)):
    page_callbacks += [make_page_callback (i)]

for i in xrange (16):
    display.add_book_to_library (page_callbacks[0], "test_bookcover.png")

display.display_library ()

while True:
    display.flush_callback_queue ()
    time.sleep (0.1)
