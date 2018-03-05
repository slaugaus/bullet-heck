import pygame
import sys
from star import Star


def check_events(settings, screen, stars, ship, gamepad):
    """Respond to key and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stars, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.JOYAXISMOTION:
            check_analog_events(event, gamepad, ship, settings)


def check_keydown_events(event, settings, screen, stars, ship):
    """Respond to pressed keys."""
    # Note: Any wacky keypress limits are your keyboard's fault.
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_UP:
        ship.moving_up = False


def check_analog_events(event, gamepad, ship, settings):
    """Respond to analog stick movement."""
    deadzone = settings.deadzone
    axis_x = settings.axis_x
    axis_y = settings.axis_y
    # If the stick is out of the deadzone, tell the ship to move.
    if gamepad.get_axis(axis_x) >= deadzone:
        ship.an_right = gamepad.get_axis(axis_x)
    if gamepad.get_axis(axis_x) <= -deadzone:
        ship.an_left = gamepad.get_axis(axis_x)
    if gamepad.get_axis(axis_y) >= deadzone:
        ship.an_down = gamepad.get_axis(axis_y)
    if gamepad.get_axis(axis_y) <= -deadzone:
        ship.an_up = gamepad.get_axis(axis_y)
    # If the stick is in the deadzone, make sure the ship doesn't move.
    if -deadzone <= gamepad.get_axis(axis_x) <= deadzone:
        ship.an_left, ship.an_right = 0, 0
    if -deadzone <= gamepad.get_axis(axis_y) <= deadzone:
        ship.an_up, ship.an_down = 0, 0


def update_stars(settings, screen, stars):
    """Update the starry background."""
    if len(stars) < settings.star_limit:
        new_star = Star(settings, screen)
        stars.add(new_star)
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
