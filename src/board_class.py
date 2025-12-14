import tkinter as tk
import random
from piece import PIECES

import numpy as np

from Move import Move


def add_tup(a, b):
    a1, a2 = a
    b1, b2 = b

    return (a1 + b1, a2 + b2)


class Board:
    def __init__(self, coord_start, coord_end, width, height, dim):
        
        self.coord_start = coord_start 
        self.coord_end = coord_end
        self.dim = dim
        self.diff = (coord_end - coord_start)//dim


        self.board = [[0 for _ in range(dim + 3)] for _ in range(dim)]
        #self.board = np.zeros((self.dim + 3, self.dim))

        #This is for the options of the pieces
        self.displayed = [None, None, None] #the pieces to choose from
        self.holders = [(1, 11), (4, 11), (7, 11)] # The coordinates for the pieces

        

        #self.dragging = False
        
        root = tk.Tk()
        c = tk.Canvas(root, width=width, height=height, bg = "grey")

        c.create_line(coord_start, coord_end, coord_end, coord_end, fill="black", width=5)
        c.create_line(coord_end, coord_start, coord_end, coord_end, fill="black", width=5)
        c.create_line(coord_end, coord_start, coord_start, coord_start, fill="black", width=5)
        c.create_line(coord_start, coord_end, coord_start, coord_start, fill="black", width=5)


        c.create_rectangle(coord_start, coord_end, coord_start + 3*self.diff, coord_end + 3*self.diff, fill="white")
        c.create_rectangle(coord_start + 3*self.diff, coord_end, coord_start + 6*self.diff, coord_end + 3*self.diff, fill="white")
        c.create_rectangle(coord_start + 6*self.diff, coord_end, coord_start + 9*self.diff, coord_end + 3*self.diff, fill="white")
        

        for x in range(coord_start, coord_end, self.diff):
            c.create_line(x, coord_start, x, coord_end, fill="black", width=5)
            c.create_line(coord_start, x, coord_end, x, fill="black", width=5)

        self.c = c
        self.root = root
        
        self.generate_pieces()

        self.entry = tk.Entry(root)
        self.entry.pack()

        btn = tk.Button(root, text="Submit", command=self.get_input)
        btn.pack()


        c.pack()
        self.root.mainloop()

  
    def flash_message(self, text, color, duration=3000):
        msg = self.c.create_text(
            200, 100,
            text=text,
            fill=color,
        )
        self.root.after(duration, lambda: self.c.delete(msg))

    def is_valid_move(self, move):
        '''
        Things to look out for:
        - Overlap with other pieces
        - Inside the board
        '''
        src = move.src
        dest = move.dest

        piece = self.displayed[src]

        if piece is None:
            self.flash_message(f"There is no piece available at {src}", "red")
            return False

        tiles = self.get_tiles(dest, piece)

        for r, c in tiles:
            if not (0 <= r <= 9) or not (0 <= c <= 9):
                self.flash_message(f"Move out of range, {r,c} not in board", "red")
                return False

        for r, c in tiles:
            if self.board[r][c] != 0:
                self.flash_message(f"Move overlaps at position {r,c}", "red")
                return False

        self.flash_message("Move is valid", color="green")
        return True
        
        
    def get_tiles(self, dest, piece):
        tiles = [add_tup(dest, p) for p in piece]

        return tiles

    def invalid_move(self):
        raise Exception
    
    def get_input(self):
        move = self.entry.get()
        move = move.split(',')

        if len(move) != 3:
            print("Length invalid")

        src = move[0]
        

        try:
            src = int(src)
        except TypeError:
            print(src)
        try:
            dest = int(move[1]), int(move[2])
        except TypeError:
            print(dest)

        move = Move(src, dest)

        self.place_piece(move)

        
    

    def place_piece(self, move):
        
        if not self.is_valid_move(move):
            print("Move is invalid")
            return


        src = move.src
        dest = move.dest
        

        piece = self.displayed[src]


        self.place(piece, dest)

        self.displayed[src] = None
        for p in piece:
            self.remove(add_tup(self.holders[src], p))

        if not any(self.displayed):
            self.generate_pieces()
        
    def coords_to_tile(self, coords):
        x, y = coords

        x -= self.coord_start
        y -= self.coord_start

        x //= 10
        y //= 10       

        print(f"Coords to tile got {x}, {y}")

        return (x ,y)

    def fill(self, t, color="blue"):
    
        x, y = t
        tl_x = self.coord_start + self.diff*x 
        tl_y = self.coord_start + self.diff*y 
    
        br_x = self.coord_start + self.diff*x + self.diff
        br_y = self.coord_start + self.diff*y + self.diff 
    
        drawn = self.c.create_rectangle(tl_x, tl_y, br_x, br_y, fill=color, width=1)
       
        self.board[x][y] = drawn
        self.c.pack()

    def remove(self, coord):
       x, y = coord
       self.c.delete(self.board[x][y])
       self.board[x][y] = 0


    def place(self, piece, coord):
        #Make the first one gold so we know where its actually being place
        for i, p in enumerate(piece):
            self.fill(add_tup(coord, p), color="gold" if i==0 else "blue")

        if not any(self.displayed):
            self.generate_pieces() 

    
    def generate_pieces(self):
        self.displayed = random.sample(PIECES,3)
        print(self.displayed)
        self.place(self.displayed[0], self.holders[0])
        self.place(self.displayed[1], self.holders[1])
        self.place(self.displayed[2], self.holders[2])
        

if __name__ == "__main__":
    b=Board(50, 550, 600, 800, 10)


