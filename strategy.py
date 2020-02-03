from dataclasses import dataclass
from typing import List, Tuple
import random
import matplotlib.pyplot as plt
import numpy as np
from settings import learning_params
from game import GameData
from utils import get_prob_q2_greater_than_q1

START_Q = 0.5
ALLOWED_ACTIONS = [0, 1]


def get_reward(initial_data, final_data):
    reward = 1 if final_data.game_over is False else 0
    return reward


class Strategy:
    def __init__(self, learning):
        self.learning = learning

        self.states = {}
        self.last_state = None
        self.last_action = None
        self.last_data = None
        #self.just_applied: bool = False

    def respond(self, game_data):
        pure_state = PureState.build_from_data(game_data)
        if pure_state in list(self.states.keys()):
            state = self.states[pure_state]
        else:
            state = State(pure_state)
            self.states[pure_state] = state

        #if self.learning:
        #    self.last_state.update_max_q_value_of_next_state(state)
        #self.last_state = state

        if self.learning:
            action = state.explore()
        else:
            action = state.exploit()

        self.last_state = state
        self.last_action = action
        self.last_data = game_data
        return action

    def return_result(self, final_data):
        if self.learning:
            reward = get_reward(self.last_data, final_data)
            self.last_state.update_q_value(self.last_action, reward)


@dataclass(frozen=True)
class PureState:
    turn: int

    @classmethod
    def build_from_data(cls, data: GameData):
        return cls(data.turn)


@dataclass(frozen=False)
class State:
    pure_state: PureState

    def __post_init__(self):
        self.actions: dict = dict([(action, START_Q) for action in ALLOWED_ACTIONS])
        self.stdevs: dict = dict([(action, np.nan) for action in ALLOWED_ACTIONS])
        #self.max_q_value_of_next_state: float = np.nan
        self.total_hits: int = 0
        self.num_hits: dict = dict([(action, 0) for action in ALLOWED_ACTIONS])
        self.history = []
        self.last_decision_type = ''

    def explore(self):
        if np.nan in self.stdevs.values():
            action = random.choice(list(self.actions.keys()))
            print('nan in stdevs, choosing at random')
        else:
            action_with_highest_q = max(self.actions, key=self.actions.get)
            other_actions = [key for key in self.actions.keys() if key != action_with_highest_q]
            p_action_is_better_than_action_with_highest_q = dict(
                [(
                    action,
                    get_prob_q2_greater_than_q1(self.actions[action_with_highest_q], self.stdevs[action_with_highest_q], self.actions[action], self.stdevs[action])
                ) for action in other_actions])

            if sum(p_action_is_better_than_action_with_highest_q.values()) > 0.5:
                print('stats not good: choosing at random')
                print('actions: {}, stdevs: {}'.format(self.actions, self.stdevs))
                print(p_action_is_better_than_action_with_highest_q)
                action = random.choice(list(self.actions.keys()))

            else:
                #print('stats good')
                weights = p_action_is_better_than_action_with_highest_q
                #print(weights)
                weights[action_with_highest_q] = 1 - sum(weights.values())
                action = random.choices(list(weights.keys()), list(weights.values()))[0]

        self.last_decision_type = 'explore'
        return action

    def exploit(self):
        action = max(self.actions, key=self.actions.get)
        self.last_decision_type = 'exploit'

        if learning_params.explain:
            print('Exploiting the state:')
            print(self.pure_state)
            print('Action to take: {}'.format(action))
            for action_ in self.actions.keys():
                selected_history = [hist for hist in self.history if hist['action'] == action_]
                plt.plot([hist['hit'] for hist in selected_history], [hist['q_value'] for hist in selected_history], label=action_)
            plt.legend()
            plt.show()

        return action

    def update_q_value(self, action, reward):
        self.total_hits += 1
        self.num_hits[action] += 1
        learned_value = reward #+ learning_params.discount_rate * self.max_q_value_of_next_state
        self.actions[action] = (((self.num_hits[action]-1) * self.actions[action]) + learned_value) / (self.num_hits[action])
        #print(action)
        self.history.append({'hit': self.num_hits[action], 'action': action, 'reward': reward, 'q_value': self.actions[action], 'decision_type': self.last_decision_type})
        if self.num_hits[action] >= learning_params.min_len_to_take_stdev_over:
            self.stdevs[action] = np.std([hist['reward'] for hist in self.history if hist['action'] == action])

'''
    def update_max_q_value_of_next_state(self, next_state):
        learned_value = max(next_state.actions.values())
        if self.max_q_value_of_next_state is np.nan:
            self.max_q_value_of_next_state = max(next_state.actions.values())
        else:
            self.max_q_value_of_next_state = (((self.total_hits-1) * self.max_q_value_of_next_state) + learned_value) / self.total_hits
'''