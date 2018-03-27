import pygame
import random
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen, stats, images):
        """Initialize the ship and set its starting position."""
        # Call the init function of pygame.sprite.Sprite
        super().__init__()
        self.screen = screen
        self.settings = settings
        # Load the animation frames and get the rect of frame 1.
        self.index = 0
        self.animdir = 1
        self.respawn_countdown = 0
        self.images = images.ship
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.hitbox = images.hitbox
        self.hb_rect = self.hitbox.get_rect()
        # Place the ship in the vertical middle with some padding.
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.left
        self.hb_rect.center = self.rect.center
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
        # Collision info
        self.radius = 3.5

    def reset_pos(self):
        """Reset the ship's position."""
        self.ready = False
        self.respawn_countdown = 29
        self.centery = self.screen_rect.centery
        # same as setting self.rect.right to self.screen_rect.left
        self.centerx = self.screen_rect.left - (self.rect.right - self.centerx)

    def update_digital(self, settings, images):
        """Animate the ship, then move it if the flags say to."""
        if not self.ready and self.respawn_countdown == 0:
            if self.centerx < settings.screen_width / 10:
                self.centerx += settings.ship_speed
            else:
                self.ready = True
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
        self.hb_rect.center = self.rect.center
        self.hitbox = images.hitbox
        if self.respawn_countdown is not 0:
            self.respawn_countdown -= 1

    def update_analog(self, settings):
        """Move the ship based on analog stick movement."""
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
        self.hb_rect.center = self.rect.center

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
        self.screen.blit(self.hitbox, self.hb_rect)


class Enemy(Sprite):
    """One enemy."""
    def __init__(self, settings, screen, id, images):
        """Figure out what enemy this is, then initialize it."""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.id = id
        self.health = 3
        self.can_damage_ship = True
        self.index = 0
        self.images = images.enemy1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)
        # Collision info
        self.radius = 25

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


class Bullet(Sprite):
    """Manages the ship's bullets."""
    def __init__(self, settings, screen, ship, y_offset=0, height=2, width=15,
                 damage=1, speed=20):
        """Make a bullet at the ship's position."""
        super().__init__()
        self.screen = screen
        self.y_offset = y_offset
        self.speed = speed
        self.damage = damage
        self.color = settings.bullet_color
        # Create a bullet rect at (0, 0) and set its real position.
        self.rect = pygame.Rect(0, 0, width, height)
        # If told to, offset the bullet from the usual value.
        self.rect.centery = ship.rect.centery + self.y_offset
        self.rect.right = ship.rect.right
        # Float the bullet's position, making it a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet right."""
        # Update position
        self.x += self.speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Star(Sprite):
    """Manages the starry background."""
    def __init__(self, settings, screen, images):
        """Put a star somewhere on the screen."""
        super().__init__()
        self.screen = screen
        self.image = images.star
        self.rect = self.image.get_rect()
        self.rect.right = settings.screen_width
        self.rect.bottom = random.randint(0, settings.screen_height)
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


class Explosion(Sprite):
    """Boom!"""
    def __init__(self, settings, screen, images, pos):
        """Place the explosion at the given coordinates."""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.index = 0
        self.images = images.explosion
        self.countdown = len(self.images) - 1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.index += 1
        self.countdown -= 1
        self.image = self.images[self.index]

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Pickup(Sprite):
    """A pickup for the ship to collect.
       Types: powerup, health, shield"""
    def __init__(self, images, screen, pos, type):
        super().__init__()
        self.screen = screen
        self.index = 0
        self.images = images.powerup
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.center = self.rect.center
        self.x = float(self.rect.x)
        self.speed = random.randint(1, 6)

    def update(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.x -= self.speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
