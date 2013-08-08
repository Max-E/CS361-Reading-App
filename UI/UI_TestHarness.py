from UI import UI
import time

display = UI ()

for i in xrange (16):
    display.add_book_to_library (str(i), "test_bookcover.png")

display.display_library ()

while True:
    time.sleep (1)
