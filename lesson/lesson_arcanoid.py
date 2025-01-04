# Повторение урока
import pygame
import sys

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Арканоид')

# Параметры кирпичей
brick_rows = 5
brick_cols = 10
brick_width = window_size[0] // brick_cols
brick_height = 20
brick_gap = 5 # Промежуток между кирпичами
# Список кирпичей:
bricks = [(col * (brick_width + brick_gap),
           row * (brick_height + brick_gap))
          for row in range(brick_rows)
          for col in range(brick_cols)]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0 , 255)

# ФПС
clock = pygame.time.Clock()
fps = 60

# Параметры платформы
paddle_width, paddle_height = 100, 10
paddle_x = (window_size[0] - paddle_width) // 2
paddle_y = window_size[1] - paddle_height - 5
paddle_speed = 5

# Параметры мяча
ball_radius = 10
ball_x = window_size[0] // 2
ball_y = paddle_y - ball_radius
ball_speed_x = 4
ball_speed_y = -4


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Движение платформы
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < window_size[0] - paddle_width:
        paddle_x += paddle_speed
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
        ball_x = window_size[0] // 2
        ball_y = paddle_y - ball_radius
        ball_speed_y *= -1
    # Столкновение с платформой
    if (paddle_x <= ball_x <= paddle_x + paddle_width and
        paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height):
        ball_speed_y *= -1

    brick_rects = [pygame.Rect(brick[0], brick[1],
                               brick_width, brick_height)
                   for brick in bricks]
    for i, brick_rect in enumerate(brick_rects):
        if brick_rect.collidepoint(ball_x, ball_y):
            bricks.pop(i) # удаление кирпича
            ball_speed_y *= -1
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
        pygame.draw.rect(screen, WHITE,
                         pygame.Rect(brick[0], brick[1],
                                     brick_width, brick_height))

    pygame.display.flip()

    # Контроль ФПС
    clock.tick(fps)

pygame.quit()
sys.exit()