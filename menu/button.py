from math import floor
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text import label
from menu.colors import BLACK
import terminalio


class Button:

    def __init__(self, x: int, y: int, width: int, height: int, color: int, label: str):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.color = color
        self.label = label
        self.drawn = False

    def drawOutline(self) -> RoundRect:
        self.drawn = True
        return RoundRect(
            x=self.x1,
            y=self.y1,
            width=self.width,
            height=self.height,
            r=20,
            fill=BLACK,
            outline=self.color,
            stroke=5
        )

    def drawLabel(self):
        return label.Label(
            font=terminalio.FONT,
            text=self.label,
            color=self.color,
            background_color=None,
            x=self.x1 + 50,
            y=floor(self.y1 + (self.height/2)),
            scale=3,
        )

    def isInBounds(self, x: int, y: int):
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

    def moveToY(self, lineToButton: Button):
        self.y1 = lineToButton.y1
        self.y2 = self.y1 + self.height
