import pygame
import evdev
import os
from collections import namedtuple

# surface resolution
surfaceSize = (320, 240)

# Used to map touch event from the screen hardware to the pygame surface pixels.
# Works with 320 x 240, would need to adjust to callibrate for other screen sizes
tftOrig = (3750, 180)
tftEnd = (150, 3750)
tftDelta = (tftEnd [0] - tftOrig [0], tftEnd [1] - tftOrig [1])
tftAbsDelta = (abs(tftDelta[0]), abs(tftDelta[1]))

# We use evdev to read events from our touchscreen
# (The device must exist and be properly installed for this to work)
touch = evdev.InputDevice('/dev/input/touchscreen')

# We make sure the events from the touchscreen will be handled only by this program
# (so the mouse pointer won't move on X when we touch the TFT screen)
touch.grab()

def printDebug():
    """ Print some info about the touch input device as evdev sees it """
    print(touch)

def printDebugMore():
    """ Print even more info about the touch input device as evdev sees it """
    print(touch.capabilities())

def getPixelsFromCoordinates(coords):
    """ Convert evdev "hardware" touch coordinates to pygame surface pixel coordinates """
    if tftDelta[0] < 0:
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

Event = namedtuple('Event', ('down', 'pos'))

class EventHandler(object):
    def tick(self):
        """ Get the relevent touch events and add to pygame, call before attempting to process pygame events """
        # can't use select, we need it to be non-blocking...
        # x and y updated in seperate events... keep track of one till the other comes in
        X = None
        Y = None
        while True:
            event = touch.read_one()
            if event == None:
                break

            if event.type == evdev.ecodes.EV_ABS:
                if event.code == 1:
                    X = event.value
                elif event.code == 0:
                    Y = event.value
                if X is not None and Y is not None:
                    (posx, posy) = getPixelsFromCoordinates((X, Y))
                    pygame.mouse.set_pos(posx, posy)
                    X = None
                    Y = None
            elif event.type == evdev.ecodes.EV_KEY:
                if event.code == 330:
                    printEvent(event)
                    if event.value == 1:
                        # mouse down
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
                    else:
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP))

_touch = EventHandler()

def beforePygameInit():
    """ Call before pygame.init() is called to initialize needed env vars specific to touch events """
    # stop reading events by pygame engine to avoid erratic mouse pointer behaviour
    os.putenv('SDL_MOUSEDEV', '/dev/null')

def tick():
    _touch.tick()
