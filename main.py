import pygame, sys
from mainGame import GameLoop
from menu import Menu
from signIn import SignIn


class SessionInfo:
    def __init__(self):
        self.data = {}

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key, None)

if __name__ == '__main__':
    pygame.init()

    signInSurfaceWidth, signInSurfaceHeight = 1800, 1000
    gameSurfaceWidth, gameSurfaceHeight = 1200, 800

    signInInstance = SignIn(SessionInfo(),signInSurfaceWidth, signInSurfaceHeight)

    if signInInstance.show_screen():
        menuRun = True
        while menuRun:
            menuInstance = Menu(gameSurfaceWidth, gameSurfaceHeight)
            menuResult = menuInstance.showScreen()

            # The logical error is here. print() returns None, so this condition is always False.
            if menuResult == 'play':
                print('running mainGame')
                gameLoopInstance = GameLoop(gameSurfaceWidth, gameSurfaceHeight)
                runGame = gameLoopInstance.showScreen()

                if runGame == 'exit':
                    menuRun = False

            elif menuResult == 'quit':
                menuRun = False

    pygame.quit()
    sys.exit()