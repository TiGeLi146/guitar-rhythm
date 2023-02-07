import os
import sys

import pygame

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


font_name = pygame.font.match_font('arial')


# Функция отрисовки текста
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, pygame.Color('white'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Функция, отрисовывающая окно
def show_final_window():
    bg = pygame.transform.scale(load_image('final.jpg'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))

    all_sprites = pygame.sprite.Group()

    rect_image = load_image("rect.png", colorkey=-1)
    rect_image = pygame.transform.scale(rect_image, (300, 125))
    rect = pygame.sprite.Sprite(all_sprites)
    rect.image = rect_image
    rect.rect = rect.image.get_rect()

    rect.rect.x = WIDTH / 2 - 195
    rect.rect.y = HEIGHT / 2 - 85

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        all_sprites.draw(screen)
        draw_text(screen, "Game over", 56, WIDTH / 2 - 50, HEIGHT / 2 - 50)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    show_final_window()
