import pygame
from os import path
from settings import WIDTH, HEIGHT, CHAR_SIZE, ENEMY_SIZE, CHEST_SIZE, MAP_DIR, MASK_DIR, CHAR_DIR, ENEMY_DIR, OBJECT_DIR, IMG_DIR, SOUND_DIR, BLACK, WHITE

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