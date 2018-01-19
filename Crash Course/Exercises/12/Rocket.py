# Have a rocket centered on the screen that can move in all 4 directions.
import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((800, 800))
rocket = pygame.image.load('rocket.png')
pygame.display.set_caption("Movable Rocket")
rocketrect = rocket.get_rect()
screen_rect = screen.get_rect()
rocketrect.centerx = screen_rect.centerx
rocketrect.centery = screen_rect.centery
centerx = float(rocketrect.centerx)
centery = float(rocketrect.centery)
moving_right = False
moving_left = False
moving_up = False
moving_down = False


def update(rocket):
    global centerx, centery, moving_right, moving_left, moving_up, moving_down
    if moving_right and rocketrect.right < screen_rect.right:
        centerx += 1
    if moving_left and rocketrect.left > 0:
        centerx -= 1
    if moving_up and rocketrect.top > 0:
        centery -= 1
    if moving_down and rocketrect.bottom < screen_rect.bottom:
        centery += 1
    rocketrect.centerx = centerx
    rocketrect.centery = centery


def check_keydown_events(event):
    """Respond to keypresses."""
    global moving_right, moving_left, moving_up, moving_down
    if event.key == pygame.K_RIGHT:
        moving_right = True
    if event.key == pygame.K_LEFT:
        moving_left = True
    if event.key == pygame.K_UP:
        moving_up = True
    if event.key == pygame.K_DOWN:
        moving_down = True


def check_keyup_events(event):
    """Respond to key releases."""
    global moving_right, moving_left, moving_up, moving_down
    if event.key == pygame.K_RIGHT:
        moving_right = False
    if event.key == pygame.K_LEFT:
        moving_left = False
    if event.key == pygame.K_UP:
        moving_up = False
    if event.key == pygame.K_DOWN:
        moving_down = False


def check_events():
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event)
        elif event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_keyup_events(event)


while True:
    screen.blit(rocket, rocketrect)
    check_events()
    update(rocket)
    pygame.display.flip()
