import pygame
import sys
import random
from entities import Star, Bullet, Enemy, Explosion, Pickup


def check_events(settings, screen, ship, gamepad, bullets, stats, sounds,
                 enemies, images):
    """Respond to key, gamepad, and mouse events."""
    if stats.game_active:
        check_repeat_keys(settings, screen, ship, bullets, stats, gamepad,
                          sounds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_debug_keys(event, settings, screen, enemies, images, stats)
        if stats.game_active:
            if event.type == pygame.KEYDOWN:
                check_keydown_events(event, settings, ship)
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
        fire_bullet(settings, screen, ship, bullets, sounds, stats)
        stats.bullet_cooldown = settings.bullet_cooldown
    if (((keys[pygame.K_SPACE] or keys[pygame.K_b]))
            and stats.bullet_cooldown == 0):
        fire_bullet(settings, screen, ship, bullets, sounds, stats)
        stats.bullet_cooldown = settings.bullet_cooldown
    if settings.gamepad_connected:
        if gamepad.get_button(settings.but_A) and stats.bullet_cooldown == 0:
            fire_bullet(settings, screen, ship, bullets, sounds, stats)
            stats.bullet_cooldown = settings.bullet_cooldown
    if stats.bullet_cooldown > 0:
        stats.bullet_cooldown -= 1


def check_keydown_events(event, settings, ship):
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


def check_debug_keys(event, settings, screen, enemies, images, stats):
    if event.key == pygame.K_1:
        spawn_enemy(settings, screen, 1, enemies, images)
    if event.key == pygame.K_l:
        print("Level up!")
        stats.ship_level += 1
    if event.key == pygame.K_p:
        stats.game_active = True if stats.game_active is False else False


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


def update_stars(settings, screen, stars, images):
    """Update the starry background."""
    if len(stars) < settings.star_limit:
        new_star = Star(settings, screen, images)
        stars.add(new_star)
    stars.update()
    for star in stars.copy():
        if star.rect.right <= 0:
            stars.remove(star)


def spawn_enemy(settings, screen, id, enemies, images):
    """Spawn an enemy."""
    enemy = Enemy(settings, screen, id, images)
    enemy.x = settings.screen_width
    enemy.y = random.randint(0, settings.screen_height - enemy.rect.height)
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y
    enemies.add(enemy)


def explode(settings, entity, screen, images, explosions, sounds):
    """Spawn an explosion where an enemy (or the ship) dies."""
    sounds.boom_med.play()
    explosion = Explosion(settings, screen, images, entity.rect.center)
    explosions.add(explosion)


def spawn_pickup(entity, screen, images, pickups, type, scatter=False):
    """Spawn a pickup where an enemy dies."""
    if not scatter:
        center = entity.rect.center
    else:
        center = (entity.rect.center[0] + random.randint(-25, 25),
                  entity.rect.center[1] + random.randint(-25, 25))
    pickup = Pickup(images, screen, center, type)
    pickups.add(pickup)


def update_enemy_stuff(settings, screen, ship, enemies, sounds, stats,
                       explosions, images, pickups, hud):
    """Update the enemies, pickups, and explosions."""
    enemies.update()
    explosions.update()
    pickups.update()
    for enemy in enemies.sprites():
        if enemy.health <= 0:
            if random.randint(1, 100) <= settings.powerup_chance:
                spawn_pickup(enemy, screen, images, pickups, "p")
            explode(settings, enemy, screen, images, explosions, sounds)
            enemies.remove(enemy)
            print("RIP enemy")
        if enemy.rect.right <= 0:
            enemies.remove(enemy)
            print("Miss")
    for explosion in explosions.sprites():
        if explosion.countdown == 0:
            explosions.remove(explosion)
    for pickup in pickups.sprites():
        if (pickup.rect.right <= 0 or
                pickup.rect.left >= settings.screen_width or
                pickup.rect.bottom <= 0 or
                pickup.rect.top >= settings.screen_height):
            pickups.remove(pickup)
    check_enemy_ship_collisions(settings, screen, enemies, ship, stats, sounds,
                                images, explosions, pickups, hud)
    check_pickup_collisions(settings, screen, ship, pickups, stats, sounds)


def fire_bullet(settings, screen, ship, bullets, sounds, stats):
    """Fire a pattern of bullets based on the ship's level."""
    if len(bullets) < settings.bullet_limit:
        if stats.ship_level == 0:
            bullet1 = Bullet(settings, screen, ship)
        if stats.ship_level == 1:
            bullet1 = Bullet(settings, screen, ship, damage=2, height=4)
        if stats.ship_level == 2:
            bullet1 = Bullet(settings, screen, ship, y_offset=6)
            bullet2 = Bullet(settings, screen, ship, y_offset=-6)
            bullets.add(bullet2)
        if stats.ship_level >= 3:
            bullet1 = Bullet(settings, screen, ship, 6, 4, 15, 2)
            bullet2 = Bullet(settings, screen, ship, -6, 4, 15, 2)
            bullets.add(bullet2)
        bullets.add(bullet1)
        sounds.pew.play()


def update_bullets(settings, screen, ship, bullets, enemies, sounds):
    """Update position of bullets, deleting the ones offscreen."""
    # Update bullet positions.
    bullets.update()
    # Delete offscreen bullets.
    for bullet in bullets.copy():
        if bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)
    check_bullet_collisions(settings, screen, enemies, bullets, sounds)


def check_bullet_collisions(settings, screen, enemies, bullets, sounds):
    """Respond to bullet-enemy collisions."""
    for enemy in enemies:
        collision = pygame.sprite.spritecollide(enemy, bullets, True)
        for bullet in collision:
            enemy.health -= bullet.damage
            sounds.hit.play()


def check_pickup_collisions(settings, screen, ship, pickups, stats, sounds):
    """Respond to ship-pickup collisions."""
    for pickup in pickups.sprites():
        if pygame.sprite.collide_rect(ship, pickup) and ship.ready:
            sounds.levelup.play()
            print("Level up!")
            stats.ship_level += 1
            pickups.remove(pickup)


def check_enemy_ship_collisions(settings, screen, enemies, ship, stats,
                                sounds, images, explosions, pickups, hud):
    """Respond to enemy-ship collisions."""
    for enemy in enemies.sprites():
        if pygame.sprite.collide_circle(ship, enemy) and enemy.can_damage_ship:
            enemy.health -= 1
            enemy.can_damage_ship = False
            if stats.ship_health > 1:
                stats.ship_health -= 1
                print("Ouch")
                sounds.hit.play()
            else:
                print("Rip you")
                stats.ship_health -= 1
                stats.ship_lives -= 1
                hud.prep_life_amount()
                explode(settings, ship, screen, images, explosions, sounds)
                ship.reset_pos()
                while stats.ship_level > 0:
                    stats.ship_level -= 1
                    spawn_pickup(ship, screen, images, pickups, "p", True)


def update_screen(settings, screen, stars, ship, bullets, enemies, explosions,
                  pickups, hud, stats):
    """Update and flip any images onscreen."""
    screen.fill(settings.black)
    hud.update(stats)
    # Stars under everything
    for star in stars.sprites():
        star.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for enemy in enemies.sprites():
        enemy.blitme()
    for explosion in explosions.sprites():
        explosion.blitme()
    for pickup in pickups.sprites():
        pickup.blitme()
    ship.blitme()
    pygame.display.flip()
