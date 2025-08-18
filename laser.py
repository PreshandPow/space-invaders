import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, surfaceHeight):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('laserpixil-frame-0.png'), (10, 30))
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.surfaceHeight = surfaceHeight

    def update(self):
        self.rect.y += self.speed
        self.destroy()

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.surfaceHeight + 50:
            self.kill()