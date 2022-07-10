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

## Main hardware used (so far)

* Raspberry Pi Zero W (running raspbian lite)
* Lulzbot stepper motor I happened to already have.
* A4988 stepper driver for the stepper motor.
* PiTFT Plus Assembled 320x240 2.8" TFT + Resistive Touchscreen
* 12V 1.2a power supply (from my "random power bricks I don't know what they go to anymore so better keep them
   just in case" box)

## GPIO Pin Use

Raspberry pi zero's GPIO pin usage for this project (so far)

| GPIO | Alt |  Pin # | Project Use |
| --- | --- | --- | --- |
| 2 | I2C1 SDA | 3 | - |
| 3 | I2C1 SCL | 5 | - |
| 4 | GPCLK0 | 7 | - |
| 5 | - | 29 | Elevator Endstop |
| 6 | - | 31 | - |
| 7 | SPI0 CE1 | 26 | - |
| 8 | SPI0 CE0 | 24 | - |
| 9 | SPI0 MISO | 21 | - |
| 10 | SPI0 MOSI | 19 | - |
| 11 | SPI0 SCLK | 23 | - |
| 12 | PWM0 | 32 | - |
| 13 | PWM1 | 33 | A4988 DIR pin |
| 14 | UART0 TXD | 8 | Future: debug console? |
| 15 | UART0 RXD | 10 | Future: debug console? |
| 16 | - | 36 | - |
| 17 | - | 11 | LCD Button 1 (top) |
| 18 | PCM CLK | 12 | - |
| 19 | PCM FS | 35 | A4988 STEP pin |
| 20 | PCM DIN | 38 | - |
| 21 | PCM DOUT | 40 | - |
| 22 | - | 15 | LCD Button 2 |
| 23 | - | 16 | LCD Button 3 |
| 24 | - | 18 | LCD |
| 25 | - | 22 | LCD |
| 26 | - | 37 | A4988 EN pin |
| 27 | - | 13 | LCD Button 4 (bottom) |

## A4988 / Pi / Stepper Wiring Map

In the order of pins on the A4988.  Skipped pins are not connected to anything.

### Left side

| A4988   | Pi       |
|---------|----------|
| ENABLE  | GPIO D26 |
| STEP    | GPIO D19 |
| DIR     | GPIO D13 |

If Pi GPIO usage is different than above, the mapping in the code in `motor.py` will need to be updated to match.
### Right side

| A4988   | Pi   | Stepper Wire Color | Stepper Extension Wire Color | Connector Wire Color |
|---------|------|--------------------|------------------------------|----------------------|
| 2B      | -    | Blue               | Blue                         | white                |
| 2A      | -    | Red                | Red                          | yellow               |
| 1A      | -    | Black              | Yellow                       | black                |
| 1B      | -    | Green              | Green                        | red                  |
| VDD     | 3.3v | -                  | -                            | -                    |
| GND     | GND  | -                  | -                            | -                    |

## A4988 Output Adjustment

The A4988 requires the pot (potentiometer) on the top to be adjusted.  See the whitesheet for details.

The specs on the stepper motor call for 1.5A.  The driver states it can go up to 2A but may require cooling above 1.2.

From the specs / datasheet:

```
VREF = 8 * IMAX * .068
```

So for goal of 1.4A (which seems to work well when using microsteps):

```
8 * 1.4 * .068 = 0.7616
```
So the pot should be adjusted so that the VREF is `0.7616`.

Reminder that it is a function of the input voltage among other things, so needs to be re-adjusted if a different power supply used.


# Onboarding

First, get raspbian lite installed with network / ssh working.

Get main [blinka library](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
installed (follow the instructions, leaving them out here in case they change over time)

Get the LCD screen set up and showing the console (note that we don't use desktop or X):
[reference](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2)

```
sudo pip3 install --upgrade adafruit-python-shell click
git clone https://github.com/adafruit/Raspberry-Pi-Installer-Scripts.git
cd Raspberry-Pi-Installer-Scripts
sudo python3 adafruit-pitft.py --display=28r --rotation=90 --install-type=console
```
Note: the last step was as of this creation.  If it changes reference the [original docs](https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2),
and the option you want is showing the console on a 2.8" resistive touch.

Get adafruit libraries installed for [adafruit motor](https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board/python-circuitpython#python-installation-of-motor-library-3070891-16)
```
pip3 install adafruit-circuitpython-motor
```

*Temp Hack*: Until I figure out how to run things on the LCD from SSH login, it needs to use `sudo` so also install
it for root:
```
sudo pip3 install adafruit-circuitpython-motor
```

Install PyGame (note the 3 - for some reason just installing `python-pygame` it could not find it)
```
sudo apt install python3-pygame
```
