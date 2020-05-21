import pygame
import random
import os

WIDTH = 1080
HEIGHT = 720
FPS = 30

 #Iniciando o PyGame, algumas funções e criando a janela
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')
clock = pygame.time.Clock()

#class Character(pygame.sprite.Sprite):
 #   def __init__(self,image):

all_sprites = pygame.sprite.Group() 
#Loop principal
gamerun = True

while gamerun:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False
    
    all_sprites.update()

    window.fill((0,0,0)) #Depois, podemos usar o comando pygame.display.flip()
    all_sprites.draw(window)

    pygame.display.update()

pygame.quit()