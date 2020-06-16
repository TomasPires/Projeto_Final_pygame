import random
import pygame
from assets import load_assets
from settings import WIDTH, HEIGHT
from sprites import Chest

# Função de troca de mapa 
# Na troca de mapas, cada vez que o jogador atinge um ponto da tela predeterminado, a imagem de fundo se altera
# Além disso, o jogador é enviado para a posição oposta da tela
# A função retorna a imagem do mapa e da sua respectiva máscara
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
                player.rect.centerx = 270
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

#Função que cria os baús
def chest_spawn(assets,MAP,chests,player):
    if MAP != assets['maps']['map4.1'] or MAP != assets['maps']['map6.2']:
            if len(chests) > 1:
                for chest in chests:
                    chest.kill()
            chest_xy = chest_pos(assets,MAP)
            chest = Chest(assets,chest_xy,player)
    return chest

# Função que define a posição dos baús
def chest_pos(assets,map_img):
    if map_img == assets['maps']['map1.1']:
        pos = [50,HEIGHT/2]
    if map_img == assets['maps']['map2.2']:
        pos = [150,130]
    if map_img == assets['maps']['map3.0']:
        pos = [450,250]
    if map_img == assets['maps']['map5.0']:
        pos = [40,250]
    if map_img == assets['maps']['map5.2']:
        pos = [50,150]
    return pos
