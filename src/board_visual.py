

import tkinter as tk
from peice import PIECES

WIDTH = 600
HEIGHT = 800

BOARD_START = 50
BOARD_END = 550
DIFF = (BOARD_END - BOARD_START)//10

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

    return 


def make_board():
    root = tk.Tk()
    
    c = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="grey")
    
    c.create_line(BOARD_START, BOARD_END, BOARD_END, BOARD_END, fill="black", width=5)
    c.create_line(BOARD_END, BOARD_START, BOARD_END, BOARD_END, fill="black", width=5)
    c.create_line(BOARD_END, BOARD_START, BOARD_START,BOARD_START, fill="black", width=5)
    c.create_line(BOARD_START, BOARD_END, BOARD_START,BOARD_START, fill="black", width=5)
    
    
    for x in range(BOARD_START, BOARD_END, DIFF):
        c.create_line(x, BOARD_START, x, BOARD_END, fill="black", width=5)
        c.create_line(BOARD_START, x, BOARD_END, x, fill="black", width=5)
    
    c.pack()

    b = tk.Button(root, text="place", command=lambda: place(PIECES[0], (4,5), c))
    b.pack()

    root.mainloop()
    return c
