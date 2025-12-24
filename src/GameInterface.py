from copy import deepcopy


class GameInterface:
    def __init__(self, logic_instance):
        self._game = logic_instance
        self._score = self._game.score

    def get_score(self):
        '''
        Getter functon to get the score to ensure nobody can edit the score through the interface
        '''
        return self._score

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
        return self._game.is_valid_move(move)
            
    def get_sandbox(self):
        """Returns a clone for the AI to mess around with"""
        return self._game.clone()