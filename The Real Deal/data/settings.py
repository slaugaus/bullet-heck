class Settings():
    """Stores settings for Bullet Heck."""
    def __init__(self):
        """Initialize static (at start) settings.
        At some point, these will be read from another file instead."""
        # Resolution
        self.screen_width = 1600
        self.screen_height = 900
        # Colors
        self.bg_color = (0, 0, 0)
        # Performance
        self.star_limit = 100
        self.fps_limit = 60
        # Gamepad stuff
        self.gamepad_connected = False
        self.gamepad_id = 0
        self.deadzone = 0.2
        self.axis_x = 0
        self.axis_y = 1

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize settings that might change at some point."""
        self.ship_speed = 10
        self.ship_diag_speed = self.ship_speed * ((2 ** 0.5) / 2)
        self.star_speed = 5
