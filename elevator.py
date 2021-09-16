""" Combines different elements to control the elevator """
import motor
import iobuttons
import board
import time

class Elevator (object):
    endstop = iobuttons.Button(board.D5)

    # current pos in whole steps... start off at 0
    pos = 0

    # Travel note:
    # measured:
    # 1000 steps = 300mm
    # so
    #
    # 1 step = .3mm
    # 1mm = 1.3333333333333 steps

    """ Steps for each floor starting with floor 0 """
    floors = [
        # first floor, yes these are 0 indexed.  as it should be... Internally anyways, externally refer to 1,2,3
        0,
        # second floor
        1410,
        # third floor
        2825
    ]

    """ max (top floor) in whole steps """
    max = 2825

    def _go(self, direction, steps = 1) -> None:
        """ Go up/down # steps, but if endstop is pressed, bounce off the endstop and stop """
        assert steps > 0
        travel = 0
        stepDelta = -1 if direction == motor.DOWN else 1
        while travel < steps:
            if self.endstop.isPressed():
                print("Reached the endstop, stopping!")
                if direction == motor.DOWN or travel == 0:
                    self._endstopBounce(motor.UP)
                    self.pos = 0
                else:
                    print("Unexpected: hit the endstop going up!")
                    self.pos = self.max
                return

            motor.onestep(direction)
            self.pos += stepDelta
            travel += 1
            time.sleep(motor.DELAY)

    def _endstopBounce(self, direction):
        # go the other direction until no longer sitting on endstop
        max = 10
        travel = 0
        # delay - go slower by x2 when bouncing off an endstop
        delay = motor.DELAY * 2.0
        while travel < max:
            if not self.endstop.isPressed():
                return
            motor.onestep(direction)
            travel += 1
            time.sleep(delay)
        print("Tried bouncing off the endstop but did not get off after %s steps"%max)

    def _firstFloor(self):
        """ Go to the first floor """
        # unlike others, keep going down until we hit endstop, use as a homing action
        self._go(motor.DOWN, self.max)

    def goToFloor(self, floor: int):
        """ Go to the given floor, 1 2 or 3 """
        assert floor < 4 and floor > 0
        if floor == 1 and False:
            # just go till it gets to endstop
            self._go(motor.DOWN, self.max)
            return

        floorIndex = floor - 1
        # figure out number of steps to go
        goToPos = self.floors[floorIndex]
        if goToPos == self.pos:
            # we're there already!  ding ding!
            print("Already at floor %s"%floor)
            return

        direction = motor.UP if goToPos > self.pos else motor.DOWN
        travel = abs(self.pos - goToPos)
        self._go(direction, travel)
