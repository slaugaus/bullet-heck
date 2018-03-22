import pygame


class Sounds():
    """Handles the sounds."""
    def __init__(self, settings):
        """Initialize the mixer, loading the sounds and stuff."""
        super().__init__()
        pygame.mixer.init(frequency=44100)
        if not settings.mute_sound:
            self.pew = pygame.mixer.Sound("assets/audio/pew.ogg")
            self.boom_small = pygame.mixer.Sound("assets/audio/boom_small.ogg")
        else:
            self.pew = pygame.mixer.Sound("assets/audio/null.ogg")
            self.boom_small = pygame.mixer.Sound("assets/audio/null.ogg")
        if not settings.mute_music:
            self.bgm = pygame.mixer.Sound("assets/audio/bgm.ogg")
        else:
            self.bgm = pygame.mixer.Sound("assets/audio/null.ogg")
        self.bgm.set_volume(0.5)
        self.pew.set_volume(0.25)
        self.boom_small.set_volume(1)
