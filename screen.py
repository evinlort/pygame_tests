from pynput import keyboard
import pygame
import random

pygame.init()
displ_info = pygame.display.Info()

screen = pygame.display.set_mode((displ_info.current_w, displ_info.current_h))

colors = tuple(color for color in [random.randint(0, 255) for _ in range(0, 3)])
screen.fill(colors)
pygame.display.flip()
prev_key = None


def update_colors(key):
    global prev_key
    if prev_key == key and key == keyboard.Key.esc:
        lst.stop()
        pygame.quit()
    if prev_key == key:
        pygame.display.flip()
        return
    prev_key = key
    colors2 = tuple(color for color in [random.randint(0, 255) for _ in range(0, 3)])
    screen.fill(colors2)
    pygame.display.flip()


lst = keyboard.Listener(on_press=update_colors)
lst.start()


while True:
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        lst.stop()
        pygame.quit()
