

class Board:

    def __init__(self, dim):
        self.dim = dim
        self.slots = ([0]*dim)*dim

    def fill(x, y):
        self.slots[x][y] = 1

