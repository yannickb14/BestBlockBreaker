import tkinter as tk
from tkinter import font
from collections import defaultdict

from game_logic import GameLogic
from Move import Move

from piece import DEBUG_PIECES


def add_tup(a, b):
    a1, a2 = a
    b1, b2 = b

    return (a1 + b1, a2 + b2)


class Board:
    def __init__(self, coord_start, coord_end, width, height, dim):

        self.game = GameLogic(dim)
        self.game.piece_options = DEBUG_PIECES

        self.coord_start = coord_start 
        self.coord_end = coord_end
        self.diff = (coord_end - coord_start)//dim

        self.board = [[None for _ in range(self.game.dim)] for _ in range(self.game.dim)] #Stores ids of the things drawn
        
        
        self.prev_score_drawn = None

        self.holders = [(1, 11), (4, 11), (7, 11)] # The coordinates for the pieces
        self.piece_options_store = defaultdict(dict) #Where to store the pieces that are displayed so we can hold the reference to be able to delete them
 
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
        

        self.entry = tk.Entry(root)
        self.entry.pack()

        btn = tk.Button(root, text="Submit", command=self.get_input)
        btn.pack()
        self.update_score()
        self.update_displayed()


        c.pack()
        self.root.mainloop()

    def update_score(self):
        pos = (self.coord_start + self.coord_end) / 2

        SCORE_FONT = font.Font(family="Arial", size=22, weight="bold", slant="italic")
        if self.prev_score_drawn:
            self.c.delete(self.prev_score_drawn)

        self.prev_score_drawn = self.c.create_text(pos, 30, 
                           text=self.game.score,
                           fill="blue",
                           font=SCORE_FONT
                           ) 

  
    def flash_message(self, text, color, duration=3000):
        msg = self.c.create_text(
            200, 100,
            text=text,
            fill=color,
        )
        self.root.after(duration, lambda: self.c.delete(msg))

        
        
    def get_tiles(self, dest, piece):
        tiles = [add_tup(dest, p) for p in piece]
        return tiles
    
    def get_input(self):
        move = self.entry.get()

        move = self.game.parse_input(move) 

        success = self.game.execute_move(move)    
        if success:
            self.update_score()
            self.refresh_board()    


    def refresh_board(self):
        for i in range(self.game.dim):
            for j in range(self.game.dim):
                if self.game.board[i][j] and not self.board[i][j]:
                    self.place([(0,0)], (i,j), self.board)
        


    ### I beleive this function will be useful should i add support for playing with the mouse
    #def coords_to_tile(self, coords):
    #    x, y = coords

    #    x -= self.coord_start
    #    y -= self.coord_start

    #    x //= 10
    #    y //= 10       

    #    print(f"Coords to tile got {x}, {y}")

    #    return (x ,y)

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


    def place(self, piece, coord, where):
        #Make the first one gold so we know where its actually being place
        for i, p in enumerate(piece):
            self.fill(add_tup(coord, p), where, color="gold" if i==0 else "blue")

 
    def update_displayed(self):
        for i in range(3):
            self.place(self.game.displayed[i], self.holders[i], where = self.piece_options_store)        

 
if __name__ == "__main__":
    b=Board(50, 550, 600, 800, 10)


