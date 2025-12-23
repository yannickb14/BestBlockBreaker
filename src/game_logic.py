'''
To segregate the logic from the UI
Just the logic of the game, no UI
'''

import random
from collections.abc import Callable


from piece import PIECES
from Move import Move

def add_tup(a, b):
    a1, a2 = a
    b1, b2 = b

    return (a1 + b1, a2 + b2)

class GameLogic:
    def __init__(self, dim: int, display_message: Callable, verbose: bool = True):

        self.verbose = verbose
        if dim != 10:
            if self.verbose:
                print("For now, dimension shall be 10.")
            dim = 10
        self.dim = dim

        self.display_message = display_message
 
        self.score = 0

        self.board = [[0 for _ in range(dim)] for _ in range(dim)]

        #This is for the options of the pieces
        self.displayed = [None, None, None] #the pieces to choose from
        self.piece_options = PIECES
  
        self.generate_pieces()


    def is_valid_move(self, move, verbose):
        '''
        Things to look out for:
        - Overlap with other pieces
        - Inside the board
        '''
        src = move.src
        dest = move.dest

        if not src in range(3):
            if verbose:
                self.display_message(f"Invalid move, src must be between 0 and 2 inclusive, you entered {src}")
            return False

        piece = self.displayed[src]

        if piece is None:
            if verbose:
                self.display_message(f"Invalid move, no piece at position {src}")
            return False

        tiles = self.get_tiles(dest, piece)

        for r, c in tiles:
            if not (0 <= r < self.dim) or not (0 <= c < self.dim):
                if verbose:
                    self.display_message(f"Invalid move, coordinate ({r},{c}) out of range for dimension {self.dim}")
                return False

        for r, c in tiles:
            if self.board[r][c] != 0:
                if verbose:
                    self.display_message("Invalid move, overlap at position ({r},{c})")
                return False

        if verbose:
            self.display_message("Valid move")
        return True
        
        
    def get_tiles(self, dest, piece):
        tiles = [add_tup(dest, p) for p in piece]

        return tiles

    def display_board(self):
        if self.verbose:
            self.display_message(self.board)

    def display_options(self):
        if self.verbose:
            self.display_message(self.displayed)

    def parse_input(self, innput):
        innput = innput.split(',')
        if len(innput) != 3:
            self.display_message("Move must consist of 3 things")
            return None

        try:
            src = int(innput[0])
            dest = int(innput[2]), int(innput[1])
        except ValueError:
            self.display_message("Invalid move, must consist of integers")
            return None

        return Move(src, dest)
        
    
    def get_input(self):
        '''
        The main game loop
        '''
        self.display_message("Enter a move to be executed, q to quit, d to display the board or p to view the piece options: ")
        while True:
            user_in = input("Enter command: ")

            if user_in == 'q':
                self.display_message(f"Thanks for playing! You reached score {self.score}")
                break

            elif user_in == 'd':
                self.display_message("Here is the board:")
                self.display_board()
                continue

            elif user_in == 'p':
                self.display_message("Here are your options:")
                self.display_options()
                continue

            move = self.parse_input(user_in)
            if not move is None:
                self.execute_move(move)

            if self.check_game_over():
                self.game_over_procedure()
                break


    def check_game_over(self):
        """
        Returns whether the game is over
        """
        for piece_idx in range(len(self.displayed)):
            if self.displayed[piece_idx] is None:
                continue
            for i in range(10):
                for j in range(10):
                    move = Move(piece_idx, (i, j))
                    if self.is_valid_move(move, verbose=False):
                        return False
        return True

    def execute_move(self, move):
        '''
        Update board state by executing the move
        Returns whether the move was succesfully executed
        '''
        if not self.is_valid_move(move, self.verbose):
            return False
            

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

        return True

    def game_over_procedure(self):
        '''
        Ends the game
        '''
        self.display_message(f"GAME OVER! You reached score {self.score}!")


    def remove(self, coord, where):
       x, y = coord
       where[x][y] = 0

    def increment_score(self, amt):
        self.score += (amt * self.dim) 

    def need_to_clear(self):
        '''
        Check if any rows or columns need to be cleared
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
    game = GameLogic(10, print)
    game.get_input()


