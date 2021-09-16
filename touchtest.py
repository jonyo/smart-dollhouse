import pygame
import time
import os
import touch

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_AUDIODRIVER', 'dummy')

surfaceSize = (320, 240)

touch.beforePygameInit()
pygame.init()

lcd = pygame.display.set_mode(surfaceSize)
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# block all events
pygame.event.set_blocked(None)

# un-block events we care about
pygame.event.set_allowed(pygame.QUIT)
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
pygame.event.set_allowed(pygame.MOUSEMOTION)

running = True

# This loop allows us to write red dots on the screen where we touch it
while running:
    # process touch events
    touch.tick()
    # go through pygame event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            print('mouse up')

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse down')
            x, y = pygame.mouse.get_pos()
            print('position found: x %s y %s'%(x,y))
            pygame.draw.circle(lcd, (255, 0, 0), (x, y) , 2, 2)
            pygame.display.update()
    time.sleep(0.1)
