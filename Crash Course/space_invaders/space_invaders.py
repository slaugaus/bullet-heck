#  Featuring the real graphics! Wow!
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    si_settings = Settings()
    screen = pygame.display.set_mode((si_settings.screen_width,
                                      si_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    # Draw the ship and create a group of bullets and aliens.
    ship = Ship(si_settings, screen)
    bullets = Group()
    aliens = Group()
    # Create a fleet of aliens.
    gf.create_fleet(si_settings, screen, aliens)
    # The game's main loop.
    while True:
        gf.check_events(si_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(si_settings, screen, ship, aliens, bullets)


run_game()
