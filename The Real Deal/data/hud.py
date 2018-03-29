import pygame
import pygame.font


class Statbar():
    """A stat bar for use in the HUD."""

    def __init__(self, settings, screen, color, pos, stat, statmax):
        self.screen = screen
        self.settings = settings
        self.stat = stat
        self.statmax = statmax
        self.color = color
        # Assumes that color is completely red, green, or blue.
        self.dark_color = color - pygame.Color(127, 127, 127, 0)
        self.rect = pygame.Rect(0, 0, 500, 4)
        self.top_rect = pygame.Rect(0, 0, 500, 4)
        (self.rect.x, self.rect.y) = pos
        self.top_rect.center = self.rect.center

    def update(self, stat):
        """Change the top rect's length to match the given stat."""
        self.stat = stat
        if self.stat > self.statmax:
            self.stat = self.statmax
        self.top_rect.width = (self.stat / self.statmax) * 500

    def draw(self):
        """Draw the two bars."""
        pygame.draw.rect(self.screen, self.dark_color, self.rect)
        pygame.draw.rect(self.screen, self.color, self.top_rect)


class HUD():
    """The HUD."""

    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.healthbar = Statbar(settings, screen, settings.red, (10, 10),
                                 stats.ship_health, settings.ship_health)
        self.powerbar = Statbar(settings, screen, settings.green, (10, 20),
                                stats.ship_level, settings.max_ship_level)

    def update(self, stats):
        """Update and draw the bars."""
        self.healthbar.update(stats.ship_health)
        self.healthbar.draw()
        self.powerbar.update(stats.ship_level)
        self.powerbar.draw()
