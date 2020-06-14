import pygame
import random
from os import path
from math import *

WIDTH = 600
HEIGHT = 500
FPS = 30

CHAR_SIZE = 82
ENEMY_SIZE = 40
CHEST_SIZE = 30

MAP_DIR = path.join(path.dirname(__file__), 'Pixel_TreasuresandBurial', 'maps')
MASK_DIR = path.join(path.dirname(__file__), 'Pixel_TreasuresandBurial', 'mask')
CHAR_DIR = path.join(path.dirname(__file__),  'Pixel_TreasuresandBurial', 'props', 'characters')
ENEMY_DIR = path.join(path.dirname(__file__),  'Pixel_TreasuresandBurial', 'props', 'enemies')
OBJECT_DIR = path.join(path.dirname(__file__),  'Pixel_TreasuresandBurial', 'props', 'objects')
IMG_DIR = path.join(path.dirname(__file__), 'Pixel_TreasuresandBurial', 'img')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')

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
    assets['score_font'] = pygame.font.Font(path.join(OBJECT_DIR, 'font.ttf'), 28)
    assets['arrow_img'] = pygame.image.load(path.join(OBJECT_DIR, 'projectiles/arrow-16x16.png')).convert_alpha()
    assets['character_img'] = pygame.image.load(path.join(CHAR_DIR, 'front/char0.0-96x96.png')).convert_alpha()
    char_front = []
    for i in range(0,8):
        filename = 'front/char0.{0}-96x96.png'.format(i)
        img = pygame.image.load(path.join(CHAR_DIR,filename)).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_front.append(img)
    char_right = []
    for i in range(0,10):
        filename = 'right/char1.{0}-96x96.png'.format(i)
        img = pygame.image.load(path.join(CHAR_DIR,filename)).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_right.append(img)
    char_back = []
    for i in range(0,8):
        filename = 'back/char2.{0}-96x96.png'.format(i)
        img = pygame.image.load(path.join(CHAR_DIR,filename)).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_back.append(img) 
    char_left = []
    for i in range(0,10):
        filename = 'left/char3.{0}-96x96.png'.format(i)
        img = pygame.image.load(path.join(CHAR_DIR,filename)).convert_alpha()
        img = pygame.transform.scale(img,(CHAR_SIZE, CHAR_SIZE))
        char_left.append(img)
    assets['char_front'] = char_front
    assets['char_right'] = char_right
    assets['char_back'] = char_back
    assets['char_left'] = char_left
    assets['init_screen'] = pygame.image.load(path.join(IMG_DIR, 'introscreen-500x400.png')).convert()
    assets['init_screen'] = pygame.transform.scale(assets['init_screen'], (WIDTH,HEIGHT))
    assets['over_screen'] = pygame.image.load(path.join(IMG_DIR, 'gameover.png')).convert()
    assets['over_screen'] = pygame.transform.scale(assets['over_screen'],(WIDTH,HEIGHT))   
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
        filename = '{0}_elemental.png'.format(elements[i])
        img = pygame.image.load(path.join(ENEMY_DIR, filename)).convert_alpha()
        img = pygame.transform.scale(img,(ENEMY_SIZE,ENEMY_SIZE))
        img.set_colorkey(WHITE)
        elementals.append(img)
    assets['elementals'] = elementals
    maps = dict()
    for i in range(1,6):
        filename = 'Mapa{0}.1.png'.format(i)
        img = pygame.image.load(path.join(MAP_DIR, filename)).convert()
        key = 'map{0}.1'.format(i)
        maps[key] = img
    maps['map2.2'] = pygame.image.load(path.join(MAP_DIR, 'Mapa2.2.png')).convert()
    maps['map3.0'] = pygame.image.load(path.join(MAP_DIR, 'Mapa3.0.png')).convert()
    maps['map3.2'] = pygame.image.load(path.join(MAP_DIR, 'Mapa3.2.png')).convert()
    maps['map5.0'] = pygame.image.load(path.join(MAP_DIR, 'Mapa5.0.png')).convert()
    maps['map5.2'] = pygame.image.load(path.join(MAP_DIR, 'Mapa5.2.png')).convert()
    maps['map6.2'] = pygame.image.load(path.join(MAP_DIR, 'Mapa6.2.png')).convert()
    assets['maps'] = maps
    masks = dict()
    for i in range(1,6):
        filename = 'Mask{0}.1.png'.format(i)
        img = pygame.image.load(path.join(MASK_DIR, filename)).convert()
        img.set_colorkey(BLACK)
        key = 'map{0}.1'.format(i)
        masks[key] = img
    masks['map2.2'] = pygame.image.load(path.join(MASK_DIR, 'Mask2.2.png')).convert()
    masks['map3.0'] = pygame.image.load(path.join(MASK_DIR, 'Mask3.0.png')).convert()
    masks['map3.2'] = pygame.image.load(path.join(MASK_DIR, 'Mask3.2.png')).convert()
    masks['map5.0'] = pygame.image.load(path.join(MASK_DIR, 'Mask5.0.png')).convert()
    masks['map5.2'] = pygame.image.load(path.join(MASK_DIR, 'Mask5.2.png')).convert()
    masks['map6.2'] = pygame.image.load(path.join(MASK_DIR, 'Mask6.2.png')).convert()
    for mask in masks.values():
        mask.set_colorkey(BLACK)
    assets['masks'] = masks

    chests = dict()
    chest1 = dict()
    chest2 = dict()
    chest1['closed'] = pygame.image.load(path.join(OBJECT_DIR, 'chests/chest1closed-32x32.png')).convert()    
    chest1['closed'] = pygame.transform.scale(chest1['closed'],(CHEST_SIZE,CHEST_SIZE))
    chest2['closed'] = pygame.image.load(path.join(OBJECT_DIR, 'chests/chest2closed-32x32.png')).convert()    
    chest2['closed'] = pygame.transform.scale(chest2['closed'],(CHEST_SIZE,CHEST_SIZE))

    
    chest1['empty'] = pygame.image.load(path.join(OBJECT_DIR, 'chests/chest1openEMPTY-32x32.png')).convert()    
    chest1['empty'] = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
    chest2['empty']= pygame.image.load(path.join(OBJECT_DIR, 'chests/chest2openEMPTY-32x32.png')).convert()    
    chest2['empty']= pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))

    item1 = []
    for i in range(1,3):
        img = pygame.image.load(path.join(OBJECT_DIR, 'chests/chest1openFULL{0}-32x32.png'.format(i))).convert()    
        img = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
        item1.append(img)
    chest1['full'] = item1

    item2 = []
    for i in range(1,3):
        img = pygame.image.load(path.join(OBJECT_DIR, 'chests/chest2openFULL{0}-32x32.png'.format(i))).convert()    
        img = pygame.transform.scale(img,(CHEST_SIZE,CHEST_SIZE))
        item1.append(img)
    chest2['full'] = item2

    chests['chest1'] = chest1
    chests['chest2'] = chest2
    assets['chests'] = chests

    assets['init_music'] = pygame.mixer.music.load(path.join(SOUND_DIR, 'init_screen.wav'))
    assets['arrow_sound'] = pygame.mixer.Sound(path.join(SOUND_DIR, 'arrow.wav'))
    assets['elemental_dying'] = pygame.mixer.Sound(path.join(SOUND_DIR, 'dead1.wav'))
    assets['background_music'] = pygame.mixer.music.load(path.join(SOUND_DIR, 'background.mp3'))
    assets['point'] = pygame.mixer.Sound(path.join(SOUND_DIR, 'point.wav'))
    pygame.mixer.music.set_volume(0.25)
    return assets

