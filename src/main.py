import loading_level
import game_sprites
import pygame
import sys


FPS = 30
SIZE = 1200, 800

pygame.init()
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Platformer")

GAME_OVER_BACKGROUND = loading_level.load_image('game_over.png')
BACKGROUND = loading_level.load_image('background.png')
HEART_IMAGE = loading_level.load_image('heart.png')
BLOCK_IMAGE = loading_level.load_image('block.png')
THORN_IMAGE = loading_level.load_image('thorn.png')
PLAYER_IMAGE = loading_level.load_image('hero_sprite(x50)/0.png')
PLAYER_LEFT_FRAMES = [loading_level.load_image(f'hero_sprite(x50)/{i}.png') for i in range(1, 6)]
PLAYER_RIGHT_FRAMES = [loading_level.load_image(f'hero_sprite(x50)/{i}.png') for i in range(6, 11)]


def terminate():
    pygame.quit()
    sys.exit()


# checking player position and finish
def finish(h, pos_x, pos_y, width=50, height=50):
    return h.rect.x == pos_x * width and h.rect.y == pos_y * height


def main():
    clock = pygame.time.Clock()
    # block_width = block_height = 50
    # thorn_width = 50
    # thorn_height = 51

    # loading level and sprites
    level_map, current_level_map, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, \
        heart_group = loading_level.next_level(BLOCK_IMAGE, THORN_IMAGE, PLAYER_IMAGE, PLAYER_RIGHT_FRAMES,
                                               PLAYER_LEFT_FRAMES)

    while True:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and hero.on_ground:
                    hero.jump_count = 15
                    hero.on_ground = False
                if event.key == pygame.K_d:
                    hero.right = True
                if event.key == pygame.K_a:
                    hero.left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    hero.right = False
                if event.key == pygame.K_a:
                    hero.left = False

        if finish(hero, finish_pos[0], finish_pos[1]):
            level_map, current_level_map, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, \
                heart_group = loading_level.next_level(BLOCK_IMAGE, THORN_IMAGE, PLAYER_IMAGE, PLAYER_RIGHT_FRAMES,
                                                       PLAYER_LEFT_FRAMES, current_level_map)
        if not hero.pos[0] in range(0, 1200) and hero.pos[1] in range(0, 800):
            hero.rect = hero.image.get_rect().move(hero.start_pos[0], hero.start_pos[1] - 5)
            hero.on_ground = True
            hero.right = False
            hero.left = False

        heart_group.empty()
        for i in range(hero.heart_count):
            heart_group.add(game_sprites.Heart(HEART_IMAGE, 10, 10 + i * 10))

        # drawing sprites
        if hero.heart_count:
            SCREEN.blit(BACKGROUND, (0, 0))
            thorn_group.draw(SCREEN)
            block_group.draw(SCREEN)
            player_group.draw(SCREEN)
            heart_group.draw(SCREEN)
            player_group.update()
            pygame.display.flip()
        # if game over
        elif not hero.heart_count:
            SCREEN.blit(GAME_OVER_BACKGROUND, (0, 0))
            if keys[pygame.K_x]:
                level_map, current_level_map, hero_pos, finish_pos, hero, block_group, thorn_group, player_group, \
                    heart_group = loading_level.next_level(BLOCK_IMAGE, THORN_IMAGE, PLAYER_IMAGE, PLAYER_RIGHT_FRAMES,
                                                           PLAYER_LEFT_FRAMES, current_level_map)
            pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
