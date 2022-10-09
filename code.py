import menu.elevator_floors
import touchscreen
from time import monotonic, sleep
import elevator

TIMEOUT_MINUTES = 5

print("Initializing elevator...")
lift = elevator.Elevator()

print("Drawing menu...")
menu.elevator_floors.drawMenu()
menu.elevator_floors.drawCurrentFloor(1)

print("Starting run loop...")

timeoutAfter = 0


def goToFloor(floor: int) -> None:
    print("going to floor %s..." % floor)
    menu.elevator_floors.drawCurrentFloor(floor)
    lift.goToFloor(floor)


while True:
    sleep(.1)
    p = touchscreen.ts.touch_point
    if p:
        print("x %s y %s z %s" % p)
        floor = menu.elevator_floors.whichFloor(p[0], p[1])
        if (floor > 0):
            goToFloor(floor)

        if (lift.isBraked()):
            # Update timeout to be 5 min after last touch (even if not touched on button)
            timeoutAfter = monotonic() + (60*TIMEOUT_MINUTES)
        else:
            timeoutAfter = 0

    if (timeoutAfter > 0 and monotonic() > timeoutAfter):
        # go to floor 1 to save energy on motor brake
        print("Timeout reached of %s minutes, going to floor 1" %
              TIMEOUT_MINUTES)
        goToFloor(1)
        timeoutAfter = 0
