import pygame
from pygame.sprite import Group
from pygame.joystick import Joystick
from settings import Settings
import game_functions as gf
from ship import Ship
from stats import Stats
from sounds import Sounds


def run_game():
    sounds = Sounds()
    pygame.init()
    settings = Settings()
    stats = Stats(settings)
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    pygame.display.set_caption("Bullet Heck!")
    ship = Ship(settings, screen, stats)
    stars = Group()
    bullets = Group()
    clock = pygame.time.Clock()
    if settings.gamepad_connected:
        gamepad = Joystick(settings.gamepad_id)
        gamepad.init()
    else:
        gamepad = 0
    while True:
        gf.check_events(settings, screen, ship, gamepad, bullets, stats,
                        sounds)
        gf.update_stars(settings, screen, stars)
        if stats.game_active:
            if settings.gamepad_connected:
                ship.update_analog(settings)
            ship.update_digital(settings)
            gf.update_bullets(settings, screen, ship, bullets)
            gf.update_screen(settings, screen, stars, ship, bullets)
            clock.tick(settings.fps_limit)
            if settings.show_fps:
                print(clock.get_fps())


run_game()
