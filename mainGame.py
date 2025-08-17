import pygame, sys
from player import Player

class GameLoop:
    def __init__(self, surfaceWidth, surfaceHeight):
        self.surfaceWidth = surfaceWidth
        self.surfaceHeight = surfaceHeight
        self.surface = pygame.display.set_mode((self.surfaceWidth, self.surfaceHeight))
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load('background.jpg').convert_alpha(), (self.surfaceWidth, self.surfaceHeight))
        playerSprite: Player = Player((self.surfaceWidth / 2, self.surfaceHeight), 8, self.surfaceWidth, self.surfaceHeight)
        self.player = pygame.sprite.GroupSingle(playerSprite)

    def showScreen(self):



        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.surface.blit(self.background, (0, 0))

            self.player.update()

            self.player.sprite.lasers.draw(self.surface)


            self.player.draw(self.surface)

            pygame.display.flip()

            self.clock.tick(60)


