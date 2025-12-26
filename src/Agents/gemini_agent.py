'''
Made a agent with gemini just to make sure the API and my code works
THis agent really sucks!
'''



from .agent import Agent
from store import register_agent

@register_agent("gemini_agent")
class GeminiAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self):
        possible_moves = self.get_possible_moves() 
        assert possible_moves, "Game should not prompt for a move if the game is over"    

        #GEMINI AI CODE BELOW:
        best_move = None
        max_score = -1

        # Loop through every pre-validated move from the superclass
        for move in possible_moves:
            # 1. Get a fresh Sandbox (clone of the current game state)
            #
            sandbox = self.game_interface.get_sandbox()

            # 2. Simulate the move in the sandbox
            # The sandbox is a raw GameLogic object, so we call execute_move directly
            sandbox.execute_move(move)

            # 3. Compare the resulting score
            # We look for the move that leaves us with the highest TOTAL score
            if sandbox.score > max_score:
                max_score = sandbox.score
                best_move = move

        return best_move


    

        