import math

import pygame

import functions
import sound
from vector import Vec2
from settings import *

class LevelInterectableContainer():
    def __init__(self):
        self.checkPoints = pygame.sprite.Group()
        self.endPoint = None
        self.powerUps = None

    def reset(self):
        for checkpoint in self.checkPoints:
            checkpoint.flipAnimationFrame = 5
            checkpoint.reached = False
            checkpoint.mainImage = checkpoint.imageUnflipped



    def add(self, type, pos):
        if type == 0:
            self.checkPoints.add(CheckPoint(pos))
        if type == -1:
            self.endPoint = EndPoint(pos)
        if type == -2:
            self.powerUps = DoubleJumpPowerup(pos)

    def update(self, player):
        self.checkPoints.update(player)
        if self.endPoint.update(player):
            player.completedLevel = True
            return 0
        nearestCheckPoint = Vec2((0, 0))
        for checkPoint in self.checkPoints:

            if checkPoint.justChanged:
                player.health = 100
                player.reachCheckpoint = True

            if checkPoint.reached:
                if checkPoint.pos.x > nearestCheckPoint.x:
                    nearestCheckPoint = Vec2((checkPoint.pos.x, 0))

        player.respawnPos = nearestCheckPoint

        if self.powerUps != None:
            self.powerUps.update(player)

    def draw(self, screen, offset):
        for checkPoint in self.checkPoints:
            checkPoint.draw(screen, offset)

        if self.powerUps != None:
            self.powerUps.Draw(screen,offset)

        self.endPoint.draw(screen, offset)

SignFlipAnimationImage = pygame.image.load("assets/miscellaneous/NNN_gameCheckPointSignFlipAnimation.png")
SignFlipAnimationFrames = []

for i in range(6):
    SignFlipAnimationFrames.append(pygame.transform.scale(functions.clip(SignFlipAnimationImage, i*20,0,20,20), (100,100)))

class CheckPoint(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos*TILE_SIZE
        self.rect = pygame.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.reached = False
        self.imageUnflipped = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameCheckPointSign.png"),(100,100))
        self.imageFlipped = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameCheckPointSignFlipped.png"),(100,100))
        self.mainImage = self.imageUnflipped
        self.Image = self.mainImage
        self.flipAnimationFrame = 5
        self.SFX = sound.SFX("assets/SFX/general/checkpoint.mp3")
        self.justChanged = False

    def update(self, player):
        self.justChanged = False
        self.SFX.update()


        if not self.reached:
            if player.pos.x > self.pos.x:
                self.SFX.playOnce(-1)
                self.reached = True
                self.justChanged = True
                self.mainImage = self.imageFlipped

                return True
            return False
        else:
            if self.flipAnimationFrame > 0:
                self.flipAnimationFrame -= 0.5

            return True

    def draw(self, screen, offset):
        self.Image = self.mainImage
        if self.flipAnimationFrame > 0 and self.reached:
            self.Image = SignFlipAnimationFrames[5-int(self.flipAnimationFrame)]


        screen.blit(self.Image, (self.pos-offset).position)
        # pygame.draw.rect(screen, (255,0,0), self.rect.move(-offset.x, -offset.y))

class EndPoint(CheckPoint):
    def __init__(self, pos):
        super().__init__(pos)
        self.Image = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameFinishSign.png"),(100,100))


    def update(self, player):
        if player.pos.x > self.pos.x:
            return True
        return False

    def draw(self, screen, offset):
        screen.blit(self.Image, (self.pos - offset).position)
        # pygame.draw.rect(screen, (255,0,0), self.rect.move(-offset.x, -offset.y))

class DoubleJumpPowerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos*TILE_SIZE
        self.time = 0
        self.size = 50
        self.SFX = sound.SFX("assets/SFX/general/ability_unlock.mp3")
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.image = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameDoubleJumpPowerup.png"), (self.size, self.size))
        self.delete = False

    def update(self, player):
        # if self.delete:
        #     self.kill()
        if self.rect.colliderect(player.hitbox) and not self.delete:
            player.canDoubleJump = True
            player.reachCheckpoint = True
            self.SFX.playOnce(-1)
            self.delete = True
        # self.delete = False
        self.time += 0.1

    def Draw(self, screen, offset):
        if not self.delete:
            # print("position", (self.pos-offset).position)
            screen.blit(self.image, (self.pos-offset+Vec2((0,math.sin(self.time)*20))).position)
#