import pygame

WIDTH = 600
HEIGHT = 400
SIZE = (WIDTH, HEIGHT) 
BACKGROUND_COLOR = pygame.Color('white')
FPS = 10
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
       
        self.images = []
        for i in range(0,8):
            self.images.append(pygame.image.load('props/characters/back/char2.{0}-96x96.png'.format(i)))
        
        self.index = 0

        self.image = self.images[self.index]
 
        self.rect = pygame.Rect(5, 5, 96, 96)

    def update(self):

        self.index += 1

        if self.index >= len(self.images):

            self.index = 0
        
        self.image = self.images[self.index]
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    my_sprite = MySprite()
    my_group = pygame.sprite.Group(my_sprite)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        my_group.update()
        screen.fill(BACKGROUND_COLOR)
        my_group.draw(screen)
        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main()

#fonte: https://www.simplifiedpython.net/pygame-sprite-animation-tutorial/