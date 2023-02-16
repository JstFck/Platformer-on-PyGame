import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


# creating thorn sprite
class Thorn(pygame.sprite.Sprite):
    def __init__(self, image, width, height, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(width * pos_x, height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


# creating heart sprite
class Heart(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)


# creating checking sprite
# using for check player sprite in air
class CheckSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect(x, y, 50, 50)
        self.mask = pygame.mask.from_surface(self.image)
