import motor
import time

# wait 5 seconds to give time to go look at the motor before it starts
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
