import pygame
import random
from settings import WIDTH, HEIGHT, INIT, PLAY, CLOSE
from intro_screen import intro_screen
from game_screen import game_window

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')

gamestate = INIT

while gamestate != CLOSE:
    if gamestate == INIT:
        gamestate = intro_screen(window)
    elif gamestate == PLAY:
        gamestate = game_window(window)

pygame.quit()
