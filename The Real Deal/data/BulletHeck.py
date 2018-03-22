import pygame
from pygame.sprite import Group
from pygame.joystick import Joystick
from settings import Settings
import game_functions as gf
from ship import Ship
from stats import Stats
from sounds import Sounds


def run_game():
    settings = Settings()
    sounds = Sounds(settings)
    pygame.init()
    stats = Stats(settings)
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    pygame.display.set_caption("Bullet Heck!")
    ship = Ship(settings, screen, stats)
    stars = Group()
    bullets = Group()
    enemies = Group()
    clock = pygame.time.Clock()
    if settings.gamepad_connected:
        gamepad = Joystick(settings.gamepad_id)
        gamepad.init()
    else:
        gamepad = 0
    sounds.bgm.play(loops=-1)
    while True:
        gf.check_events(settings, screen, ship, gamepad, bullets, stats,
                        sounds, enemies)
        gf.update_stars(settings, screen, stars)
        if stats.game_active:
            if settings.gamepad_connected:
                ship.update_analog(settings)
            ship.update_digital(settings)
            gf.update_bullets(settings, screen, ship, bullets, enemies)
            gf.update_enemies(settings, screen, ship, enemies, sounds, stats)
            gf.update_screen(settings, screen, stars, ship, bullets, enemies)
            clock.tick(settings.fps_limit)
            if settings.show_fps:
                print(clock.get_fps())


run_game()
