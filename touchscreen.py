from time import sleep
import displayio
import board
import busio
import displayio
from adafruit_hx8357 import HX8357
import adafruit_touchscreen

print("Initializing display...")
# wait a little to give time for the display to initialize internally
sleep(.1)

displayio.release_displays()

# PICO

xminus = board.GP26 # pin 31 (analog)
yminus = board.GP27 # pin 32 (analog)
xplus = board.GP28 # pin 34 (analog)
yplus = board.GP16 # pin 21

rst = board.GP21 # pin 27
dc = board.GP20 # pin 26
cs = board.GP17 # pin 22
mosi = board.GP19 # pin 25
miso = None # DISCONNECTED
clk = board.GP18 # pin 24

# Pi 4
# rst = board.D26
# dc = board.D13
# cs = board.D8
# mosi = board.D10
# miso = board.D9
# clk = board.D11

display_bus = displayio.FourWire(
    busio.SPI(
        clock=clk,
        MOSI=mosi,
        MISO=miso
    ),
    command=dc,
    chip_select=cs,
)

display = HX8357(
    display_bus,
    width=480,
    height=320,
    # todo: rotate this and touch
    #rotation=90
)

# Actual min/max values measured for reference
calibration = ((7959, 57839), (10087, 51907))
# adjusted
calibration = ((7900, 57839), (10087, 51907))

print("Loading touchscreen...")
ts = adafruit_touchscreen.Touchscreen(
    xminus,
    xplus,
    yplus,
    yminus,
    # Original "actual" min/max for x/y:
    # calibration=((7959, 57839), (10087, 51907))
    calibration=calibration,
    size=(480,320),
)
