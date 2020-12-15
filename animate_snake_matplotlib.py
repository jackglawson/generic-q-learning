import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from settings import settings


def animate(log):
    plt.ioff()

    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.set_xlim(-0.01, settings.grid_size + 0.01), ax.set_xticks(range(0, settings.grid_size + 1))
    ax.set_ylim(-0.01, settings.grid_size + 0.01), ax.set_yticks(range(0, settings.grid_size + 1))
    ax.grid(True)
    # ax.xaxis.set_ticklabels([])
    # ax.yaxis.set_ticklabels([])

    head = ax.scatter([], [], s=40000 / settings.grid_size, c='r')
    body = ax.scatter([], [], s=30000 / settings.grid_size, c='k')
    food = ax.scatter([], [], s=5000 / settings.grid_size, c='g')


    def update(i):
        snapshot = log[i]
        food_loc = snapshot.food_loc
        snake_loc = snapshot.snake_loc
        head_loc = snake_loc[0]
        body_locs = snake_loc[1:]
        head.set_offsets([[head_loc[0] + 0.5, head_loc[1] + 0.5]])
        if body_locs:
            body.set_offsets([[body_loc[0] + 0.5, body_loc[1] + 0.5] for body_loc in body_locs])
        food.set_offsets([[food_loc[0] + 0.5, food_loc[1] + 0.5]])

    animation = FuncAnimation(fig, update, interval=500, frames=len(log))
    plt.ion()
    return HTML(animation.to_html5_video())
