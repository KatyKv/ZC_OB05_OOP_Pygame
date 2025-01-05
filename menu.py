import pygame
import sys


class BaseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 36)
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.button_color = (169, 169, 169)  # Светло-серый
        self.selected_color = (0, 200, 0)

    def draw_text(self, text, font, color, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.centerx = self.screen.get_width() // 2  # Центровка по горизонтали
        text_rect.y = y
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, x, y, width, height, selected):
        color = self.selected_color if selected else self.button_color
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, button_rect)
        text_obj = self.font_medium.render(text, True, self.bg_color)
        text_rect = text_obj.get_rect(center=button_rect.center)
        self.screen.blit(text_obj, text_rect)
        return button_rect

class MainGameMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)

            # Рисуем заголовок
            self.draw_text('Главное меню', self.font_large, self.text_color, 50)

            # Рисуем кнопки
            arcanoid_button = self.draw_button('Арканоид', self.screen.get_width() // 2 - 100, 200, 200, 50, False)
            snake_button = self.draw_button('Змейка', self.screen.get_width() // 2 - 100, 300, 200, 50, False)
            exit_button = self.draw_button('Выход', self.screen.get_width() // 2 - 100, 400, 200, 50, False)
            self.draw_text('Выход в главное меню из игр: F10', self.font_medium, self.text_color, 540)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if arcanoid_button.collidepoint(event.pos):
                        return 'arcanoid'
                    elif snake_button.collidepoint(event.pos):
                        return 'snake'
                    elif exit_button.collidepoint(event.pos):
                        return 'exit'

            pygame.display.update()
        return 'exit'


class ArcanoidMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True
        self.selected_lives = 5

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)

            # Рисуем заголовок и инструкции
            self.draw_text('Арканоид', self.font_large, self.text_color, 50)
            self.draw_text('Управление: стрелки влево, вправо', self.font_medium, self.text_color, 160)
            self.draw_text('Скорость платформы: стрелки вверх, вниз', self.font_medium, self.text_color, 200)
            self.draw_text('Запуск шарика: пробел', self.font_medium, self.text_color, 240)
            self.draw_text('Выберите количество потерь шарика:', self.font_medium, self.text_color, 450)

            # Рисуем кнопки
            start_button = self.draw_button('Начать игру', self.screen.get_width() // 2 - 100, 320, 200, 50, True)
            lives_buttons = [
                self.draw_button('3', self.screen.get_width() // 2 - 150, 500, 50, 50, self.selected_lives == 3),
                self.draw_button('5', self.screen.get_width() // 2 - 50, 500, 50, 50, self.selected_lives == 5),
                self.draw_button('10', self.screen.get_width() // 2 + 50, 500, 50, 50, self.selected_lives == 10)
            ]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False, self.selected_lives
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        return True, self.selected_lives
                    for i, button in enumerate(lives_buttons):
                        if button.collidepoint(event.pos):
                            self.selected_lives = [3, 5, 10][i]

            pygame.display.update()
        return False, self.selected_lives

class SnakeMenu(BaseMenu):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True
        self.selected_length_win = 10
        self.selected_difficulty = "easy"
        self.difficulty_fps = {"easy": 10, "hard": 20}

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)

            # Рисуем заголовок и инструкции
            self.draw_text('Змейка', self.font_large, self.text_color, 50)
            self.draw_text('Выберите длину для победы:', self.font_medium, self.text_color, 180)

            # Кнопки для длины змейки
            length_buttons = [
                self.draw_button('10', self.screen.get_width() // 2 - 150, 250, 50, 50, self.selected_length_win == 10),
                self.draw_button('15', self.screen.get_width() // 2 - 50, 250, 50, 50, self.selected_length_win == 15),
                self.draw_button('20', self.screen.get_width() // 2 + 50, 250, 50, 50, self.selected_length_win == 20)
            ]

            # Выбор сложности
            self.draw_text('Выберите сложность:', self.font_medium, self.text_color, 350)
            difficulty_buttons = [
                self.draw_button('Легко', self.screen.get_width() // 2 - 100, 400, 100, 50, self.selected_difficulty == "easy"),
                self.draw_button('Сложно', self.screen.get_width() // 2 + 20, 400, 100, 50, self.selected_difficulty == "hard")
            ]

            # Кнопка запуска игры
            start_button = self.draw_button('Начать игру', self.screen.get_width() // 2 - 100, 500, 200, 50, True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False, self.selected_length_win, self.difficulty_fps[self.selected_difficulty]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        return True, self.selected_length_win, self.difficulty_fps[self.selected_difficulty]
                    for i, button in enumerate(length_buttons):
                        if button.collidepoint(event.pos):
                            self.selected_length_win = [10, 15, 20][i]
                    for i, button in enumerate(difficulty_buttons):
                        if button.collidepoint(event.pos):
                            self.selected_difficulty = ["easy", "hard"][i]

            pygame.display.update()
        return False, self.selected_length_win, self.difficulty_fps[self.selected_difficulty]

class GameOverMenu(BaseMenu):
    def __init__(self, screen, result):
        super().__init__(screen)
        self.result = result

    def run(self):
        while True:
            self.screen.fill(self.bg_color)

            # Рисуем текст завершения игры
            if self.result == 'win':
                self.draw_text('Победа!', self.font_large, self.text_color, 50)
            else:
                self.draw_text('Поражение!', self.font_large, self.text_color, 50)

            # Рисуем кнопки
            restart_button = self.draw_button('Рестарт', self.screen.get_width() // 2 - 150, 300, 300, 50, False)
            exit_button = self.draw_button('Выход в главное меню', self.screen.get_width() // 2 - 150, 400, 300, 50, False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        return 'restart'
                    elif exit_button.collidepoint(event.pos):
                        return 'exit'

            pygame.display.update()


if __name__ == '__main__':
    # test - menu Arcanoid
    pygame.init()

    # Экран и настройки
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    main_menu = ArcanoidMenu(screen)
    start_game, selected_lives = main_menu.run()

    if start_game:
        # Игровая логика
        game_over_menu = GameOverMenu(screen, 'win')  # Или 'lose', в зависимости от результата
        result = game_over_menu.run()
        if result == 'restart':
            # Перезапуск игры
            main_menu.run()
        else:
            pygame.quit()
            sys.exit()
