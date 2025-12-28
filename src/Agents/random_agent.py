'''Trial run. This agent will pick a random move'''

import random
from .agent import Agent
from store import register_agent

@register_agent("random_agent")
class RandomAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self):
        possible_moves = self.get_possible_moves() 
        
        if possible_moves:
            return random.choice(possible_moves)
    

        