import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manages the ship's bullets."""

    def __init__(self, si_settings, screen, ship):
        """Make a bullet at the ship's position."""
        super().__init__()  # simpler python 3 syntax
        self.screen = screen
        # Create a bullet rect at (0, 0) and set its real position.
        self.rect = pygame.Rect(0, 0, si_settings.bullet_width,
                                si_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # Float the bullet's position, making it a decimal value.
        self.y = float(self.rect.y)

        self.color = si_settings.bullet_color
        self.speed_factor = si_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up."""
        # Update position
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet."""
        pygame.draw.rect(self.screen, self.color, self.rect)
