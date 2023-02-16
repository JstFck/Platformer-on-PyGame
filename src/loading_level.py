from random import randrange
import game_sprites
import player
import pygame
import os


def load_image(name, color_key=None):
    fullname = os.path.join('../data', name)
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


# loading level file
def load_level(filename):
    fullname = os.path.join('../levels', filename)
    with open(fullname, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# loading level and sprites
def next_level(block_image, thorn_image, player_image, player_right_frames, player_left_frames, cur_level_map=None):
    level_map = load_level(f'level{randrange(1, 4)}.txt')
    while level_map == cur_level_map:
        level_map = load_level(f'level{randrange(1, 4)}.txt')
    cur_level = level_map

    block_arr, thorn_arr, hero_pos, finish_pos = generate_level(level_map, block_image, thorn_image)

    block_group = pygame.sprite.Group()
    thorn_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    heart_group = pygame.sprite.Group()
    block_group.add(i for i in block_arr)
    thorn_group.add(i for i in thorn_arr)

    hero = player.Player(player_image, player_right_frames, player_left_frames, hero_pos[0], hero_pos[1], block_group,
                         thorn_group)
    player_group.add(hero)

    return level_map, cur_level, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, heart_group


# generate level
def generate_level(level, b_img, t_img, b_width=50, t_width=50, b_height=50, t_height=51):
    start_x, start_y, finish_x, finish_y = None, None, None, None
    block_arr = []
    thorn_arr = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                block_arr.append(game_sprites.Block(b_img, b_width, b_height, x, y))
            elif level[y][x] == '*':
                thorn_arr.append(game_sprites.Thorn(t_img, t_width, t_height, x, y))
            elif level[y][x] == '@':
                start_x, start_y = x, y
            elif level[y][x] == '$':
                finish_x, finish_y = x, y
    return block_arr, thorn_arr, (start_x, start_y), (finish_x, finish_y)
