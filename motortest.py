import motor
import time

# wait 5 seconds to give time to go look at the motor before it starts
print('Waiting 5 seconds, look at it to see what it does!')
time.sleep(5)
print('going up 30 steps...')
motor.manySteps(motor.UP, 30)

print('done, waiting 5 seconds')

time.sleep(5)

print('going down 30 steps...')

motor.manySteps(motor.DOWN, 30)

motor.release()
print('done!')
