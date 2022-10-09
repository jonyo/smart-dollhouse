# SPDX-FileCopyrightText: 2022 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

"""
touch_calibrator_built_in.py  2022-05-27 v2.2

Author(s): JG for Cedar Grove Maker Studios

On-screen touchscreen calibrator for built-in displays.

When the test screen appears, use a stylus to swipe to the four edges
of the visible display area. As the screen is calibrated, the small red
square tracks the stylus tip (REPL_ONLY=False). Minimum and maximum
calibration values will display on the screen and in the REPL. The calibration
tuple can be copied and pasted into the calling code's touchscreen
instantiation statement.

DISPLAY_ROTATION: Display rotation value in degrees. Only values of
None, 0, 90, 180, and 270 degrees are accepted. Defaults to None, the
previous orientation of the display.

REPL_ONLY: If False, calibration values are shown graphically on the screen
and printed to the REPL. If True, the values are only printed to the REPL.
Default value is False.
"""

import time
import displayio
import touchscreen


# Operational parameters:
DISPLAY_ROTATION = 0  # Specify 0, 90, 180, or 270 degrees
REPL_ONLY = True  # True to disable graphics

# pylint: disable=too-few-public-methods
class Colors:
    """A collection of colors used for graphic objects."""

    BLUE_DK = 0x000060  # Screen fill
    RED = 0xFF0000  # Boundary
    WHITE = 0xFFFFFF  # Text


# Instantiate the built-in display
display = touchscreen.display

# Check rotation value and update display.
# Always set rotation before instantiating the touchscreen.
if DISPLAY_ROTATION is not None and DISPLAY_ROTATION in (0, 90, 180, 270):
    display.rotation = DISPLAY_ROTATION
else:
    print("Warning: invalid rotation value -- defaulting to zero")
    display.rotation = 0
    time.sleep(1)

# Activate the display graphics unless REPL_ONLY=True
if not REPL_ONLY:
    display_group = displayio.Group()
    display.show(display_group)

# Instantiate touch screen without calibration or display size parameters

ts = touchscreen.ts

# pylint: disable=invalid-name
# Reset x and y values to raw touchscreen mid-point before measurement
x_min = x_max = y_min = y_max = 65535 // 2

print("Touchscreen Calibrator")
print("  Use a stylus to swipe slightly beyond the")
print("  four edges of the visible display area.")
print(" ")
print(f"  display rotation: {display.rotation} degrees")
print("  Calibration values follow:")
print(" ")

while True:
    time.sleep(0.100)
    touch = ts.touch_point  # Check for touch
    if touch:
        # Remember minimum and maximum values for the calibration tuple
        x_min = min(x_min, touch[0])
        x_max = max(x_max, touch[0])
        y_min = min(y_min, touch[1])
        y_max = max(y_max, touch[1])

        # Show the calibration tuple.
        print(f"(({x_min}, {x_max}), ({y_min}, {y_max}))")
