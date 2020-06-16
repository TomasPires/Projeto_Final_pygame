import pygame
import random
from os import path
from settings import IMG_DIR, SOUND_DIR, IMG_WIDTH, IMG_HEIGHT, BLACK, FPS, PLAY, CLOSE
from assets import load_assets

def intro_screen(window):
    
    clock = pygame.time.Clock()
    
    # Carrega a imagem de fundo
    background = pygame.image.load(path.join(IMG_DIR, 'introscreen-500x400.png')).convert()  
    background = pygame.transform.scale(background, (IMG_WIDTH, IMG_HEIGHT))
    background_rect = background.get_rect()

    # Loop da tela
    run = True
    # Carrega a música da tela de início
    pygame.mixer.music.load(path.join(SOUND_DIR, 'init_screen.wav'))
    pygame.mixer.music.play(loops=-1)

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
            

