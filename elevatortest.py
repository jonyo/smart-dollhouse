import elevator
import iobuttons
import time

lift = elevator.Elevator()

floors = [3]
print("I hope you remembered: start out at bottom!!!")
print("You have 5 seconds to stop it if not!")
time.sleep(5)
for floor in floors:
    print("going to floor %s"%floor)
    lift.goToFloor(floor)
    print("Done!")
    print("Now on floor %s at position %s"%(floor, lift.pos))
    time.sleep(5)

print("Elevator tour is complete!")
