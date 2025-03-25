
import tkinter as tk
import random
from piece import PIECES
from board_logic import *


WIDTH = 600
HEIGHT = 800
BOARD_START = 50
BOARD_END = 550
DIFF = (BOARD_END - BOARD_START)//10

BOARD = [[0]*13]*10


displayed = [False, False, False]
dragging = False


def add_tup(a, b):
    a1, a2 = a
    b1, b2 = b
    return (a1 + b1, a2 + b2)

def fill(t, c):

    x, y = t
    tl_x = BOARD_START + DIFF*x 
    tl_y = BOARD_START + DIFF*y 

    br_x = BOARD_START + DIFF*x + DIFF
    br_y = BOARD_START + DIFF*y + DIFF

    BOARD[x][y] = c.create_rectangle(tl_x, tl_y, br_x, br_y, fill="blue", width=1)
    c.pack()


def delete(grids, c):
    for x, y in grids:
        c.delete(BOARD[x][y])

def place(piece, coord, c):
    for p in piece:
        fill(add_tup(coord, p), c)
    
    if displayed == []:
        #TODO
        "Something needs to be done here idk"

        return 


def handle(event, i, c):
    delete(

def drag_piece(event, i, c):
    if dragging:
       x, y = event.x, event.y
       x_grid = x//DIFF - BOARD_START
       y_grid = y//DIFF - BOARD_START
       place(PIECES[i], (x_grid, y_grid), c)
       
       root.after(100, lambda: (delete(PIECES[i]); drag_piece(event, i, c)))
        

def done_dragging(event):
    dragging = False

def track_mouse(event, c = None):
    dragging = True
    
    if BOARD_START <= x <= BOARD_START + 150 and BOARD_END + 10 <= y <= BOARD_END + 150:
        drag_piece(event, 0, c)

    elif BOARD_START + 150 <= x <= BOARD_START + 300 and BOARD_END + 10 <= y <= BOARD_END + 150:
        print("Clicked R2")

    elif BOARD_START + 300 <= x <= BOARD_START + 450 and BOARD_END + 10 <= y <= BOARD_END + 150:
        print("Clicked R3")
    
    else:
        print("Clicked nothing relavent")

def generate_pieces(c, ls):
    if (not any(displayed)):
        print("generate_pieces running")
        items = random.sample(PIECES,3)
   
        for (i,p) in enumerate(items):
            ls[i] = p

        place(items[0], (1, 12), c)
        place(items[1], (5, 12), c)
        place(items[2], (7, 12), c)


def make_board():

    global displayed
    b = Board(10)


    root = tk.Tk()
    
    c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="grey")
    #generate_pieces(c, displayed)
    
    c.create_line(BOARD_START, BOARD_END, BOARD_END, BOARD_END, fill="black", width=5)
    c.create_line(BOARD_END, BOARD_START, BOARD_END, BOARD_END, fill="black", width=5)
    c.create_line(BOARD_END, BOARD_START, BOARD_START,BOARD_START, fill="black", width=5)
    c.create_line(BOARD_START, BOARD_END, BOARD_START,BOARD_START, fill="black", width=5)

    c.create_rectangle(BOARD_START, BOARD_END +10, BOARD_START + 150, BOARD_END + 150, fill="white") 
    c.create_rectangle(BOARD_START + 150, BOARD_END +10, BOARD_START + 300, BOARD_END + 150, fill="white") 
    c.create_rectangle(BOARD_START + 300, BOARD_END +10, BOARD_START + 450, BOARD_END + 150, fill="white") 
        
for x in range(BOARD_START, BOARD_END, DIFF):
        c.create_line(x, BOARD_START, x, BOARD_END, fill="black", width=5)
        c.create_line(BOARD_START, x, BOARD_END, x, fill="black", width=5)


    
    generate_pieces(c, displayed)
    c.bind("<Button-1>", drag_piece)
    c.pack()

    root.mainloop()
    
    return c,b
