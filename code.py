import menu.elevator_floors
import touchscreen
import adafruit_display_shapes.circle as circle
from time import sleep
import elevator

print("Initializing elevator...")
lift = elevator.Elevator()

print("waiting 2 seconds...")
sleep(2)
print("going to floor 2")
# lift.goToFloor(2)

menu.elevator_floors.drawMenu()

print("Done showing")

while True:
    sleep(.1)
    p = touchscreen.ts.touch_point
    if p:
        print("x %s y %s z %s" % p)
        # put a dot here
        dot = circle.Circle(
            x0=p[0],
            y0=p[1],
            r=5,
            fill=0xAA0088,
            outline=0xFFFF00
        )
        print("made a dot")
        splash.append(dot)
        print("going to floor 2")
        lift.goToFloor(2)
        print("keeping at floor for 3 seconds...")
        sleep(3)
        print("exiting!")
        break
