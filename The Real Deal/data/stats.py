class Stats():
    """Tracks statistics."""

    def __init__(self, settings):
        """Initialize stats."""
        self.settings = settings
        self.game_active = True
        self.done = False
        self.reset_stats()

    def reset_stats(self):
        """Reset the stats that will change."""
        self.bullet_cooldown = 0
        self.ship_health = self.settings.ship_health
        self.ship_lives = self.settings.ship_lives
        self.ship_level = 0
        self.ship_inv = False
        self.ship_inv_timer = 1
