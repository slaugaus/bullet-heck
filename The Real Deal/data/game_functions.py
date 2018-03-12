import pygame
import sys
from star import Star
from bullet import Bullet
current_frame = 0


def check_events(settings, screen, ship, gamepad, bullets):
    """Respond to key and mouse events."""
    check_held_keys(settings, screen, ship, bullets)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.JOYAXISMOTION:
            check_analog_events(event, gamepad, ship, settings)


def check_held_keys(settings, screen, ship, bullets):
    global current_frame
    keys = pygame.key.get_pressed()
    current_frame += 1
    if keys[pygame.K_SPACE]:
        if current_frame == 10:
            fire_bullets(settings, screen, ship, bullets)
            current_frame = 0
    elif current_frame == 10:
        current_frame = 0


def check_keydown_events(event, settings, screen, ship, bullets):
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


def check_keyup_events(event, settings, screen, ship, bullets):
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


def fire_bullets(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_limit:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)
        print("pew")


def update_bullets(settings, screen, ship, bullets):
    """Update position of bullets, deleting the ones offscreen."""
    # Update bullet positions.
    bullets.update()
    # Delete offscreen bullets.
    for bullet in bullets.copy():
        if bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)


def update_screen(settings, screen, stars, ship, bullets):
    """Update and flip any images onscreen."""
    screen.fill(settings.bg_color)
    for star in stars.sprites():
        star.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    pygame.display.flip()
