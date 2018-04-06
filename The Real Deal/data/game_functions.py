import pygame
import pygame.gfxdraw
import random
from entities import Star, Bullet, Enemy, EnemyBullet, Explosion, Pickup
angle = 0


def check_events(settings, screen, ship, gamepad, bullets, stats, sounds,
                 enemies, images, enemy_bullets):
    """Respond to key, gamepad, and mouse events."""
    if stats.game_active:
        check_repeat_keys(settings, screen, ship, bullets, stats, gamepad,
                          sounds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.done = True
        if event.type == pygame.KEYDOWN:
            check_debug_keys(event, settings, screen, enemies, images, stats,
                             ship, enemy_bullets)
        if stats.game_active:
            if event.type == pygame.KEYDOWN:
                check_keydown_events(event, settings, ship)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, settings, ship)
            elif event.type == pygame.JOYAXISMOTION:
                check_analog_events(gamepad, ship, settings)
            elif event.type == pygame.JOYHATMOTION:
                check_hat_events(gamepad, ship, settings)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == settings.but_B:
                    ship.dodge_mode = True
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == settings.but_B:
                    ship.dodge_mode = False


def check_repeat_keys(settings, screen, ship, bullets, stats, gamepad, sounds):
    """Check for keys that will repeat an action when held."""
    keys = pygame.key.get_pressed()
    if not ship.dodge_mode:
        if settings.autofire and stats.bullet_cooldown == 0:
            fire_bullet(settings, screen, ship, bullets, sounds, stats)
            stats.bullet_cooldown = settings.bullet_cooldown
        if not settings.autofire:
            if ((keys[pygame.K_SPACE] or keys[pygame.K_z])
                    and stats.bullet_cooldown == 0):
                fire_bullet(settings, screen, ship, bullets, sounds, stats)
                stats.bullet_cooldown = settings.bullet_cooldown
            if settings.gamepad_connected:
                if (gamepad.get_button(settings.but_A) and
                        stats.bullet_cooldown == 0):
                    fire_bullet(settings, screen, ship, bullets, sounds, stats)
                    stats.bullet_cooldown = settings.bullet_cooldown
        # If autofire is on, hold a fire button to NOT fire.
        elif keys[pygame.K_SPACE] or keys[pygame.K_z]:
            stats.bullet_cooldown = settings.bullet_cooldown
        elif settings.gamepad_connected:
            if gamepad.get_button(settings.but_A):
                stats.bullet_cooldown = settings.bullet_cooldown
        if stats.bullet_cooldown > 0:
            stats.bullet_cooldown -= 1


def check_keydown_events(event, settings, ship):
    """Respond to pressed keys."""
    # Note: Any wacky keypress limits are your keyboard's fault.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_x:
        ship.dodge_mode = True
    if event.key == pygame.K_a:
        settings.autofire = True if settings.autofire is False else False


def check_debug_keys(event, settings, screen, enemies, images, stats, ship,
                     enemy_bullets):
    global angle
    if event.key == pygame.K_ESCAPE:
        stats.done = True
    # There's definitely a better way to do this, but none of these will be in
    # the final product anyway
    if event.key == pygame.K_1:
        spawn_enemy(settings, screen, enemies, images, 1)
    if event.key == pygame.K_2:
        spawn_enemy(settings, screen, enemies, images, 2)
    if event.key == pygame.K_3:
        spawn_enemy(settings, screen, enemies, images, 3)
    if event.key == pygame.K_4:
        spawn_enemy(settings, screen, enemies, images, 4)
    if event.key == pygame.K_5:
        spawn_enemy(settings, screen, enemies, images, 5)
    if event.key == pygame.K_6:
        spawn_enemy(settings, screen, enemies, images, 6)
    if event.key == pygame.K_l:
        print("Level up!")
        stats.ship_level += 1
    if event.key == pygame.K_p:
        stats.game_active = True if stats.game_active is False else False
    if event.key == pygame.K_r:
        ship.reset_pos()


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
    if event.key == pygame.K_x:
        ship.dodge_mode = False


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


def spawn_enemy(settings, screen, enemies, images, id):
    """Spawn an enemy."""
    enemy = Enemy(settings, screen, images, id)
    enemy.x = settings.screen_width
    enemy.y = random.randint(0, settings.screen_height - enemy.rect.height)
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y
    enemies.add(enemy)


def explode(settings, entity, screen, images, explosions, sounds, size="s"):
    """Spawn an explosion where an enemy (or the ship) dies."""
    if size == "s":
        sounds.boom_small.play()
        explosion = Explosion(settings, screen, images, entity.rect.center)
    elif size == "l":
        sounds.boom_med.play()
        explosion = Explosion(settings, screen, images, entity.rect.center,
                              "l")
    explosions.add(explosion)


def spawn_pickup(entity, settings, stats, screen, images, pickups, type=None,
                 scatter=False):
    """Spawn a pickup where something dies."""
    if type is None:
        if stats.ship_health < settings.ship_health:
            type = random.choice(["p", "h"])
        else:
            type = "p"
    if not scatter:
        center = entity.rect.center
    else:
        center = (entity.rect.center[0] + random.randint(-25, 25),
                  entity.rect.center[1] + random.randint(-25, 25))
    pickup = Pickup(images, screen, center, type)
    pickups.add(pickup)


