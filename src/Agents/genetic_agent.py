
from .agent import Agent
from store import register_agent
from bitboard import BitboardSimulator

@register_agent("genetic_agent")
class GeneticAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self):
        possible_moves = self.get_possible_moves() 
        for move in possible_moves:
            self.game_interface.submit_move(move)
            bitboard = BitboardSimulator(self.game_interface.get_board_state())


        