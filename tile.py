import pygame
from random import randint
from vector import Vec2
from functions import *
from settings import *

# grassTileImages = (pygame.image.load("assets/grass_tile2.png"), pygame.image.load("assets/grass_tile3.png"), pygame.transform.flip(pygame.image.load("assets/grass_tile2.png"),1,0),pygame.image.load("assets/grass_tile4.png"), pygame.image.load("assets/grass_tile1.png"), pygame.transform.flip(pygame.image.load("assets/grass_tile4.png"),1,0), pygame.image.load("assets/grass_tile5.png"), pygame.image.load("assets/grass_tile6.png"), pygame.transform.flip(pygame.image.load("assets/grass_tile5.png"),1,0))
grassTiles = pygame.image.load("assets/grassTiles.png")
grassTileImages_clipped = []

for y in range(2):
    for x in range(3):
        grassTileImages_clipped.append(pygame.transform.scale(clip(grassTiles,x*10,y*10,10,10),(100,100)))

grassTileImages = (pygame.transform.flip(grassTileImages_clipped[2],1,0), grassTileImages_clipped[1], grassTileImages_clipped[2], grassTileImages_clipped[0], grassTileImages_clipped[0], grassTileImages_clipped[0], pygame.transform.flip(grassTileImages_clipped[3],1,0), grassTileImages_clipped[0], grassTileImages_clipped[3], pygame.transform.flip(grassTileImages_clipped[4],1,0),grassTileImages_clipped[4])


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        self.size = size
        self.pos = Vec2(pos)*self.size
        self.offset = Vec2((0,0))
        self.mappos = self.pos + self.offset

        self.x, self.y = self.pos.x, self.pos.y
        self.map_x, self.map_y = self.mappos.x, self.mappos.y
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.image = pygame.Surface((self.size, self.size))
        self.image = self.init_image(type)

    @staticmethod
    def init_image(type):
        if type == 5:
            return pygame.transform.flip(grassTileImages[5],randint(0,1),randint(0,1))
        return grassTileImages[type]

    def __hash__(self):
        return hashFunction(self.x, self.y)


    def update(self):
        self.pos = self.mappos + self.offset
        self.x, self.y = self.pos.x, self.pos.y

    def draw(self,screen):
        screen.blit(self.image, self.pos.position)

    def playerCollision_x(self, player):
        self.rect = pygame.Rect(self.map_x, self.map_y, self.size, self.size)
        if player.hitbox.colliderect(self.rect):

            if player.pos.x + player.dim[0] > self.map_x and player.vec.x > 0:
                player.pos.update_x(self.map_x - player.dim[0])
                player.vec.update_x(0)

            elif player.pos.x < self.map_x+self.size and player.vec.x < 0:
                player.pos.update_x(self.map_x +self.size)
                player.vec.update_x(0)
        player.updateHitbox()

    def playerCollision_y(self, player):
        if player.hitbox.colliderect(self.rect):
            if player.pos.y < self.map_y+self.size and player.vec.y < 0:
                player.pos.update_y(self.map_y + self.size)
                player.vec.update_y(0)


            elif player.pos.y + player.dim[1] > self.map_y and player.vec.y > 0:
                player.grounded = True
                if player.type == -1:
                    player.doubleJump = True
                player.pos.update_y(self.map_y - player.dim[1])
                player.vec.update_y(0)
        player.updateHitbox()











