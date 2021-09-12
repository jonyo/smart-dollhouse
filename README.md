# smart-dollhouse
Software running on pi zero for smart dollhouse.

This is a work in progress.  Also I am using it to learn python, so this is probably not a good example of python
best practices.

## Plans

* Control the elevator with a resistive touchscreen, this is the primary reason for this project.
* Control LED lights, possibly with motion sensor but also control via touchscreen.
* For a kid still learning to read, so menus are picture based (maybe will add text below picture as well).

## Future Upgrades
* Add sound / mic to give:
  * Doorbell
  * maybe voice control.
  * Lightswitch raves w/o the lightswitch

# Main hardware used (so far)

* Raspberry Pi Zero W (running raspbian lite)
* Lulzbot stepper motor I happened to already have.
* DRV8833 driver for the stepper motor on adafruit breakout board.
* PiTFT Plus Assembled 320x240 2.8" TFT + Resistive Touchscreen
* 10V 1.2a power supply (from my "random power bricks I don't know what they go to anymore so better keep them
   just in case" box)
