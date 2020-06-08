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

pygame.init()
pygame.mixer.init()


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')
clock = pygame.time.Clock()


def load_assets():
    assets = {}
    assets['flecha_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/objects/projectiles/arrow-16x16.png').convert_alpha()
    assets['character_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/characters/front/char0.0-96x96.png').convert()
    assets['init_screen'] = pygame.image.load('Pixel_TreasuresandBurial/img/introscreen-500x400.png').convert()
    assets['init_screen'] = pygame.transform.scale(assets['init_screen'], (WIDTH,HEIGHT))
    over_anim = []
    for i in range(1,3):
        filename = 'Pixel_TreasuresandBurial/img/gameover{0}.png'.format(i)
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img,(WIDTH,HEIGHT))
        over_anim.append(img)
    assets['over_screen'] = over_anim    
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
    assets['mapas'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa3.1.png').convert()
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
        self.delta = {"esquerda":0,"direita":0,"acima":0,"abaixo":0}
        self.velo = 5
        self.groups = groups
        self.assets = assets

        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500

    def update(self):

        self.rect.x += (self.delta["direita"]-self.delta["esquerda"])*self.velo
        self.rect.y += (self.delta["abaixo"]-self.delta["acima"])*self.velo


        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
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
        self.angle = degrees(-angle)
        self.speedx = cos(angle)*self.speed
        self.speedy = sin(angle)*self.speed 
        self.image = pygame.transform.rotate(self.image,(self.angle-45))
        self.assets = assets


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self,groups,assets,player):
        n = random.randint(0,3)
        self.assets = assets
        self.image = self.assets['elementals'][n]
        self.groups = groups
        self.rect = self.image.get_rect()
        self.rect.centerx = 550
        self.rect.centery = HEIGHT/2
        self.speed = 0
        distax = player.rect.centerx - self.rect.centerx
        distay = player.rect.centery - self.rect.centery
        angle = atan2(distay,distax)
        self.angle = degrees(angle)
        self.speedx = cos(angle)*self.speed
        self.speedy = sin(angle)*self.speed
        self.groups = groups
        self.assets = assets


    def update(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speed = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed = 0

def janela(window):        
    #grupos das sprites
    all_sprites = pygame.sprite.Group()
    all_flechas = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_flechas'] = all_flechas
    groups['all_enemies'] = all_enemies
    assets = load_assets()
    player = Char(groups, assets)
    enemy = Enemy(groups,assets,player)
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
                    player.delta["esquerda"] =1
                if event.key == pygame.K_d:
                    player.delta["direita"] =1
                if event.key == pygame.K_w:
                    player.delta["acima"] =1
                if event.key == pygame.K_s:
                    player.delta["abaixo"] =1
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.delta["esquerda"] =0
                if event.key == pygame.K_d:
                    player.delta["direita"] =0
                if event.key == pygame.K_w:
                    player.delta["acima"] =0
                if event.key == pygame.K_s:
                    player.delta["abaixo"] =0
                
            if event.type == pygame.MOUSEMOTION:
                mouse = list(pygame.mouse.get_pos())
                print(mouse) 

        if player.rect.right >= (WIDTH)-100:
            if (HEIGHT/2)-50<player.rect.bottom<(HEIGHT/2+50):
                MAPA = assets['mapas']
                player.kill()
                player = Char(groups,assets)
                player.rect.centerx = 0
                all_sprites.add(player)
                
        else:
            MAPA = assets['mapas']
            x = 0    
        all_sprites.update()
    
        window.blit(MAPA,(0,0)) #Depois, podemos usar o comando pygame.display.flip()
        all_sprites.draw(window)
        all_flechas.draw(window)
        all_enemies.draw(window)
        pygame.draw.circle(window, BLUE,(550,250),10)
        pygame.display.update()
        
janela(window)

pygame.quit()