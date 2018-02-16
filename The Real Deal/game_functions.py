import pygame
import sys
from star import Star


def check_events(settings, screen, stars, ship):
    """Respond to key and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydowns(event, settings, screen, stars, ship)
        elif event.type == pygame.KEYUP:
            check_keysup(event, ship)


def check_keydowns(event, settings, screen, stars, ship):
    """Respond to pressed keys."""
    # Note: Any keypress limits are your keyboard's fault.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True


def check_keysup(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_UP:
        ship.moving_up = False


def add_star(settings, screen, stars):
    if len(stars) < settings.star_limit:
        new_star = Star(settings, screen)
        stars.add(new_star)


def update_stars(settings, screen, stars):
    stars.update()
    for star in stars.copy():
        if star.rect.right <= 0:
            stars.remove(star)


def update_screen(settings, screen, stars, ship):
    """Update and flip any images onscreen."""
    screen.fill(settings.bg_color)
    for star in stars.sprites():
        star.blitme()
    ship.blitme()
    pygame.display.flip()
