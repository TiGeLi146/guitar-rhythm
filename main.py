import os
import sys

import pygame

from start_window import show_start_window
from level1 import run_level1
from level1_results import show_level1_results_window
from level2 import run_level2
from level2_results import show_level2_results_window
from final_window import show_final_window

FPS = 50

size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Error")
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    f = open("data/res.txt", mode="r")
    show_start_window()
    run_level1()
    show_level1_results_window(f.read())
    run_level2()
    f = open("data/res.txt", mode="r")
    show_level2_results_window(f.read())
    show_final_window()
