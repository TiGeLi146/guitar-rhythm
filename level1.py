import os
import sys
import random

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


def run_level1():
    pygame.mixer.music.load('data/level2.mp3')
    pygame.mixer.music.play()

    arrow_images = {
        'left': load_image('left.png', colorkey=-1),
        'right': load_image('right.png', colorkey=-1),
        'up': load_image('top.png', colorkey=-1),
        'down': load_image('down.png', colorkey=-1)
    }

    arrow_names = ['left', 'right', 'up', 'down']

    circle_image = load_image("circle.png", colorkey=-1)

    all_sprites = pygame.sprite.Group()
    arrows_group = pygame.sprite.Group()
    circle_group = pygame.sprite.Group()

    bg = pygame.transform.scale(load_image('level_bg.jpg'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))

    NEWARROWEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(NEWARROWEVENT, 1000)

    ENDLEVELEVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(ENDLEVELEVENT, 62000, 1)

    CHANGERADEVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGERADEVENT, 100)

    class Circle(pygame.sprite.Sprite):
        def __init__(self, rad, x, y):
            super().__init__(circle_group, all_sprites)
            self.image = circle_image
            self.image = pygame.transform.scale(self.image, (rad, rad))
            self.rect = self.image.get_rect().move(
                x, y)

    class Arrow(pygame.sprite.Sprite):
        def __init__(self, tile_type):
            super().__init__(arrows_group, all_sprites)
            self.image = arrow_images[tile_type]
            self.image = pygame.transform.scale(self.image, (500, 250))
            self.rect = self.image.get_rect().move(
                390, 235)

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for k in range(columns):
                    frame_location = (self.rect.w * k, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def draw_new_arrow():
        global current_arrow
        current_arrow = random.choice(arrow_names)
        Arrow(current_arrow)

    font_name = pygame.font.match_font('arial')

    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def save_result(res):
        f = open("data/res.txt", 'w')
        f.write(str(res))

    current_arrow = 'left'

    draw_new_arrow()
    rad = 700
    c_x = 290
    c_y = 10
    Circle(rad, c_x, c_y)
    AnimatedSprite(load_image("animation.png", colorkey=-1), 5, 6, 220, 330)

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_result(score)
                pygame.mixer.music.stop()
                return
            if event.type == NEWARROWEVENT:
                rad = 700
                for i in arrows_group:
                    i.kill()
                    arrows_group.clear(screen, bg)
                for i in circle_group:
                    i.kill()
                    circle_group.clear(screen, bg)
                draw_new_arrow()
                c_x = 290
                c_y = 10
                Circle(rad, c_x, c_y)
            if event.type == CHANGERADEVENT:
                rad -= 15
                c_x += 7.5
                c_y += 7.5
                for i in circle_group:
                    i.kill()
                    all_sprites.clear(screen, bg)
                Circle(rad, c_x, c_y)
            if event.type == ENDLEVELEVENT:
                save_result(score)
                return
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP
                    and current_arrow == 'up') or \
                        (event.key == pygame.K_DOWN
                         and current_arrow == 'down') or \
                        (event.key == pygame.K_LEFT
                         and current_arrow == 'left') or \
                        (event.key == pygame.K_RIGHT
                         and current_arrow == 'right'):
                    score += 1

            screen.blit(bg, (0, 0))
            all_sprites.draw(screen)
            all_sprites.update()
            draw_text(screen, 'Score: ' + str(score), 56, WIDTH - 150, 10)
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == '__main__':
    run_level1()
