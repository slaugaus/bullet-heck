import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('assets/images/ship_simple.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left + (settings.screen_width / 10)
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def reset_ship_pos(self, settings):
        """Reset the ship's position."""
        self.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left + (settings.screen_width / 10)

    def update(self, settings):
        """Move the ship if the flags say to."""
        if self.moving_right and self.rect.right < settings.screen_width:
            self.centerx += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < settings.screen_height:
            self.centery += self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.settings.ship_speed
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """Draw the ship."""
        self.screen.blit(self.image, self.rect)
