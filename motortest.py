import motor
import time


time.sleep(5)
print('going forward 1 turn...')
for i in range(motor.STEPS * 5):
    motor.onestep(motor.FORWARD)

time.sleep(5)
print('going backward 1 turn...')
for i in range(motor.STEPS * 5):
    motor.onestep(motor.BACKWARD)

motor.release()
print('done!')