def update_enemy_stuff(settings, screen, ship, enemies, sounds, stats,
                       explosions, images, pickups, hud,):
    """Update the enemies, pickups, and explosions."""
    enemies.update()
    explosions.update()
    pickups.update()
    for enemy in enemies.sprites():
        if enemy.health <= 0:
            if random.randint(1, 100) <= settings.powerup_chance:
                spawn_pickup(enemy, settings, stats, screen, images, pickups)
            if enemy.id is not 2:
                explode(settings, enemy, screen, images, explosions, sounds)
            else:
                explode(settings, enemy, screen, images, explosions, sounds,
                        "l")
            enemies.remove(enemy)
        if enemy.rect.right <= 0:
            enemies.remove(enemy)
            print("Miss! You would lose score if it existed.")
        if pygame.sprite.collide_circle(ship, enemy) and not stats.ship_inv:
            enemy.health -= 1
            damage_ship(settings, stats, sounds, ship, hud, screen, images,
                        explosions, pickups)
    for explosion in explosions.sprites():
        if explosion.countdown == 0:
            explosions.remove(explosion)
    for pickup in pickups.sprites():
        if (pickup.rect.right <= 0 or
                pickup.rect.left >= settings.screen_width or
                pickup.rect.bottom <= 0 or
                pickup.rect.top >= settings.screen_height):
            pickups.remove(pickup)
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
        if stats.ship_level == 3:
            bullet1 = Bullet(settings, screen, ship, y_offset=6)
            bullet2 = Bullet(settings, screen, ship, y_offset=-6)
            bullet3 = Bullet(settings, screen, ship, speed=21)
            bullets.add(bullet2, bullet3)
        if stats.ship_level >= 4:
            bullet1 = Bullet(settings, screen, ship, y_offset=6)
            bullet2 = Bullet(settings, screen, ship, y_offset=-6)
            bullet3 = Bullet(settings, screen, ship, 0, 4, 15, 2, 21)
            bullets.add(bullet2, bullet3)
        bullets.add(bullet1)
        sounds.pew.play()


def update_bullets(settings, screen, ship, bullets, enemies, sounds,
                   enemy_bullets):
    """Update the position of bullets, deleting the ones offscreen."""
    # Update bullet positions.
    bullets.update()
    enemy_bullets.update()
    # Delete offscreen bullets.
    for bullet in bullets.copy():
        if bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)
    for bullet in enemy_bullets.copy():
        if (bullet.rect.left >= settings.screen_width or
                bullet.rect.right <= 0 or
                bullet.rect.top >= settings.screen_height or
                bullet.rect.bottom <= 0):
            enemy_bullets.remove(bullet)
    check_bullet_collisions(settings, screen, enemies, bullets, sounds, ship)


def check_bullet_collisions(settings, screen, enemies, bullets, sounds, ship):
    """Respond to bullet-enemy or bullet-ship collisions."""
    for enemy in enemies.sprites():
        if enemy.id is not 3:
            # Enemy 3 isn't a circle.
            collide = pygame.sprite.spritecollide(enemy, bullets, True,
                                                  pygame.sprite.collide_circle)
        else:
            collide = pygame.sprite.spritecollide(enemy, bullets, True)
        for bullet in collide:
            enemy.health -= bullet.damage
            sounds.enemy_hit.play()


def check_pickup_collisions(settings, screen, ship, pickups, stats, sounds):
    """Respond to ship-pickup collisions."""
    for pickup in pickups.sprites():
        if pygame.sprite.collide_rect(ship, pickup) and ship.ready:
            sounds.levelup.play()
            if pickup.type == "h" and stats.ship_health < settings.ship_health:
                stats.ship_health += 1
            else:
                # If you get health when you don't need it, you just level up.
                stats.ship_level += 1
            pickups.remove(pickup)


def damage_ship(settings, stats, sounds, ship, hud, screen, images, explosions,
                pickups):
    """Damage the ship."""
    if stats.ship_health > 1:
        stats.ship_health -= 1
        if stats.ship_level > 0:
            sounds.leveldown.play()
            stats.ship_level -= 1
        stats.ship_inv_timer = settings.ship_mercy_inv
        sounds.ship_hit.play()
    else:
        stats.ship_health -= 1
        stats.ship_lives -= 1
        hud.prep_life_amount()
        explode(settings, ship, screen, images, explosions, sounds)
        ship.reset_pos()
        while stats.ship_level > 0:
            stats.ship_level -= 1
            spawn_pickup(ship, settings, stats, screen, images, pickups, "p",
                         True)


def update_screen(settings, screen, stars, ship, bullets, enemies, explosions,
                  pickups, hud, stats, enemy_bullets):
    """Update and flip any images onscreen."""
    screen.fill(settings.black)
    for star in stars.sprites():
        star.blitme()
    hud.update(stats)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in enemy_bullets.sprites():
        bullet.blitme()
    for enemy in enemies.sprites():
        enemy.blitme()
    for explosion in explosions.sprites():
        explosion.blitme()
    for pickup in pickups.sprites():
        pickup.blitme()
    ship.blitme()
    pygame.display.flip()
