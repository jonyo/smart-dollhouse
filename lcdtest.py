import pygame
import os
import time
import iobuttons

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_AUDIODRIVER', 'dummy')

# first test the display drivers


buttons = iobuttons.buttons

buttons[0].color = (255,0,0)
buttons[1].color = (0,255,0)
buttons[2].color = (0,0,255)
buttons[3].color = (0,0,0)

#Colours
WHITE = (255,255,255)



pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 100)

while True:
    # if bottom button is pressed, it closes
    if buttons[3].isPressed():
        print("Button pressed, closing test.")
        break

    # Scan the buttons
    for button in buttons:
        if button.isPressed():
            lcd.fill(button.color)
            text_surface = font_big.render('%d'%button._id, True, WHITE)
            rect = text_surface.get_rect(center=(160,120))
            lcd.blit(text_surface, rect)
            pygame.display.update()
    time.sleep(0.1)
