import pygame
import pygame.font
from entities import Ship


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
        """Change the top rect's length to match the given stat, then draw."""
        self.stat = stat
        if self.stat > self.statmax:
            self.stat = self.statmax
        self.top_rect.width = (self.stat / self.statmax) * 500
        pygame.draw.rect(self.screen, self.dark_color, self.rect)
        if self.stat > 0:
            pygame.draw.rect(self.screen, self.color, self.top_rect)


class HUD():
    """The HUD."""

    def __init__(self, settings, screen, stats, images):
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.images = images
        self.text_color = settings.white
        self.font = pygame.font.Font("assets/unoestado.ttf", 32)
        self.healthbar = Statbar(settings, screen, settings.red, (5, 50),
                                 stats.ship_health, settings.ship_health)
        self.powerbar = Statbar(settings, screen, settings.green, (5, 55),
                                stats.ship_level, settings.max_ship_level)
        self.prep_life_amount()

    def prep_life_amount(self):
        self.ship = Ship(self.settings, self.screen, self.stats, self.images)
        (self.ship.rect.x, self.ship.rect.y) = (5, 5)
        lives_left = self.stats.ship_lives
        lives_str = "x " + str(lives_left)
        self.lives_image = self.font.render(lives_str, True, self.text_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.ship.rect.right + 5
        self.lives_rect.y = self.ship.rect.y

    def update(self, stats):
        """Update and draw the bars."""
        self.ship.blitme()
        self.screen.blit(self.lives_image, self.lives_rect)
        self.healthbar.update(stats.ship_health)
        self.powerbar.update(stats.ship_level)
