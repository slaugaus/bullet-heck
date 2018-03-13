import pickle


class Settings():
    """Loads and stores settings for Bullet Heck."""
    def __init__(self):
        """Load settings.pickle and convert the list to variables."""
        try:
            file = open("../settings.pickle", mode="r+b")
            vars = pickle.load(file)
            [self.gamepad_connected, self.screen_width, self.screen_height,
             self.gamepad_id, self.deadzone, self.axis_x, self.axis_y,
             self.hat_id, self.but_A, self.but_B, self.show_fps] = vars
        except (FileNotFoundError, EOFError):
            print("ERROR: Couldn't read settings.pickle!\n",
                  "Did you run the launcher?")
            quit()
        # Colors
        self.bg_color = (0, 0, 0)
        # Performance
        self.star_limit = 100
        self.fps_limit = 60
        # Movement
        self.ship_speed = 10
        self.diag_factor = ((2 ** 0.5) / 2)  # (root2)/2
        self.star_speed = 5
        # Bullets
        self.bullet_color = (255, 0, 0)
        self.bullet_speed = 20
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_limit = 50
        self.bullet_cooldown = 5
