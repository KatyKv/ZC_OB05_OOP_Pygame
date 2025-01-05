import pygame
import sys
from menu import ArcanoidMenu, GameOverMenu

def main():
    pygame.init()

    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Арканоид')

    def start_position(window_size, paddle_width, paddle_height, ball_radius):
        pd_x = (window_size[0] - paddle_width) // 2
        pd_y = window_size[1] - paddle_height - 5
        b_x = window_size[0] // 2
        b_y = pd_y - ball_radius
        return pd_x, pd_y, b_x, b_y

    def restart_game():
        losses = 0
        start_game = True
        bricks = [(offset_x + col * (brick_width + brick_gap),
                   row * (brick_height + brick_gap))
                  for row in range(brick_rows)
                  for col in range(brick_cols)]  # Перезаполнение кирпичей
        ball_on_paddle = True
        return losses, start_game, bricks, ball_on_paddle

    # Параметры кирпичей
    brick_width = 75
    brick_height = 20
    brick_gap = 5 # Промежуток между кирпичами
    brick_rows = 5
    # Вычисляем количество колонок, чтобы вписать кирпичи в ширину окна
    brick_cols = (window_size[0] + brick_gap) // (brick_width + brick_gap)
    # Общая ширина всех кирпичей и зазоров в строке
    total_bricks_width = ((brick_width + brick_gap) *
                        brick_cols - brick_gap)
    # Отступ слева для центрирования
    offset_x = (window_size[0] - total_bricks_width) // 2
    # Список кирпичей:
    bricks = [(offset_x + col * (brick_width + brick_gap),
               row * (brick_height + brick_gap))
              for row in range(brick_rows)
              for col in range(brick_cols)]

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0 , 255)
    GREEN = (0, 255, 0)

    # ФПС
    clock = pygame.time.Clock()
    fps = 60

    # Параметры платформы
    paddle_width, paddle_height = 100, 10
    paddle_speed = 5
    # Параметры мяча
    ball_radius = 10
    ball_speed_mod = 4
    ball_speed_x = ball_speed_mod
    ball_speed_y = -ball_speed_mod

    paddle_x, paddle_y, ball_x, ball_y = start_position(window_size, paddle_width, paddle_height, ball_radius)

    ball_on_paddle = True
    running = True
    losses = 0

    main_menu = ArcanoidMenu(screen)
    start_game, max_losses = main_menu.run()

    while running and start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Обработка запуска мяча
            if event.type == pygame.KEYDOWN and ball_on_paddle:
                # Стартуем мяч по нажатию пробела
                if event.key == pygame.K_SPACE:
                    ball_on_paddle = False
                    ball_speed_y = -ball_speed_mod
        # Нажатие клавиш клавиатуры
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < window_size[0] - paddle_width:
            paddle_x += paddle_speed
        if keys[pygame.K_UP]:
            paddle_speed = min(paddle_speed + 0.5, 20)
        if keys[pygame.K_DOWN]:
            paddle_speed = max(paddle_speed - 0.5, 3)
        if keys[pygame.K_F10]:
            return

        if ball_on_paddle:
            # Если мяч на платформе, он следует за ней
            ball_x = paddle_x + paddle_width // 2
            ball_y = paddle_y - ball_radius
        else:
            # Движение мяча
            ball_x += ball_speed_x
            ball_y += ball_speed_y
            # Столкновение с краями экрана
            if ball_x <= 0 or ball_x >= window_size[0]:
                ball_speed_x *= -1
            if ball_y <= 0:
                ball_speed_y *= -1
            if ball_y >= window_size[1]:
                # Сброс мяча
                ball_on_paddle = True
                losses += 1
                if losses >= max_losses:
                    start_game = False
                    game_over_menu = GameOverMenu(screen, losses)
                    result = game_over_menu.run()
                    if result == 'restart':
                        # Перезапуск игры
                        losses, start_game, bricks, ball_on_paddle = restart_game()
                        paddle_x, paddle_y, ball_x, ball_y = start_position(window_size, paddle_width,
                                                                            paddle_height, ball_radius)
                    else:
                        return

        # Столкновение с платформой
        if (not ball_on_paddle and
            paddle_x <= ball_x <= paddle_x + paddle_width and
            paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height):
            ball_speed_y *= -1

        brick_rects = [pygame.Rect(brick[0], brick[1],
                                   brick_width, brick_height)
                       for brick in bricks]
        for i, brick_rect in enumerate(brick_rects):
            if brick_rect.collidepoint(ball_x, ball_y):
                bricks.pop(i) # удаление кирпича
                ball_speed_y *= -1
                if not bricks:
                    start_game = False
                    game_over_menu = GameOverMenu(screen, 'win')
                    result = game_over_menu.run()
                    if result == 'restart':
                        # Перезапуск игры
                        losses, start_game, bricks, ball_on_paddle = restart_game()
                        paddle_x, paddle_y, ball_x, ball_y = start_position(window_size, paddle_width,
                                                                            paddle_height, ball_radius)
                    else:
                        return
                break # Выход после удаления одного кирпича,
                      # чтобы не удалять несколько за кадр

        # Очистка экрана
        screen.fill(BLACK)

        # Отрисовка объектов
        pygame.draw.rect(screen, WHITE, (
            paddle_x, paddle_y, paddle_width, paddle_height
        ))
        pygame.draw.circle(screen, BLUE,
                           (ball_x, ball_y), ball_radius)
        for brick in bricks:
            pygame.draw.rect(screen, GREEN,
                             pygame.Rect(brick[0], brick[1],
                                         brick_width, brick_height))

        pygame.display.flip()

        # Контроль ФПС
        clock.tick(fps)

    return