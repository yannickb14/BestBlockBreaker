import argparse

from GameInterface import GameInterface
from store import AGENT_REGISTRY


print(AGENT_REGISTRY)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play the game with an autonomous agent"
    )

    parser.add_argument('--agent', type=str, help="The agent that will play the game", default="random_agent")
    args = parser.parse_args()
    chosen_agent = args.agent
    assert chosen_agent in AGENT_REGISTRY, f"{chosen_agent} is not in AGENT_REGISTRY"

    #Start a game interface instance. Query chosen_agent for a move. Execute move
    game = GameInterface()
    agent = chosen_agent()    
    move = agent.choose_move()

    while game.submit_move(move):
        move = agent.choose_move()

    


