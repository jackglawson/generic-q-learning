from dataclasses import dataclass
from typing import Tuple


@dataclass
class Settings:
    ai_plays_as: str = 'x'
    narrate_game: bool = False


@dataclass
class LearningParams:
    random_action_rate: float = 0.5
    discount_rate: float = 0.5
    num_epochs: int = 500
    explain: bool = False
    learning: bool = True
    explore_multiplier: float = 1.0     # increasing this will make it more likely to choose action at random
    next_state_is_predictable = True
    min_hits_before_using_stats = 5
    max_hits_used_in_stats = 100
    predictive = True                  # if True, strategy will use max q of next state. Should be True if the reward is not given immediately


settings = Settings()
learning_params = LearningParams()
