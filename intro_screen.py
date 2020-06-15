import pygame
import random
from os import path
from settings import IMG_DIR, IMG_WIDTH, IMG_HEIGHT, BLACK, FPS, PLAY, CLOSE

def intro_screen(window):
    clock = pygame.time.Clock()

    background = pygame.image.load(path.join(IMG_DIR, 'introscreen-500x400.png')).convert()
    background = pygame.transform.scale(background, (IMG_WIDTH, IMG_HEIGHT))
    background_rect = background.get_rect()

    run = True
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = CLOSE
                run = False
            if event.type == pygame.KEYUP:
                gamestate = PLAY
                run = False
            
            window.fill(BLACK)
            window.blit(background, background_rect)
            pygame.display.flip()

    return gamestate
            

