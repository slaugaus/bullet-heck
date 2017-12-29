import pygame
class Ship():
    def __init__(self, screen):
        """Initializes the ship and sets its starting position."""
        self.screen = screen
        #  Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #  New ships go in the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
    def blitme(self):
        """Draws the ship."""
        self.screen.blit(self.image, self.rect)
