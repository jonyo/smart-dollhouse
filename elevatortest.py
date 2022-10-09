import elevator
import time

lift = elevator.Elevator()

floors = [2, 3, 1]
print("I hope you remembered: start out at bottom!!!")
print("You have 3 seconds to stop it if not!")
time.sleep(3)
for floor in floors:
    print("going to floor %s"%floor)
    lift.goToFloor(floor)
    print("Done!")
    print("Now on floor %s at position %s"%(floor, lift.pos))
    time.sleep(3)

print("Elevator tour is complete!")
