from dataclasses import dataclass


class GameData:
    def __init__(self):
        self.game_over: bool = False
        self.turn: int = 1
        self.turns_since_first_1 = None

    def __repr__(self):
        return str(vars(self))


def propagate_game(initial_game_data, action):
    final_game_data = initial_game_data

    if initial_game_data.turns_since_first_1 is not None:
        final_game_data.turns_since_first_1 += 1
    elif action == 1:
        final_game_data.turns_since_first_1 = 0

    if (initial_game_data.turns_since_first_1 is not None and initial_game_data.turns_since_first_1 >= 5)\
            or initial_game_data.turn >= 100:
        final_game_data.game_over = True

    final_game_data.turn += 1

    return final_game_data


def get_reward(initial_data, final_data):
    reward = 1 if final_data.game_over is False or final_data.turn == 101 else 0
    return reward


@dataclass(frozen=True)
class PureState:
    turns_since_first_1: int

    @classmethod
    def build_from_data(cls, data: GameData):
        return cls(data.turns_since_first_1)


START_Q = 0.5
ALLOWED_ACTIONS = [0, 1]
