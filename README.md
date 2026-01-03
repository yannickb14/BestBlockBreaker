# 1010! Game Clone & Evolutionary AI Framework

A high-performance Python simulation of the logic-based puzzle game *1010!*, designed as a testbed for developing and training autonomous Artificial Intelligence agents.

Unlike standard clones, this project decouples the game logic from the visualization to support **headless training**, **multiprocessing**, and **evolutionary learning** strategies.

---

## 🎮 Project Overview
This project replicates the mechanics of the *1010!* mobile game (by Gram Games Limited), where players place polyomino shapes onto a 10x10 grid to clear lines.

The core goal of this repository was not just to recreate the game, but to engineer an **Evolutionary AI** capable of surpassing human-level "greedy" heuristics through genetic optimization and lookahead search strategies.

---

## 🚀 Key Features

### Core Engine
* **Decoupled Architecture:** Strict separation of concerns between the Game State (Model) and the Tkinter GUI (View). This allows the AI to train in "headless" mode (no graphics) at maximum speed.
* **Deterministic Logic:** Fully deterministic collision detection and line-clearing algorithms, validated by a comprehensive `unittest` suite.
* **Plug-and-Play AI:** An abstract `Agent` interface using the **Strategy Pattern**, allowing easy hot-swapping between Human, Random, Greedy, and Genetic agents.

### AI & Performance Optimization
* **Bitboard Optimization:** The Genetic Agent uses **100-bit integers** (bitboards) instead of 2D arrays to represent the grid. This reduces collision checks and pattern matching to **O(1)** bitwise operations.
* **Evolutionary Learning:** A Genetic Algorithm (GA) that autonomously tunes heuristic weights (e.g., *Bumpiness*, *Holes*, *Aggregate Height*) over generations using Elitism and Mutation.
* **Multiprocessing:** Training is parallelized across CPU cores to evaluate population fitness rapidly.
* **Survival Lookahead:** Features a "Survival Gene" and a 3-step permutation search to break the "Greedy Limit" (approx. 800 points), enabling the bot to plan ahead for large pieces.

---

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Visualization:** Tkinter (Standard Library)
* **Performance:** `multiprocessing`, Bitwise Operations
* **Testing:** `unittest` module

---
## 🤖 Creating & Running Agents

You can create custom AI agents and plug them directly into the simulation.

### 1. Create the Agent File

Duplicate the template file to create your new agent:

    cp Agents/blank_agent.py Agents/my_custom_agent.py

### 2. Register the Agent

Open your new file (`Agents/my_custom_agent.py`) and add the registration decorator above your class definition.  
This allows the system to find your agent by name.

    from . import register_agent

    @register_agent("my_agent")  # <--- This is the name you will use in the command line
    class MyCustomAgent(Agent):
        def get_move(self, board, pieces):
            # Your logic here
            pass

### 3. Expose the Agent

Open `Agents/__init__.py` and import your new file so the registry can load it:

    # Agents/__init__.py
    from . import blank_agent
    from . import my_custom_agent  # <--- Add this line

### 4. Run the Simulation

Run the game with your agent using `run.py`.

**With Visuals (GUI Mode):**  
Use this to watch the agent play in real-time.

    python3.10 run.py --agent my_agent --gui

**Headless Mode (Fast):**  
Use this for rapid testing or training without the window overhead.

    python3.10 run.py --agent my_agent

## 🧠 AI Implementation Details

The AI moves beyond simple greedy strategies by utilizing a weighted heuristic function:

$$
Score = (w_1 \cdot Lines) + (w_2 \cdot Holes) + (w_3 \cdot Bumpiness) + (w_4 \cdot Survival)
$$

**Initial Approach (Greedy):**  
The agent simply picked the move that cleared the most lines immediately.  
This typically failed around 800 points due to lack of foresight.

**Evolutionary Approach:**  
By simulating thousands of games and "breeding" the best performing weight sets, the agent learned to prioritize flat board states and avoid creating wells (deep holes).

**Optimization:**  
Converting the board state to a 100-bit integer allowed the simulation to run thousands of moves per second, making the training of large populations feasible on consumer hardware (e.g., Apple Silicon).

## 📜 Future Improvements

- **Deep Reinforcement Learning (DQN):**  
  Implementing a neural network approach to compare against the Genetic Algorithm.

- **C++ Extension:**  
  Rewriting the core bitboard logic in C++ for even faster training throughput.





