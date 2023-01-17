import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)


# creating thorn sprite
class Thorn(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)


# creating heart sprite
class Heart(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
