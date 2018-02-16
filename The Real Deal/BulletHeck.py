import pygame
from pygame.sprite import Group
from settings import Settings
import game_functions as gf
from ship import Ship


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    pygame.display.set_caption("Bullet Heck")
    ship = Ship(settings, screen)
    stars = Group()
    clock = pygame.time.Clock()
    while True:
        gf.add_star(settings, screen, stars)
        gf.check_events(settings, screen, stars, ship)
        gf.update_stars(settings, screen, stars)
        ship.update(settings)
        gf.update_screen(settings, screen, stars, ship)
        clock.tick(settings.fps_limit)
        # print(clock.get_fps())


run_game()
