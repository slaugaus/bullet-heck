import pygame


class Sounds():
    """Handles the sounds."""
    def __init__(self):
        """Initialize the mixer, loading the sounds and stuff."""
        super().__init__()
        pygame.mixer.init(frequency=44100)
        self.pew = pygame.mixer.Sound("assets/audio/pew.ogg")
        self.pew.set_volume(0.25)
