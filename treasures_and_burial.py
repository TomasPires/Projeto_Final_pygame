import pygame
import random
import os
from math import *
WIDTH = 600
HEIGHT = 500
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


def load_assets():
    assets = {}
    assets['flecha_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/objects/projectiles/arrow-16x16.png').convert_alpha()
    assets['character_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/characters/front/char0.0-96x96.png').convert_alpha()
    anim_right = []
    anim_left = []
    anim_front = []
    anim_back = []
    for i in range(10):
        frame_right = 'Pixel_TreasuresandBurial/props/characters/right/char1.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_right).convert_alpha()
        img = pygame.transform.scale(img,(96,96))
        anim_right.append(img)
    assets['character_right'] = anim_right
    for i in range(10):
        frame_left = 'Pixel_TreasuresandBurial/props/characters/left/char3.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_left).convert_alpha()
        img = pygame.transform.scale(img,(96,96))
        anim_left.append(img)
    assets['character_left'] = anim_left
    for i in range(8):
        frame_front = 'Pixel_TreasuresandBurial/props/characters/front/char0.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_front).convert_alpha()
        img = pygame.transform.scale(img,(96,96))
        anim_front.append(img)
    assets['character_front'] = anim_front
    for i in range(8):
        frame_back = 'Pixel_TreasuresandBurial/props/characters/back/char2.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_back).convert_alpha()
        img = pygame.transform.scale(img,(96,96))
        anim_front.append(img)
    assets['character_back'] = anim_back
    anim_torch = []
    for i in range(1,5):
        frame_torch = 'Pixel_TreasuresandBurial/props/animation/fire{0}-128x128.png'.format(i)
        img = pygame.image.load(frame_torch).convert_alpha()
        img = pygame.transform.scale(img,(32,32))
        anim_torch.append(img)
    assets['torch_anim'] = anim_torch 
    elementals = []
    for i in range(4):
        elements = ['fire','water','air','earth']
        filename = 'Pixel_TreasuresandBurial/props/enemies/{0}_elemental.png'.format(elements[i])
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img,(32,32))
        elementals.append(img)
    assets['elementals'] = elementals
    return assets
    
#Classes
class Char(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)


        self.image = assets['character_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        self.x_speed = 0
        self.y_speed = 0
        self.groups = groups
        self.assets = assets

        # Só será possível atirar uma vez a cada 500 milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500

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

    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # A nova bala vai ser criada logo acima e no centro horizontal da nave
            nova_flecha = Flecha(self.assets, self.rect.centery, self.rect.centerx)
            self.groups['all_sprites'].add(nova_flecha)
            self.groups['all_flechas'].add(nova_flecha)

class Flecha(pygame.sprite.Sprite):
    def __init__(self,assets,bottom,centerx):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['flecha_img']
        self.mask=pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speed = 10
        mouse = list(pygame.mouse.get_pos()) 
        distx = mouse[0] - self.rect.centerx
        disty = mouse[1] - self.rect.centery
        angle = atan2(disty,distx)
        self.angle = degrees(angle)
        self.speedx = cos(angle)*self.speed
        self.speedy = sin(angle)*self.speed 

    def update(self):
        # A bala só se move no eixo y
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

def janela(window):        
    #grupos das sprites
    all_sprites = pygame.sprite.Group()
    all_flechas = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_flechas'] = all_flechas
    assets = load_assets()
    player = Char(groups, assets)
    all_sprites.add(player)
    

    #Loop principal
    gamerun = True

    while gamerun:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.x_speed -=5
                if event.key == pygame.K_d:
                    player.x_speed +=5
                if event.key == pygame.K_w:
                    player.y_speed -=5
                if event.key == pygame.K_s:
                    player.y_speed +=5
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.x_speed +=5
                if event.key == pygame.K_d:
                    player.x_speed -=5
                if event.key == pygame.K_w:
                    player.y_speed +=5
                if event.key == pygame.K_s:
                    player.y_speed -=5
                
            if event.type == pygame.MOUSEMOTION:
                mouse = list(pygame.mouse.get_pos())  ###
                print(mouse) 

        if player.rect.right >= (WIDTH)-100:
            if (HEIGHT/2)-50<player.rect.bottom<(HEIGHT/2+50):
                MAPA = BLACK
        else:
            MAPA = GREEN
                
        all_sprites.update()
    
        window.fill(MAPA) #Depois, podemos usar o comando pygame.display.flip()
        all_sprites.draw(window)
        all_flechas.draw(window)
        pygame.draw.circle(window, BLUE,(400,360),10) ###
        pygame.display.update()
        
janela(window)

pygame.quit()