***1010!* Game Clone (Python/Tkinter)**
---
Find the original game [here](https://apps.apple.com/us/app/1010-block-puzzle-game/id911793120)

A logic-based puzzle game developed in Python using the Tkinter library. This project is a working clone of the popular *1010!* mobile game, focusing on grid-based spatial reasoning and efficient state management.
while still rough around the edges, the game does work!
___
**Instructions to Play**

Run the file *board_class.py* and the game will open right up!

For now, the moves are commands you put on the text box at the bottom. A move consisits of 3 comma seperated values like so: 

PIECE,ROW,COL
It is 0-indexed. If you wanted to actually play the game, I recommend playing the iOS version as mine is stil **VERY** rough around the edges and barely tested.
___
**🎮 Project Overview**
*1010!* is a mobile game by *Gram Games Limited* in which players are tasked with placing various polyomino shapes onto a 10x10 grid. Unlike Tetris, blocks do not fall; the player must strategically place them to complete full rows or columns, which then clear to make space for more pieces.

Current Features
* Grid Logic: A robust 10x10 coordinate system that tracks occupied and empty cells.

* Piece Generation: Random generation of unique shapes that fit in a 3x3 space (single blocks, lines and L-shapes).

* Collision Detection: Ensures pieces can only be placed in valid, unoccupied spaces.

* Line Clearing: Automated detection and removal of completed horizontal and vertical lines.
___
**🛠 Tech Stack**

* Language: Python 3.9

* GUI: Tkinter

Logic: Custom coordinate-mapping and collision algorithms.
___
**🤖 Future Roadmap: AI Integration**

The primary objective of this project—beyond the game itself is to create a testing environment for Artificial Intelligence.

Once the game mechanics are fully polished, I plan to develop an AI Agent (or maybe a few) capable of playing the game autonomously. This will involve:

* State Evaluation: Teaching the agent to value board "emptiness" and penalize "islands" (trapped empty squares).

* Heuristic Search: Implementing algorithms to calculate the optimal placement of the three available pieces to maximize the score and longevity of the game.

* Reinforcement Learning: Exploring how a model can learn the best strategies through thousands of iterations of trial and error.
___
**📈 Learning Objectives**
* GUI State Persistence: Managing real-time updates to a complex grid UI in Tkinter.

* Algorithm Design: Optimizing the check for "Game Over" states (verifying if any of the three current pieces can fit anywhere on the remaining board).

* Scalability: Structuring the code so the game engine can be easily hooked into an AI script without a complete rewrite.
