import motor
import time

# wait 5 seconds to give time to go look at the motor before it starts
time.sleep(5)
print('going forward 3 turns...')
for i in range(motor.STEPS * 3):
    motor.onestep(motor.UP)
    time.sleep(motor.DELAY)

time.sleep(5)
print('going backward 3 turns...')
for i in range(motor.STEPS * 3):
    motor.onestep(motor.DOWN)
    time.sleep(motor.DELAY)

motor.release()
print('done!')
