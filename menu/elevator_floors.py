from menu.button import Button
from menu.colors import BLACK, PINK
import touchscreen
import displayio

# Screen is 480 x 320

floor1 = Button(
    x=20,
    y=220,
    width=300,
    height=80,
    color=PINK,
    label="Ground Floor"
)

floor2 = Button(
    x=20,
    y=120,
    width=300,
    height=80,
    color=PINK,
    label="Floor 2"
)

floor3 = Button(
    x=20,
    y=20,
    width=300,
    height=80,
    color=PINK,
    label="Floor 3"
)

currentFloor = Button(
    x=340,
    y=0,
    width=120,
    height=80,
    color=PINK,
    label='<=',
)

splash = displayio.Group()

touchscreen.display.show(splash)


def drawMenu() -> None:
    # background - use black

    color_bitmap = displayio.Bitmap(480, 320, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = BLACK

    bg_sprite = displayio.TileGrid(
        color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # make the floors
    splash.append(floor1.drawOutline())
    splash.append(floor1.drawLabel())
    splash.append(floor2.drawOutline())
    splash.append(floor2.drawLabel())
    splash.append(floor3.drawOutline())
    splash.append(floor3.drawLabel())


def whichFloor(x: int, y: int) -> int:
    if (floor1.isInBounds(x, y)):
        return 1
    if (floor2.isInBounds(x, y)):
        return 2
    if (floor3.isInBounds(x, y)):
        return 3
    return 0


def drawCurrentFloor(floor: int):
    if (currentFloor.drawn):
        # avoid adding more and more things and running out of memory (I think)
        splash.pop()
        splash.pop()
        splash.pop()

    color_bitmap = displayio.Bitmap(160, 320, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = BLACK

    bg_sprite = displayio.TileGrid(
        color_bitmap, pixel_shader=color_palette, x=320, y=0)
    splash.append(bg_sprite)

    if (floor == 1):
        currentFloor.moveToY(floor1)
    elif (floor == 2):
        currentFloor.moveToY(floor2)
    else:
        currentFloor.moveToY(floor3)

    splash.append(currentFloor.drawOutline())
    splash.append(currentFloor.drawLabel())
