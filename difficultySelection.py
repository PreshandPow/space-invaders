import pygame


class DifficultyScreen:
    def __init__(self, surfaceWidth, surfaceHeight, sessionInfo):
        self.surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
        self.surfaceWidth = surfaceWidth
        self.surfaceHeight = surfaceHeight
        self.font = pygame.font.Font('LEMONMILK-Bold.otf', 50)
        self.background = pygame.transform.scale(pygame.image.load('background.jpg').convert_alpha(),
                                                 (surfaceWidth, surfaceHeight))

        self.dataStore = sessionInfo

    def showScreen(self):
        easy_rect = pygame.Rect(self.surfaceWidth / 2 - 100, 250, 200, 60)
        normal_rect = pygame.Rect(self.surfaceWidth / 2 - 100, 350, 200, 60)
        hard_rect = pygame.Rect(self.surfaceWidth / 2 - 100, 450, 200, 60)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rect.collidepoint(event.pos):
                        return 'easy'
                    if normal_rect.collidepoint(event.pos):
                        return 'normal'
                    if hard_rect.collidepoint(event.pos):
                        return 'hard'

            self.surface.blit(self.background, (0, 0))

            # Draw buttons and text
            easy_text = self.font.render('Easy', True, 'white')
            normal_text = self.font.render('Normal', True, 'white')
            hard_text = self.font.render('Hard', True, 'white')

            self.surface.blit(easy_text, easy_rect.topleft)
            self.surface.blit(normal_text, normal_rect.topleft)
            self.surface.blit(hard_text, hard_rect.topleft)

            pygame.display.flip()