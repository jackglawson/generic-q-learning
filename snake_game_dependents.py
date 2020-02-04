from dataclasses import dataclass
from typing import List, Tuple
from settings import settings
import numpy as np
from copy import deepcopy

DIRECTIONS = {'u': (0, 1), 'r': (1, 0), 'd': (0, -1), 'l': (-1, 0)}


class GameData:
    def __init__(self):
        self.game_over: bool = False
        self.turn: int = 1
        self.snake_loc: List[Tuple] = [(0, 1), (0, 0)]
        self.snake_dir: str = 'u'

    def __repr__(self):
        return str(vars(self))


def propagate_game(initial_game_data, action):
    final_game_data = deepcopy(initial_game_data)

    final_game_data.snake_dir = action

    new_x = initial_game_data.snake_loc[0][0] + DIRECTIONS[initial_game_data.snake_dir][0]
    new_y = initial_game_data.snake_loc[0][1] + DIRECTIONS[initial_game_data.snake_dir][1]
    new_loc = (new_x, new_y)
    final_game_data.snake_loc.insert(0, new_loc)
    del final_game_data.snake_loc[-1]

    if (final_game_data.snake_loc[0] in initial_game_data.snake_loc
            or not 0 <= final_game_data.snake_loc[0][0] < settings.grid_size
            or not 0 <= final_game_data.snake_loc[0][1] < settings.grid_size):
        final_game_data.game_over = True

    final_game_data.turn += 1
    if final_game_data.turn >= 100:
        final_game_data.game_over = True

    return final_game_data


def get_reward(initial_data, final_data):
    reward = 1 if final_data.game_over is False or final_data.turn == 101 else 0
    return reward


@dataclass(frozen=True)
class PureState:
    snake_loc: Tuple[Tuple]
    snake_dir: str

    @classmethod
    def build_from_data(cls, data: GameData):
        return cls(tuple(data.snake_loc), data.snake_dir)

    def __repr__(self):
        grid = np.full((settings.grid_size, settings.grid_size), ' ')
        head_loc = self.snake_loc[0]
        HEAD_FORMAT = {'u': '↑', 'r': '→', 'd': '↓', 'l': '←'}
        grid[settings.grid_size - head_loc[1] - 1, head_loc[0]] = HEAD_FORMAT[self.snake_dir]
        for loc in self.snake_loc[1:]:
            grid[settings.grid_size - loc[1] - 1, loc[0]] = 'o'
        return str(grid)


START_Q = 1
ALLOWED_ACTIONS = ['u', 'r', 'd', 'l']
