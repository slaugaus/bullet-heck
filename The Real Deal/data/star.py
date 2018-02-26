import pygame
import random
from pygame.sprite import Sprite


class Star(Sprite):
    """Manages the starry background."""
    def __init__(self, settings, screen):
        """Put a star somewhere on the screen."""
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(('assets/star.png'))
        self.rect = self.image.get_rect()
        self.rect.right = settings.screen_width
        self.rect.bottom = random.randint(0, settings.screen_height)
        # self.x = float(self.rect.x)
        # self.color = (255, 255, 255)
        self.speed_factor = settings.star_speed
        self.x = float(self.rect.x)

    def update(self):
        """Move the star left."""
        self.x -= self.speed_factor
        self.speed_factor += 0.5
        self.rect.x = self.x

    def blitme(self):
        """Draw the star."""
        self.screen.blit(self.image, self.rect)
