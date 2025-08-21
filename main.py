import pygame, sys
from mainGame import GameLoop
from menu import Menu
from signIn import SignIn
from leaderboard import Leaderboard
from difficultySelection import DifficultyScreen


# stores the current users information e.g., their userId, username
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

    sessionInfo = SessionInfo()

    user = signInInstance = SignIn(sessionInfo,signInSurfaceWidth, signInSurfaceHeight)

    username = sessionInfo.get_data('username')

    # Start the first loop of the sign-in page
    if signInInstance.show_screen():
        menuRun = True
        while menuRun:

            # if logged in, run menu instance
            menuInstance = Menu(gameSurfaceWidth, gameSurfaceHeight, sessionInfo)
            menuResult = menuInstance.showScreen()

            if menuResult == 'play':
                # if choice is to play, let user select difficulty then start the game
                difficulty_instance = DifficultyScreen(gameSurfaceWidth, gameSurfaceHeight, sessionInfo)
                difficulty_choice = difficulty_instance.showScreen()

                if difficulty_choice in ['easy', 'normal', 'hard']:
                    gameLoopInstance = GameLoop(gameSurfaceWidth, gameSurfaceHeight, difficulty_choice, sessionInfo)
                    runGame = gameLoopInstance.showScreen()

            # show leaderboard screen
            elif menuResult == 'leaderboard':
                leaderboardInstance = Leaderboard(gameSurfaceWidth, gameSurfaceHeight, sessionInfo)
                runGame = leaderboardInstance.showScreen()

                if runGame == 'exit':
                    menuRun = False


            elif menuResult == 'quit':
                menuRun = False

    pygame.quit()
    sys.exit()