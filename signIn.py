import sqlite3
import pygame
import os
import time


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (200, 200, 200)
        self.color_active = (255, 255, 255)
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = pygame.font.Font('LEMONMILK-Medium.otf', 20).render(text, True, self.color_inactive)
        self.active = False
        self.font = pygame.font.Font('LEMONMILK-Medium.otf', 20)
        self.placeholder_color = (150, 150, 150)
        self.placeholder_text = ''
        self.is_password_field = False
        self.draw_placeholder = True

    def set_placeholder(self, text):
        self.placeholder_text = text
        self.draw_placeholder = True

    def set_password_field(self, is_password):
        self.is_password_field = is_password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user's clicked on the input box, toggle active state
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.draw_placeholder = False
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Draw the text and the rectangle
        text_to_draw = self.text
        if self.is_password_field:
            text_to_draw = '*' * len(self.text)

        txt_surface = self.font.render(text_to_draw, True, (0, 0, 0))

        if self.active:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=4)
        else:
            pygame.draw.rect(screen, (220, 220, 220), self.rect, border_radius=4)

        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw placeholder text if active and the text-bar is empty
        if not self.active and not self.text:
            placeholder_surface = self.font.render(self.placeholder_text, True, self.placeholder_color)
            screen.blit(placeholder_surface, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=4)


