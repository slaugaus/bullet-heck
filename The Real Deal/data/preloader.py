import pygame
import os


class Sounds():
    """Handles the sound mixer."""

    def __init__(self, settings):
        """Edit mixer settings, then load all of the audio and set volumes."""
        pygame.mixer.set_num_channels(32)
        self.null = pygame.mixer.Sound("assets/audio/null.ogg")
        if not settings.mute_sound:
            self.pew = pygame.mixer.Sound("assets/audio/pew.ogg")
            self.boom_med = pygame.mixer.Sound("assets/audio/boom_med.ogg")
            self.boom_small = pygame.mixer.Sound("assets/audio/boom_small.ogg")
            self.enemy_hit = pygame.mixer.Sound("assets/audio/enemy_hit.ogg")
            self.ship_hit = pygame.mixer.Sound("assets/audio/ship_hit.ogg")
            self.levelup = pygame.mixer.Sound("assets/audio/levelup.ogg")
            self.leveldown = pygame.mixer.Sound("assets/audio/leveldown.ogg")
        else:
            self.pew = self.null
            self.boom_med = self.null
            self.boom_small = self.null
            self.enemy_hit = self.null
            self.ship_hit = self.null
            self.levelup = self.null
            self.leveldown = self.null
        if not settings.mute_music:
            pygame.mixer.music.load("assets/audio/bgm.ogg")
            pygame.mixer.music.set_volume(0.4)
        self.pew.set_volume(0.25)
        self.boom_med.set_volume(0.3)
        self.boom_small.set_volume(0.75)
        self.enemy_hit.set_volume(0.1)
        self.ship_hit.set_volume(0.5)
        self.levelup.set_volume(0.5)


class Images():
    """Handles all of the sprites."""

    def __init__(self):
        """Load each of the sprites and sprite lists."""
        self.hitbox = pygame.image.load("assets/hitbox.png")
        self.hitbox_inv = pygame.image.load("assets/hitbox_inv.png")
        self.star = pygame.image.load("assets/star.png")
        self.enemy_bullet = pygame.image.load("assets/enemy_bullet.png")
        # Loading icon_16 screws it up for some reason.
        self.icon = pygame.image.load("assets/icon/icon_16_2x.png")
        self.logo = pygame.image.load("assets/logo.png")
        self.enemy = [0, 0, 0, 0, 0, 0]
        self.enemy[0] = self.load_anim("enemies/1")
        self.enemy[1] = self.load_anim("enemies/2", 60)
        self.enemy[2] = self.load_anim("enemies/3")
        self.enemy[3] = self.load_anim("enemies/4", 60)
        self.enemy[4] = self.load_anim("enemies/5")
        self.enemy[5] = self.load_anim("enemies/6", 20)
        self.ship = self.load_anim("ship")
        self.explosion = self.load_anim("explosion", 45)
        self.explosion_large = self.load_anim("explosion_large", 45)
        self.powerup = self.load_anim("powerup")
        self.health = self.load_anim("health")

    def load_anim(self, dir, length=30):
        target = []
        self.image_list = os.listdir("assets/%s" % dir)
        # Only load the images in the folder, not stuff like Thumbs.db.
        while len(self.image_list) > length:
            self.image_list.pop()
        for filename in self.image_list:
            image = pygame.image.load("assets/%s/" % dir + filename)
            target.append(image)
        return target
