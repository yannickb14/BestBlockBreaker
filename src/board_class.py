

import tkinter as tk
import random
from piece import PIECES
from holder import Holder

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



        #c.bind("<Button-1>", self.track_mouse)
        #c.bind("<ButtonRelease-1>", self.track_mouse)

        c.bind("<ButtonRelease-1>", self.place_piece)

        self.c = c
        
        self.generate_pieces()


        c.pack()
        root.mainloop()

  
            

    def place_piece(self, event):
        x, y = event.x, event.y
        if self.dragging:
            x_tile, y_tile = self.coords_to_tile((x, y))
            self.place(self.displayed[0], (x_tile, y_tile)) 
            


            self.dragging = False

        else:
            #Start dragging
            self.dragging = True


    def coords_to_tile(self, coords):
        x, y = coords

        x -= self.coord_start
        y -= self.coord_start
        
        x //= self.dim * 10 
        y //= self.dim * 10

        return (x,y)

    def fill(self, t):
    
        x, y = t
        tl_x = self.coord_start + self.diff*x 
        tl_y = self.coord_start + self.diff*y 
    
        br_x = self.coord_start + self.diff*x + self.diff
        br_y = self.coord_start + self.diff*y + self.diff
    
        drawn = self.c.create_rectangle(tl_x, tl_y, br_x, br_y, fill="blue", width=1)
       
#        if y <= self.dim:            
        print(x,y)
        self.board[x][y] = drawn
        self.c.pack()

    def remove(self, coord):
       x,y = coord
       self.c.delete(self.board[x][y])
       self.board[x][y] = 0


    def place(self, piece, coord):
        for p in piece:
            self.fill(add_tup(coord, p))

        if not any(self.displayed):
            self.generate_pieces() 

        
    def drag(self, piece, event):
        x,y = event.x, event.y
        x,y = self.coords_to_tile((x,y))

        #slot_x = x - self.coord_start
        #slot_y = y - self.coord_start

        self.place(piece, (x, y))
        self.c.after(100, self.track_mouse_cont)
        

    def track_mouse(self, event): 
        if self.dragging:

            #Place the piece
            self.dragging = False

        else:
            #Start dragging


            self.dragging = False

            self.track_mouse_cont(event) 
        
    def track_mouse_cont(self, event): 
        x,y = event.x, event.y
                
        if self.coord_start <= x <= self.coord_start + 150 and self.coord_end <= y <= self.coord_end + 150:
            self.drag(self.displayed[0], event)

        elif self.coord_start + 150 <= x <= self.coord_start + 300 and self.coord_end <= y <= self.coord_end + 150:
            print("Clicked R2")

        elif self.coord_start + 300 <= x <= self.coord_start + 450 and self.coord_end  <= y <= self.coord_end + 150:
            print("Clicked R3")
        
        else:
            print("Clicked nothing relavent")



    def generate_pieces(self):
        self.displayed = random.sample(PIECES,3)
        self.place(self.displayed[0], (1, 12))
        self.place(self.displayed[1], (5, 12))
        self.place(self.displayed[2], (7, 12))
        

b=Board(50, 550, 600, 800, 10)


