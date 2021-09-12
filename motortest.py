import motor
import time


time.sleep(5)
print('going forward 1 turn...')
for i in range(200):
    motor.onestep(motor.FORWARD)

time.sleep(5)
print('going backward 1 turn...')
for i in range(800):
    motor.onestep(motor.BACKWARD)
print('done!')
