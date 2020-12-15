from dataclasses import dataclass
from typing import List, Tuple
from settings import settings
import numpy as np
from copy import deepcopy
import random

DIRECTIONS = {'u': (0, 1), 'r': (1, 0), 'd': (0, -1), 'l': (-1, 0)}


class GameData:
    def __init__(self):
        self.game_over: bool = False
        self.turn: int = 1
        self.snake_loc: List[Tuple] = [(0, 0)]
        self.snake_dir: str = 'r'
        self.food_loc: Tuple = new_food_loc(self.snake_loc)

    def __repr__(self):
        return str(vars(self))


def new_food_loc(snake_loc):
    while True:
        food_loc = (random.randint(0, settings.grid_size - 1), random.randint(0, settings.grid_size - 1))
        if food_loc not in snake_loc:
            break
    return food_loc


def propagate_game(initial_game_data, action):
    final_game_data = deepcopy(initial_game_data)

    final_game_data.snake_dir = action

    new_x = initial_game_data.snake_loc[0][0] + DIRECTIONS[final_game_data.snake_dir][0]
    new_y = initial_game_data.snake_loc[0][1] + DIRECTIONS[final_game_data.snake_dir][1]
    new_loc = (new_x, new_y)

    # Move snake
    if new_loc == initial_game_data.food_loc:
        final_game_data.snake_loc.insert(0, new_loc)
        if len(final_game_data.snake_loc) == settings.grid_size ** 2:
            final_game_data.game_over = True
        else:
            final_game_data.food_loc = new_food_loc(final_game_data.snake_loc)
    else:
        final_game_data.snake_loc.insert(0, new_loc)
        del final_game_data.snake_loc[-1]

    # Check for death
    if (final_game_data.snake_loc[0] in initial_game_data.snake_loc
            or not 0 <= final_game_data.snake_loc[0][0] < settings.grid_size
            or not 0 <= final_game_data.snake_loc[0][1] < settings.grid_size):
        final_game_data.game_over = True

    final_game_data.turn += 1
    if final_game_data.turn >= 100:
        final_game_data.game_over = True

    return final_game_data


def get_reward(initial_data, final_data):
    if initial_data.food_loc == final_data.snake_loc[0]:
        reward = 10
    elif final_data.game_over is False or final_data.turn == 101 or len(final_data.snake_loc) == settings.grid_size ** 2:
        reward = 0
    else:
        reward = -10
    return reward


@dataclass(frozen=True)
class PureState:
    next_to_wall: Tuple
    food_dir: Tuple
    snake_dir: str

    @classmethod
    def build_from_data(cls, data: GameData):
        wall_left = True if data.snake_loc[0][0] == 0 else False
        wall_right = True if data.snake_loc[0][0] == settings.grid_size - 1 else False
        wall_down = True if data.snake_loc[0][1] == 0 else False
        wall_up = True if data.snake_loc[0][1] == settings.grid_size - 1 else False
        next_to_wall = (wall_up, wall_right, wall_down, wall_left)

        if data.snake_loc[0][0] > data.food_loc[0]:
            food_right = True
        elif data.snake_loc[0][0] < data.food_loc[0]:
            food_right = False
        else:
            food_right = None

        if data.snake_loc[0][1] > data.food_loc[1]:
            food_up = True
        elif data.snake_loc[0][1] < data.food_loc[1]:
            food_up = False
        else:
            food_up = None

        food_dir = (food_right, food_up)

        return cls(next_to_wall, food_dir, data.snake_dir)

    # def __repr__(self):
    #     grid = np.full((settings.grid_size, settings.grid_size), ' ')
    #     head_loc = self.snake_loc[0]
    #     # HEAD_FORMAT = {'u': '↑', 'r': '→', 'd': '↓', 'l': '←'}
    #     grid[settings.grid_size - head_loc[1] - 1, head_loc[0]] = '@' #HEAD_FORMAT[self.snake_dir]
    #     for loc in self.snake_loc[1:]:
    #         grid[settings.grid_size - loc[1] - 1, loc[0]] = 'o'
    #     grid[settings.grid_size - self.food_loc[1] - 1, self.food_loc[0]] = 'x'
    #     return str(grid)


START_Q = 1
ALLOWED_ACTIONS = ['u', 'r', 'd', 'l']
