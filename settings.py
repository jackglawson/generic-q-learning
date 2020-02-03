from dataclasses import dataclass
from typing import Tuple


@dataclass
class Settings:
    grid_size: int = 3
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
    discount_rate: float = 1.0
    num_epochs: int = 500
    explain: bool = False
    min_len_to_take_stdev_over = 10
    next_state_is_predictable = True


settings = Settings()
display_settings = DisplaySettings()
learning_params = LearningParams()
