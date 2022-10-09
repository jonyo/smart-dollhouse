from menu.button import Button
from menu.colors import BLACK, PINK
import touchscreen
import displayio

floor1 = Button(
    x=20,
    y=20,
    width=440,
    height=80,
    color=PINK,
    label="Floor 1"
)

floor2 = Button(
    x=20,
    y=120,
    width=440,
    height=80,
    color=PINK,
    label="Floor 2"
)

floor3 = Button(
    x=20,
    y=220,
    width=440,
    height=80,
    color=PINK,
    label="Floor 3"
)


def drawMenu() -> None:
    splash = displayio.Group()

    touchscreen.display.show(splash)

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
