import elevator
import motor
import os
import pygame
import time
import touch

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_AUDIODRIVER', 'dummy')

PINK = (255,105,180)

# Let touch init pygame
touch.beforePygameInit()
pygame.init()

surfaceSize = (320, 240)

lcd = pygame.display.set_mode(surfaceSize)
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))

def drawButton():
    # todo: draw a button
    pygame.draw.circle(lcd, PINK, (100,100), 50)

drawButton()
pygame.display.update()

time.sleep(10)
exit(0)

upImg = pygame.image.load('img/up.png').convert()
upActiveImg = pygame.image.load('img/up_active.png').convert()
downImg = pygame.image.load('img/down.png').convert()
downActiveImg = pygame.image.load('img/down_active.png').convert()

print("rect %s"%upImg.get_rect())

MARGIN = 25
# up / down are squares
IMGSIZE = 100
Y_CENTER = int((surfaceSize[1] / 2) - (IMGSIZE / 2))

upPos = (MARGIN, Y_CENTER)
downPos = (surfaceSize[0] - IMGSIZE - MARGIN, Y_CENTER)

# Positions do not change, get them once to use for collision detection
upRect:pygame.Rect = upImg.get_rect().move(upPos[0], upPos[1])
downRect:pygame.Rect = downImg.get_rect().move(downPos[0], downPos[1])

# max number of steps to go continuously as a failsafe
MAXSTEPS = 2000
DISPLAY_DELAY = 0.1

class App(object):
    _up = False
    _down = False
    running = True
    delay = DISPLAY_DELAY

    def __init__(self) -> None:
        # paint the initial state
        self.refresh()

    def refresh(self):
        lcd.fill((0,0,0))
        if self._up:
            lcd.blit(upActiveImg, upPos)
        else:
            lcd.blit(upImg, upPos)
        if self._down:
            lcd.blit(downActiveImg, downPos)
        else:
            lcd.blit(downImg, downPos)
        pygame.display.update()

    def up(self):
        self._up = True
        self._down = False
        # delay built into movement
        self.delay = 0.00001
        self.refresh()

    def down(self):
        self._up = False
        self._down = True
        # delay built into movement
        self.delay = 0.00001
        self.refresh()

    def stop(self):
        self._up = False
        self._down = False
        # switch to the slower delay since we do not need to drive motors
        self.delay = DISPLAY_DELAY
        self.refresh()

    def stopped(self):
        return not self._up and not self._down

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.MOUSEBUTTONUP:
            print('mouse up!')
            self.stop()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse down')
            if not self.stopped():
                self.stop()
            x, y = pygame.mouse.get_pos()
            print('position found: x %s y %s'%(x,y))
            if upRect.collidepoint(x, y):
                print('coliding with up image position')
                self.up()
            elif downRect.collidepoint(x, y):
                print('coliding with down image')
                self.down()

    _motorStopped = False

    def stopMotor(self):
        # todo: something to do motor break in a less noisy way
        self._motorStopped = True

    def startMotor(self):
        # todo: possibly switch motor controls back to non PWM mode if that was used during stopped state
        self._motorStopped = False

    _steps = 0
    def handleMotor(self):
        if self.stopped():
            if not self._motorStopped:
                self.stopMotor()
            # nothing else to do this tick
            return

        if self._steps > MAXSTEPS:
            print('Failsafe: stopping movement after %s max continuous steps.'%MAXSTEPS)
            self.stop()
            self.stopMotor()

        if self._motorStopped:
            # Previously stopped but need to start moving
            self.startMotor()
            self._steps = 0

        self._steps += 1

        if self._up:
            motor.manySteps(motor.UP, 50)
        elif self._down:
            motor.manySteps(motor.DOWN, 50)

    def tick(self):
        touch.tick()
        for event in pygame.event.get():
            self.handleEvent(event)
        self.handleMotor()
        if self.stopped():
            # If stopped, add delay... (if not stopped, will have delay built in to motor movement)
            time.sleep(DISPLAY_DELAY)

app = App()
while app.running:
    app.tick()
