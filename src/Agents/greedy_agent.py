from .agent import Agent
from store import register_agent


@register_agent("greedy_agent")
class GreedyAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self):
        moves = self.get_possible_moves()
        
        min_dist_to_clear = 11
        best_move = None
        for move in moves:
            dummy_game = self.game_interface.get_sandbox()
            dummy_game.submit_move(move)

            dummy_board = dummy_game.get_board_state()
            #To find the longest contiguous block of unfilled cells 
            #in the row in one pass of the row
            for row in dummy_board:
                cur_dist_to_clear = 0
                for cell in row:
                    if not cell:
                        cur_dist_to_clear += 1
                    else: #If a cell is filled, check if this contiguous block is smaller then the min found thus far set the cur distance to 0
                        if cur_dist_to_clear < min_dist_to_clear:
                            min_dist_to_clear = cur_dist_to_clear
                            best_move = move
                        cur_dist_to_clear = 0 

            for col in zip(*dummy_board): #zip(*... to get the columns
                cur_dist_to_clear = 0
                for cell in col:
                    if not cell:
                        cur_dist_to_clear += 1
                    else: #If a cell is filled, check if this contiguous block is smaller then the min found thus far set the cur distance to 0
                        if cur_dist_to_clear < min_dist_to_clear:
                            min_dist_to_clear = cur_dist_to_clear
                            best_move = move
                        cur_dist_to_clear = 0 


        assert best_move, "No best move found"        
        return best_move
            

        

         