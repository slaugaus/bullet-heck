import pickle


class Settings():
    """Stores settings for Bullet Heck."""
    def __init__(self):
        """Load settings.pkl and convert the array to variables."""
        try:
            file = open("../test.pkl", mode="r+b")
            vars = pickle.load(file)
            print(vars)
        except FileNotFoundError:
            print("ERROR: Couldn't find settings.pkl!\n",
                  "Did you run the launcher?")
            quit()
        # Resolution
        self.screen_width = 1600
        self.screen_height = 900
        # Colors
        self.bg_color = (0, 0, 0)
        # Performance
        self.star_limit = 100
        self.fps_limit = 60
        self.show_fps = False
        # Gamepad stuff
        self.gamepad_connected = False
        self.gamepad_id = 0
        self.deadzone = 0.2
        self.axis_x = 0
        self.axis_y = 1
        self.hat_id = 0

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """Initialize settings that might change at some point."""
        self.ship_speed = 10
        self.ship_diag_speed = self.ship_speed * ((2 ** 0.5) / 2)  # (root2)/2
        self.star_speed = 5
