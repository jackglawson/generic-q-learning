import pygame
from settings import display_settings, settings
import sys


def animate(log):
    pygame.init()
    screen = pygame.display.set_mode((display_settings.screen_size, display_settings.screen_size))
    pygame.display.set_caption('Snake')

    if display_settings.grid_on == True:
        for x in list(range(settings.grid_size)):
            pygame.draw.line(screen, (0, 0, 0), (x * display_settings.cell_size, 0),
                             (x * display_settings.cell_size, display_settings.screen_size))
        for y in list(range(settings.grid_size)):
            pygame.draw.line(screen, (0, 0, 0), (0, y * display_settings.cell_size),
                             (display_settings.screen_size, y * display_settings.cell_size))

    for snapshot in log:
        screen.fill(display_settings.bg_color)

        # draw body
        for body in snapshot.snake_loc[1:]:
            pygame.draw.circle(
                screen,
                display_settings.body_color,
                (body[0] * settings.cell_size, body[1] * settings.cell_size),
                settings.body_radius)

        # draw head
        pygame.draw.circle(
            screen,
            display_settings.head_color,
            (snapshot.snake_loc[0][0] * display_settings.cell_size,
             snapshot.snake_loc[0][1] * display_settings.cell_size),
            display_settings.head_radius)

        # # draw food
        # pygame.draw.circle(
        #     screen,
        #     display_settings.food_color,
        #     (snapshot.food_loc[0] * display_settings.cell_size, snapshot.food_loc[1] * display_settings.cell_size),
        #     display_settings.food_radius)

        pygame.display.flip()
        pygame.time.wait(200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()