import pygame
import random
import os
from math import *

WIDTH = 600
HEIGHT = 500
FPS = 30

CHAR_SIZE = 96
ENEMY_SIZE = 40
CHEST_SIZE = 40


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
map_n0 = 1
map_n1 = 1

def load_assets():
    assets = {}
    assets['arrow_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/objects/projectiles/arrow-16x16.png').convert_alpha()
    assets['character_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/characters/front/char0.0-96x96.png').convert_alpha()
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
        img = pygame.transform.scale(img,(CHAR_SIZE,CHAR_SIZE))
        anim_right.append(img)
    assets['character_right'] = anim_right
    for i in range(10):
        frame_left = 'Pixel_TreasuresandBurial/props/characters/left/char3.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_left).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE,CHAR_SIZE))
        anim_left.append(img)
    assets['character_left'] = anim_left
    for i in range(8):
        frame_front = 'Pixel_TreasuresandBurial/props/characters/front/char0.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_front).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE,CHAR_SIZE))
        anim_front.append(img)
    assets['character_front'] = anim_front
    for i in range(8):
        frame_back = 'Pixel_TreasuresandBurial/props/characters/back/char2.{0}-96x96.png'.format(i)
        img = pygame.image.load(frame_back).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE,CHAR_SIZE))
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
        img = pygame.transform.scale(img,(ENEMY_SIZE,ENEMY_SIZE))
        elementals.append(img)
    assets['elementals'] = elementals
    maps = dict()
    for i in range(1,7):
        filename = 'Pixel_TreasuresandBurial/maps/Mapa{0}.1.png'.format(i)
        img = pygame.image.load(filename).convert()
        key = 'map{0}.1'.format(i)
        maps[key] = img
    maps['map3.2'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa3.2.png').convert()
    maps['map3.0'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa3.0.png').convert()
    maps['map5.0'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa5.0.png').convert()
    maps['map5.2'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa5.2.png').convert()
    assets['maps'] = maps
    masks = dict()
    for i in range(2,4):
        filename = 'Pixel_TreasuresandBurial/mask/Mask{0}.1.png'.format(i)
        img = pygame.image.load(filename).convert()
        img.set_colorkey(BLACK)
        key = 'map{0}.1'.format(i)
        masks[key] = img
    for i in range(5,7):
        filename = 'Pixel_TreasuresandBurial/mask/Mask{0}.1.png'.format(i)
        img = pygame.image.load(filename).convert()
        img.set_colorkey(BLACK)
        key = 'map{0}.1'.format(i)
        masks[key] = img
    masks['map2.2'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask2.2.png').convert()
    masks['map3.0'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask3.0.png').convert()
    masks['map5.0'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask5.0.png').convert()
    masks['map5.2'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask5.2.png').convert()
    masks['map6.1'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask6.1.png').convert()
    
    assets['masks'] = masks
    chests = dict()
    closed_chests = []
    for i in range(1,3):
        img = pygame.image.load('Pixel_TreasuresandBurial/props/objects/chests/chest{0}closed-32x32.png'.format(i)).convert_alpha()
        img = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
        closed_chests.append(img)
    open_chests = []
    for i in range(1,3):
        img = pygame.image.load('Pixel_TreasuresandBurial/props/objects/chests/chest{0}openEMPTY-32x32.png'.format(i)).convert_alpha()
        img = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
        closed_chests.append(img)
    chests['closed'] = closed_chests
    chests['open'] = open_chests
    content = dict()
    chest1 = []
    chest2 = []
    for i in range(1,3):
        img = pygame.image.load('Pixel_TreasuresandBurial/props/objects/chests/chest1openFULL{0}-32x32.png'.format(i)).convert_alpha()
        img = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
        chest1.append(img)
    for i in range(1,3):
        img = pygame.image.load('Pixel_TreasuresandBurial/props/objects/chests/chest2openFULL{0}-32x32.png'.format(i)).convert_alpha()
        img = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
        chest2.append(img)
    content['chest1'] = chest1
    content['chest2'] = chest2
    chests['content'] = content
    assets['chests'] = chests
    return assets

#Classes
class Char(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['character_img']
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        self.delta = {"left":0,"right":0,"up":0,"down":0}
        self.speed = 5
        self.groups = groups
        self.assets = assets

        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500

    def update(self):
        self.rect.x += (self.delta["right"]-self.delta["left"])*self.speed
        self.rect.y += (self.delta["down"]-self.delta["up"])*self.speed

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
            new_arrow = Arrow(self.assets, self.rect.centery, self.rect.centerx)
            self.groups['all_sprites'].add(new_arrow)
            self.groups['all_arrows'].add(new_arrow)

    def undo(self):
        self.rect.x += (self.delta["left"]-self.delta["right"])*self.speed
        self.rect.y += (self.delta["up"]-self.delta["down"])*self.speed

class Arrow(pygame.sprite.Sprite):
    def __init__(self,assets,bottom,centerx):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['arrow_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speed = 15
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
        
        pygame.sprite.Sprite.__init__(self)
        n = random.randint(0,3)
        self.assets = assets
        self.image = self.assets['elementals'][n]
        self.mask = pygame.mask.from_surface(self.image)
        self.groups = groups
        self.rect = self.image.get_rect()
        self.rect.centerx = 550
        self.rect.centery = HEIGHT/2
        self.speed = 5
        distax = player.rect.centerx - self.rect.centerx
        distay = player.rect.centery - self.rect.centery
        angle = atan2(distay,distax)
        self.angle = degrees(-angle)
        self.speedx = -self.speed
        self.speedy = self.speed
        self.groups = groups
        self.assets = assets


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

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

class Map(pygame.sprite.Sprite):
    def __init__(self,assets,key):
        pygame.sprite.Sprite.__init__(self)
        self.key = key
        self.image = assets['maps'][self.key]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2 

class MapMask(pygame.sprite.Sprite):
    def __init__(self,img): 
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

#Função de troca de mapa   
def map_def(player,map_name):
    
    if player.rect.top == 0 and 500 < player.rect.centerx < 600:
        if 'map{0}.{1}'.format(map_n0,(map_n1+1)) in assets['maps']:
            map_n1 += 1
            player.rect.centerx = 0
        else:
            map_n1 += 0
    elif 200 < player.rect.centery < 300 and player.rect.right == WIDTH:
        if 'map{0}.{1}'.format((map_n0+1),map_n1) in assets['maps']:
            map_n0 += 1
            player.rect.centerx = 0
        else:
            map_n0 += 0
            
    map_name = 'map{0}.{1}'.format(map_n0,map_n1)
    map_img = assets['maps'][map_name]
    return map_n0,map_n1

def game_window(window):
    #grupos das sprites
    all_sprites = pygame.sprite.Group()
    all_arrows = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    water_mask_group = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_arrows'] = all_arrows
    groups['all_enemies'] = all_enemies
    assets = load_assets()
    player = Char(groups, assets)
    enemy = Enemy(groups, assets, player)
    water_mask = MapMask(assets['masks']['map3.1'])
    all_sprites.add(player)
    all_enemies.add(enemy)
    water_mask_group.add(water_mask)
    
    #Loop principal
    gamerun = True
    while gamerun:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.delta["left"] =1
                if event.key == pygame.K_d:
                    player.delta["right"] =1
                if event.key == pygame.K_w:
                    player.delta["up"] =1
                if event.key == pygame.K_s:
                    player.delta["down"] =1
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.delta["left"] =0
                if event.key == pygame.K_d:
                    player.delta["right"] =0
                if event.key == pygame.K_w:
                    player.delta["up"] =0
                if event.key == pygame.K_s:
                    player.delta["down"] =0
                
            if event.type == pygame.MOUSEMOTION:
                mouse = list(pygame.mouse.get_pos())
                print(mouse) 

                

        hits = pygame.sprite.groupcollide(all_enemies, all_arrows, True, True, pygame.sprite.collide_mask)

        all_sprites.update()
        
        in_water = pygame.sprite.spritecollide(player,water_mask_group,False,pygame.sprite.collide_mask)
        
        if in_water:
            player.undo()
            print(in_water)

        all_sprites.draw(window)
        all_arrows.draw(window)
        all_enemies.draw(window)
        pygame.display.update()
        
game_window(window)

pygame.quit()