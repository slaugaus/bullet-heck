"""Place a bitmap in the center of the screen and match the backgrounds of it
and the screen."""
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
tux = pygame.image.load('tux.bmp')
pygame.display.set_caption("Tux!")
tuxrect = tux.get_rect()
screen_rect = screen.get_rect()
tuxrect.centerx = screen_rect.centerx
tuxrect.centery = screen_rect.centery
while True:
    screen.fill((204, 204, 204))
    screen.blit(tux, tuxrect)
    pygame.display.flip()
