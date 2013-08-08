from UI import UI
import time

display = UI ()

def printer (x):
    print x

for i in xrange (16):
    display.add_book_to_library (lambda: printer ("clicked book "+str(i)), "test_bookcover.png")

display.display_library ()

while True:
    display.flush_callback_queue ()
    time.sleep (0.1)
