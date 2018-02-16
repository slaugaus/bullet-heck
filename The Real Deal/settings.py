class Settings():
    """Stores settings for Bullet Heck."""
    def __init__(self):
        """Initialize static settings.
        At some point, these will be read from another file instead."""
        # Resolution
        self.screen_width = 1600
        self.screen_height = 900
        # Colors
        self.bg_color = (0, 0, 0)
        # Performance
        self.star_limit = 100
        self.fps_limit = 60

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize settings that will change."""
        self.ship_speed = 10
        self.star_speed = 5
