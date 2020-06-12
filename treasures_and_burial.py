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


def load_assets():
    assets = {}
    assets['arrow_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/objects/projectiles/arrow-16x16.png').convert_alpha()
    assets['character_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/characters/front/char0.0-96x96.png').convert_alpha()
    char_front = []
    for i in range(0,8):
        filename = 'Pixel_TreasuresandBurial/props/characters/front/char0.{0}-96x96.png'.format(i)
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_front.append(img)
    char_right = []
    for i in range(0,10):
        filename = 'Pixel_TreasuresandBurial/props/characters/right/char1.{0}-96x96.png'.format(i)
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_right.append(img)
    char_back = []
    for i in range(0,8):
        filename = 'Pixel_TreasuresandBurial/props/characters/back/char2.{0}-96x96.png'.format(i)
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_back.append(img) 
    char_left = []
    for i in range(0,10):
        filename = 'Pixel_TreasuresandBurial/props/characters/left/char3.{0}-96x96.png'.format(i)
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_left.append(img)
    assets['char_front'] = char_front
    assets['char_right'] = char_right
    assets['char_back'] = char_back
    assets['char_left'] = char_left
    assets['init_screen'] = pygame.image.load('Pixel_TreasuresandBurial/img/introscreen-500x400.png').convert()
    assets['init_screen'] = pygame.transform.scale(assets['init_screen'], (WIDTH,HEIGHT))
    over_anim = []
    for i in range(1,3):
        filename = 'Pixel_TreasuresandBurial/img/gameover{0}.png'.format(i)
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img,(WIDTH,HEIGHT))
        over_anim.append(img)
    assets['over_screen'] = over_anim    
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
        img.set_colorkey(WHITE)
        elementals.append(img)
    assets['elementals'] = elementals
    maps = dict()
    for i in range(1,6):
        filename = 'Pixel_TreasuresandBurial/maps/Mapa{0}.1.png'.format(i)
        img = pygame.image.load(filename).convert()
        key = 'map{0}.1'.format(i)
        maps[key] = img
    maps['map2.2'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa2.2.png').convert()
    maps['map3.0'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa3.0.png').convert()
    maps['map3.2'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa3.2.png').convert()
    maps['map5.0'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa5.0.png').convert()
    maps['map5.2'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa5.2.png').convert()
    maps['map6.2'] = pygame.image.load('Pixel_TreasuresandBurial/maps/Mapa6.2.png').convert()
    assets['maps'] = maps
    masks = dict()
    for i in range(1,6):
        filename = 'Pixel_TreasuresandBurial/mask/Mask{0}.1.png'.format(i)
        img = pygame.image.load(filename).convert()
        img.set_colorkey(BLACK)
        key = 'map{0}.1'.format(i)
        masks[key] = img
    masks['map2.2'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask2.2.png').convert()
    masks['map3.0'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask3.0.png').convert()
    masks['map3.2'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask3.2.png').convert()
    masks['map5.0'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask5.0.png').convert()
    masks['map5.2'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask5.2.png').convert()
    masks['map6.2'] = pygame.image.load('Pixel_TreasuresandBurial/mask/Mask6.2.png').convert()
    
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

    assets['init_music'] = pygame.mixer.music.load('sound/init_screen.wav')
    assets['arrow_sound'] = pygame.mixer.music.load('sound/arrow.wav')
    assets['background_music'] = pygame.mixer.music.load('sound/background.mp3')
    pygame.mixer.music.set_volume(0.4)
    return assets

#Classes
class Char(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)
        
        self.groups = groups
        self.assets = assets
        #Tiro
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500
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

        if self.deltax != 0:
            if self.delta['right'] > 0:
                self.imgkey = 'char_right'
                self.index += 1
            elif self.delta['left'] > 0:
                self.imgkey = 'char_left'
                self.index += 1
        elif self.deltay != 0 and self.deltax == 0:
            if self.delta['up'] > 0:
                self.imgkey = 'char_back'
                self.index += 1
            elif self.delta['down'] > 0:
                self.imgkey = 'char_front'
                self.index += 1
        elif self.deltax == 0 and self.deltay == 0:
            self.imgkey = 'char_front'
            self.index = 0

        if self.index >= len(self.assets[self.imgkey]):
            self.index = 0
        
        center = self.rect.center
        self.image = self.assets[self.imgkey][self.index]
        if self.small:
            self.image=pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.center = center


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

        self.small = False
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

        center = self.rect.center
        if self.small:
            self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = center

class Enemy(pygame.sprite.Sprite):
    def __init__(self,groups,assets,player):
        
        pygame.sprite.Sprite.__init__(self)
        n = random.randint(0,3)
        self.small = False
        self.assets = assets
        self.image = self.assets['elementals'][n]
        self.mask = pygame.mask.from_surface(self.image)
        self.groups = groups
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - player.rect.centerx
        self.rect.centery = HEIGHT - player.rect.centery
        self.speed = 5
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

        distax = player.rect.centerx - self.rect.centerx
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

        center = self.rect.center
        if self.small:
            self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = center


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

#Função de troca de mapa   
def map_def(player,enemy,map_k,assets):
    map_name = 'map{0}.{1}'.format(map_k["map_n0"],map_k["map_n1"])
    player.small = False
    enemy.small = False
    if map_name == 'map4.1':#Mapa diferente requer condições diferentes
        player.small = True
        enemy.small = True
        if 290<=player.rect.centerx <= 320 and 330 <= player.rect.centery <= 385:
            map_k["map_n0"] += 1
            player.rect.left = 30
            player.rect.centery = 250
        elif player.rect.bottom == 500 and player.rect.left == 0:
            map_k["map_n0"] -= 1
            player.rect.right = WIDTH-1
            player.rect.centery = HEIGHT
        elif 215 <= player.rect.centery <= 385 and player.rect.right == WIDTH:
            map_k["map_n0"] += 0
    elif map_name == 'map5.1':#Saída para mapa diferente
        if 215 <= player.rect.centery <= 385 and player.rect.left == 0:
            map_k["map_n0"] -= 1
            player.rect.centerx = 310
            player.rect.centery = 386
        elif player.rect.top <= 30 and  215<=player.rect.centerx <=385: #Mudança pra cima
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]+1)) in assets['maps']:
                map_k["map_n1"] +=1
                player.rect.centery = 474
            else:
                map_k["map_n1"] +=0
        elif 475< player.rect.centery  and 215 <= player.rect.centerx <= 385: #Mudança pra baixo
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]-1)) in assets['maps']:
                map_k["map_n1"] -=1
                player.rect.top = 31
            else:
                map_k["map_n1"] -=0
    else:
        if player.rect.top <= 30 and  215<=player.rect.centerx <=385: #Mudança pra cima
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]+1)) in assets['maps']:
                map_k["map_n1"] +=1
                player.rect.centery = 424
            else:
                map_k["map_n1"] +=0
        elif 215 <= player.rect.centery <= 385 and player.rect.right == WIDTH: #Mudança pra direita
            if 'map{0}.{1}'.format((map_k["map_n0"]+1),map_k["map_n1"]) in assets['maps']:
                map_k["map_n0"] += 1
                player.rect.left = 1
            else:
                map_k["map_n0"] += 0
        elif 425< player.rect.centery  and 215 <= player.rect.centerx <= 385: #Mudança pra baixo
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]-1)) in assets['maps']:
                map_k["map_n1"] -=1
                player.rect.top = 31
            else:
                map_k["map_n1"] -=0
        elif 215 <= player.rect.centery <= 385 and player.rect.left == 0: #Mudança pra esquerda
            if 'map{0}.{1}'.format((map_k["map_n0"]-1),map_k["map_n1"]) in assets['maps']:
                map_k["map_n0"] -= 1
                player.rect.right = WIDTH-1
            else:
                map_k["map_n0"] -= 0
    map_name = 'map{0}.{1}'.format(map_k["map_n0"],map_k["map_n1"])
    map_img = assets['maps'][map_name]
    mask_img = assets['masks'][map_name]
    return map_img, mask_img

