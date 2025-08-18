import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed, xConstraint, yConstraint, laserSound):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('Space-Invaders-ship.png'), (100, 100))
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.xConstraint = xConstraint
        self.yConstraint = yConstraint
        self.ready = True
        self.laserTime = 0
        self.laserCooldown = 500
        self.laserSound = laserSound

        self.lasers = pygame.sprite.Group()


    def getInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.laserSound.play()
            self.shootLaser()
            self.ready = False
            self.laserTime = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserTime >= self.laserCooldown:
                self.ready = True

    def shootLaser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def constraints(self):
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= self.xConstraint:
            self.rect.right = self.xConstraint


    def update(self, laserSound):
        self.getInput()
        self.constraints()
        self.recharge()
        self.lasers.update()


