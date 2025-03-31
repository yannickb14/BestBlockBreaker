

class Holder:
    def __init__(self, pid):
        self.containment = [[False]*3]*3
        self.pid = 0


    def fill(self, slot, thing):
        x,y = slot
        self.containment[x][y] = thing
        

         
