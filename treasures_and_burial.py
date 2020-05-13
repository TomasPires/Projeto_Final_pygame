import pygame
import random

pygame.init()

WIDTH = 1080
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')

gamerun = True

while gamerun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False
    
    window.fill((0,0,0))
    pygame.display.update()

pygame.quit()