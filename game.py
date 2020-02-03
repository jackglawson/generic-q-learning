from typing import Tuple, List
import random
from copy import deepcopy
from dataclasses import dataclass
from settings import settings

random.seed(2000)


def propagate_game(initial_game_data, action):
    final_game_data = initial_game_data
    answer = 0 if initial_game_data.turn % 2 == 0 else 1
    if action != answer or initial_game_data.turn > 100:
        final_game_data.game_over = True
    return final_game_data


class GameData:
    def __init__(self):
        self.game_over: bool = False
        self.turn: int = 1

    def __repr__(self):
        return str(vars(self))


class Game:
    def __init__(self, strategy):
        self.strategy = strategy
        self.data: GameData = GameData()
        self.log: List[GameData] = []

    def play(self):
        assert self.data.game_over is False, 'Game is already over!'

        if settings.narrate_game:
            print(self.data)
        self.log.append(deepcopy(self.data))

        while not self.data.game_over:
            action = self.strategy.respond(self.data)
            self.data = propagate_game(self.data, action)
            self.strategy.return_result(self.data)
            self.log.append(deepcopy(self.data))

            if settings.narrate_game:
                print(self.data)

            self.data.turn += 1
