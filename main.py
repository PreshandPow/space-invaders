import pygame, sys
from mainGame import GameLoop


if __name__ == '__main__':
    pygame.init()

    gameSurfaceWidth, gameSurfaceHeight = 1200, 800


    gameLoopInstance = GameLoop(gameSurfaceWidth, gameSurfaceHeight)
    gameLoopInstance.showScreen()

    pygame.quit()
    sys.exit()
