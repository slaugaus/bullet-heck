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
        self.an_up, self.an_down = 0, 0
        self.an_right, self.an_left = 0, 0

    def reset_ship_pos(self, settings):
        """Reset the ship's position."""
        self.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left + (settings.screen_width / 10)

    def update_digital(self, settings):
        """Move the ship if the flags say to."""
        if self.moving_right and self.rect.right < settings.screen_width:
            self.centerx += settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.centerx -= settings.ship_speed
        if self.moving_down and self.rect.bottom < settings.screen_height:
            self.centery += settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.centery -= settings.ship_speed
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def update_analog(self, settings):
        """Move the ship based on analog stick movement."""
        if self.an_right > 0 and self.rect.right < settings.screen_width:
            self.centerx += self.an_right * settings.ship_speed
        if self.an_left < 0 and self.rect.left > 0:
            self.centerx += self.an_left * settings.ship_speed
        if self.an_up < 0 and self.rect.top > 0:
            self.centery += self.an_up * settings.ship_speed
        if self.an_down > 0 and self.rect.bottom < settings.screen_height:
            self.centery += self.an_down * settings.ship_speed
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """Draw the ship."""
        self.screen.blit(self.image, self.rect)
        pygame.draw.circle(self.screen, (255, 0, 0), self.rect.center, 5)
