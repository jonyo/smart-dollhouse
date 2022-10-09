# Simple stepper motor control

import time
import board
import digitalio

"""State for EN pin so that the stepper is active (will not allow moving, and may buzz)"""
ENABLED = True

"""State for EN pin so that the stepper is disabled (free moving, not locked in place, no buzz)"""
DISABLED = False

# Intended to wire MS1, MS2, MS3 directly to 3.3 logic high to control, not set up to be controlled with IO pins

"""Full step, pins expected to be wired: MS1 = low, MS2 = low, MS3 = low"""
FULL_STEP = 1
"""1/2 microstep, pins expected to be wired: MS1 = high, MS2 = low, MS3 = low"""
HALF_STEP = 2
"""1/4 microstep, pins expected to be wired: MS1 = low, MS2 = high, MS3 = low"""
QUARTER_STEP = 4
"""1/8 microstep, pins expected to be wired: MS1 = high, MS2 = high, MS3 = low"""
EIGHTH_STEP = 8
"""1/16 microstep, pins expected to be wired: MS1 = high, MS2 = high, MS3 = high"""
SIXTEENTH_STEP = 16


class Speed(object):
    def __init__(self, delay, style) -> None:
        self.delay = delay
        self.stepMode = style

# Experiments - Will need to be re-done if changing power supply or adjusting output POT on the A4988

# FULL 0.00100 -


currentSpeed = Speed(.001, FULL_STEP)


class Motor(object):
    def __init__(self) -> None:
        self.enablePin = digitalio.DigitalInOut(board.GP15)
        self.stepPin = digitalio.DigitalInOut(board.GP12)
        self.dirPin = digitalio.DigitalInOut(board.GP13)

        self.stepPin.direction = digitalio.Direction.OUTPUT
        self.dirPin.direction = digitalio.Direction.OUTPUT
        self.enablePin.direction = digitalio.Direction.OUTPUT

        # Start off with it disengaged
        self.enablePin.value = DISABLED

    def __del__(self):
        self.enablePin.value = DISABLED


UP = False
DOWN = True

_motor = Motor()


def onestep(direction):
    _motor.enablePin.value = ENABLED
    _motor.dirPin.value = direction
    _motor.stepPin.value = True
    time.sleep(currentSpeed.delay)
    _motor.stepPin.value = False


def manySteps(direction, steps):
    count = 0
    while count < steps:
        onestep(direction)
        count += 1
        time.sleep(currentSpeed.delay)


def engage():
    _motor.enablePin.value = ENABLED


def release():
    _motor.enablePin.value = DISABLED


def isEngaged() -> bool:
    return _motor.enablePin.value == ENABLED
