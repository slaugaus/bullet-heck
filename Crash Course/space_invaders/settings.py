class Settings():
    """Stores the settings for this Space Invaders clone."""
    def __init__(self):
        """Initializes the game's settings."""
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (0, 0, 0)  # not really necessary
        #  Ship settings
        self.ship_speed_factor = 1.5  # in pixels per update during keypress
        #  Bullet settings
        self.bullet_speed_factor = 1.5  # default: 1
        self.bullet_width = 3  # default: 3
        self.bullet_height = 15  # default: 15
        self.bullet_color = 0, 255, 0
        self.bullets_allowed = 3  # default: 3
