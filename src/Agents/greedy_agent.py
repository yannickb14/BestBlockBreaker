from .agent import Agent
from store import register_agent

from ..Move import Move

@register_agent("blank_agent")
class BlankAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self) -> Move:
        moves = self.get_possible_moves()
        pieces = self.game_interface.get_piece_options()
        
         