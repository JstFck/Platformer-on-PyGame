from random import randrange
import sys
import pygame
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def next_level(block_image, thorn_image, player_image, player_right_frames, player_left_frames):
    level_map = load_level(f'level{randrange(1, 3)}.txt')

    block_arr, thorn_arr, hero_pos, finish_pos = generate_level(level_map, block_image, thorn_image)
    player = Player(player_image, player_right_frames, player_left_frames, 50, 50, hero_pos[0], hero_pos[1])

    block_group = pygame.sprite.Group()
    thorn_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player_group.add(player)
    block_group.add(i for i in block_arr)
    thorn_group.add(i for i in thorn_arr)

    return level_map, block_arr, thorn_arr, hero_pos, finish_pos, player, block_group, thorn_group, player_group


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, b_img, t_img, b_width=50, t_width=50, b_height=50, t_height=51):
    start_x, start_y, finish_x, finish_y = None, None, None, None
    block_arr = []
    thorn_arr = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                block_arr.append(Block(b_img, b_width, b_height, x, y))
            elif level[y][x] == '*':
                thorn_arr.append(Thorn(t_img, t_width, t_height, x, y))
            elif level[y][x] == '@':
                start_x, start_y = x, y
            elif level[y][x] == '$':
                finish_x, finish_y = x, y
    return block_arr, thorn_arr, (start_x, start_y), (finish_x, finish_y)


def finish(player, pos_x, pos_y, width=50, height=50):
    if player.pos[0] == pos_x * width and player.pos[1] == pos_y * height:
        return True
    return False


class Block(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)


class Thorn(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, right_frames, left_frames, width, height, x, y):
        super().__init__()
        self.right_frames = right_frames
        self.left_frames = left_frames
        self.main_frame = player_image
        self.right_cur_frame, self.left_cur_frame = 0, 0
        self.image = self.main_frame
        self.rect = self.image.get_rect().move(width * x, height * y)
        self.pos = width * x, height * y

    def move_right(self, block, thorn, pos_x, pos_y, width=50, height=50):
        if pygame.sprite.spritecollideany(self, thorn):
            self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)
            self.pos = width * pos_x, height * pos_y
        elif not pygame.sprite.spritecollideany(self, block):
            self.right_cur_frame = (self.right_cur_frame + 1) % len(self.right_frames)
            self.image = self.right_frames[self.right_cur_frame]
            self.rect = self.image.get_rect().move(self.pos[0] + 10, self.pos[1])
            self.pos = self.pos[0] + 10, self.pos[1]

    def move_left(self, block, thorn, pos_x, pos_y, width=50, height=50):
        if pygame.sprite.spritecollideany(self, thorn):
            self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)
            self.pos = width * pos_x, height * pos_y
        elif not pygame.sprite.spritecollideany(self, block):
            self.left_cur_frame = (self.left_cur_frame + 1) % len(self.left_frames)
            self.image = self.left_frames[self.left_cur_frame]
            self.rect = self.image.get_rect().move(self.pos[0] - 10, self.pos[1])
            self.pos = self.pos[0] - 10, self.pos[1]

    def jump(self, level_map, width=50, height=50):
        level = level_map
        x, y = self.pos[0] // width, self.pos[1] // height + 1
        jump_height = self.pos[1]
        if level[y][x] == '#':
            for i in range(50):
                if jump_height - 2 >= 0:
                    self.rect = self.image.get_rect().move(self.pos[0], jump_height - 2)
                    self.pos = self.pos[0], jump_height - 2
                    jump_height -= 2

    def fall(self, level_map, pos_x, pos_y, width=50, height=50):
        level = level_map
        x, y = self.pos[0] // width, self.pos[1] // height + 1
        if level[y][x] == '.':
            self.rect = self.image.get_rect().move(self.pos[0], self.pos[1] - 5)
            self.pos = self.pos[0], self.pos[1] + 5
        elif level[y][x] == '*':
            self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)
            self.pos = width * pos_x, height * pos_y

    def update(self):
        self.image = self.main_frame


def main():
    pygame.init()
    fps = 30
    size = 1200, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    # block width and height = 50
    # thorn width = 50
    # thorn height = 51

    heart_image = load_image('heart.png')
    background = load_image('background.png')
    block_image = load_image('block.png')
    thorn_image = load_image('thorn.png')
    player_image = load_image('hero_sprite(x50)/0.png')
    player_left_frames = [load_image(f'hero_sprite(x50)/{i}.png') for i in range(1, 6)]
    player_right_frames = [load_image(f'hero_sprite(x50)/{i}.png') for i in range(6, 11)]

    level_map, block_arr, thorn_arr, hero_pos, finish_pos, player, block_group, thorn_group, player_group = \
        next_level(block_image, thorn_image, player_image, player_right_frames, player_left_frames)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if finish(player, finish_pos[0], finish_pos[1]):
            level_map, block_arr, thorn_arr, hero_pos, finish_pos, player, block_group, thorn_group, player_group = \
                next_level(block_image, thorn_image, player_image, player_right_frames, player_left_frames)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.move_right(block_group, thorn_group, hero_pos[0], hero_pos[1])
        elif keys[pygame.K_a]:
            player.move_left(block_group, thorn_group, hero_pos[0], hero_pos[1])
        elif keys[pygame.K_SPACE]:
            player.jump(level_map)
        player.fall(level_map, hero_pos[0], hero_pos[1])

        screen.blit(background, (0, 0))
        thorn_group.draw(screen)
        block_group.draw(screen)
        player_group.draw(screen)
        player_group.update()
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
