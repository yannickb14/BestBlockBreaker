
from board_visual import *
from board_logic import *

c = make_board()
b = Board(10)




b= tk.button(c, text="click", command=lambda: place(PIECES[0], (4,5)))
b.pack()

place(PIECES[0], (5,5))

