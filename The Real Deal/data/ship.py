import pygame
import os
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen):
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
        self.rect.left = self.screen_rect.left + (settings.screen_width / 10)
        self.hitbox.center = self.rect.center
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

    def reset_ship_pos(self, settings):
        """Reset the ship's position."""
        self.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left + (settings.screen_width / 10)

    def update_digital(self, settings):
        """Animate the ship, then move it if the flags say to."""
        # Don't call animate() twice with a gamepad connected.
        if not settings.gamepad_connected:
            self.animate()
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
        self.hitbox.center = self.rect.center

    def update_analog(self, settings):
        """Animate the ship, then move it based on analog stick movement."""
        self.animate()
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
        self.hitbox.center = self.rect.center

    def prep_anim(self):
        """Load each animation frame and prepare for animation."""
        # Code "inspired by" https://stackoverflow.com/a/42013186
        # Load the images.
        self.images = []
        self.image_list = os.listdir("assets/ship")
        # Only load the images in the folder.
        while len(self.image_list) > 30:
            self.image_list.pop()
        for filename in self.image_list:
            image = pygame.image.load("assets/ship/" + filename)
            self.images.append(image)
        self.index = 0
        self.current_frame = 0

    def animate(self):
        """Animate the ship."""
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def blitme(self):
        """Draw the ship and its hitbox."""
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.hb_image, self.hitbox)
