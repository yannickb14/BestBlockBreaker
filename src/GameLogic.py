'''
To segregate the logic from the UI
Just the logic of the game, no UI
'''



import random
from collections import defaultdict
from tkinter import font

from piece import PIECES, DEBUG_PIECES
from Move import Move

def add_tup(a, b):
    a1, a2 = a
    b1, b2 = b

    return (a1 + b1, a2 + b2)

class GameLogic:
    def __init__(self, dim):

        if dim != 10:
            print("For now, dimension shall be 10.")
            dim = 10
        self.dim = dim
        
        self.score = 0

        self.board = [[0 for _ in range(dim)] for _ in range(dim)]

        #This is for the options of the pieces
        self.displayed = [None, None, None] #the pieces to choose from
        self.piece_options = PIECES
  
        self.generate_pieces()


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
            print(f"Invalid move, no piece at position {src}")
            return False

        tiles = self.get_tiles(dest, piece)

        for r, c in tiles:
            if not (0 <= r < self.dim) or not (0 <= c < self.dim):
                print("Invalid move, coordinate ({r},{c} out of range for dimension {self.dim})")
                return False

        for r, c in tiles:
            if self.board[r][c] != 0:
                print("Invalid move, overlap at position ({r},{c})")
                return False

        print("Valid move")
        return True
        
        
    def get_tiles(self, dest, piece):
        tiles = [add_tup(dest, p) for p in piece]

        return tiles

    def display_board(self):
        print(self.board)

    def display_options(self):
        print(self.displayed)
    
    def get_input(self):
        '''
        The main game loop
        '''
        print("Enter a move to be executed, q to quit, d to display the board or p to view the piece options: ")
        while True:
            user_in = input("Enter command: ")

            if user_in == 'q':
                print(f"Thanks for playing! You reached score {self.score}")
                break

            elif user_in == 'd':
                print("Here is the board:")
                self.display_board()
                continue

            elif user_in == 'p':
                print("Here are your options:")
                self.display_options
                continue

            user_in = user_in.split(',')
        
            if len(user_in) != 3:
                print("Invalid move, moves should have length 3")
                continue

            src = user_in[0]
            dest = (user_in[2], user_in[1])
        
            try:
                src = int(src)
            except TypeError:
                print(f'Invalid move, {src} is not a valid piece option')
                continue
            try:
                dest = (int(dest[0]), int(dest[1]))
            except TypeError:
                print(f"Invalid move, {dest} is not a valid coordinate to place")
                continue

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

        if not any(self.displayed):
            self.generate_pieces()

        rows_to_clear, cols_to_clear = self.need_to_clear()
 
        for row in rows_to_clear:
            for i in range(self.dim):
                self.remove((row, i), self.board) 

        for col in cols_to_clear:
            for i in range(self.dim):
                self.remove((i, col), self.board)



    def remove(self, coord, where):
       x, y = coord
       where[x][y] = 0

    def increment_score(self, amt):
        self.score += (amt * self.dim) 

    def need_to_clear(self):
        '''
        Check if any of the inputted rows or columns need to be cleared
        and increment score (for now)
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
        
        for c in piece:
            r, c = add_tup(coord, c)
            where[r][c] = 1
  
    def generate_pieces(self):
        self.displayed = random.sample(self.piece_options, 3)

 
if __name__ == "__main__":
    game = GameLogic(10)
    game.get_input()