#Classes
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

class Chest(pygame.sprite.Sprite):
    def __init__(self,assets,chest_type,chest_pos,player):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.type = chest_type #Recebe uma string do tipo do baú: outside(tipo 1) ou dungeon(tipo 2) 
        self.status = 'closed' #Recebe uma sting que define o status do baú: fechado, cheio ou vazio
        if self.type == 'outside':
            self.key = 'chest1'
        elif self.type == 'dungeon':
            self.key = 'chest2'
        self.image = self.assets['chests'][self.key][self.status]
        self.rect = self.image.get_rect()
        self.rect.centerx = chest_pos[0]
        self.rect.centery = chest_pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def open(self):
        self.image = self.assets['chests'][self.key]['full'] #Troca a imagem para a do baú aberto

#Função de troca de mapa   
def map_def(player,map_k,assets):
    map_name = 'map{0}.{1}'.format(map_k["map_n0"],map_k["map_n1"])
    player.small = False
    if map_name == 'map4.1':#Mapa diferente requer condições diferentes
        player.small = True
        if 290<=player.rect.centerx <= 320 and 330 <= player.rect.centery <= 385:
            map_k["map_n0"] += 1
            player.rect.left = 30
            player.rect.centery = 250
        elif 450 < player.rect.bottom <= 500 and player.rect.left == 0:
            map_k["map_n0"] -= 1
            player.rect.right = WIDTH-10
            player.rect.centery = HEIGHT/2
        elif 215 <= player.rect.centery <= 385 and player.rect.right == WIDTH:
            map_k["map_n0"] += 0
    elif map_name == 'map5.1':#Saída para mapa diferente
        if 215 <= player.rect.centery <= 385 and player.rect.left == 0:
            map_k["map_n0"] -= 1
            player.rect.centerx = 280
            player.rect.centery = 386
        elif player.rect.top <= 15 and  215<=player.rect.centerx <=385: #Mudança pra cima
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]+1)) in assets['maps']:
                map_k["map_n1"] +=1
                player.rect.centerx = 280
                player.rect.centery = 440
            else:
                map_k["map_n1"] +=0
        elif player.rect.bottom == 500  and 340 <= player.rect.centerx <= 370: #Mudança pra baixo
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]-1)) in assets['maps']:
                map_k["map_n1"] -=1
                player.rect.top = 31
            else:
                map_k["map_n1"] -=0
    else:
        if player.rect.top <= 25 and  215<=player.rect.centerx <=385: #Mudança pra cima
            if 'map{0}.{1}'.format(map_k["map_n0"],(map_k["map_n1"]+1)) in assets['maps']:
                map_k["map_n1"] +=1
                player.rect.centery = 440
            else:
                map_k["map_n1"] +=0
        elif 215 <= player.rect.centery <= 385 and player.rect.right == WIDTH: #Mudança pra direita
            if 'map{0}.{1}'.format((map_k["map_n0"]+1),map_k["map_n1"]) in assets['maps']:
                map_k["map_n0"] += 1
                if map_name == 'map3.1':
                    player.rect.bottom = 500
                player.rect.left = 1   
            else:
                map_k["map_n0"] += 0
        elif 445< player.rect.centery  and 215 <= player.rect.centerx <= 385: #Mudança pra baixo
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

