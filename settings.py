from os import path

WIDTH = 600
HEIGHT = 500
FPS = 30

CHAR_WIDTH = 82
CHAR_HEIGHT = 82
ENEMY_SIZE = 40
CHEST_SIZE = 30
IMG_WIDTH = 600
IMG_HEIGHT = 500

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

INIT = 0
PLAY = 1
CLOSE = 2
