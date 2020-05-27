import pygame
import random
import os

WIDTH = 1080
HEIGHT = 720
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
    assets['flecha_img'] = pygame.image.load('assets/img/background.png').convert()
    assets['character_img'] = pygame.image.load('Pixel_TreasuresandBurial/props/characters/front/char0.0-96x96.png').convert_alpha()
    
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

    def tirobaixo(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # A nova bala vai ser criada logo acima e no centro horizontal da nave
            new_bullet = Bullet(self.assets, self.rect.centery, self.rect.centerx)
            self.groups['all_sprites'].add(new_bullet)
            self.groups['all_bullets'].add(new_bullet)

class Flecha(pygame.sprite.Sprite):
    def __init__(self,assets,bottom,centerx):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['flecha_img']
        self.mask=pygame.mask.from_window
        self.rect=self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = -10

    def update(self):
        # A bala só se move no eixo y
        self.rect.y += self.speedy

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
                if event.key == pygame.K_LEFT:
                    player.x_speed -=5
                if event.key == pygame.K_RIGHT:
                    player.x_speed +=5
                if event.key == pygame.K_UP:
                    player.y_speed -=5
                if event.key == pygame.K_DOWN:
                    player.y_speed +=5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.x_speed +=5
                if event.key == pygame.K_RIGHT:
                    player.x_speed -=5
                if event.key == pygame.K_UP:
                    player.y_speed +=5
                if event.key == pygame.K_DOWN:
                    player.y_speed -=5
        
        if player.rect.right >= (WIDTH)-100:
            if (HEIGHT/2)-50<player.rect.bottom<(HEIGHT/2+50):
                MAPA = BLACK
        else:
            MAPA = GREEN
                
        all_sprites.update()
    
        window.fill(MAPA) #Depois, podemos usar o comando pygame.display.flip()
        pygame.draw.circle(window, BLUE,(980,360),10)
        all_sprites.draw(window)

        pygame.display.update()
        
janela(window)

pygame.quit()