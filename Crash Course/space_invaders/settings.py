class Settings():
    """A class to store the settings for my Space Invaders clone."""
    def __init__(self):
        """Initializes the game's settings."""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)  # not really necessary
        #  Ship settings
        self.ship_speed_factor = 1.5  # in pixels per update during keypress
