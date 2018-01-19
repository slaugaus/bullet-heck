#  Featuring the real graphics! Wow!
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    si_settings = Settings()
    screen = pygame.display.set_mode((si_settings.screen_width,
                                      si_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    #  Draw the ship.
    ship = Ship(si_settings, screen)
    while True:
        gf.check_events(ship)
        ship.update()
        gf.update_screen(si_settings, screen, ship)


run_game()
