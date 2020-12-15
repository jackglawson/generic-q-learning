from dataclasses import dataclass
from typing import List, Tuple
import random
import matplotlib.pyplot as plt
import numpy as np
from settings import learning_params
from game import GameData
from utils import get_prob_q2_greater_than_q1
from copy import deepcopy
from noughts_and_crosses_game_dependents import START_Q, ALLOWED_ACTIONS, get_reward, PureState


class Strategy:
    def __init__(self):
        self.states = {}
        self.last_state = None
        self.last_action = None
        self.last_data = None
        #self.just_applied: bool = False

    def start_new_game(self):
        self.last_state = None
        self.last_action = None
        self.last_data = None

    def respond(self, game_data):
        pure_state = PureState.build_from_data(game_data)
        if pure_state in list(self.states.keys()):
            state = self.states[pure_state]
        else:
            state = State(pure_state)
            self.states[pure_state] = state

        if learning_params.learning and learning_params.predictive and self.last_state is not None:
            self.last_state.update_max_q_values_of_next_states(state, self.last_action)

        if learning_params.learning:
            action = state.explore()
        else:
            action = state.exploit()

        self.last_state = state
        self.last_action = action
        self.last_data = game_data
        return action

    def return_result(self, final_data):
        if learning_params.learning:
            reward = get_reward(self.last_data, final_data)
            self.last_state.update_q_value(self.last_action, reward)


@dataclass(frozen=False)
class State:
    pure_state: PureState

    def __post_init__(self):
        self.actions: dict = dict([(action, START_Q) for action in ALLOWED_ACTIONS])
        # self.stdevs: dict = dict([(action, np.nan) for action in ALLOWED_ACTIONS])
        self.max_q_values_of_next_states = dict([(action, np.nan) for action in ALLOWED_ACTIONS])
        self.total_hits: int = 0
        self.num_hits: dict = dict([(action, 0) for action in ALLOWED_ACTIONS])
        self.history = []
        self.past_learned_values: dict = dict([(action, []) for action in ALLOWED_ACTIONS])
        self.last_decision_type = ''

    def explore(self):
        if any([hit < learning_params.min_hits_before_using_stats for hit in self.num_hits.values()]):
            action = random.choice(list(self.actions.keys()))
            if learning_params.explain:
                print('Exploring the state:')
                print(self.pure_state)
                print('Not enough hits, choosing at random')
                print('Action to take: {}'.format(action))

        else:
            random_choices_from_past = dict([(action, random.choice(past_values[-learning_params.max_hits_used_in_stats:])) for action, past_values in self.past_learned_values.items()])
            action = max(random_choices_from_past, key=random_choices_from_past.get)

            if learning_params.explain:
                print('Exploring the state:')
                print(self.pure_state)
                print('Actions: {}'.format(self.actions))
                print('Hits: {}'.format(self.num_hits))
                print('Random samples chosen: {}'.format(random_choices_from_past))
                print('Action to take: {}'.format(action))
                plt.hist([self.past_learned_values[action_][-learning_params.max_hits_used_in_stats:] for action_ in ALLOWED_ACTIONS], label=ALLOWED_ACTIONS)
                plt.legend()
                plt.show()

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

        if learning_params.predictive:
            learned_value = reward + learning_params.discount_rate * self.max_q_values_of_next_states[action] if not np.isnan(self.max_q_values_of_next_states[action]) else reward
        else:
            learned_value = reward

        self.actions[action] = (((self.num_hits[action]-1) * self.actions[action]) + learned_value) / (self.num_hits[action])

        self.history.append(deepcopy({'hit': self.num_hits[action],
                                      'action': action,
                                      'reward': reward,
                                      'learned_value': learned_value,
                                      'q_value': self.actions[action],
                                      'decision_type': self.last_decision_type,
                                      }))
        if learning_params.predictive:
            self.history[-1]['max_q_of_next_state'] = self.max_q_values_of_next_states

        self.past_learned_values[action].append(learned_value)

    def update_max_q_values_of_next_states(self, next_state, last_action):
        learned_value = max(next_state.actions.values())
        if learning_params.next_state_is_predictable or np.isnan(self.max_q_values_of_next_states[last_action]):
            self.max_q_values_of_next_states[last_action] = learned_value
        else:
            self.max_q_values_of_next_states[last_action] = (((self.total_hits-1) * self.max_q_values_of_next_states[last_action]) + learned_value) / self.total_hits
