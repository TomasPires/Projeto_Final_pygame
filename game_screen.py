import pygame
import random
from settings import FPS, WIDTH, HEIGHT, BLACK, RED, CHAR_SIZE,ENEMY_SIZE,CHEST_SIZE
from assets import load_assets
from sprites import Char, Arrow, Enemy, MapMask, Chest 
from map_settings import map_def, chest_pos, chest_spawn

def game_window(window):    

    clock = pygame.time.Clock()

    assets = load_assets()

    map_k = {"map_n0":5,"map_n1":0}
    #Pontuação e HP iniciais
    score = 0 
    health = 5

    #Estados do gamerun 
    RUNNING = 0
    PAUSED = 1

    #Fonte para os scores e o HP
    myfont = pygame.font.SysFont("monospace", 16)

    #Grupos das sprites e para as mascaras dos mapas
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

    #Criando sprite do jogador e adicionando-a ao grupo 
    player = Char(groups, assets)
    all_sprites.add(player)

    #Definição dos mapas e seus parâmetros (quais possuem mapas e variável para spawn de mobs (True para permitir spawn e False para bloquear o spawn))
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
        
        # O ultimo mapa apresenta uma mecanica de waves, que o jogador deve derrotar para vencer o jogo.
        if MAP == assets['maps']['map6.2'] and wave != 0 and len(all_enemies) == 0:  
            spawn = True                                                            #Entrando no mapa, os mobs podem spawnar caso ainda restem waves e não haja inimigos vivos

        if spawn == True:          # Caso os inimigos possam nascer, são gerados de 3 a 8 inimigos no mapa se este não for o mapa 1.1 (zona segura)
            if MAP != assets['maps']['map1.1']:
                if MAP == assets['maps']['map6.2']:  #Aqui implementa-se o sistema de waves para o mapa 6.2
                    if wave != 0 and len(all_enemies) == 0:
                        n = random.randint(3,8)
                        for i in range(n):
                            xy = random.randint(50,400)
                            enemy = Enemy(groups, assets, player,[xy,xy])
                            all_enemies.add(enemy)
                        wave -= 1
                        
                    elif wave == 0 and len(all_enemies) == 0:
                        gamerun = PAUSED
                else:                       #Se o mapa for outro, não há waves   
                    n = random.randint(3,8)
                    for i in range(n):
                        xy = random.randint(50,400)
                        enemy = Enemy(groups, assets, player,[xy,xy])
                        all_enemies.add(enemy)
                    spawn = False

            if MAP == assets['maps']['map1.1'] or MAP == assets['maps']['map4.1']:  #Para que os mobs não sigam o jogador, se este entrar nos mapas 1.1 ou 4.2, os mobs morrem
                for enemy in all_enemies:
                    enemy.kill()

        all_sprites.update()
        all_enemies.update(player)
        
        #
        MASK.kill()
        new_map = map_def(player,map_k,assets)[0]
        if new_map != MAP:
            spawn = True
            MAP = new_map
            if MAP in map_w_chest:
                if len(chests) > 1:
                    for chest in chests:
                        chest.kill()
                if MAP == ['map5.2']:
                    n_chests = 2
                else:
                    n_chests = 1
                for i in range(n_chests):
                    chest = chest_spawn(assets,MAP,chests,player,i+1)      
                    chests.add(chest)
            else:
                for chest in chests:
                    chest.kill()
            for enemy in all_enemies:
                enemy.kill()
        else:
            spawn = False

        
        MASK = MapMask(map_def(player,map_k,assets)[1])
        map_masks.add(MASK)
        
        
        #Colisões
        map_collide = pygame.sprite.spritecollide(player,map_masks,False,pygame.sprite.collide_mask)  #Colisão do jogador com as máscaras do mapa
        hits = pygame.sprite.groupcollide(all_enemies, all_arrows, True, True, pygame.sprite.collide_mask)  #Colisão das flechas com os inimigos
        impact = pygame.sprite.groupcollide(all_enemies,all_sprites,True,False, pygame.sprite.collide_mask) #Colisão dos inimigos com o jogador
        item_collect = pygame.sprite.spritecollide(player,chests,True)   #Colisão do jogador com os baús

        if item_collect:     #Ao colidir com o baú, o jogador ganha 200 pontos 
            chest.open()
            score += 200
            assets['point'].play()
            

        if map_collide:      #Ao colidir com o mapa, o jogador para de se mover
            player.undo()
            print(map_collide)   

        if hits:             #Ao matar um inimigo, o jogador ganha 10 pontos e, a cada 200 pontos ganhos, o jogador ganha mais uma vida, caso tenha perdido alguma
            assets['elemental_dying'].play()
            score += 10
            if score%200 == 0 and health < 5:
                health += 1

        if impact:           #Quando um inimigo toca em um jogador, o inimigo morre e o jogador perde uma vida
            health -= 1
        
        #Desenhando o mapa e as sprites
        window.blit(MAP,(0,0))
        
        chests.draw(window)
        all_sprites.draw(window)
        all_arrows.draw(window)
        all_enemies.draw(window)
        
        
        #Desenhando Health e Score
        text_surface = assets['score_font'].render(chr(9829) * health, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)
        text_surface = assets['score_font'].render("Score:{:0d}".format(score), True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (0,  0)
        window.blit(text_surface, text_rect)

        #Caso a vida acabe, o jogo entra na tela de game over
        if health == 0:
            gamerun = PAUSED
            
        if gamerun == PAUSED:  #Na tela de game over, o jogador pode escolher se para ou recomeça o jogo
            pygame.mixer.music.pause()
            window.blit(assets['over_screen'],(0,0))
            text_surface = assets['score_font'].render("Score:{:0d}".format(score), True, (255,255,255))
            text_rect = text_surface.get_rect()
            text_rect = ((WIDTH/2-125), (HEIGHT/2+15))
            window.blit(text_surface, text_rect)
            gamerun = PAUSED
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #Caso aperte Enter, o jogo recomeça no primeiro mapa, o estado volta pra RUNNING, a vida para 5 e os pontos zeram
                    pygame.mixer.music.play(loops=-1)
                    map_k["map_n0"] = 1
                    map_k["map_n1"] = 1
                    gamerun = RUNNING
                    health = 5
                    score = 0
                    window.blit(MAP,(0,0))

                elif event.key == pygame.K_ESCAPE:   #Caso aperte Esc, o jogo fecha
                    pygame.quit()
            pygame.display.flip()
            continue

        pygame.display.update()
        