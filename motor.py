# Simple stepper motor test script

import time
import board
import digitalio
import pwmio
from adafruit_motor import stepper

DELAY = 0.003
STEPS = 200
MICRO = None
STYLE = stepper.SINGLE

class Motor(object):
    def __init__(self) -> None:
        if MICRO == None:
            # From the top: black green red blue
            self.coils = (
                digitalio.DigitalInOut(board.D19), # A1
                digitalio.DigitalInOut(board.D26), # A2
                digitalio.DigitalInOut(board.D20), # B1
                digitalio.DigitalInOut(board.D21), # B2
            )
        else:
            # From the top: black green red blue
            self.coils = (
                pwmio.PWMOut(board.D19), # A1
                pwmio.PWMOut(board.D26), # A2
                pwmio.PWMOut(board.D20), # B1
                pwmio.PWMOut(board.D21), # B2
            )
        for coil in self.coils:
            coil.direction = digitalio.Direction.OUTPUT
        self.motor = stepper.StepperMotor(self.coils[0], self.coils[1], self.coils[2], self.coils[3], microsteps=MICRO)

    def __del__(self):
        self.motor.release()

FORWARD = stepper.FORWARD
BACKWARD = stepper.BACKWARD

_motor = Motor()

def onestep(direction):
    _motor.motor.onestep(style=STYLE, direction=direction)
    time.sleep(DELAY)

def manySteps(direction, steps):
    count = 0
    while count < steps:
        onestep(direction)
        count += 1

def release():
    _motor.motor.release()