def chest_spawn(assets,MAP,chests,player):
    dungeon = ['map5.0','map5.1','map5.2','map6.2']
    if MAP != assets['maps']['map4.1'] or MAP != assets['maps']['map6.2']:
            if len(chests) > 1:
                for chest in chests:
                    chest.kill()
            if MAP in dungeon:
                chest_type = 'dungeon'
            else:
                chest_type = 'outside'
            chest_xy = chest_pos(assets,MAP)
            chest = Chest(assets,chest_type,chest_xy,player)
    return chest

def chest_pos(assets,map_img):
    if map_img == assets['maps']['map1.1']:
        pos = [50,HEIGHT/2]
    if map_img == assets['maps']['map2.2']:
        pos = [150,130]
    if map_img == assets['maps']['map5.0']:
        pos = [100,100]
    if map_img == assets['maps']['map5.2']:
        pos = [100,100]
    return pos

def game_window(window):    
    map_k = {"map_n0":5,"map_n1":2}
    score = 0  
    health = 5
    RUNNING = 0
    PAUSED = 1
    myfont = pygame.font.SysFont("monospace", 16)
    #grupos das sprites
    all_sprites = pygame.sprite.Group()
    all_arrows = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    chests = pygame.sprite.Group()
    map_masks = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_arrows'] = all_arrows
    groups['all_enemies'] = all_enemies
    groups['chests'] = chests
    assets = load_assets()
    player = Char(groups, assets)
    all_sprites.add(player)
    MASK = MapMask(map_def(player,map_k,assets)[1])
    map_masks.add(MASK)
    MAP = assets['maps']['map1.1']
    spawn = False
    map_w_chest = [assets['maps']['map1.1'],assets['maps']['map2.2'],assets['maps']['map5.0'],assets['maps']['map5.2']]
    
    wave = 3 #Variável para guardar o número da wave de mobs do último mapa
    #Loop principal
    gamerun = RUNNING
    pygame.mixer.music.play(loops=-1)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        
        if spawn == True:
            if MAP != assets['maps']['map1.1']:

                if MAP == assets['maps']['map6.2']:
                    if wave != 0 and len(all_enemies) == 0:
                        n = random.randint(3,8)
                        for i in range(n):
                            xy = random.randint(50,400)
                            enemy = Enemy(groups, assets, player,[xy,xy])
                            all_enemies.add(enemy)
                            wave -= 1
                        spawn = True

                else:
                    n = random.randint(3,8)
                    for i in range(n):
                        xy = random.randint(50,400)
                        enemy = Enemy(groups, assets, player,[xy,xy])
                        all_enemies.add(enemy)
                    spawn = False

            if MAP == assets['maps']['map1.1'] or MAP == assets['maps']['map4.1']:
                for enemy in all_enemies:
                    enemy.kill()

                        


        if health == 0:
            pygame.mixer.music.pause()
            window.blit(assets['over_screen'],(0,0))
            text_surface = assets['score_font'].render("Score:{:0d}".format(score), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect = ((WIDTH/2-125), (HEIGHT/2+15))
            window.blit(text_surface, text_rect)
            gamerun = PAUSED
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    map_k["map_n0"] = 1
                    map_k["map_n1"] = 1
                    gamerun = RUNNING
                    health = 5
                    score = 0
                    window.blit(MAP,(0,0))
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

        if gamerun == PAUSED:
            pygame.display.flip()
            continue

        all_sprites.update()
        all_enemies.update(player)

        MASK.kill()
        new_map = map_def(player,map_k,assets)[0]
        if new_map != MAP:
            spawn = True
            MAP = new_map
            
            for enemy in all_enemies:
                enemy.kill()
        else:
            spawn = False

        
        MASK = MapMask(map_def(player,map_k,assets)[1])
        map_masks.add(MASK)
        
        if MAP in map_w_chest:
            if len(chests) > 1:
                for chest in chests:
                    chest.kill()
            chest = chest_spawn(assets,MAP,chests,player)        
            chests.add(chest)
        else:
            for chest in chests:
                chest.kill()

        map_collide = pygame.sprite.spritecollide(player,map_masks,False,pygame.sprite.collide_mask)
        
        hits = pygame.sprite.groupcollide(all_enemies, all_arrows, True, True, pygame.sprite.collide_mask)
        impact = pygame.sprite.groupcollide(all_enemies,all_sprites,True,False, pygame.sprite.collide_mask)
        item_collect = pygame.sprite.groupcollide(chests,all_sprites,True,False,pygame.sprite.collide_mask)
        
        if item_collect:
            chest.open()
            

        if map_collide:
            player.undo()
            print(map_collide)   

        window.blit(MAP,(0,0))
        
        chests.draw(window)
        all_sprites.draw(window)
        all_arrows.draw(window)
        all_enemies.draw(window)
        
        if item_collect:
            score += 100
            assets['point'].play()
            print(item_collect)

        if hits:
            assets['elemental_dying'].play()
            score += 10
            if score%200 == 0 and health < 5:
                health += 1
        if impact:
            health -= 1
        
        #Health e Score
        text_surface = assets['score_font'].render(chr(9829) * health, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)
        text_surface = assets['score_font'].render("Score:{:0d}".format(score), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (0,  0)
        window.blit(text_surface, text_rect)

        pygame.display.update()
        
game_window(window)

pygame.quit()