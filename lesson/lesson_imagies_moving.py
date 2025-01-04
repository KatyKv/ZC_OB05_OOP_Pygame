# Повторение урока
import pygame
import time

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Тестовый проект')

image1 = pygame.image.load('../img/1.png')
image_rect1 = image1.get_rect()
image2 = pygame.image.load('../img/2.png')
image_rect2 = image2.get_rect()


speed = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Движение мышью
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            image_rect1.x = mouse_x - image_rect1.width / 2
            image_rect1.y = mouse_y - image_rect1.height / 2
    # Столкновение изображений
    if image_rect1.colliderect(image_rect2):
        print('Booom!')
        time.sleep(1)

    # Движение стрелками клавиатуры
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        image_rect1.x -= speed
    if keys[pygame.K_RIGHT]:
        image_rect1.x += speed
    if keys[pygame.K_UP]:
        image_rect1.y -= speed
    if keys[pygame.K_DOWN]:
        image_rect1.y += speed





    # Зацикливание за границами окна
    if image_rect1.x == window_size[0]:
        image_rect1.x = 0
    if image_rect1.x == -1:
        image_rect1.x = window_size[0]
    if image_rect1.y == window_size[1]:
        image_rect1.y = 0
    if image_rect1.y == -1:
        image_rect1.y = window_size[1]






    screen.fill((0, 0 ,0))
    screen.blit(image1, image_rect1)
    screen.blit(image2, image_rect2)




    pygame.display.flip()

pygame.quit()
