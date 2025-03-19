

import tkinter as tk
import random
from piece import PIECES
from board_logic import *


WIDTH = 600
HEIGHT = 800
BOARD_START = 50
BOARD_END = 550
DIFF = (BOARD_END - BOARD_START)//10

displayed = []

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

    c.create_rectangle(tl_x, tl_y, br_x, br_y, fill="blue", width=1)
    c.pack()

def place(piece, coord, c):
    for p in piece:
        fill(add_tup(coord, p), c)
    
    if displayed == []:
        c.event_generate("huh")

    return 

def track_mouse(event, c):
    x, y = event.x, event.y

    x1 = 4 * DIFF
    x2 = 6 * DIFF

    y1 = 11 * DIFF
    y2 = 13 * DIFF

    while x1 <= x <= x2 and y1 <= y <= y2:
        place(PIECES[0], (x,y), c)


def generate_pieces(c, ls):
    items = random.sample(PIECES,3)
   
    for p in items:
        ls.append(p)

    place(items[0], (3, 12), c)
    place(items[1], (5, 12), c)
    place(items[2], (7, 12), c)


def make_board():

    global displayed
    b = Board(10)

    displayed += random.sample(PIECES, 3)

    root = tk.Tk()
    
    c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="grey")
    
    c.create_line(BOARD_START, BOARD_END, BOARD_END, BOARD_END, fill="black", width=5)
    c.create_line(BOARD_END, BOARD_START, BOARD_END, BOARD_END, fill="black", width=5)
    c.create_line(BOARD_END, BOARD_START, BOARD_START,BOARD_START, fill="black", width=5)
    c.create_line(BOARD_START, BOARD_END, BOARD_START,BOARD_START, fill="black", width=5)
        
    for x in range(BOARD_START, BOARD_END, DIFF):
        c.create_line(x, BOARD_START, x, BOARD_END, fill="black", width=5)
        c.create_line(BOARD_START, x, BOARD_END, x, fill="black", width=5)

    c.bind("huh", lambda : generate_pieces(c, displayed))
    


    c.pack()
    


    root.mainloop()
    



    return c,b
