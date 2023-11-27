import random

import pygame
from vector import Vec2
from functions import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vec, lifespan):
        super().__init__()
        self.pos = pos
        self.vec = Vec2(vec)
        self.lifeSpan = lifespan
        self.lifeTime = 0
        self.image = None
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 10,10)


    def update(self):
        self.pos += self.vec

        if self.lifeTime >= self.lifeSpan:
            self.kill()
        self.lifeTime += 1

    def draw(self,screen, offset):
        screen.blit(self.image, (self.pos+offset).position)

dirtParticleColors = ((166,67,24), (128,70,31), (94,67,10))

class DirtParticle(Particle):
    def __init__(self, pos, playerDirection):
        if playerDirection == 1:
            vec_x = random.randint(0,3)
        else:
            vec_x = random.randint(-3,0)

        super().__init__(pos, (vec_x,random.randint(-3,-1)),random.randint(3,60))
        self.color = dirtParticleColors[random.randint(0,2)]
        self.image = pygame.Surface((random.randint(2,5), random.randint(2,5)))
        self.image.fill(self.color)


    def update(self):
        super().update()

    def draw(self,screen, offset):
        screen.blit(self.image,(self.pos-offset).int().position)

bulletExplodeImage = pygame.image.load("assets/player/gun/NNN_gameBulletExplodingAnimationFrames.png")
bulletExplodeFrames = []

for i in range(5):
    bulletExplodeFrames.append(pygame.transform.scale(clip(bulletExplodeImage,10*i,0,10,5), (30,15)))

class BulletExplode(Particle):
    def __init__(self, bullet):
        super().__init__(bullet.pos-bullet.vec,(0,0),10000)
        self.explodingFrame = 0
        self.angle = bullet.angle


    def update(self):

        self.explodingFrame += 0.5
        if self.explodingFrame >= len(bulletExplodeFrames):
            self.kill()

    def draw(self,screen, offset):
        self.image = pygame.transform.rotate(bulletExplodeFrames[int(self.explodingFrame)], self.angle)
        imageRotOffset = Vec2((self.image.get_size()))*0.5
        screen.blit(self.image, (self.pos-offset+imageRotOffset).position)


peanutBulletExplodeImage = pygame.image.load("assets/enemys/peanut/NNN_gamePeanutEnemyAttackProjectileExplodeAnimation.png")
peanutBulletExplodeFrames = []
for i in range(4):
    peanutBulletExplodeFrames.append(pygame.transform.scale(clip(peanutBulletExplodeImage,14*i,0,14,5), (42,15)))

class PeanutBulletExplode(Particle):
    def __init__(self, bullet):
        super().__init__(bullet.pos-bullet.vec,(0,0),10000)
        self.explodingFrame = 0
        self.angle = bullet.angle


    def update(self):

        self.explodingFrame += 0.5
        if self.explodingFrame >= len(peanutBulletExplodeFrames):
            self.kill()

    def draw(self,screen, offset):
        self.image = pygame.transform.rotate(peanutBulletExplodeFrames[int(self.explodingFrame)], self.angle)
        imageRotOffset = Vec2((self.image.get_size()))*0.5
        screen.blit(self.image, (self.pos-offset+imageRotOffset).position)

class DoubleJumpParticle(Particle):
    def __init__(self, player):
        n = random.randint(-157,157)/100
        speed = random.randint(2,5)
        vec = (math.sin(n)*speed,math.cos(n)*speed)
        super().__init__(player.pos+Vec2((player.dim[0]/2,player.dim[1])), vec, random.randint(5,15))

        self.size = random.randint(5,15)
        self.currSize = self.size

    def update(self):
        super().update()
        self.currSize = self.size*((self.lifeSpan-self.lifeTime)/self.lifeSpan)

        if self.currSize == 0:
            self.kill()

    def draw(self,screen, offset):
        pygame.draw.circle(screen,(252, 227,219) ,(self.pos-offset).position, self.currSize)

# key : color, speed, lifetime
checkPointParticleTypeArray = (((182,255, 165),Vec2((0,-1)),20),((153, 242, 104),Vec2((0,-2)),10),((171, 204, 54),Vec2((0,-3)),10))

