import pygame
import os
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen, stats):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings
        # Load the animation frames and get the rect of frame 1.
        self.prep_anim()
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.hb_image = pygame.image.load("assets/hitbox.png")
        self.hitbox = self.hb_image.get_rect()
        # Place the ship in the vertical middle with some padding.
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.left
        self.hitbox.center = self.rect.center
        self.ready = False
        # Store the ship's center as decimals.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Flags for digital movement
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        # Flags for analog movement
        self.an_up, self.an_down = 0, 0
        self.an_right, self.an_left = 0, 0

    def reset_pos(self):
        """Reset the ship's position."""
        self.ready = False
        self.centery = self.screen_rect.centery
        # same as setting self.rect.right to self.screen_rect.left
        self.centerx = self.screen_rect.left - (self.rect.right - self.centerx)

    def update_digital(self, settings):
        """Animate the ship, then move it if the flags say to."""
        if not self.ready:
            if self.centerx < settings.screen_width / 10:
                self.centerx += settings.ship_speed
            else:
                self.ready = True
        # Don't call animate() twice with a gamepad connected.
        if not settings.gamepad_connected:
            self.animate()
        # The ship should be moving the same speed when moving diagonally.
        if (self.moving_up and self.moving_left or
                self.moving_up and self.moving_right or
                self.moving_down and self.moving_left or
                self.moving_down and self.moving_right):
            speed = settings.ship_speed * settings.diag_factor
        else:
            speed = settings.ship_speed
        # If it's been animated in, allow horizontal movement.
        if self.ready:
            if self.moving_right and self.rect.right < settings.screen_width:
                self.centerx += speed
            if self.moving_left and self.rect.left > 0:
                self.centerx -= speed
        if self.moving_down and self.rect.bottom < settings.screen_height:
            self.centery += speed
            self.animdir = -1
        if self.moving_up and self.rect.top > 0:
            self.centery -= speed
            self.animdir = 1
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.hitbox.center = self.rect.center

    def update_analog(self, settings):
        """Animate the ship, then move it based on analog stick movement."""
        self.animate()
        if self.ready:
            if self.an_right > 0 and self.rect.right < settings.screen_width:
                self.centerx += self.an_right * settings.ship_speed
            if self.an_left < 0 and self.rect.left > 0:
                self.centerx += self.an_left * settings.ship_speed
        if self.an_up < 0 and self.rect.top > 0:
            self.centery += self.an_up * settings.ship_speed
            self.animdir = 1
        if self.an_down > 0 and self.rect.bottom < settings.screen_height:
            self.centery += self.an_down * settings.ship_speed
            self.animdir = -1
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.hitbox.center = self.rect.center

    def prep_anim(self):
        """Load each animation frame and prepare for animation."""
        # Code "inspired by" https://stackoverflow.com/a/42013186
        # Load the images.
        self.images = []
        self.image_list = os.listdir("assets/ship")
        # Only load the images in the folder, not stuff like Thumbs.db.
        while len(self.image_list) > 30:
            self.image_list.pop()
        for filename in self.image_list:
            image = pygame.image.load("assets/ship/" + filename)
            self.images.append(image)
        self.index = 0
        self.animdir = 1

    def animate(self):
        """Animate the ship."""
        self.index += self.animdir
        # <> are there in case the index ever goes past 30 or 0.
        if self.animdir == 1 and self.index >= len(self.images):
            self.index = 0
        if self.animdir == -1 and self.index <= 0:
            self.index = len(self.images) - 1
        self.image = self.images[self.index]

    def blitme(self):
        """Draw the ship and its hitbox."""
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.hb_image, self.hitbox)
