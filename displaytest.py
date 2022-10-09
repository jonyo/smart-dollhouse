import touchscreen
import displayio

bitmap = displayio.Bitmap(320, 480, 2)

palette = displayio.Palette(2)
palette[0] = 0
palette[1] = 0xFFFFFF

for x in range(10, 20):
    for y in range(10, 20):
        bitmap[x, y] = 1

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)
touchscreen.display.show(group)

print("Done showing")

while True:
    pass
