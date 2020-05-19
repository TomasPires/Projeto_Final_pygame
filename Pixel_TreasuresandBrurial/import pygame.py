import pygame
import random

pygame.init()

WIDTH = 1080
HEIGHT = 720
frames = []
for i in range(1,5):
    image = pygame.image.load('props/animation/fire{0}-128x128.png'.format(i))
    frames.append(image)
#imagem=pygame.transform.scale(image,(50,50))

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Treasures and Burial')

class Fogo(pygame.sprite.Sprite):
    def __init__(self,center,image):
        pygame.sprite.Sprite.__init__(self)
        self.fire_anim = frames
        self.frame = 0
        self.imag = self.fire_anim[self.frame]
        self.rect.center = center

        self.last_update = pygame.time.get_ticks()
        
        self.frame_tickes = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        if elapsed_ticks > self.frame_ticks:
            
            self.last_update = now
            
            self.frame += 1

            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

gamerun = True
clock = pygame.time.Clock()
FPS = 30

while gamerun:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False
    animacao = Fogo((0,0),image)
    window.fill((0,0,0))
    window.blit(animacao,(0,0))
    pygame.display.update()

pygame.quit()