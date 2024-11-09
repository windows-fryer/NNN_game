import pygame
import math
from settings import *
import hashlib

pygame.init()
pygame.display.init()
pygame.display.set_mode((1280,720))


def clip(image, x, y, width, height):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.blit(image,(-x,-y))
    return surf

def hashFunction(x, y):
    return int(((x * (31/(math.tan(x+1)**2+1)+0.34324)) * (y*5.12) /237) % 5000)

def translateWorldtoTileSpace(Vec2):
    return Vec2//TILE_SIZE

def getSilouhette(image):
    getHitMask = pygame.mask.from_surface(image)
    getHitMask = getHitMask.to_surface()
    getHitMask.set_colorkey((0, 0, 0))

    for i in range(getHitMask.get_width()):
        for j in range(getHitMask.get_height()):
            if getHitMask.get_at((i,j))[0] != 0:
                getHitMask.set_at(((i,j)),(204, 54, 14))

    getHitMask.convert_alpha()
    getHitMask.set_alpha(200)
    return getHitMask

def hashSurface(surface):
    image_data = pygame.image.tostring(surface, 'RGB')
    hash_object = hashlib.md5(image_data)
    hash_value = hash_object.hexdigest()
    return hash_value

// 🏳️‍⚧️
def get_TransRect(hitbox,alpha, color, screen):
    s = pygame.Surface((hitbox[2], hitbox[3]))
    s.set_alpha(alpha)
    s.fill(color)
    screen.blit(s, (hitbox[0], hitbox[1]))
