import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_events(si_settings, screen, ship, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, si_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, si_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(si_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(si_settings, screen, ship, bullets):
    # Put a bullet in the bullets group.
    if len(bullets) < si_settings.bullets_allowed:
        new_bullet = Bullet(si_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullets(bullets):
    """Update position of bullets, deleting the ones offscreen."""
    # Update bullet positions.
    bullets.update()
    # Delete offscreen bullets.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets)) # Prints the current number of bullets.


def create_fleet(si_settings, screen, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of them in a row.
    # Spacing between each alien = one alien width.
    alien = Alien(si_settings, screen)
    alien_width = alien.rect.width
    available_space_x = si_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    # Create the first row of aliens.
    for alien_number in range(number_aliens_x):
        # Create an alien and place it in the row.
        alien = Alien(si_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)

def update_screen(si_settings, screen, ship, aliens, bullets):
    """Update the images onscreen and flip them."""
    screen.fill(si_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()
