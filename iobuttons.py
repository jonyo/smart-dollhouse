import board
import digitalio

class Button:
    def __init__(self, pin):
        self._id = pin.id
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def isPressed(self):
        return self.button.value == False

buttons = [
    Button(board.D17),
    Button(board.D22),
    Button(board.D23),
    Button(board.D27),
]
