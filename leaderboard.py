import pygame, sqlite3


class Leaderboard:
    def __init__(self, inventoryWidth, inventoryHeight, sessionInfo):
        self.inventoryWidth = inventoryWidth
        self.inventoryHeight = inventoryHeight
        self.surface = pygame.display.set_mode((inventoryWidth, inventoryHeight))
        self.dataStore = sessionInfo

        self.font = pygame.font.Font('LEMONMILK-Bold.otf', 20)
        self.background = pygame.transform.scale(
            pygame.image.load('background.jpg').convert_alpha(), self.surface.get_size()
        )

    def runsql(self, *args):
        conn = sqlite3.connect('spaceInvadersDatabase.sqlite')
        conn.execute('PRAGMA foreign_keys = 1')
        cursor = conn.cursor()
        if len(args) == 1:
            cursor.execute(args[0])
        else:
            cursor.execute(args[0], args[1])
        conn.commit()
        return cursor.fetchall()

    def getLeaderboardData(self):
        query = "SELECT username, highscore FROM tblUser ORDER BY highscore DESC LIMIT 10"
        return self.runsql(query)

    def showScreen(self):
        leaderboard_data = self.getLeaderboardData()

        # Button to go back to menu
        back_button_rect = pygame.Rect(50, 50, 150, 50)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        return 'quit'

            self.surface.blit(self.background, (0, 0))

            # Display the title
            title_text = self.font.render("LEADERBOARD", True, "white")
            title_rect = title_text.get_rect(center=(self.surface.get_width() / 2, 100))
            self.surface.blit(title_text, title_rect)

            y_offset = 200  # Starting Y position for the list
            rank_font = pygame.font.Font('LEMONMILK-Medium.otf', 30)

            # Iterate through the data and display each player
            for rank, player in enumerate(leaderboard_data):
                username = player[0]
                highscore = player[1]

                # Format using username and highscore
                leaderboard_text = f"#{rank + 1}  {username} - {highscore}"
                rendered_text = rank_font.render(leaderboard_text, True, "white")
                rendered_rect = rendered_text.get_rect(center=(self.surface.get_width() / 2, y_offset))
                self.surface.blit(rendered_text, rendered_rect)

                y_offset += 50  # Move down

            # Draw the back button
            pygame.draw.rect(self.surface, (200, 200, 200), back_button_rect, border_radius=10)
            back_text_surface = self.font.render("Back", True, (0, 0, 0))
            back_text_rect = back_text_surface.get_rect(center=back_button_rect.center)
            self.surface.blit(back_text_surface, back_text_rect)

            pygame.display.flip()

        return 'quit'
