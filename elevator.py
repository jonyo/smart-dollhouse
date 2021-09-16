""" Combines different elements to control the elevator """
import motor
import iobuttons
import board
import time

class Elevator (object):
    endstop = iobuttons.Button(board.D5)

    # current pos in whole steps... start off at 0
    pos = 0

    floors = [
        # first floor, yes these are 0 indexed.  as it should be... Internally anyways, externally refer to 1,2,3
        0,
        # second floor
        100,
        # third floor
        200
    ]

    # max (top floor) in whole steps
    max = 200

    def _go(self, direction, steps = 1) -> None:
        """ Go up/down # steps, but if endstop is pressed, bounce off the endstop and stop """
        assert steps > 0
        travel = 0
        stepDelta = -1 if direction == motor.DOWN else 1
        while travel < steps:
            if self.endstop.isPressed():
                print("Reached the endstop, stopping!")
                if direction == motor.DOWN:
                    self._endstopBounce(motor.UP)
                    self.pos = 0
                else:
                    self._endstopBounce(motor.DOWN)
                    self.pos = self.max
                return

            motor.onestep(direction)
            self.pos += stepDelta
            travel += 1
            time.sleep(motor.DELAY)

    def _endstopBounce(self, direction):
        # go the other direction until no longer sitting on endstop
        max = 5
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
        if floor == 1:
            # just go till it gets to endstop
            self._go(motor.DOWN, self.max)
            return
        if floor == 3:
            # go up till we hit endstop
            self._go(motor.UP, self.max)
            return
        # middle floor... figure out steps to go

        goToPos = self.floors[floor - 1]
        if goToPos == self.pos:
            # we're there already!  ding ding!
            return

        if goToPos > self.pos:
            # going down!
            self._go(motor.DOWN, goToPos - self.pos)
        else:
            # going up!
            self._go(motor.UP, self.pos - goToPos)
