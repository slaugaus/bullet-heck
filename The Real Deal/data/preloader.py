import pygame
import os


class Sounds():
    """Handles the sound mixer."""
    def __init__(self, settings):
        """Initialize the mixer."""
        pygame.mixer.init(frequency=44100)
        pygame.mixer.set_num_channels(32)
        if not settings.mute_sound:
            self.pew = pygame.mixer.Sound("assets/audio/pew.ogg")
            self.boom_small = pygame.mixer.Sound("assets/audio/boom_small.ogg")
            self.hit = pygame.mixer.Sound("assets/audio/hit.ogg")
        else:
            self.pew = pygame.mixer.Sound("assets/audio/null.ogg")
            self.boom_small = pygame.mixer.Sound("assets/audio/null.ogg")
            self.hit = pygame.mixer.Sound("assets/audio/null.ogg")
        if not settings.mute_music:
            self.bgm = pygame.mixer.Sound("assets/audio/bgm.ogg")
        else:
            self.bgm = pygame.mixer.Sound("assets/audio/null.ogg")
        self.bgm.set_volume(0.5)
        self.pew.set_volume(0.25)
        self.boom_small.set_volume(1)
        self.hit.set_volume(0.15)


class Images():
    """Handles all of the sprites."""
    def __init__(self):
        """Load each of the sprites and sprite lists."""
        self.hitbox = pygame.image.load("assets/hitbox.png")
        self.star = pygame.image.load("assets/star.png")
        self.enemy1 = self.load_anim("enemy1")
        self.ship = self.load_anim("ship")
        self.explosion = self.load_anim("explosion")
        self.powerup = self.load_anim("powerup", 60)

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
