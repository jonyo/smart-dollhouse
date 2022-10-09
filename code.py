import touchscreen
import displayio
import adafruit_display_shapes.circle as circle
from time import sleep
import elevator

print("Initializing elevator...")
lift = elevator.Elevator()

print("waiting 2 seconds...")
sleep(2)
print("going to floor 2")
# lift.goToFloor(2)

splash = displayio.Group()

touchscreen.display.show(splash)

color_bitmap = displayio.Bitmap(480, 320, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x550000  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(200, 400, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

print("Done showing")

while True:
    sleep(.1)
    p = touchscreen.ts.touch_point
    if p:
        print("x %s y %s z %s"%p)
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
