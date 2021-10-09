import pygame
import evdev
from evdev import ecodes
import os

class TouchAxis(object):
    def __init__(self, min: int, max: int, invert: bool) -> None:
        if min > max:
            # is all good, just fix it...
            print("Normally min is less than max, auto correcting by swapping values...")
            realMin = max
            max = min
            min = realMin
            del realMin
            invert = not invert
        # keep track of original values for debugging
        self.min = min
        self.max = max
        self.invert = invert
        # we do as much manipulation during init so those parts are only done once at the start
        self.offset = min
        self.delta = max - min
        # prevent config issues leading to divide by 0 errors
        assert self.delta is not 0
        self.invert = invert

    def scale(self, value) -> float:
        """ Scales the value to be 0 to 1 based on original min/max """
        value -= self.offset
        # if out of bounds, set to min or max
        if value > self.delta:
            return 1.0
        if value <= 0:
            return 0.0
        if self.invert:
            value = self.delta - value
        return float(value) / float(self.delta)

class TouchHandler(object):
    """ LCD pixel screen size (resolution) to translate touch coordinates onto """
    surfaceSize = (320, 240)

    """ TouchAxis details for x axis, callibrated for the 2.8" PiTFT Plus, would need adjustment for another device. """
    xTouch = TouchAxis(min=180, max=3750, invert=False)

    """ TouchAxis details for x axis, callibrated for the 2.8" PiTFT Plus, would need adjustment for another device. """
    yTouch = TouchAxis(min=150, max=3750, invert=True)

    """ Latest x value reported by evdev events """
    x_val = None

    """ Latest y value reported by evdev events """
    y_val = None

    # going from evdev x/y values to touchscreen, is x and y swapped?  Normally yes but maybe you want different
    # orientation, if so set to False
    """ Going from evdev reported x/y values for touchscreen, to the coords on the display, are the axis swapped?"""
    swapAxis = True

    """ for touch event, code for touch end / key up """
    KEY_UP = 0

    """ for touch event, code for touch start / key down """
    KEY_DOWN = 1

    def _screenCoords(self):
        """ calculate the surface screen coordinates of the last x/y reported values from evdev """
        assert self.x_val is not None and self.y_val is not None
        if self.swapAxis:
            x = self.yTouch.scale(self.y_val)
            y = self.xTouch.scale(self.x_val)
        else:
            x = self.xTouch.scale(self.x_val)
            y = self.yTouch.scale(self.y_val)
        return (
            int(x * self.surfaceSize[0]),
            int(y * self.surfaceSize[1])
        )

    def handleEvent(self, event: evdev.events.InputEvent or None) -> None:
        """ Handle an InputEvent from evdev """
        if event == None:
            return

        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                self.x_val = event.value
            elif event.code == ecodes.ABS_Y:
                self.y_val = event.value

            if self.x_val is not None and self.y_val is not None:
                (posx, posy) = self._screenCoords()
                print("abs: x: %s y: %s - screen pixel x: %s y: %s"%( self.x_val, self.y_val, posx, posy ))
                pygame.mouse.set_pos(posx, posy)
                self.x_val = None
                self.y_val = None

        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_TOUCH:
                # this is actually the only key event reported by touchscreen, still it is good to check...
                if event.value == self.KEY_DOWN:
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
                elif event.value == self.KEY_UP:
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP))

touch = evdev.InputDevice('/dev/input/touchscreen')
touch.grab()
handler = TouchHandler()

def beforePygameInit():
    """ Call before pygame.init() is called to initialize needed env vars specific to touch events """
    # stop reading events by pygame engine to avoid erratic mouse pointer behaviour
    os.putenv('SDL_MOUSEDEV', '/dev/null')

def tick() -> None:
    """ Get the relevent touch events and add to pygame, call before attempting to process pygame events """
    while True:
        # can't use select, we need it to be non-blocking...
        event = touch.read_one()
        if event == None:
            # no more events this tick, break out of our little infinite loop we had going
            break
        handler.handleEvent(event)
