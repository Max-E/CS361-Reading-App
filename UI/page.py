import math

def lerp (start, end, dist):
    return start + (end - start) * dist

def get_color_for_confidence (confidence):
    
    if confidence == None:
        return None
    
    color_stages = [
        (255, 0, 0),    # red - 0 confidence
        (255, 255, 0),  # yellow
        (0, 255, 0),    # green - 1 confidence
    ]
    
    color_idx = confidence * (len (color_stages) - 1.0)
    
    if confidence <= 0:
        return color_stages[0]
    
    first_color = color_stages[int (math.floor (color_idx))]
    second_color = color_stages[int (math.ceil (color_idx))]
    dist = color_idx%1.0
    
    return tuple (lerp(first_color[i], second_color[i], dist) for i in xrange (3))

class Page:
    
    def __init__ (self, display, text, illustration_path = "test_bookpage.png", prevpage_callback = None, nextpage_callback = None):
        
        self.display = display
        
        self.words = text.split ()
        self.numwords = len (self.words)
        self.confidences = [None]*self.numwords
        
        self.prevpage_callback, self.nextpage_callback = prevpage_callback, nextpage_callback
        
        self.illustration_path = illustration_path
    
    def show (self):
        
        self.display.clear_bookpage ()
        
        if self.prevpage_callback != None:
            self.display.set_bookpage_prev (self.prevpage_callback)
        
        if self.nextpage_callback != None:
            self.display.set_bookpage_next (self.nextpage_callback)
        
        self.display.set_bookpage_illustration_path (self.illustration_path)
        
        for wordnum in xrange (self.numwords):
            word = self.words[wordnum]
            color = get_color_for_confidence (self.confidences[wordnum])
            self.display.add_bookpage_word (word, color)
            if wordnum+1 != self.numwords:
                self.display.add_bookpage_word (" ", None)
        
        self.display.display_bookpage ()
    
    def set_confidences (self, confidence_list):
        
        assert len (confidence_list) == self.numwords
        self.confidences = confidence_list
    
    def advance (self):
        
        if self.nextpage_callback == None:
            self.display.display_library ()
        else:
            self.nextpage_callback ()