class SignIn:
    def __init__(self, data_store, surfaceWidth, surfaceHeight):
        # Utility
        self.Session_Info = data_store
        self.surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))


        # Colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.MINT_GREEN = (194, 239, 235)
        self.CERULEAN = (0, 126, 167)
        self.POMP_AND_POWER = (161, 103, 165)
        self.TEKHELET = (74, 48, 109)
        self.MOONSTONE = (0, 159, 183)
        self.PALINSTINATE_BLUE = (35, 46, 209)
        self.RICH_BLACK = (14, 19, 23)
        self.OUTER_SPACE = (67, 80, 88)
        self.BACKGROUND_BASE = (240, 238, 228)
        self.PANEL_BACKGROUND = (249, 245, 235)
        self.HIGHLIGHT_ACTIVE = (217, 138, 111)
        self.TAB_TEXT_INACTIVE = (136, 128, 118)
        self.PRIMARY_TEXT = (74, 67, 61)
        self.SECONDARY_TEXT = (120, 114, 106)

        # Database
        self.DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'spaceInvadersDatabase.sqlite')

        # Animation Rects
        self.highlight_rect_width = 190
        self.highlight_rect_height = 60
        self.highlight_rect_y = 136

        # Login and signup rects
        self.login_rect_target = pygame.Rect(620, self.highlight_rect_y, self.highlight_rect_width,
                                             self.highlight_rect_height)
        self.sign_up_rect_target = pygame.Rect(833, self.highlight_rect_y, self.highlight_rect_width,
                                               self.highlight_rect_height)

        self.current_highlight_rect = pygame.Rect(0, 0, 0, 0)

        # Animation
        self.is_animating_highlight = False
        self.animation_start_time = 0
        self.animation_duration = 120

        self.animation_start_rect = None
        self.animation_target_rect = None

        self.active_tab = 'none'

        self.highlight_active = False

        # Login input boxes
        self.login_username_box = InputBox(580, 420, 500, 50)
        self.login_username_box.set_placeholder('Username')
        self.login_password_box = InputBox(580, 680, 500, 50)
        self.login_password_box.set_placeholder('Password')
        self.login_password_box.set_password_field(True)

        # Signup input boxes
        self.signup_username_box = InputBox(580, 420, 500, 50)
        self.signup_username_box.set_placeholder('Username')
        self.signup_password_box = InputBox(580, 680, 500, 50)
        self.signup_password_box.set_placeholder('Password')
        self.signup_password_box.set_password_field(True)

        # Button for submissions
        self.submit_button_rect = pygame.Rect(720, 780, 200, 60)
        self.submit_button_text = 'Enter'

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

    def draw_gradient(self, surface, start_color, end_color):
        width, height = surface.get_size()
        delta_r = (end_color[0] - start_color[0]) / width
        delta_g = (end_color[1] - start_color[1]) / width
        delta_b = (end_color[2] - start_color[2]) / width
        for x in range(width):
            new_color = (
                int(start_color[0] + delta_r * x),
                int(start_color[1] + delta_g * x),
                int(start_color[2] + delta_b * x)
            )
            pygame.draw.line(surface, new_color, (x, 0), (x, height))

    def draw(self, surface):
        start_color = self.OUTER_SPACE
        end_color = self.BACKGROUND_BASE
        self.draw_gradient(surface, start_color, end_color)

    def UI(self):
        font = pygame.font.Font('LEMONMILK-Medium.otf', 40)
        pygame.draw.rect(self.surface, self.PANEL_BACKGROUND, pygame.Rect(500, 100, 650, 800), border_radius=18)

        if self.highlight_active:
            pygame.draw.rect(self.surface, self.RICH_BLACK, self.current_highlight_rect, border_radius=2)

        sign_in_text = font.render('Log In', True, self.TAB_TEXT_INACTIVE)
        log_in_text = font.render('Sign Up', True, self.TAB_TEXT_INACTIVE)
        self.surface.blit(sign_in_text, (643, 137))
        self.surface.blit(log_in_text, (843, 138))

    def _start_highlight_animation(self, target_rect):
        self.is_animating_highlight = True
        self.animation_start_time = pygame.time.get_ticks()

        self.animation_start_rect = self.current_highlight_rect.copy()
        self.animation_target_rect = target_rect.copy()

    def update_highlight_animation(self):
        if not self.is_animating_highlight:
            return

        current_time = pygame.time.get_ticks()  # FIX: Corrected typo
        elapsed_time = current_time - self.animation_start_time

        progress = min(1.0, max(0.0, elapsed_time / self.animation_duration))

        new_x = self.animation_start_rect.x + (self.animation_target_rect.x - self.animation_start_rect.x) * progress
        new_y = self.animation_start_rect.y + (self.animation_target_rect.y - self.animation_start_rect.y) * progress
        new_width = self.animation_start_rect.width + (
                    self.animation_target_rect.width - self.animation_start_rect.width) * progress
        new_height = self.animation_start_rect.height + (
                    self.animation_target_rect.height - self.animation_start_rect.height) * progress

        self.current_highlight_rect.x = int(new_x)
        self.current_highlight_rect.y = int(new_y)
        self.current_highlight_rect.width = int(new_width)
        self.current_highlight_rect.height = int(new_height)

        if progress >= 1.0:
            self.is_animating_highlight = False

            self.current_highlight_rect = self.animation_target_rect.copy()

    def display_log_in(self):
        font = pygame.font.Font('LEMONMILK-Medium.otf', 20)

        enter_username_text = font.render('Enter Username', True, (self.OUTER_SPACE))
        enter_password_text = font.render('Enter Password', True, (self.OUTER_SPACE))

        self.surface.blit(enter_username_text, (580, 340))
        self.surface.blit(enter_password_text, (580, 600))
        self.login_username_box.draw(self.surface)
        self.login_password_box.draw(self.surface)

    def display_sign_up(self):
        font = pygame.font.Font('LEMONMILK-Medium.otf', 20)
        enter_username_text = font.render('Enter Username', True, (self.OUTER_SPACE))
        enter_password_text = font.render('Enter Password', True, (self.OUTER_SPACE))

        self.surface.blit(enter_username_text, (580, 340))
        self.surface.blit(enter_password_text, (580, 600))

        self.signup_username_box.draw(self.surface)
        self.signup_password_box.draw(self.surface)

    def handle_login(self):
        username = self.login_username_box.text
        password = self.login_password_box.text
        result = self.runsql('''
            select * from tblUser where username = ? and password = ?
        ''', (username, password))


        if result:
            print('Log in is successful')
            self.Session_Info.add_data('username', username)
            return username, True
        else:
            print('Invalid username or password please try again')

    def handle_signup(self):
        username = self.signup_username_box.text
        password = self.signup_password_box.text

        try:
            self.runsql('''
                insert into tblUser (username, password) values (?, ?)
            ''', (username, password))

            print('Sign up is successful')
            self.Session_Info.add_data('username', username)
            return True

        except sqlite3.IntegrityError:
            print(f'Sign up failed for {username}. Username may already exists')

        except sqlite3.Error as e:
            print(f"Sign up failed due to a database error: {e}")

        return False

    def show_screen(self):
        on_log = False
        on_sign = False

        clock = pygame.time.Clock()

        run = True

        while run:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT:
                    return False


                # Handle events for the input boxes for both log in and sign up
                if on_log:
                    self.login_username_box.handle_event(event)
                    self.login_password_box.handle_event(event)
                elif on_sign:
                    self.signup_username_box.handle_event(event)
                    self.signup_password_box.handle_event(event)

                # Allow the user to confirm by pressing enter as well
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if on_log:
                        print("Log In via Enter key")
                        self.handle_login()
                    elif on_sign:
                        print("Sign Up via Enter key")
                        self.handle_signup()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for Log In tab click
                    if self.login_rect_target.collidepoint(mouse_pos):
                        on_log = True
                        on_sign = False

                        if not self.highlight_active or self.active_tab != 'log':
                            if not self.highlight_active:
                                self.current_highlight_rect = self.login_rect_target.copy()
                            self.highlight_active = True
                            self._start_highlight_animation(self.login_rect_target)
                            self.active_tab = 'log'

                    # Check for Sign Up tab click
                    elif self.sign_up_rect_target.collidepoint(mouse_pos):
                        on_log = False
                        on_sign = True

                        if not self.highlight_active or self.active_tab != 'sign':
                            if not self.highlight_active:
                                self.current_highlight_rect = self.sign_up_rect_target.copy()
                            self.highlight_active = True
                            self._start_highlight_animation(self.sign_up_rect_target)
                            self.active_tab = 'sign'

                    # Check for submission
                    elif self.submit_button_rect.collidepoint(mouse_pos):
                        if on_log:
                             if self.handle_login():
                                 return True
                        elif on_sign:
                            if self.handle_signup():
                                return True

            self.update_highlight_animation()
            self.draw(self.surface)
            self.UI()

            # Draw the appropriate input boxes and the submit button
            if on_log:
                self.display_log_in()
                self._draw_submit_button()
            elif on_sign:
                self.display_sign_up()
                self._draw_submit_button()

            clock.tick(60)
            pygame.display.update()

        return True

    # Helper method to clean the code a bit
    def _draw_submit_button(self):
        pygame.draw.rect(self.surface, self.RICH_BLACK, self.submit_button_rect, border_radius=10)
        font = pygame.font.Font('LEMONMILK-Medium.otf', 30)
        text_surface = font.render(self.submit_button_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=self.submit_button_rect.center)
        self.surface.blit(text_surface, text_rect)