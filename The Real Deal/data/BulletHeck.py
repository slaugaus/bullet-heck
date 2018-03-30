import pygame
from pygame.sprite import Group
from pygame.joystick import Joystick
from settings import Settings
import game_functions as gf
from entities import Ship
from stats import Stats
from preloader import Sounds, Images
from hud import HUD


def run_game():
    # Initialize settings and preload assets
    settings = Settings()
    sounds = Sounds(settings)
    images = Images()
    # Initialize Pygame and set up the window
    pygame.init()
    pygame.display.set_icon(images.icon)
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    pygame.display.set_caption("Bullet Heck!")
    # Initialize the stats and HUD
    stats = Stats(settings)
    hud = HUD(settings, screen, stats, images)
    # Create the ship and groups for everything else
    ship = Ship(settings, screen, stats, images)
    stars = Group()
    bullets = Group()
    enemies = Group()
    explosions = Group()
    pickups = Group()
    clock = pygame.time.Clock()
    if settings.gamepad_connected:
        gamepad = Joystick(settings.gamepad_id)
        gamepad.init()
    else:
        gamepad = 0
    sounds.bgm.play(loops=-1)
    while True:
        gf.check_events(settings, screen, ship, gamepad, bullets, stats,
                        sounds, enemies, images)
        gf.update_stars(settings, screen, stars, images)
        if stats.game_active:
            if settings.gamepad_connected:
                ship.update_analog(settings)
            ship.update_digital(settings, images)
            gf.update_bullets(settings, screen, ship, bullets, enemies, sounds)
            gf.update_enemy_stuff(settings, screen, ship, enemies, sounds,
                                  stats, explosions, images, pickups, hud)
        gf.update_screen(settings, screen, stars, ship, bullets, enemies,
                         explosions, pickups, hud, stats)
        clock.tick(settings.fps_limit)
        if settings.show_fps:
            print(clock.get_fps())


run_game()
