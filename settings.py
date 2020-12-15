from dataclasses import dataclass
from typing import Tuple


@dataclass
class Settings:
    grid_size: int = 6
    snake_start_loc: Tuple = (1, 1)
    snake_start_dir: str = 'r'
    narrate_game: bool = False


@dataclass
class DisplaySettings:
    cell_size = 50
    grid_on = True

    head_radius = 23
    bg_color = (200, 200, 200)
    head_color = (255, 0, 0)
    body_color = (50, 50, 50)
    body_radius = 20

    new_food_freq = 25
    food_color = (0, 255, 0)
    food_radius = 20

    def __post_init__(self):
        self.screen_size = settings.grid_size * self.cell_size


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
display_settings = DisplaySettings()
learning_params = LearningParams()
