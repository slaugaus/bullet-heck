import pygame
import sys
import random
from entities import Star, Bullet, Enemy


def check_events(settings, screen, ship, gamepad, bullets, stats, sounds,
                 enemies):
    """Respond to key, gamepad, and mouse events."""
    check_repeat_keys(settings, screen, ship, bullets, stats, gamepad, sounds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, ship, screen, enemies)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, settings, ship)
        elif event.type == pygame.JOYAXISMOTION:
            check_analog_events(gamepad, ship, settings)
        elif event.type == pygame.JOYHATMOTION:
            check_hat_events(gamepad, ship, settings)


def check_repeat_keys(settings, screen, ship, bullets, stats, gamepad, sounds):
    keys = pygame.key.get_pressed()
    """If spacebar or b key or A button are held, fire bullets,
       waiting 10 frames between fires."""
    if settings.autofire and stats.bullet_cooldown == 0:
        fire_bullet(settings, screen, ship, bullets, sounds)
        stats.bullet_cooldown = settings.bullet_cooldown
    if (((keys[pygame.K_SPACE] or keys[pygame.K_b]))
            and stats.bullet_cooldown == 0):
        fire_bullet(settings, screen, ship, bullets, sounds)
        stats.bullet_cooldown = settings.bullet_cooldown
    if settings.gamepad_connected:
        if gamepad.get_button(settings.but_A) and stats.bullet_cooldown == 0:
            fire_bullet(settings, screen, ship, bullets, sounds)
            stats.bullet_cooldown = settings.bullet_cooldown
    if stats.bullet_cooldown > 0:
        stats.bullet_cooldown -= 1


def check_keydown_events(event, settings, ship, screen, enemies):
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
    if event.key == pygame.K_a:
        settings.autofire = True if settings.autofire is False else False
    if event.key == pygame.K_1:
        spawn_enemy(settings, screen, 1, enemies)


def check_keyup_events(event, settings, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_UP:
        ship.moving_up = False


def check_analog_events(gamepad, ship, settings):
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


def check_hat_events(gamepad, ship, settings):
    """Respond to hat events."""
    hat = settings.hat_id
    motion = gamepad.get_hat(hat)
    if motion[0] == -1:
        ship.moving_left = True
    elif motion[0] == 1:
        ship.moving_right = True
    else:
        ship.moving_left, ship.moving_right = False, False
    if motion[1] == -1:
        ship.moving_down = True
    elif motion[1] == 1:
        ship.moving_up = True
    else:
        ship.moving_down, ship.moving_up = False, False


def update_stars(settings, screen, stars):
    """Update the starry background."""
    if len(stars) < settings.star_limit:
        new_star = Star(settings, screen)
        stars.add(new_star)
    stars.update()
    for star in stars.copy():
        if star.rect.right <= 0:
            stars.remove(star)


def spawn_enemy(settings, screen, id, enemies):
    """Spawn an enemy."""
    enemy = Enemy(settings, screen, id)
    enemy.x = settings.screen_width
    enemy.y = random.randint(0 + enemy.rect.height, (settings.screen_height -
                                                     enemy.rect.height))
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y
    enemies.add(enemy)


def update_enemies(settings, screen, ship, enemies, sounds, stats):
    """Update the enemies."""
    enemies.update()
    for enemy in enemies.sprites():
        if enemy.health == 0:
            enemies.remove(enemy)
            print("RIP enemy")
            sounds.boom_small.play()
        if enemy.rect.right <= 0:
            enemies.remove(enemy)
            print("Miss")
    check_enemy_ship_collisions(settings, screen, enemies, ship, stats, sounds)


def fire_bullet(settings, screen, ship, bullets, sounds):
    if len(bullets) < settings.bullet_limit:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)
        sounds.pew.play()


def update_bullets(settings, screen, ship, bullets, enemies):
    """Update position of bullets, deleting the ones offscreen."""
    # Update bullet positions.
    bullets.update()
    # Delete offscreen bullets.
    for bullet in bullets.copy():
        if bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)
    check_bullet_collisions(settings, screen, enemies, bullets)


def check_bullet_collisions(settings, screen, enemies, bullets):
    """Respond to bullet-enemy collisions."""
    for enemy in enemies.sprites():
        collision = pygame.sprite.spritecollide(enemy, bullets, True)
        if collision:
            enemy.health -= 1


def check_enemy_ship_collisions(settings, screen, enemies, ship, stats,
                                sounds):
    """Respond to enemy-ship collisions."""
    for enemy in enemies.sprites():
        if pygame.sprite.collide_circle(ship, enemy) and enemy.can_damage_ship:
            if stats.ship_health > 0:
                stats.ship_health -= 1
                enemy.health -= 1
                enemy.can_damage_ship = False
                print("Ouch")
                sounds.boom_small.play()
            else:
                print("Rip you")
                ship.reset_pos()
                stats.ship_health = settings.ship_health
                sounds.boom_small.play()


def update_screen(settings, screen, stars, ship, bullets, enemies):
    """Update and flip any images onscreen."""
    screen.fill(settings.bg_color)
    for star in stars.sprites():
        star.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for enemy in enemies.sprites():
        enemy.blitme()
    pygame.display.flip()
