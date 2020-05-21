import pygame
import random
import os

WIDTH = 1080
HEIGHT = 720
FPS = 30

WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
BLACK = (0,0,0)

MAPA = GREEN #Variável para mudança de mapas conforme o movimento do personagem (teste com cores)
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
        self.image = pygame.image.load('Pixel_TreasuresandBurial/props/characters/front/char0.0-96x96.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.x_speed = 0
        self.y_speed = 0
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_speed -=5
            if event.key == pygame.K_RIGHT:
                player.x_speed +=5
            if event.key == pygame.K_UP:
                player.y_speed -=5
            if event.key == pygame.K_DOWN:
                player.y_speed +=5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.x_speed +=5
            if event.key == pygame.K_RIGHT:
                player.x_speed -=5
            if event.key == pygame.K_UP:
                player.y_speed +=5
            if event.key == pygame.K_DOWN:
                player.y_speed -=5
    
    if player.rect.right >= (WIDTH)-100:
        if (HEIGHT/2)-50<player.rect.bottom<(HEIGHT/2+50):
            MAPA = BLACK
    else:
        MAPA = GREEN
            
    all_sprites.update()
   
    window.fill(MAPA) #Depois, podemos usar o comando pygame.display.flip()
    pygame.draw.circle(window, BLUE,(980,360),10)
    all_sprites.draw(window)

    pygame.display.update()

pygame.quit()