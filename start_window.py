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


def main():
    bg = pygame.transform.scale(load_image('bg.jpg'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))

    btn_image = load_image("button.png", colorkey=-1)
    btn_image = pygame.transform.scale(btn_image, (500, 250))
    btn = pygame.sprite.Sprite(all_sprites)
    btn.image = btn_image
    btn.rect = btn.image.get_rect()

    btn.rect.x = 390
    btn.rect.y = 235

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN \
                    and btn.rect.collidepoint(event.pos):
                return
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    main()
