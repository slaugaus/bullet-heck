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
        # Animation code "borrowed" from https://stackoverflow.com/a/42013186
        self.images = []
        self.images.append(pygame.image.load('images/alien1.png'))
        self.images.append(pygame.image.load('images/alien2.png'))
        self.index = 0
        self.current_frame = 0
        self.animation_frames = si_settings.alien_anim_frames
        # Give the alien a rect.
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        # Start each alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left, attempting to animate it."""
        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        self.x += (self.si_settings.alien_speed_factor *
                   self.si_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien."""
        self.screen.blit(self.image, self.rect)