class checkPointParticle(Particle):
    def __init__(self, pos, type):
        super().__init__(pos, (0,0),checkPointParticleTypeArray[type][2]+random.randint(-3,3))
        self.size = self.vec.mag/3
        self.color = checkPointParticleTypeArray[type][0]
        self.accelerationVec = checkPointParticleTypeArray[type][1]

    def update(self):
        self.vec += self.accelerationVec

        super().update()
        self.size = self.vec.mag*2

    def draw(self,screen, offset):
        pygame.draw.line(screen, self.color, *((self.pos-offset).position,((self.pos-offset)+Vec2((0,-self.size))).position),4)

surface = pygame.Surface((3,3),pygame.SRCALPHA)
for x in range(-1,2):
    for y in range(-1,2):
        if (abs(x)+abs(y) == 2):
            continue
        else:
            surface.set_at((1+x,1+y),(255,255,255))



class deathParticle(Particle):
    def __init__(self,pos, size):
        self.randomOffset = Vec2((random.randint(0, size.x), (random.randint(0, size.y))))
        self.scale = random.randint(2, 4)
        self.image = pygame.transform.scale(surface, (9 * self.scale, 9 * self.scale))
        self.rect = self.image.get_rect()
        super().__init__(pos+ self.randomOffset, (random.randint(-3,3),random.randint(-10,-5)), 1000)


    def update(self):
        if self.scale > 0:
            self.scale -= 0.2

        if self.scale < 0:
            self.kill()
            return 0
        self.image = pygame.transform.scale(surface, (int(9 * self.scale), int(9 * self.scale)))
        # self.pos += self.vec

    def draw(self, screen, offset):
        screen.blit(self.image, (self.pos-offset).position)

drawParticles = True

class ParticleContainer():
    def __init__(self):
        self.dirtParticles = pygame.sprite.Group()
        self.bulletParticles = pygame.sprite.Group()
        self.checkPointParticles = pygame.sprite.Group()
        self.checkPointTimer = 0

    def add(self, level, player):
        if player.running and player.grounded and drawParticles:

            particle = DirtParticle(player.pos+Vec2((25,100)), player.direction)
            self.dirtParticles.add(particle)

        if player.justDoubledJumped and drawParticles:
            for i in range(10):
                particle = DoubleJumpParticle(player)
                self.dirtParticles.add(particle)


        if player.reachCheckpoint:
            self.checkPointTimer = 10

        if self.checkPointTimer > 0 and drawParticles:
            bottomPos = player.pos+Vec2((0,player.dim[1]))
            for i in range(3):
                randVec = Vec2((random.randint(0,player.dim[1]),0))
                self.checkPointParticles.add(checkPointParticle(bottomPos+randVec,0))
            for i in range(5):
                randVec = Vec2((random.randint(0, player.dim[1]), 0))
                self.checkPointParticles.add(checkPointParticle(bottomPos + randVec, 1))

            for i in range(7):
                randVec = Vec2((random.randint(0, player.dim[1]), 0))
                self.checkPointParticles.add(checkPointParticle(bottomPos + randVec, 1))

            self.checkPointTimer -= 1


        for enemy in level.EnemyContainer.enemies:
            if enemy.vec.mag > 0 and enemy.grounded and drawParticles and enemy.awakened:
                particle = DirtParticle(enemy.pos + Vec2((25, 100)), -enemy.toPlayerVec)
                self.dirtParticles.add(particle)

            if enemy.type == 2:
                for bullet in enemy.bullets:
                    if bullet.Delete:
                        self.bulletParticles.add(PeanutBulletExplode(bullet))

            if enemy.delete and drawParticles:
                for i in range(20) :
                    self.dirtParticles.add(deathParticle(enemy.pos,Vec2(enemy.dim)))


        for bullet in player.bullets:
            if bullet.Delete:
                self.bulletParticles.add(BulletExplode(bullet))



    def update(self):
        self.dirtParticles.update()
        self.bulletParticles.update()
        self.checkPointParticles.update()

    def draw(self, screen, offset):
        for dirtParticle in self.dirtParticles:
            dirtParticle.draw(screen, offset)
        for bulletExplodingParticle in self.bulletParticles:
            bulletExplodingParticle.draw(screen, offset)

        for checkPointParticle in self.checkPointParticles:
            checkPointParticle.draw(screen, offset)
