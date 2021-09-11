import pygame
import time
import os
import evdev
import select

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_AUDIODRIVER', 'dummy')

surfaceSize = (320, 240)

pygame.init()

lcd = pygame.display.set_mode(surfaceSize)
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))

upImg = pygame.image.load('img/up.png')
lcd.blit(upImg, (25, (surfaceSize[1] / 2) - 50))

downImg = pygame.image.load('img/down.png')
lcd.blit(downImg, (surfaceSize[0] - 125, (surfaceSize[1] / 2) - 50))

def up(x,y):
    lcd.blit(upImg, (x,y))

pygame.display.update()
# Used to map touch event from the screen hardware to the pygame surface pixels.
# (Those values have been found empirically, but I'm working on a simple interactive calibration tool
tftOrig = (3750, 180)
tftEnd = (150, 3750)
tftDelta = (tftEnd [0] - tftOrig [0], tftEnd [1] - tftOrig [1])
tftAbsDelta = (abs(tftEnd [0] - tftOrig [0]), abs(tftEnd [1] - tftOrig [1]))

def refresh():
    pygame.display.update()
    time.sleep(0.1)

# We use evdev to read events from our touchscreen
# (The device must exist and be properly installed for this to work)
touch = evdev.InputDevice('/dev/input/touchscreen')

# We make sure the events from the touchscreen will be handled only by this program
# (so the mouse pointer won't move on X when we touch the TFT screen)
touch.grab()
# Prints some info on how evdev sees our input device
print(touch)
# Even more info for curious people
#print(touch.capabilities())

# Here we convert the evdev "hardware" touch coordinates into pygame surface pixel coordinates
def getPixelsFromCoordinates(coords):
    # TODO check divide by 0!
    if tftDelta [0] < 0:
        x = float(tftAbsDelta [0] - coords [0] + tftEnd [0]) / float(tftAbsDelta [0]) * float(surfaceSize [0])
    else:
        x = float(coords [0] - tftOrig [0]) / float(tftAbsDelta [0]) * float(surfaceSize [0])
    if tftDelta [1] < 0:
        y = float(tftAbsDelta [1] - coords [1] + tftEnd [1]) / float(tftAbsDelta [1]) * float(surfaceSize [1])
    else:
        y = float(coords [1] - tftOrig [1]) / float(tftAbsDelta [1]) * float(surfaceSize [1])
    return (int(x), int(y))

# Was useful to see what pieces I would need from the evdev events
def printEvent(event):
    print(evdev.categorize(event))
    print("Value: {0}".format(event.value))
    print("Type: {0}".format(event.type))
    print("Code: {0}".format(event.code))

# This loop allows us to write red dots on the screen where we touch it
while True:
    # TODO get the right ecodes instead of int
    r,w,x = select.select([touch], [], [])
    for event in touch.read():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == 1:
                X = event.value
            elif event.code == 0:
                Y = event.value
        elif event.type == evdev.ecodes.EV_KEY:
            if event.code == 330 and event.value == 1:
                printEvent(event)
                p = getPixelsFromCoordinates((X, Y))
                print("TFT: {0}:{1} | Pixels: {2}:{3}".format(X, Y, p [0], p [1]))
                pygame.draw.circle(lcd, (255, 0, 0), p , 2, 2)
                refresh()
