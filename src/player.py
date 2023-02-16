import game_sprites
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, right_frames, left_frames, x, y, blocks, thorns, width=50, height=50):
        super().__init__()
        self.right_frames, self.left_frames, self.main_frame = right_frames, left_frames, player_image
        self.right_cur_frame, self.left_cur_frame = 0, 0
        self.image = self.main_frame
        self.rect = self.image.get_rect().move(width * x, height * y)
        self.start_pos, self.pos = (width * x, height * y), (width * x, height * y)
        self.heart_count = 3
        self.blocks, self.thorns = blocks, thorns
        self.jump_count = 0
        self.right, self.left, self.on_ground = False, False, True

    def set_right_cur_frame(self):
        self.right_cur_frame = (self.right_cur_frame + 1) % len(self.right_frames)
        self.image = self.right_frames[self.right_cur_frame]

    def set_left_cur_frame(self):
        self.left_cur_frame = (self.left_cur_frame + 1) % len(self.left_frames)
        self.image = self.left_frames[self.left_cur_frame]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def move_right(self):
        self.set_right_cur_frame()
        self.move(10, 0)

    def move_left(self):
        self.set_left_cur_frame()
        self.move(-10, 0)

    def fall(self):
        self.move(0, -self.jump_count)
        self.jump_count -= 1

    def collide(self):
        if pygame.sprite.spritecollideany(self, self.thorns):
            self.heart_count -= 1
            self.on_ground = True
            self.right = False
            self.left = False
            self.rect = self.image.get_rect().move(self.start_pos[0], self.start_pos[1])
        if pygame.sprite.spritecollideany(self, self.blocks):
            if self.right:
                self.move(-10, 0)
            if self.left:
                self.move(10, 0)
            rect = game_sprites.CheckSprite(self.main_frame, self.pos[0], self.pos[1] - 25)
            if pygame.sprite.spritecollideany(rect, self.blocks):
                self.move(0, -self.jump_count)
                self.jump_count = 0
            else:
                self.on_ground = True
                self.move(0, self.jump_count)
                self.jump_count = 0
        else:
            self.on_ground = False

    def update(self):
        if not self.on_ground:
            self.fall()
        if self.right:
            self.move_right()
        if self.left:
            self.move_left()
        if not self.right and not self.left:
            self.image = self.main_frame
        self.collide()
