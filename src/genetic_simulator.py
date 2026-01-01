import random
import multiprocessing
from Agents.bitboard import BitboardSimulator 

from piece import PIECES

POPULATUON_SIZE = 1_000_0


# --- CONFIGURATION ---
# Define the shapes (Use the exact same shapes from your GameInterface)
# Format: List of (row, col) tuples

def get_random_hand():
    """Generates 3 random pieces."""
    return [random.choice(PIECES) for _ in range(3)]

def play_single_game(weights):
    """
    Plays one full game using the given weights.
    Returns: Final Score (Int)
    """
    # 1. Initialize Fast Simulator
    sim = BitboardSimulator()
    score = 0
    
    # 2. Game Loop
    game_active = True
    while game_active:
        # Get 3 new pieces
        hand = get_random_hand()
        
        # Play until hand is empty
        while hand:
            best_move_score = -float('inf')
            best_move = None  # Tuple: (piece_index, row, col, piece_mask)
            
            # --- FIND BEST MOVE (Greedy Search) ---
            # Check every piece currently in hand
            can_move = False
            
            for i, shape in enumerate(hand):
                # Convert shape to bitmask (Cache this in a real implementation)
                piece_mask = sim.make_piece_mask(shape)
                
                # Check every valid position on board (0..9, 0..9)
                # Optimization: Limit range based on piece width/height to avoid wrap/bounds
                piece_h = max(r for r, _ in shape) + 1
                piece_w = max(c for _, c in shape) + 1
                
                for r in range(10 - piece_h + 1):
                    for c in range(10 - piece_w + 1):
                        
                        # 1. Check Collision
                        if sim.check_collision(piece_mask, r, c):
                            continue # Occupied
                            
                        can_move = True
                        
                        # 2. Simulate Placement (Lookahead)
                        # Clone board state (Integers copy instantly by value)
                        original_board = sim.board
                        
                        sim.place_piece(piece_mask, r, c)
                        lines = sim.clear_full_lines()
                        
                        # 3. Calculate Heuristics
                        feat_lines = lines
                        feat_holes = sim.count_isolated_holes() / 100.
                        feat_empty = sim.count_empty_cells() / 100.
                        
                        # 4. Dot Product Score
                        move_score = (weights[0] * feat_lines) + \
                                     (weights[1] * feat_holes) + \
                                     (weights[2] * feat_empty)
                                     
                        if move_score > best_move_score:
                            best_move_score = move_score
                            best_move = (i, r, c, piece_mask)
                            
                        # Revert board for next iteration
                        sim.board = original_board

            # --- EXECUTE MOVE ---
            if not can_move:
                game_active = False
                break # GAME OVER
            
            if best_move:
                idx, r, c, mask = best_move
                
                # Execute on real board
                sim.place_piece(mask, r, c)
                cleared = sim.clear_full_lines()
                score += (1 + len(hand[idx])) + (10 * cleared) # Example scoring
                
                # Remove played piece from hand
                del hand[idx]
            else:
                # Should not happen if can_move is True
                game_active = False
                break

    return score

# --- PARALLEL RUNNER ---
if __name__ == "__main__":
    # Example: Evaluation Phase of Genetic Algorithm
    # We have 100 agents, each with different weights
    
    # Generate random population: [lines_w, holes_w, bump_w]
    population = [
        [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1,1)]
        for _ in range(POPULATUON_SIZE)
    ]

    print(f"Starting simulation for {POPULATUON_SIZE} agents...")
    
    # Create a Pool of workers equal to your CPU cores
    with multiprocessing.Pool() as pool:
        # map() distributes the 'population' list across cores
        # each core runs play_single_game(weights)
        scores = pool.map(play_single_game, population)
        
    # Results
    for i, score in enumerate(scores[:10]):
        print(f"Agent {i}: Weights {population[i]} -> Score: {score}")