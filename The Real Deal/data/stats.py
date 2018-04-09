import pickle


class Stats():
    """Tracks statistics."""

    def __init__(self, settings):
        """Initialize stats and load the high score."""
        try:
            self.file = open("../highscore.pickle", mode="r+b")
            self.high_score = pickle.load(self.file)
        except (FileNotFoundError, EOFError):
            self.file = open("../highscore.pickle", mode="w+b")
            self.file = open("../highscore.pickle", mode="r+b")
            self.high_score = 0
        self.settings = settings
        self.game_active = True
        self.done = False
        self.reset_stats()

    def reset_stats(self):
        """Reset the stats that will change."""
        self.score = 0
        self.bullet_cooldown = 0
        self.ship_health = self.settings.ship_health
        self.ship_lives = self.settings.ship_lives
        self.ship_level = 0
        self.ship_inv = False
        self.ship_inv_timer = 1

    def update_high_score(self):
        """If the high score is beaten, update it and save the file."""
        if self.score > self.high_score:
            self.high_score = self.score
            pickle.dump(self.high_score, self.file)
            return True
        else:
            return False
