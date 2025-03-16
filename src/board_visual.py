

import tkinter as tk


WIDTH = 600
HEIGHT = 800

BOARD_START = 50
BOARD_END = 550
DIFF = (BOARD_END - BOARD_START)//10

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

def fill(x, y):
    tl_x = BOARD_START + DIFF*x - DIFF
    tl_y = BOARD_START + DIFF*y - DIFF

    br_x = BOARD_START + DIFF*x + DIFF
    br_y = BOARD_START + DIFF*y + DIFF

    c.create_rectangle(tl_x, tl_y, br_x, br_y, fill="blue", width=1)
    c.pack()
    
fill(5,4)


root.mainloop()
