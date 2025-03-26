
import tkinter as tk
from piece import PIECES






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

        self.board = [[0] * (dim + 3)] * dim

        self.displayed = [False, False, False]
        self.dragging = False
        
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



        c.bind("<Button-1>", self.track_mouse)

        self.c = c

        c.pack()
        root.mainloop()

    def fill(self, t):
    
        x, y = t
        tl_x = self.coord_start + DIFF*x 
        tl_y = self.coord_start + DIFF*y 
    
        br_x = self.coord_start + DIFF*x + DIFF
        br_y = self.coord_start + DIFF*y + DIFF
    
        drawn = self.c.create_rectangle(tl_x, tl_y, br_x, br_y, fill="blue", width=1)

        if y <= self.dim:
            self.board[x][y] = drawn
        

        c.pack()

    def place(self, piece, coord):
        for p in piece:
            self.fill(add_tup(coord, p))
        
        if not any(self.displayed):
            self.generate_pieces() 


    def track_mouse(self, event):
        self.dragging = True
        
        x,y = event.x, event.y
        
        if self.coord_start <= x <= self.coord_start + 150 and self.coord_end <= y <= self.coord_end + 150:
            print("Clicked R1")

        elif self.coord_start + 150 <= x <= self.coord_start + 300 and self.coord_end <= y <= self.coord_end + 150:
            print("Clicked R2")

        elif self.coord_start + 300 <= x <= self.coord_start + 450 and self.coord_end  <= y <= self.coord_end + 150:
            print("Clicked R3")
        
        else:
            print("Clicked nothing relavent")


    def generate_pieces(self):
        if (not any(self.displayed)):
            self.displayed = random.sample(PIECES,3)

            self.place(self.displayed[0], (1, 12))
            self.place(self.displayed[1], (5, 12))
            self.place(self.displayed[2], (7, 12))
        

b=Board(50, 550, 600, 800, 10)


