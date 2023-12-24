import random

import functions
import pygame
from vector import Vec2
from particles import ParticleContainer

class object(pygame.sprite.Sprite):
    def __init__(self, pos, vec, speed, maxTime):
        super().__init__()
        self.mappos = Vec2(pos)
        self.vec = Vec2(vec)
        self.speed = speed
        self.lifeSpan = maxTime
        self.lifetime = 0
        self.image = None
        self.getRect()

    def getRect(self):
        if self.image == None:
            self.rect = pygame.Rect(0,0,10,10)
        else:
            self.rect = self.image.get_rect()

    def update(self):
        if self.lifetime >= self.lifeSpan:
            self.kill()
        self.lifetime += 1
        self.mappos+=self.vec*self.speed


    def draw(self,screen, offset):
        screen.blit(self.image, (self.mappos-offset).position)

cloudImage = pygame.image.load("assets/clouds.png")
cloudImages = []
for i in range(3):
    cloudImages.append(pygame.transform.scale(functions.clip(cloudImage,0,10*i+1,20,10), (200,100)))

class cloud(object):
    def __init__(self, pos):
        super().__init__(pos, (-1,0), random.randint(1,2), 2000)
        self.type = random.randint(0,2)
        self.image = cloudImages[self.type]

    def update(self):
        super().update()

    def draw(self,screen, offset):
        super().draw(screen, offset)

class foreGroundContainer:
    def __init__(self):
        self.clouds = pygame.sprite.Group()
        self.particles = ParticleContainer()

    def add(self, level, player):
        n = random.randint(0,3600)
        if n % 240 == 0:
            cloud1 = cloud((player.pos.x+1000, random.randint(0,200)))
            self.clouds.add(cloud1)

        self.particles.add(level, player)


    def update(self):
        self.clouds.update()
        self.particles.update()

    def draw(self, screen, offset):
        self.particles.draw(screen, offset)
        for cloud in self.clouds:
            cloud.draw(screen, offset)

