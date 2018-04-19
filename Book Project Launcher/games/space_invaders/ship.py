import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, si_settings, screen):
        """Initializes the ship and sets its starting position."""
        super().__init__()
        self.screen = screen
        self.si_settings = si_settings
        #  Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #  New ships go in the bottom center of the screen with some padding.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 6
        #  Store the ship's center as a decimal value.
        self.center = float(self.rect.centerx)
        #  Movement flags
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def update(self):
        """Moves the ship if the flags say to."""
        #  Makes sure that the ship never goes offscreen.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.si_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.si_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """Draws the ship."""
        self.screen.blit(self.image, self.rect)
