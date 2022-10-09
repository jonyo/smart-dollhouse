import menu.elevator_floors
import touchscreen
from time import sleep, time
import elevator

print("Initializing elevator...")
lift = elevator.Elevator()

print("Drawing menu...")
menu.elevator_floors.drawMenu()
menu.elevator_floors.drawCurrentFloor(1)

print("Starting run loop...")

timeout = 0

while True:
    sleep(.1)
    p = touchscreen.ts.touch_point
    if p:
        print("x %s y %s z %s" % p)
        floor = menu.elevator_floors.whichFloor(p[0], p[1])
        if (floor > 0):
            print("going to floor %s" % floor)
            menu.elevator_floors.drawCurrentFloor(floor)
            lift.goToFloor(floor)
            if (floor == 1):
                lift.release()

        if (lift.isBraked()):
            timeout = time() + 60*5  # 5 minutes from now
        else:
            timeout = 0

    if (timeout > 0 and time() > timeout):
        # go to floor 1 to save energy on motor brake
        lift.goToFloor(1)
