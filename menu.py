import pygame


class Menu:
    def __init__(self, gameSurfaceWidth, gameSurfaceHeight, sessionInfo):
        # Utility
        self.surface = pygame.display.set_mode((gameSurfaceWidth, gameSurfaceHeight))
        self.surfaceWidth = gameSurfaceWidth
        self.surfaceHeight = gameSurfaceHeight
        self.background = pygame.transform.scale(pygame.image.load('background.jpg').convert_alpha(),
                                                 (gameSurfaceWidth, gameSurfaceHeight))
        self.font = pygame.font.Font('LEMONMILK-Bold.otf', 100)
        self.dataStore = sessionInfo

        #  Text is rendered early to make the loop more efficient
        self.playText = self.font.render('PLAY', True, 'white')
        self.leaderboardText = self.font.render('LEADERBOARD', True, 'white')
        self.titleText = self.font.render('Space Invaders', True, 'red')

    def showScreen(self):
        playTextRect = self.playText.get_rect(center=(self.surfaceWidth / 2, self.surfaceHeight / 2 - 75))
        leaderboardTextRect = self.leaderboardText.get_rect(center=(self.surfaceWidth / 2, self.surfaceHeight / 2 + 75))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playTextRect.collidepoint(event.pos):
                        return 'play'
                    if leaderboardTextRect.collidepoint(event.pos):
                        return 'leaderboard'

            self.surface.blit(self.background, (0, 0))

            # Render and blit the text with hover effect
            # Play button
            play_text = self.font.render('PLAY', True, 'white')
            if playTextRect.collidepoint(pygame.mouse.get_pos()):
                play_text = self.font.render('PLAY', True, 'red')
            self.surface.blit(play_text, playTextRect)

            # Leaderboard
            leaderboard_text = self.font.render('LEADERBOARD', True, 'white')
            if leaderboardTextRect.collidepoint(pygame.mouse.get_pos()):
                leaderboard_text = self.font.render('LEADERBOARD', True, 'red')
            self.surface.blit(leaderboard_text, leaderboardTextRect)

            # Title
            titleTextRect = self.titleText.get_rect(center=(self.surfaceWidth / 2, 100))
            self.surface.blit(self.titleText, titleTextRect)

            pygame.display.flip()