import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, colour, x, y, size):
        super().__init__()
        filePath = colour + 'png'
        self.image = pygame.transform.scale(pygame.image.load(filePath).convert_alpha(), size)
        self.rect = self.image.get_rect(topleft = (x, y))

        if colour == 'red.':
            self.value = 50
        elif colour == 'yellow.':
            self.value = 100
        else:
            self.value = 200

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screenWidth):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('mystery.png'), (60, 30))

        if side == 'right':
            x = screenWidth + 50
            self.speed = -3

        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x, 80))

    def update(self):
        self.rect.x += self.speed

