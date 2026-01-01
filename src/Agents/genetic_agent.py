
from .agent import Agent
from store import register_agent
from .bitboard import BitboardSimulator, make_piece_mask

@register_agent("genetic_agent")
class GeneticAgent(Agent):
    def __init__(self, game_interface):
        super().__init__(game_interface)
        
        self.weights = [6.737, -0.889, -6.631]

    def choose_move(self):
        moves = self.get_possible_moves()
        if not moves:
            return None

        best_score = -float('inf')
        best_move = moves[0] 

        # 1. Optimization: Convert the slow List-of-Lists to a Fast Integer ONCE.
        current_board_state = self.game_interface.get_board_state()
        base_sim = BitboardSimulator(current_board_state)
        base_board_int = base_sim.board 

        # Cache piece masks so we don't recalculate them for the same piece shape repeatedly
        piece_mask_cache = {}

        for move in moves:
            # 2. Get the piece shape and convert to mask
            piece_idx = move.src
            if piece_idx not in piece_mask_cache: 
                piece_shape = self.game_interface.get_piece_options()[piece_idx]
                piece_mask_cache[piece_idx] = make_piece_mask(piece_shape)
            
            piece_mask = piece_mask_cache[piece_idx]
            
            # 3. Create a fresh simulator for this specific move
            # We initialize it with the integer we calculated earlier (extremely fast)
            sim = BitboardSimulator() 
            sim.board = base_board_int 

            row, col = move.dest 
            sim.place_piece(piece_mask, row, col)

            # 5. Clear Lines 
            lines_cleared = sim.clear_full_lines()

            # 6. Calculate Features (The "Genes")
            # Feature 1: Lines Cleared (We want to maximize this)
            feat_lines = lines_cleared / 6.
            
            # Feature 2: Isolated Holes (We want to minimize this)
            # Normalize: divide by 100 so it's between 0 and 1
            feat_holes = sim.count_isolated_holes() / 100.0 

            feat_empty = sim.count_empty_cells() / 100.
            
            # 7. Calculate Weighted Score (Dot Product)
            # Weights order: [Lines, Holes, Bumpiness]
            # Example weights might be: [5.0, -10.0, -2.0]
            score = (self.weights[0] * feat_lines) + \
                    (self.weights[1] * feat_holes) + \
                    (self.weights[2] * feat_empty)


                

            if score > best_score:
                best_score = score
                best_move = move

        return best_move



        