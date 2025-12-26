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
    
        # Randomly pick a default move in case no move is found 
        # (prevents crash if all moves result in gaps >= 11)
        if moves:
            best_move = moves[0]

        for move in moves:
            dummy_game = self.game_interface.get_sandbox()
            dummy_game.submit_move(move)
            dummy_board = dummy_game.get_board_state()

            # Helper function to process a single list (row or col)
            def process_line(line):
                nonlocal min_dist_to_clear, best_move
                cur_dist = 0
                for cell in line:
                    if not cell: # If empty
                        cur_dist += 1
                    else: # If filled
                        if cur_dist > 0: 
                            if cur_dist < min_dist_to_clear:
                                min_dist_to_clear = cur_dist
                                best_move = move
                        cur_dist = 0

                # BUG FIX 2: Check again after loop finishes for gaps at the end
                if cur_dist > 0 and cur_dist < min_dist_to_clear:
                    min_dist_to_clear = cur_dist
                    best_move = move

            # Check rows
            for row in dummy_board:
                process_line(row)

            # Check cols
            for col in zip(*dummy_board):
                process_line(col)
        
        print()
        return best_move
            

        

         