import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manages the ship's bullets."""
    def __init__(self, si_settings, screen, ship):
        """Make a bullet at the ship's position."""
        super().__init__()
        self.screen = screen
        # Create a bullet rect at (0, 0) and set its real position.
        self.rect = pygame.Rect(0, 0, si_settings.bullet_width,
                                si_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # Float the bullet's position.
        self.y = float(self.rect.y)

        self.color = si_settings.bullet_color
        self.speed_factor = si_settings.bullet_speed_factor
    
