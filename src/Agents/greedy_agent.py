from .agent import Agent
from store import register_agent


def count_empty_contiguous_block(line):
    cur_dist = 0
    min_dist_to_clear = -1
    for cell in line:
        if not cell: # If empty
            cur_dist += 1
        else: # If filled
            if cur_dist > min_dist_to_clear:
                min_dist_to_clear = cur_dist
            cur_dist = 0

    if cur_dist > min_dist_to_clear:
        min_dist_to_clear = cur_dist

    return min_dist_to_clear



@register_agent("greedy_agent")
class GreedyAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)

    def choose_move(self):
        moves = self.get_possible_moves()
    
        max_diff = -1
        best_move = None
    
        if moves:
            best_move = moves[0]

        for move in moves:

            row_lengths = {}
            col_lengths = {}

            dummy_game = self.game_interface.get_sandbox()

            src = move.src
            dest_x, dest_y = move.dest
            piece = self.game_interface.get_piece_options()[src]

            #Find what rows and columns are being affected by the move
            rows_to_check = {dest_x + x for x, _ in piece}
            cols_to_check = {dest_y + y for _, y in piece}
            
            dummy_board = dummy_game.get_board_state()
            col_indexed_board = list(zip(*dummy_board))
            
            for row in rows_to_check:
                line = dummy_board[row]
                row_lengths[row] = count_empty_contiguous_block(line)

            for col in cols_to_check:
                line = col_indexed_board[col]
                col_lengths[col] = count_empty_contiguous_block(line)

            dummy_game.submit_move(move)
            dummy_board = dummy_game.get_board_state()
            col_indexed_board = list(zip(*dummy_board))

            for row in rows_to_check:
                line = dummy_board[row]
                new_len = count_empty_contiguous_block(line)
                old_len = row_lengths[row]
                
                if new_len > old_len:
                    # We cleared a line! Give this a massive priority score 
                    row_lengths[row] = 100 + new_len
                else:
                    # Standard hole filling
                    row_lengths[row] = old_len - new_len

            for col in cols_to_check:
                line = col_indexed_board[col]
                new_len = count_empty_contiguous_block(line)
                old_len = col_lengths[col] # Fixed Typo: changed [row] to [col]
                
                if new_len > old_len:
                    col_lengths[col] = 100 + new_len
                else:
                    col_lengths[col] = old_len - new_len

            # Check if we found a new best move
            # We use 0 as a default to prevent crashing if the dicts are empty
            best_row_score = max(row_lengths.values()) if row_lengths else -999
            best_col_score = max(col_lengths.values()) if col_lengths else -999
            
            cur_max_diff = max(best_row_score, best_col_score)
            
            if cur_max_diff > max_diff: 
                max_diff = cur_max_diff 
                best_move = move

            return best_move
            
                
        #    for row in rows_to_check:
        #        line = dummy_board[row]
        #        line_diff = row_lengths[row] - count_empty_contiguous_block(line)
        #        if line_diff < 0: #Cleared this line
        #            row_lengths[row] += 100
        #        else:
        #            row_lengths[row] = line_diff

        #    for col in cols_to_check:
        #        line = col_indexed_board[col]
        #        line_diff = col_lengths[col] - count_empty_contiguous_block(line)
        #        if line_diff < 0:
        #            col_lengths[col] += 100
        #        else:
        #            col_lengths[col] = line_diff

        #    cur_max_diff = max(max(row_lengths.values()), max(col_lengths.values()))
        #    if cur_max_diff > max_diff: 
        #        max_diff = cur_max_diff 
        #        best_move = move
        
        #return best_move
            

        

         