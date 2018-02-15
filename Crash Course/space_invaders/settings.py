class Settings():
    """Stores the settings for this Space Invaders clone."""
    def __init__(self):
        """Initializes the game's static settings."""
        self.screen_width = 960
        self.screen_height = 600
        self.bg_color = (0, 0, 0)  # not really necessary
        #  Ship settings
        self.ship_lives = 3
        #  Bullet settings
        self.bullet_width = 3  # default: 3
        self.bullet_height = 15  # default: 15
        self.bullet_color = 0, 255, 0
        self.bullets_allowed = 3  # default: 3
        # Alien settings
        self.fleet_drop_speed = 5  # default: 10
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        # How quickly the alien point value increases.
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Initialize game settings that can change."""
        self.ship_speed_factor = 5  # in pixels per update during keypress
        self.bullet_speed_factor = 10  # default: 3
        self.alien_speed_factor = 2  # default: 1
        self.alien_anim_frames = 30
        # 1 is right, -1 is left.
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed and alien point value."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_anim_frames *= (1 / self.speedup_scale)
        self.alien_points = int(self.alien_points * self.score_scale)
