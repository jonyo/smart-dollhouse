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

if MICRO == None:
    # From the top: black green red blue
    coils = (
        digitalio.DigitalInOut(board.D19), # A1
        digitalio.DigitalInOut(board.D26), # A2
        digitalio.DigitalInOut(board.D20), # B1
        digitalio.DigitalInOut(board.D21), # B2
    )
else:
    # From the top: black green red blue
    coils = (
        pwmio.PWMOut(board.D19), # A1
        pwmio.PWMOut(board.D26), # A2
        pwmio.PWMOut(board.D20), # B1
        pwmio.PWMOut(board.D21), # B2
    )



for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=MICRO)

FORWARD = stepper.FORWARD
BACKWARD = stepper.BACKWARD

def onestep(direction):
    motor.onestep(style=STYLE, direction=direction)
    time.sleep(DELAY)

def release():
    motor.release()
