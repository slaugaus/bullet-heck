#  Featuring the real graphics! Wow!
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    si_settings = Settings()
    screen = pygame.display.set_mode((si_settings.screen_width,
                                      si_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    # Draw the Play button.
    play_button = Button(si_settings, screen, "Play")
    # Draw the ship and create a group of bullets and aliens.
    ship = Ship(si_settings, screen)
    bullets = Group()
    aliens = Group()
    # Create a fleet of aliens.
    gf.create_fleet(si_settings, screen, ship, aliens)
    # Create an instance to store game stats and make a scoreboard.
    stats = GameStats(si_settings)
    sb = Scoreboard(si_settings, screen, stats)
    # The game's main loop.
    while True:
        gf.check_events(si_settings, screen, stats, play_button, ship, aliens,
                        sb, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(si_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(si_settings, screen, stats, sb, ship, aliens,
                             bullets)
        gf.update_screen(si_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


run_game()
