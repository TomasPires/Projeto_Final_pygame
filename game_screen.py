import pygame
import random
from settings import FPS, WIDTH, HEIGHT, BLACK, RED, CHAR_SIZE,ENEMY_SIZE,CHEST_SIZE
from assets import load_assets
from sprites import Char, Arrow, Enemy, MapMask, Chest 
from map_settings import map_def, chest_pos, chest_spawn

def game_window(window):    

    clock = pygame.time.Clock()

    assets = load_assets()

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
        