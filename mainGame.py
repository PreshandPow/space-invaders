import pygame, sys, random
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser

class GameLoop:
    def __init__(self, surfaceWidth, surfaceHeight):
        self.surfaceWidth = surfaceWidth
        self.surfaceHeight = surfaceHeight

        # Health and Score setup
        self.lives = 3
        self.liveSurface = pygame.transform.scale(pygame.image.load('heart.png'), (50, 50))
        self.liveXStartPos = self.surfaceWidth - (self.liveSurface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('LEMONMILK-Medium.otf', 20)

        # Import audio
        self.laserSound = pygame.mixer.Sound('laser sound.wav')
        self.laserSound.set_volume(0.1)

        self.alienDeathSound = pygame.mixer.Sound('alien death.mp3')
        self.alienDeathSound.set_volume(0.2)

        self.playerDeathSound = pygame.mixer.Sound('player death.wav')
        self.playerDeathSound.set_volume(0.1)

        self.obstacleSound = pygame.mixer.Sound('laser sound.wav')
        self.obstacleSound.set_volume(0.1)

        self.gameMusic = pygame.mixer.Sound('gameloop music.mp3')
        self.gameMusic.set_volume(0.2)
        self.gameMusic.play(-1)

        # surface setup
        self.surface = pygame.display.set_mode((self.surfaceWidth, self.surfaceHeight))
        self.clock = pygame.time.Clock()
        self.background = pygame.transform.scale(pygame.image.load('background.jpg').convert_alpha(), (self.surfaceWidth, self.surfaceHeight))

        # Player setup
        playerSprite: Player = Player((self.surfaceWidth / 2, self.surfaceHeight), 8, self.surfaceWidth, self.surfaceHeight, self.laserSound)
        self.player = pygame.sprite.GroupSingle(playerSprite)

        # Obstacle setup
        self.shape = obstacle.shape
        self.blockSize = 6
        self.blocks = pygame.sprite.Group()
        self.createMultipleObstacles(40, 550, 60, 360, 660, 960)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alienLasers = pygame.sprite.Group()
        self.alienSetup(5, 7)
        self.alienDirection = 5

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extraSpawnTime = random.randint(40, 80)



    def createObstacles(self, xStart, yStart, offsetX):
        for rowIndex, row in enumerate(self.shape):
            for colIndex, col in enumerate(row):
                if col == 'x':
                    x = xStart + colIndex * self.blockSize + offsetX
                    y = yStart + rowIndex * self.blockSize
                    block = obstacle.Blocks(self.blockSize, 'red', x, y)
                    self.blocks.add(block)


    def createMultipleObstacles(self, xStart, yStart, *offset):
        for offsetX in offset:
            self.createObstacles(xStart, yStart, offsetX)

    def alienSetup(self, rows, cols, xDistance = 100, yDistance = 75, offsetX = 25, offsetY = 100):
        for rowIndex, row in enumerate(range(rows)):
            for colIndex, col in enumerate(range(cols)):
                x = colIndex * xDistance + offsetX
                y = rowIndex * yDistance + offsetY

                if rowIndex == 0:
                    alienSprite = Alien('blue.', x, y, (100,100))

                elif 1 <= rowIndex <= 2:
                    alienSprite = Alien('yellow.', x, y, (100, 100))

                else:
                    alienSprite = Alien('red.', x, y, (100, 100))

                self.aliens.add(alienSprite)

    def alienPosChecker(self):
        allAliens = self.aliens.sprites()
        moveDown = 0
        if moveDown >= 2:
            print('addad')
            self.alienMoveDown(2)
            moveDown = 0

        for alien in allAliens:

            if alien.rect.right >= self.surfaceWidth:
                self.alienMoveDown(2)
                self.alienDirection = -5

            if alien.rect.left <= 0:
                self.alienMoveDown(5)
                self.alienDirection = 5

    def alienMoveDown(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alienShoot(self):
        if self.aliens.sprites():
            randomAlien = random.choice(self.aliens.sprites())
            laserSprite = Laser(randomAlien.rect.center, 6, self.surfaceHeight)
            self.alienLasers.add(laserSprite)

    def extraAlienTimer(self):
        self.extraSpawnTime -= 1
        if self.extraSpawnTime <= 0:
            self.extra.add(Extra(random.choice(['right', 'left']), self.surfaceWidth))
            self.extraSpawnTime = random.randint(400, 800)

    def collisionChecks(self):

        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:

                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # Alien collisions
                aliensHit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliensHit:
                    for alien in aliensHit:
                        self.score += alien.value
                        self.alienDeathSound.play()
                        laser.kill()

                # Extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.obstacleSound.play()
                    self.score += 500
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.alienLasers, True):
                    self.obstacleSound.play()
                    laser.kill()

        # Alien lasers
        if self.alienLasers:
            for laser in self.alienLasers.sprites():

                # Obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    self.obstacleSound.play()
                    laser.kill()

                # Player collisions
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.obstacleSound.play()
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        print('dead')
                        self.playerDeathSound.play()

        if self.aliens:

            # Block collision
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

            # Player collision
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.player, True)


    def displayLives(self):
        for life in range(self.lives - 1):
            x = self.liveXStartPos + (life * self.liveSurface.get_size()[0] + 10)
            self.surface.blit(self.liveSurface, (x, 8))

    def displayScore(self):
        scoreSurface = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(topleft = (20, 30))
        self.surface.blit(scoreSurface, scoreRect)

    def showScreen(self):
        ALIENLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIENLASER, 2000)

        CRTInstance = CRT(self.surface)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == ALIENLASER:
                    self.alienShoot()

            self.surface.blit(self.background, (0, 0))
            CRTInstance.draw()

            # Update the player
            self.player.update(self.laserSound)

            # Update the aliens, lasers, and blocks
            self.aliens.update(self.alienDirection)
            self.alienPosChecker()
            self.alienLasers.update()
            self.extraAlienTimer()
            self.extra.update()

            # Collisions checker
            self.collisionChecks()

            # Draw players
            self.player.sprite.lasers.draw(self.surface)
            self.player.draw(self.surface)

            # Draw blocks
            self.blocks.draw(self.surface)

            # Draw the aliens, lasers and extra
            self.aliens.draw(self.surface)
            self.alienLasers.draw(self.surface)
            self.extra.draw(self.surface)

            # Draw the score and lives
            self.displayLives()
            self.displayScore()

            pygame.display.flip()

            self.clock.tick(60)

class CRT:
    def __init__(self, surface):
        self.tv = pygame.transform.smoothscale(pygame.image.load('tv.png').convert_alpha(), (1200, 800))
        self.tv.set_alpha(15)
        self.surface = surface

    def draw(self):
        self.surface.blit(self.tv, (0,0))


