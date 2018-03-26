class Stats():
    """Tracks statistics."""
    def __init__(self, settings):
        """Initialize stats."""
        self.settings = settings
        self.game_active = True
        self.reset_stats()

    def reset_stats(self):
        """Reset the stats that will change."""
        self.bullet_cooldown = 0
        self.ship_health = self.settings.ship_health
        self.ship_level = 0
