class GameStats():
    """Tracks statistics for Space Invaders."""
    def __init__(self, si_settings):
        """Initialize stats."""
        self.si_settings = si_settings
        self.reset_stats()
        # Start in an inactive state.
        self.game_active = False
        # Has the game been lost yet? (For changing the button text)
        self.game_lost = False
        # Never reset the high score.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.si_settings.ship_lives
        self.score = 0
        self.level = 1
