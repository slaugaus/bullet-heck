# Have a rocket centered on the screen that can move in all 4 directions.
import pygame
from pygame.joystick import Joystick
import sys
pygame.init()
screen = pygame.display.set_mode((800, 800))
rocket = pygame.image.load('rocket.png')
joystick = Joystick(0)
joystick.init()
clock = pygame.time.Clock()
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
an_up, an_down, an_left, an_right = 0, 0, 0, 0


def update_digital(rocket):
    global centerx, centery, moving_right, moving_left, moving_up, moving_down
    if moving_right and rocketrect.right < screen_rect.right:
        centerx += 10
    if moving_left and rocketrect.left > 0:
        centerx -= 10
    if moving_up and rocketrect.top > 0:
        centery -= 10
    if moving_down and rocketrect.bottom < screen_rect.bottom:
        centery += 10
    rocketrect.centerx = centerx
    rocketrect.centery = centery


def update_analog(rocket):
    global centerx, centery, an_up, an_down, an_left, an_right
    if an_right > 0 and rocketrect.right < screen_rect.right:
        centerx += an_right * 10
    if an_left < 0 and rocketrect.left > 0:
        centerx += an_left * 10
    if an_up < 0 and rocketrect.top > 0:
        centery += an_up * 10
    if an_down > 0 and rocketrect.bottom < screen_rect.bottom:
        centery += an_down * 10
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


def check_joy_events(event, joystick):
    global an_up, an_down, an_left, an_right
    global moving_right, moving_left, moving_up, moving_down
    if joystick.get_axis(0) >= 0.2:
        an_right = joystick.get_axis(0)
    if joystick.get_axis(0) <= -0.2:
        an_left = joystick.get_axis(0)
    if joystick.get_axis(1) >= 0.2:
        an_down = joystick.get_axis(1)
    if joystick.get_axis(1) <= -0.2:
        an_up = joystick.get_axis(1)
    if -0.2 <= joystick.get_axis(0) <= 0.2:
        an_left, an_right = 0, 0
    if -0.2 <= joystick.get_axis(1) <= 0.2:
        an_up, an_down = 0, 0


def check_events(joystick):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event)
        elif event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            check_keyup_events(event)
        elif event.type == pygame.JOYAXISMOTION:
            check_joy_events(event, joystick)


while True:
    screen.fill((0, 0, 0))
    screen.blit(rocket, rocketrect)
    check_events(joystick)
    update_digital(rocket)
    update_analog(rocket)
    clock.tick(60)
    print(clock.get_fps())
    pygame.display.flip()
