import tkinter as tk
import random
from collections import defaultdict
from tkinter import font

from piece import PIECES, DEBUG_PIECES
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
        
        self.score = 0
        self.prev_score_drawn = None


        self.board = [[0 for _ in range(dim)] for _ in range(dim)]

        #This is for the options of the pieces
        self.displayed = [None, None, None] #the pieces to choose from
        self.holders = [(1, 11), (4, 11), (7, 11)] # The coordinates for the pieces
        #Where to store the pieces that are displayed so we can hold the reference to be
        #able to delete them
        self.piece_options_store = defaultdict(dict)
 
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
        self.update_score()


        c.pack()
        self.root.mainloop()

    def update_score(self):
        pos = (self.coord_start + self.coord_end) / 2

        if self.prev_score_drawn:
            self.c.delete(self.prev_score_drawn)

        my_font = font.Font(family="Arial", size=22, weight="bold", slant="italic")
        self.prev_score_drawn = self.c.create_text(pos, 30, 
                           text=self.score,
                           fill="blue",
                           font=my_font
                           ) 

  
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
            dest = (int(move[2]), int(move[1]))
        except TypeError:
            print(dest)

        move = Move(src, dest)

        self.execute_move(move)

        
    

    def execute_move(self, move):
        if not self.is_valid_move(move):
            return

        src = move.src
        dest = move.dest
        
        piece = self.displayed[src]

        self.place(piece, dest, where = self.board)
        self.score += len(piece)

        self.displayed[src] = None
        for p in piece:
            self.remove(add_tup(self.holders[src], p), self.piece_options_store)

        if not any(self.displayed):
            self.generate_pieces()

        rows_to_clear, cols_to_clear = self.need_to_clear()

        if rows_to_clear or cols_to_clear:
            print("To clear")
        else:
            print("Not to clear")
        
        for row in rows_to_clear:
            for i in range(self.dim):
                self.remove((row, i), self.board) 

        for col in cols_to_clear:
            for i in range(self.dim):
                self.remove((i, col), self.board)

        self.update_score()

 
    def coords_to_tile(self, coords):
        x, y = coords

        x -= self.coord_start
        y -= self.coord_start

        x //= 10
        y //= 10       

        print(f"Coords to tile got {x}, {y}")

        return (x ,y)

    def fill(self, t, where, color="blue"):
        x, y = t
        tl_x = self.coord_start + self.diff*x 
        tl_y = self.coord_start + self.diff*y 
    
        br_x = self.coord_start + self.diff*x + self.diff
        br_y = self.coord_start + self.diff*y + self.diff 
    
        drawn = self.c.create_rectangle(tl_x, tl_y, br_x, br_y, fill=color, width=1)
       
        try:
            where[x][y] = drawn
        except IndexError as e:
            print(f'Problem indices are ({x}, {y}) in {where}')
            raise e
        
        self.c.pack()

    def remove(self, coord, where):
       x, y = coord
       self.c.delete(where[x][y])
       where[x][y] = 0

    def increment_score(self, amt):
        self.score += (amt * self.dim) 

    def need_to_clear(self):
        '''
        Check if any of the inputted rows or columns need to be cleared
        '''
        rows_to_clear = []
        cols_to_clear = []
        for i, row in enumerate(self.board):
            if all(row):
                rows_to_clear.append(i)

        for c in range(self.dim):
            all_1s = True
            for row in self.board:
                if row[c] == 0:
                    all_1s = False
                    break

            if all_1s:
                cols_to_clear.append(c)

        self.increment_score(len(rows_to_clear) + len(cols_to_clear))
        return rows_to_clear, cols_to_clear

    def place(self, piece, coord, where):
        #Make the first one gold so we know where its actually being place
        for i, p in enumerate(piece):
            self.fill(add_tup(coord, p), where, color="gold" if i==0 else "blue")
 
    def generate_pieces(self):
        self.displayed = random.sample(DEBUG_PIECES, 3)

        for i in range(3):
            self.place(self.displayed[i], self.holders[i], where = self.piece_options_store)        


    
if __name__ == "__main__":
    b=Board(50, 550, 600, 800, 10)


