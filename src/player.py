import pygame
import sprites


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, right_frames, left_frames, x, y, width=50, height=50):
        super().__init__()
        self.right_frames = right_frames
        self.left_frames = left_frames
        self.main_frame = player_image
        self.right_cur_frame, self.left_cur_frame = 0, 0
        self.image = self.main_frame
        self.rect = self.image.get_rect().move(width * x, height * y)
        self.pos = width * x, height * y
        self.heart_count = 3
        self.heart_arr = []

    def move_right(self, block, thorn, pos_x, pos_y, heart_image):
        if pygame.sprite.spritecollideany(self, thorn):
            self.damage(heart_image, pos_x, pos_y)
        elif not pygame.sprite.spritecollideany(self, block):
            self.right_cur_frame = (self.right_cur_frame + 1) % len(self.right_frames)
            self.image = self.right_frames[self.right_cur_frame]
            self.rect = self.image.get_rect().move(self.pos[0] + 10, self.pos[1])
            self.pos = self.pos[0] + 10, self.pos[1]

    def move_left(self, block, thorn, pos_x, pos_y, heart_image):
        if pygame.sprite.spritecollideany(self, thorn):
            self.damage(heart_image, pos_x, pos_y)
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

    def fall(self, heart_image, level_map, pos_x, pos_y, width=50, height=50):
        level = level_map
        x, y = self.pos[0] // width, self.pos[1] // height + 1
        if level[y][x] == '.':
            self.rect = self.image.get_rect().move(self.pos[0], self.pos[1] - 5)
            self.pos = self.pos[0], self.pos[1] + 5
        elif level[y][x] == '*':
            self.damage(heart_image, pos_x, pos_y)

    def damage(self, heart_image, pos_x, pos_y, width=50, height=50):
        self.heart_arr = []
        self.heart_count -= 1
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)
        self.pos = width * pos_x, height * pos_y
        for i in range(self.heart_count):
            self.heart_arr.append(sprites.Heart(heart_image, 10, 10 + i * 10))

    def update(self):
        self.image = self.main_frame
