import pygame
import sys
import random
from menu import SnakeMenu, GameOverMenu

def main():
    pygame.init()

    # Параметры экрана
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Змейка')

    # Цвета
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

    # Размеры блоков
    block_size = 20

    font = pygame.font.Font(None, 36)

    def draw_food():
        """Создаёт случайные координаты еды в допустимой области."""
        text_height = font.size("Съедено 00 / 00")[1]  # Высота текста
        return (random.randrange(1, window_size[0] // block_size) * block_size,
                random.randrange(1 + text_height // block_size, window_size[1] // block_size) * block_size)


    # Инициализация змейки
    snake = [(100, 100), (80, 100), (60, 100)]  # Начальная длина змейки
    start_len = len(snake)
    snake_direction = (block_size, 0)  # Направление змейки (вправо)


    # Инициализация еды
    apple_image = pygame.image.load('./img/apple.jpg')
    apple_image = pygame.transform.scale(apple_image, (block_size, block_size))
    food = draw_food()

    # Длина змейки для победы + Скорость игры
    clock = pygame.time.Clock()
    snake_menu = SnakeMenu(screen)
    start_game, length_win, fps = snake_menu.run()

    # Функция рисования змейки и еды
    def draw_snake_and_food():
        # Рисуем голову змейки как круг
        head_x, head_y = snake[0]
        pygame.draw.circle(screen, GREEN, (head_x + block_size // 2, head_y + block_size // 2), block_size // 2)
        # Рисуем остальные части тела змейки как квадратные блоки
        for segment in snake[1:]:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], block_size, block_size))
        # Еда
        screen.blit(apple_image, (food[0], food[1]))

    # Основной цикл игры
    running = True
    while running and start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, block_size):
                    snake_direction = (0, -block_size)
                if event.key == pygame.K_DOWN and snake_direction != (0, -block_size):
                    snake_direction = (0, block_size)
                if event.key == pygame.K_LEFT and snake_direction != (block_size, 0):
                    snake_direction = (-block_size, 0)
                if event.key == pygame.K_RIGHT and snake_direction != (-block_size, 0):
                    snake_direction = (block_size, 0)
                if event.key == pygame.K_F10:
                    return

        # Обновление позиции змейки
        head_x, head_y = snake[0]
        new_head = (head_x + snake_direction[0], head_y + snake_direction[1])
        snake = [new_head] + snake[:-1]  # Перемещаем голову и удаляем последний сегмент

        # Проверка столкновения с едой
        if new_head == food:
            snake.append(snake[-1])  # Увеличиваем длину змейки
            food = draw_food()

        # Проверка столкновения с границей экрана или самой собой
        if new_head[0] < 0 or new_head[0] >= window_size[0] or \
           new_head[1] < 0 or new_head[1] >= window_size[1] or \
           new_head in snake[1:]:
            start_game = False
            game_over_menu = GameOverMenu(screen, 'loss')
            result = game_over_menu.run()
            if result == 'restart':
                # Перезапуск игры
                # Инициализация змейки
                snake = [(100, 100), (80, 100), (60, 100)]  # Начальная длина змейки
                snake_direction = (block_size, 0)  # Направление змейки (вправо)
                start_game = True
            else:
                return

        # Победа, если длина змейки достигла цели
        if len(snake) - start_len >= length_win:
            start_game = False
            game_over_menu = GameOverMenu(screen, 'win')
            result = game_over_menu.run()
            if result == 'restart':
                # Перезапуск игры
                # Инициализация змейки
                snake = [(100, 100), (80, 100), (60, 100)]  # Начальная длина змейки
                snake_direction = (block_size, 0)  # Направление змейки (вправо)
                start_game = True
            else:
                return

        # Отрисовка экрана
        screen.fill(BLACK)
        draw_snake_and_food()

        # Текст
        text = f"Съедено {len(snake) - start_len} / {length_win}"
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()

        # Установка скорости игры
        clock.tick(fps)

    return
