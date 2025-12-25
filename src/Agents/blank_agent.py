'''
**BLANK AGENT DO NOT EDIT blank_agent.py**

Instructions:
 * cp this file your_agent.py
 * open the new file
 * change the name of the agent: @register_agent("your_agent")
 * change the class name: YourAgent(Agent)
 * open src/Agents/__init__.py and add the line:
        * from . import your_agent * 
 * it is now ready to run
'''

import random
from .agent import Agent
from store import register_agent

@register_agent("blank_agent")
class BlankAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self):
        possible_moves = self.get_possible_moves() 
        assert possible_moves, "Game should not prompt for a move if the game is over"    

        if possible_moves:
            return random.choice(possible_moves)
    

        