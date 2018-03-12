import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manages the ship's bullets."""
    def __init__(self, settings, screen, ship):
        """Make a bullet at the ship's position."""
        super().__init__()
        self.screen = screen
        # Create a bullet rect at (0, 0) and set its real position.
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                settings.bullet_height)
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right
        # Float the bullet's position, making it a decimal value.
        self.x = float(self.rect.x)

        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        """Move the bullet right."""
        # Update position
        self.x += self.speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet."""
        pygame.draw.rect(self.screen, self.color, self.rect)
