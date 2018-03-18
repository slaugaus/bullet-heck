class Stats():
    """Tracks statistics."""
    def __init__(self, settings):
        """Initialize stats."""
        self.settings = settings
        self.game_active = True
        self.bullet_cooldown = 0
        self.ship_health = settings.ship_health
