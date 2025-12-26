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
    parser.add_argument('--gui', action="store_true", help="Enable the GUI")
    parser.add_argument('--delay', type=int, help="Amount of time between each autoplayed displayed move", default=2000)

    args = parser.parse_args()
    chosen_agent = args.agent
    gui = args.gui
    delay = args.delay

    assert chosen_agent in AGENT_REGISTRY, f"{chosen_agent} is not in AGENT_REGISTRY"
    chosen_agent_callable = AGENT_REGISTRY[chosen_agent]

    
    game = GameLogic(10, print) #This game should be shared across game_interface and game_gui
    game_interface = GameInterface(game=game, display_message=game.display_message)
    agent = chosen_agent_callable(game_interface)    

    
    print(f"Playing with {chosen_agent}")
    if gui:
        game_gui = GameGUI(game=game)   
        game.display_message = game_gui.flash_message
        game_interface.display_message = game_gui.flash_message
        

        def run_gui_step():
            if game_interface.check_game_over():
                return

            move = agent.choose_move()
            src = move.src
            piece = game.displayed[src]
            
            if game_interface.submit_move(move):
                game_gui.successful_move_protocol(src, piece)

            game_gui.root.after(delay, run_gui_step)
            


        game_gui.root.after(3000, run_gui_step)
        game_gui.root.mainloop()


        
        





    


