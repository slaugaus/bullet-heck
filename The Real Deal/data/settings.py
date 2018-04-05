import pickle
import pygame


class Settings():
    """Loads and stores settings for Bullet Heck. Also a bunch of constants."""

    def __init__(self):
        """Load settings.pickle and convert the list to variables."""
        try:
            file = open("../settings.pickle", mode="r+b")
            vars = pickle.load(file)
            [self.gamepad_connected, self.screen_res, self.gamepad_id,
             self.deadzone, self.axis_x, self.axis_y, self.hat_id, self.but_A,
             self.but_B, self.show_fps, skip_launcher, self.autofire,
             self.mute_music, self.mute_sound] = vars
        except (FileNotFoundError, EOFError, ValueError):
            print("ERROR: Couldn't load from settings.pickle!\n"
                  "Did you run the launcher?")
            input("Press any key to quit...")
            quit()
        # Split the screen resolution into useful values
        reslist = self.screen_res.split()
        self.screen_width = int(reslist[0])
        self.screen_height = int(reslist[2])
        # Colors
        self.white = pygame.Color(255, 255, 255, 255)
        self.black = pygame.Color(0, 0, 0, 255)
        self.red = pygame.Color(255, 0, 0, 255)
        self.green = pygame.Color(0, 255, 0, 255)
        self.blue = pygame.Color(0, 0, 255, 255)
        # Performance
        self.star_limit = 100
        self.fps_limit = 60
        # Ship
        self.ship_speed = 10  # pixels/frame
        self.ship_health = 3
        self.ship_lives = 3
        self.diag_factor = ((2 ** 0.5) / 2)  # (root2)/2
        self.star_speed = 5
        self.max_ship_level = 3
        self.ship_mercy_inv = 60  # frames
        # Bullets
        self.bullet_limit = 100
        self.bullet_cooldown = 5  # frames
        # Enemies
        self.enemy_1_speed = 4
        self.powerup_chance = 25  # percent

    def reset_settings(self):
        """Reset any settings that change during the game."""
