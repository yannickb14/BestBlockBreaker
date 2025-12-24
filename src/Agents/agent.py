import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from Move import Move

DIM = 10

class Agent:
    def __init__(self, game_interface):
        self.game_interface = game_interface

    def get_possible_moves(self):
        possible_moves = []
        for idx, piece in enumerate(self.game_interface.get_piece_options()):
            if not piece is None:
                for i in range(DIM):
                    for j in range(DIM):
                        move = Move(idx, (i, j))
                        if self.game_interface.is_valid_move(move):
                            possible_moves.append(move)

        return possible_moves
             
    def choose_move(self):
        pass

