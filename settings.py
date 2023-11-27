import pygame
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCROLL_PERCENTAGE = (0.4, 0.6)
SCROLL_LEFT, SCROLL_RIGHT = SCREEN_WIDTH*SCROLL_PERCENTAGE[0], SCREEN_WIDTH*SCROLL_PERCENTAGE[1]
GRAVITY = 3.5
FRAMERATE = 60
TILE_SIZE = 100
font = pygame.font.Font("assets/fonts/Inconsolata,Lexend_Peta,Pixelify_Sans/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 50)

