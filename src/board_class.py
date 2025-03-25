
import tkinter as tk

class Board:
    def __init__(self, coord_start, coord_end, width, height, dim):
        self.coord_start = coord_start
        self.coord_end = coord_end
        self.width = width
        self.height = height
        self.dim = dim
        self.diff = (coord_end - coord_start)//dim

        self.board = [[0] * (dim + 3)] * dim
        self.displated = [False, False, False]
        self.dragging = False
        
        root = tk.Tk()
        c = tk.Canvas(root, width = self.width, height =height, bg = "grey")

        c.create_line(coord_start, coord_end, coord_end, coord_end, fill="black", width=5)
        c.create_line(coord_end, coord_start, coord_end, coord_end, fill="black", width=5)
        c.create_line(coord_end, coord_start, coord_start, coord_start, fill="black", width=5)
        c.create_line(coord_start, coord_end, coord_start, coord_start, fill="black", width=5)
    
        c.create_rectangle(coord_start, coord_end, coord_start + 3*self.diff, coord_end + 3*self.diff, fill="white")
        c.create_rectangle(coord_start + 3*self.diff, coord_end, coord_start + 6*self.diff, coord_end + 3*self.diff, fill="white")
        c.create_rectangle(coord_start + 6*self.diff, coord_end, coord_start + 9*self.diff, coord_end + 3*self.diff, fill="white")

        c.pack()
        root.mainloop()


b=Board(50, 550, 600, 800, 10)


'''
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


'''

