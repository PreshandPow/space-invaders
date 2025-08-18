import pygame


class Blocks(pygame.sprite.Sprite):
    def __init__(self, size, colour, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft = (x, y))

shape = [
    '   xxxxxxxxx',
    '  xxxxxxxxxxxx',
    '  xxxxxxxxxxxx',
    ' xxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxx',
    'xxx          xxx',
    'xx            xx'
]