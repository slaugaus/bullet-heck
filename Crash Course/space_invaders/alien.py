import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Represents one alien in the fleet."""
    def __init__(self, si_settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.si_settings = si_settings
        # Load the alien images and prepare for animation.
        self.images = []
        self.images.append(pygame.image.load('images/alien1.png'))
        self.images.append(pygame.image.load('images/alien2.png'))
        self.index = 0
        # Give the alien a rect.
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        # Start each alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien."""
        self.screen.blit(self.image, self.rect)
