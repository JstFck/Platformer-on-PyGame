import loading_level
import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()


# checking player position and finish
def finish(hero, pos_x, pos_y, width=50, height=50):
    return hero.pos[0] == pos_x * width and hero.pos[1] == pos_y * height


def main():
    pygame.init()
    fps = 30
    size = 1200, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    # block_width = block_height = 50
    # thorn_width = 50
    # thorn_height = 51

    # loading image
    game_over_background = loading_level.load_image('game_over.png')
    heart_image = loading_level.load_image('heart.png')
    background = loading_level.load_image('background.png')
    block_image = loading_level.load_image('block.png')
    thorn_image = loading_level.load_image('thorn.png')
    player_image = loading_level.load_image('hero_sprite(x50)/0.png')
    player_left_frames = [loading_level.load_image(f'hero_sprite(x50)/{i}.png') for i in range(1, 6)]
    player_right_frames = [loading_level.load_image(f'hero_sprite(x50)/{i}.png') for i in range(6, 11)]

    # loading level and sprites
    level_map, current_level_map, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, \
        heart_group = loading_level.next_level(block_image, thorn_image, player_image, player_right_frames,
                                               player_left_frames, heart_image)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        if finish(hero, finish_pos[0], finish_pos[1]):
            level_map, current_level_map, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, \
                heart_group = loading_level.next_level(block_image, thorn_image, player_image, player_right_frames,
                                                       player_left_frames, heart_image, current_level_map)

        # checked what keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            hero.move_right(block_group, thorn_group, hero_pos[0], hero_pos[1], heart_image)
        elif keys[pygame.K_a]:
            hero.move_left(block_group, thorn_group, hero_pos[0], hero_pos[1], heart_image)
        elif keys[pygame.K_SPACE]:
            hero.jump(level_map)
        hero.fall(heart_image, level_map, hero_pos[0], hero_pos[1])

        for item in heart_group:
            item.kill()
            heart_group.clear(screen, background)
        heart_group.add(hero.heart_arr)

        # drawing sprites
        if hero.heart_count:
            screen.blit(background, (0, 0))
            thorn_group.draw(screen)
            block_group.draw(screen)
            player_group.draw(screen)
            heart_group.draw(screen)
            player_group.update()
            pygame.display.flip()
        # if game over
        elif not hero.heart_count:
            screen.blit(game_over_background, (0, 0))
            if keys[pygame.K_x]:
                level_map, current_level_map, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, \
                    heart_group = loading_level.next_level(block_image, thorn_image, player_image, player_right_frames,
                                                           player_left_frames, heart_image, current_level_map)
            pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
