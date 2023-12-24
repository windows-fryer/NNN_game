import pygame
from vector import Vec2
from settings import GRAVITY
from functions import *
from sound import SFX

bulletAnimationImage = pygame.image.load("assets/player/gun/NNN_gameBulletAnimationFrames.png")
bulletAnimationFrames = []

for i in range(5):
    bulletAnimationFrames.append(pygame.transform.scale(clip(bulletAnimationImage,i*10,0,10,5), (30,15)))

peanutBulletAnimationImage = pygame.image.load("assets/enemys/peanut/NNN_gamePeanutEnemyAttackProjectileAnimation.png")
peanutBulletAnimationFrames = []

for i in range(6):
    peanutBulletAnimationFrames.append(pygame.transform.scale(clip(peanutBulletAnimationImage,i*11,0,11,5), (33,15)))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, vec):
        super().__init__()
        self.pos = pos
        self.vec = vec
        self.size = 20
        self.damage = 20
        self.lifeSpan = 200
        self.angle = self.vec.get_angle()
        self.lifeTime = 0
        self.offset = Vec2((0,0))
        self.animationFrame = 0
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y,20,20)
        self.SFX = SFX("assets/SFX/player/projectile/player_projectile_explode.mp3")
        self.Delete = False


    def gravity(self):
        self.vec.y_increment(GRAVITY/8)

    def update(self, offset, player):
        self.animationFrame += 0.3
        if self.animationFrame >= len(bulletAnimationFrames):
            self.animationFrame = 0

        if self.Delete:
            self.kill()
            # self.SFX.playOnce((self.pos-player.pos).mag)
        self.offset = offset
        self.pos += self.vec
        self.gravity()
        self.lifeTime += 1
        self.angle = self.vec.get_angle()
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.image = pygame.transform.rotate(bulletAnimationFrames[int(self.animationFrame)], self.angle-90)
        self.Delete = self.lifeTime > self.lifeSpan

    def draw(self, screen):
        imageRotOffset = Vec2((self.image.get_size()))*0.5
        screen.blit(self.image, (self.pos-imageRotOffset+self.offset+Vec2((self.size/2, self.size/2))).position)
        # pygame.draw.rect(screen, (255,255,0), self.hitbox.move(self.offset.x, self.offset.y))

class PeanutBullet(pygame.sprite.Sprite):
    def __init__(self, pos, vec, speed):
        super().__init__()
        self.pos = pos
        self.vec = vec
        self.speed = speed
        self.size = 20
        self.lifeSpan = 200
        self.angle = self.vec.get_angle()
        self.lifeTime = 0
        self.offset = Vec2((0, 0))
        self.animationFrame = 0
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, 20, 20)
        self.Delete = False
        self.SFX = SFX("assets/SFX/peanut/projectile/peanut_projectile_explode.mp3")
        self.direction = False

    def update(self, player):
        self.animationFrame += 0.3
        if self.animationFrame >= len(peanutBulletAnimationFrames):
            self.animationFrame = 0

        self.offset = player.offset

        if self.Delete:
            self.SFX.play((player.pos-self.pos).mag)
            self.kill()


        self.vec += (player.pos-self.pos).normalise()

        if self.vec.mag > self.speed:
            self.vec *= 0.9
        # self.vec.makeToLength(7)
        self.direction = self.vec.x > 0
        self.pos += self.vec
        self.lifeTime += 1
        self.angle = self.vec.get_angle()
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.image = pygame.transform.rotate(peanutBulletAnimationFrames[int(self.animationFrame)], self.angle - 90)
        self.Delete = self.lifeTime > self.lifeSpan

    def draw(self, screen):
        imageRotOffset = Vec2((self.image.get_size()))*0.5

        screen.blit(self.image, (self.pos-imageRotOffset+self.offset).position)

