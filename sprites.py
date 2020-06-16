import pygame
import random
from math import *
from settings import FPS, WIDTH, HEIGHT, BLACK, RED, CHAR_WIDTH, CHAR_HEIGHT, ENEMY_SIZE, CHEST_SIZE
from assets import load_assets

class Char(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.groups = groups
        self.assets = assets
        #Tiro
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 400
        #Animção
        self.imgkey = 'char_front'
        self.index = 0
        #Imagem
        self.small = False
        self.image = self.assets[self.imgkey][self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        #Movimento
        self.delta = {"left":0,"right":0,"up":0,"down":0}
        self.speed = 5

    def update(self):
        self.deltax = (self.delta["right"]-self.delta["left"])*self.speed #Variáveis de delta para serem utilizadas, também, na animação
        self.deltay = (self.delta["down"]-self.delta["up"])*self.speed
        self.rect.x += self.deltax
        self.rect.y += self.deltay

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.deltax != 0:               #Caso o personagem esteja se movendo, dependendo da direção é rodada uma animação
            if self.delta['right'] > 0:  #Direita
                self.imgkey = 'char_right'
                self.index += 1
            elif self.delta['left'] > 0: #Esquerda
                self.imgkey = 'char_left'
                self.index += 1
        elif self.deltay != 0 and self.deltax == 0: #Verticalmente e apenas verticalmente
            if self.delta['up'] > 0:
                self.imgkey = 'char_back'  #Cima
                self.index += 1
            elif self.delta['down'] > 0:   #Baixo
                self.imgkey = 'char_front'
                self.index += 1
        elif self.deltax == 0 and self.deltay == 0: #Parado
            self.imgkey = 'char_front'
            self.index = 0

        if self.index >= len(self.assets[self.imgkey]):
            self.index = 0
        
        center = self.rect.center
        self.image = self.assets[self.imgkey][self.index]
        if self.small:
            self.image=pygame.transform.scale(self.image, (41, 41))
        self.rect = self.image.get_rect()
        self.rect.center = center


    def shoot(self):                       #Sempre que atira, gera uma nova flecha
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        if elapsed_ticks > self.shoot_ticks:
            self.last_shot = now
            new_arrow = Arrow(self.assets, self.rect.centery, self.rect.centerx)
            self.groups['all_sprites'].add(new_arrow)
            self.groups['all_arrows'].add(new_arrow)
            self.assets['arrow_sound'].play()

    def undo(self):
        self.rect.x += (self.delta["left"]-self.delta["right"])*self.speed
        self.rect.y += (self.delta["up"]-self.delta["down"])*self.speed

class Arrow(pygame.sprite.Sprite):
    def __init__(self,assets,bottom,centerx):
        pygame.sprite.Sprite.__init__(self)

        self.small = False
        self.image = assets['arrow_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speed = 15
        mouse = list(pygame.mouse.get_pos())         #Trecho para que a flecha seja gerada e se movimente na direção do mouse
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

        center = self.rect.center
        if self.small:
            self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = center

class Enemy(pygame.sprite.Sprite):
    def __init__(self,groups,assets,player,pos):
        
        pygame.sprite.Sprite.__init__(self)
        n = random.randint(0,3)
        self.small = False
        self.assets = assets
        self.image = self.assets['elementals'][n]
        self.mask = pygame.mask.from_surface(self.image)
        self.groups = groups
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.centerx = WIDTH - pos[0]
        self.rect.centery = HEIGHT - pos[1]
        self.speed = 3
        distax = player.rect.centerx - self.rect.centerx   
        distay = player.rect.centery - self.rect.centery
        angle = atan2(distay,distax)
        self.angle = degrees(-angle)
        self.speedx = cos(angle)*self.speed
        self.speedy = sin(angle)*self.speed
        self.groups = groups
        self.assets = assets

    def update(self,player):
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx

        distax = player.rect.centerx - self.rect.centerx    #O inimigo se move na direção do personagem
        distay = player.rect.centery - self.rect.centery
        angle = atan2(distay,distax)
        self.angle = degrees(-angle)
        self.speedx = cos(angle)*self.speed
        self.speedy = sin(angle)*self.speed

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

#Classe das máscaras do mapa que atualizam conforme a mudança de mapa
class MapMask(pygame.sprite.Sprite):                
    def __init__(self,img): 
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def update(self,img):
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

#Classe dos baús cujas posições são definidas pelas funções chest_spawn() e chest_pos()
class Chest(pygame.sprite.Sprite):     
    def __init__(self,assets,chest_pos,player):             
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.image = self.assets['chest']
        self.rect = self.image.get_rect()
        self.rect.centerx = chest_pos[0]
        self.rect.centery = chest_pos[1]
        self.mask = pygame.mask.from_surface(self.image)

