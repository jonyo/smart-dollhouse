# Simple stepper motor control

import time
import board
import digitalio
import pwmio

"""State for EN pin so that the stepper is active (will not allow moving, and may buzz)"""
ENABLED = False

"""State for EN pin so that the stepper is disabled (free moving, not locked in place, no buzz)"""
DISABLED = True

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
# SINGLE .0010 - goes BRRRRRZT
# SINGLE .0030 - skips 1cm total
# SINGLE .0040 - skips 1cm total
# SINGLE .0050 - slow but mostly works
# SINGLE .0100 - slips / misses steps
# SINGLE .0500 - slips / misses steps

# 1/4    .0045 - good but slow
# 1/4    .0020 - good, faster
# 1/4    .0010 - good, good speed

# 1/8    .0010 - Good, slow
# 1/8    .0005 - Great, perfect speed

# 1/16   .0005 - Good, slow
# 1/16   .0001 - Great, perfect speed


currentSpeed = Speed(.0001, SIXTEENTH_STEP)

class Motor(object):
    def __init__(self) -> None:
        self.step = digitalio.DigitalInOut(board.D19)
        self.dir = digitalio.DigitalInOut(board.D13)
        self.en = digitalio.DigitalInOut(board.D26)

        self.step.direction = digitalio.Direction.OUTPUT
        self.dir.direction = digitalio.Direction.OUTPUT
        self.en.direction = digitalio.Direction.OUTPUT

        # Start off with it disengaged
        self.en.value = DISABLED

    def __del__(self):
        self.en.value = DISABLED


UP = False
DOWN = True

_motor = Motor()

def onestep(direction):
    _motor.en.value = ENABLED
    _motor.dir.value = direction
    _motor.step.value = True
    time.sleep(currentSpeed.delay)
    _motor.step.value = False

def manySteps(direction, steps):
    count = 0
    while count < steps:
        onestep(direction)
        count += 1
        time.sleep(currentSpeed.delay)

def engage():
    _motor.en.value = ENABLED

def release():
    _motor.en.value = DISABLED
