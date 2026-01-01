import random
import multiprocessing
from Agents.bitboard import BitboardSimulator, make_piece_mask 

from piece import PIECES

OUTPUT_FILE = "genetic_weights.txt"
RANGE_MIN = -10
RANGE_MAX = 10

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
                piece_mask = make_piece_mask(shape)
                
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
                        feat_lines = lines / 6.
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

def mutate(weights, mutation_rate=2, mutation_strength=1.2):
    """
    Randomly changes some weights to explore new strategies.
    Args:
        mutation_rate: Chance a single weight gets changed.
        mutation_strength: How much to change the weight (standard deviation).
    """
    new_weights = []
    for w in weights:
        if random.random() < mutation_rate:
            # Add random noise (Gaussian)
            change = random.gauss(0, mutation_strength)
            new_w = w + change
            
            # Optional: Clamp between -1 and 1 to prevent exploding values
            new_w = max(RANGE_MIN, min(RANGE_MAX, new_w))
            new_weights.append(new_w)
        else:
            new_weights.append(w)
    return new_weights

def crossover(parent1, parent2):
    """
    Mixes two parents to create a child.
    Uses 'Uniform Crossover': each gene is randomly picked from Mom or Dad.
    """
    child = []
    for w1, w2 in zip(parent1, parent2):
        # 50% chance to take from Parent 1, 50% from Parent 2
        if random.random() < 0.5:
            child.append(w1)
        else:
            child.append(w2)
    return child

def breed_next_generation(ranked_results, population_size):
    """
    Creates the next generation based on the best performers of the last one.
    ranked_results: List of (score, weights), sorted by score.
    """
    next_generation = []
    
    # --- 1. ELITISM (Keep the best) ---
    # Keep the top 10% exactly as they are. This guarantees we never get worse.
    elite_count = int(population_size * 0.1)
    elites = [res[1] for res in ranked_results[:elite_count]]
    next_generation.extend(elites)
    
    # --- 2. BREEDING (Fill the rest) ---
    # We only breed from the top 50% of agents (The Survivors)
    survivors_count = int(population_size * 0.5)
    survivors = [res[1] for res in ranked_results[:survivors_count]]
    
    while len(next_generation) < population_size:
        # Pick two random parents from the survivors
        parent1 = random.choice(survivors)
        parent2 = random.choice(survivors)
        
        # Create child
        child = crossover(parent1, parent2)
        
        # Mutate child (crucial for learning!)
        child = mutate(child)
        
        next_generation.append(child)
        
    return next_generation

# --- PARALLEL RUNNER ---

if __name__ == "__main__":
    # --- CONFIGURATION ---
    POPULATION_SIZE = 1000
    GENERATIONS = 500
    
    # Initial Population: Random weights between -1 and 1
    population = [
        [random.uniform(RANGE_MIN, RANGE_MIN) for _ in range(3)] 
        for _ in range(POPULATION_SIZE)
    ]

    print(f"--- Starting Training for {GENERATIONS} Generations ---")

    # Re-use the pool to save overhead (Create it once)
    with multiprocessing.Pool() as pool:
        
        for gen in range(GENERATIONS):
            # 1. Run Simulation (Parallel)
            # scores will be a list of integers: [120, 50, 400, ...]
            scores = pool.map(play_single_game, population)
            
            # 2. Rank Results
            # Create pairs: (Score, Weights)
            results = list(zip(scores, population))
            # Sort descending (Best score first)
            results.sort(key=lambda x: x[0], reverse=True)
            
            # 3. Print Stats
            best_score = results[0][0]
            best_weights = results[0][1]
            avg_score = sum(scores) / len(scores)
            
            print(f"Gen {gen+1}: Best Score = {best_score} | Avg = {avg_score:.1f}")
            print(f"   Best Weights: {['%.3f' % w for w in best_weights]}")
            
            # 4. Save the absolute best weights to a file (checkpoint)
            with open("best_weights.txt", "w") as f:
                f.write(str(best_weights))
            
            # 5. Evolve
            # If it's the last generation, we don't need to breed
            if gen < GENERATIONS - 1:
                population = breed_next_generation(results, POPULATION_SIZE)

    print("\n--- Training Complete ---")
    print(f"Final Best Weights: {best_weights}")


#if __name__ == "__main__":
#    # Example: Evaluation Phase of Genetic Algorithm
#    # We have 100 agents, each with different weights
#     
#    # Generate random population: [lines_w, holes_w, bump_w]
#    population = [
#        [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1,1)]
#        for _ in range(POPULATUON_SIZE)
#    ]
#
#    print(f"Starting simulation for {POPULATUON_SIZE} agents...")
#    
#    # Create a Pool of workers equal to your CPU cores
#    with multiprocessing.Pool() as pool:
#        # map() distributes the 'population' list across cores
#        # each core runs play_single_game(weights)
#        scores = pool.map(play_single_game, population)
#
#    # Results
#    results = list(zip(scores, population))
#
#    # 2. Sort by Score (Descending)
#    # x[0] is the score. reverse=True means biggest first.
#    results.sort(key=lambda x: x[0], reverse=True)
#
#    # 3. Print the Top 10
#    print("\n--- TOP 10 AGENTS ---")
#    for i in range(10):
#        score, weights = results[i]
#        print(f"Rank {i+1}: Score {score} | Weights {weights}")
        

