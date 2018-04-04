import pygame
import sys
from pygame.sprite import Group
from pygame.joystick import Joystick
from settings import Settings
import game_functions as gf
from entities import Ship
from stats import Stats
from preloader import Sounds, Images
from hud import HUD


def run_game():
    # Initialize Pygame
    pygame.mixer.pre_init(frequency=44100)
    pygame.init()
    # Initialize settings, preload assets, and create a clock
    settings = Settings()
    sounds = Sounds(settings)
    images = Images()
    clock = pygame.time.Clock()
    # Set up the window
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
    # Try to create a joystick object
    try:
        gamepad = Joystick(settings.gamepad_id)
        gamepad.init()
        settings.gamepad_connected = True
    except pygame.error:
        gamepad = 0
        settings.gamepad_connected = False
    if not settings.mute_music:
        pygame.mixer.music.play(loops=-1)
    # Main loop.
    while stats.done is False:
        gf.check_events(settings, screen, ship, gamepad, bullets, stats,
                        sounds, enemies, images)
        gf.update_stars(settings, screen, stars, images)
        if stats.game_active:
            ship.update(settings, images)
            gf.update_bullets(settings, screen, ship, bullets, enemies, sounds)
            gf.update_enemy_stuff(settings, screen, ship, enemies, sounds,
                                  stats, explosions, images, pickups, hud)
        gf.update_screen(settings, screen, stars, ship, bullets, enemies,
                         explosions, pickups, hud, stats)
        clock.tick(settings.fps_limit)
        if settings.show_fps:
            print(clock.get_fps())
        print(stats.ship_inv, stats.ship_inv_timer)


run_game()
# Stop Pygame (necessary if ran from IDLE)
pygame.quit()
# Stop the process (necessary if launcher was skipped)
sys.exit()
