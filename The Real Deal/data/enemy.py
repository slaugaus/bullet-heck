import pygame
import os
from pygame.sprite import Sprite


class Enemy(Sprite):
    """One enemy."""
    def __init__(self, settings, screen, id):
        """Figure out what enemy this is, then initialize it."""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.id = id
        self.health = 5
        self.can_damage_ship = True
        self.prep_anim()
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def prep_anim(self):
        """Load each animation frame and prepare for animation."""
        # Load the images.
        self.images = []
        self.image_list = os.listdir("assets/enemy%s" % self.id)
        # Only load the images in the folder, not stuff like Thumbs.db.
        while len(self.image_list) > 30:
            self.image_list.pop()
        for filename in self.image_list:
            image = pygame.image.load("assets/enemy%s/" % self.id + filename)
            self.images.append(image)
        self.index = 0

    def animate(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0

    def update(self):
        self.animate()
        self.image = self.images[self.index]
        self.x -= self.settings.enemy_1_speed
        self.rect.x = self.x

    def blitme(self):
        """Draw the enemy."""
        self.screen.blit(self.image, self.rect)
