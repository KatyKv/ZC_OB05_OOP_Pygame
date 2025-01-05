import pygame
import sys
from menu import MainGameMenu
import arcanoid
import snake

pygame.init()

# Экран и настройки
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Игры Pygame')

while True:
    main_menu = MainGameMenu(screen)
    choice = main_menu.run()

    if choice == 'arcanoid':
        arcanoid.main()
    elif choice == 'snake':
        snake.main()
    elif choice == 'exit':
        pygame.quit()
        sys.exit()