def game_window(window):    
    map_k = {"map_n0":5,"map_n1":1}  
    #grupos das sprites
    all_sprites = pygame.sprite.Group()
    all_arrows = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    mask_group = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_arrows'] = all_arrows
    groups['all_enemies'] = all_enemies
    assets = load_assets()
    player = Char(groups, assets)
    enemy = Enemy(groups, assets, player)
    all_sprites.add(player)
    all_enemies.add(enemy)
    
    MASK = MapMask(map_def(player,enemy,map_k,assets)[1])
    mask_group.add(MASK)

    #Loop principal
    gamerun = True
    pygame.mixer.music.play(loops=-1)
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
        all_enemies.update(player)
        all_arrows.update()
        
        MASK.kill()
        MAP = map_def(player,enemy,map_k,assets)[0]
        MASK = MapMask(map_def(player,enemy,map_k,assets)[1])
        mask_group.add(MASK)
        
        
        map_collide = pygame.sprite.spritecollide(player,mask_group,False,pygame.sprite.collide_mask)
        
        if map_collide:
            player.undo()
            print(map_collide)   
        
        window.blit(MAP,(0,0))
        
        all_sprites.draw(window)
        all_arrows.draw(window)
        all_enemies.draw(window)
        pygame.display.update()
        
game_window(window)

pygame.quit()