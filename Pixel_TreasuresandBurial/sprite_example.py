import pygame
import random
import os


WIDTH = 1080
HEIGHT = 720
FPS = 30

#game_folder = os.path.dirname(__file__)
#img_folder = os.path.join(game_folder,'"pasta das imagens"')

 #Iniciando o PyGame, algumas funções e criando a janela
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')
clock = pygame.time.Clock()

#Classes
class Char(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('props/characters/front/char0.0-96x96.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        self.x_speed = 0
        self.y_speed = 0
        keystate = pygame.key.get_pressed()

#grupos das sprites
all_sprites = pygame.sprite.Group() 
player = Char()
all_sprites.add(player)

#Loop principal
gamerun = True

while gamerun:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False
    
    all_sprites.update()

    window.fill((255,255,255)) #Depois, podemos usar o comando pygame.display.flip()
    all_sprites.draw(window)

    pygame.display.update()

pygame.quit()