import pygame
import random
from settings import WIDTH, HEIGHT, INIT, PLAY, CLOSE
from intro_screen import intro_screen
from game_screen import game_window

#Inicia o pygame
pygame.init()
pygame.mixer.init()

#Define a janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')

#Roda o jogo
gamestate = INIT

while gamestate != CLOSE:
    if gamestate == INIT:
        gamestate = intro_screen(window)  #Tela de início 
    elif gamestate == PLAY:
        gamestate = game_window(window)   #Tela do jogo e game over

#Fecha o pygame
pygame.quit()
