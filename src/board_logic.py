

class Board:

    def __init__(dim):
        self.dim = dim
        self.slots = ([0]*dim)*dim

    def fill(x, y):
        self.slots[x][y] = 1

