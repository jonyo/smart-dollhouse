import touchscreen
import displayio


def drawMenu():
    splash = displayio.Group()

    touchscreen.display.show(splash)

    color_bitmap = displayio.Bitmap(480, 320, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x550000  # Bright Green

    bg_sprite = displayio.TileGrid(
        color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(200, 400, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xAA0088  # Purple
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
    splash.append(inner_sprite)
