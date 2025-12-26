import argparse

from game_logic import GameLogic
from game_interface import GameInterface
from game_gui import GameGUI
from store import AGENT_REGISTRY

import Agents

assert AGENT_REGISTRY, "Agent registry is empty"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play the game with an autonomous agent"
    )

    parser.add_argument('--agent', type=str, help="The agent that will play the game", default="random_agent")
    parser.add_argument('--gui', type=bool, help="Enable or disable the GUI", default=False)
    args = parser.parse_args()
    chosen_agent = args.agent
    gui = args.gui
    assert chosen_agent in AGENT_REGISTRY, f"{chosen_agent} is not in AGENT_REGISTRY"
    chosen_agent_callable = AGENT_REGISTRY[chosen_agent]

    #Start a game interface instance. Query chosen_agent for a move. Execute move
    game = GameLogic(10, print) #This game should be shared across game_interface and game_gui
    game_interface = GameInterface(game=game, display_message=game.display_message)
    agent = chosen_agent_callable(game_interface)    

    if gui:
        game_gui = GameGUI(game=game) 
        game_gui.root.after(500, game_gui.successful_move_protocol)

    print(f"Playing the game with {chosen_agent}")
    while not game_interface.check_game_over():
        move = agent.choose_move()
        game_interface.submit_move(move)
        
        if gui:
            game_gui.root.mainloop()

        
        





    


