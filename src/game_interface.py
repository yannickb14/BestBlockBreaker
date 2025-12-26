from copy import deepcopy

from game_logic import GameLogic
from game_gui import GameGUI

class GameInterface:
    def __init__(self, game = None, display_message = print):
        self._game = game if game else GameLogic(10, display_message)

    def get_score(self):
        '''
        Getter functon to get the score to ensure nobody can edit the score through the interface
        '''
        return self._game.score

    def get_piece_options(self):
        '''
        returns the options of pieces that can be made
        '''
        return deepcopy(self._game.displayed)

    def get_board_state(self):
        """Read-only view of the board"""
        return deepcopy(self._game.board)

    def submit_move(self, move):
        """The ONLY way to change the real game state"""
        return self._game.execute_move(move) 

    def is_valid_move(self, move):
        return self._game.is_valid_move(move, verbose=False)
            
    def get_sandbox(self):
        """Returns a clone for the AI to mess around with"""
        game = self._game.clone()
        dummy_game = GameInterface(game)
        return dummy_game

    def check_game_over(self):
        if self._game.check_game_over():
            self.game_over_procedure()
            return True

        return False

    def game_over_procedure(self):
        self._game.game_over_procedure()