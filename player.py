import random

import pygame

import sound
from vector import Vec2
from gun import Gun
from settings import *
from functions import *
pygame.init()
pygame.display.init()
pygame.display.set_mode((1280,720))

playerImage = pygame.transform.scale(pygame.image.load("assets/player/NNN_gamePlayerCharacterImage.png"),(50,100))

runningAnimationImage = pygame.image.load("assets/player/NNN_gamePlayerCharacter_runAnimationFrames.png")
reloadAnimationImage = pygame.image.load("assets/player/NNN_gameWaterGunReloadAnimationFrames.png")

getHitImage = pygame.transform.flip((pygame.image.load("assets/player/NNN_gamePlayerCharacter_GetHitImage.png")),1,0)
getHitMask = pygame.transform.scale(getSilouhette(getHitImage),(100,50))

playerHealthBar = pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gameHealthBar.png"), (45*5, 10*5))
playerHealthBar_green = pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gameHealthBar_green.png"), (39*5, 4*5))
bulletImage = pygame.transform.scale(clip(pygame.image.load("assets/player/gun/NNN_gameBulletAnimationFrames.png"),0,0,10,5), (100,50))

getHitImage = pygame.transform.scale(getHitImage,(100,50))
runningAnimationFrames = []
reloadAnimationFrames = []

for i in range(1,8):
    runningAnimationFrames.append(pygame.transform.scale(clip(runningAnimationImage,i*10,0, 10,20), (50,100)))

for i in range(16):
    reloadAnimationFrames.append(pygame.transform.scale(clip(reloadAnimationImage,i*12,0, 12,20), (60,100)))

heartImages = [pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gamePlayer0Hearts.png"),(35*7,10*7)),pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gamePlayer1Hearts.png"),(35*7,10*7)),pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gamePlayer2Hearts.png"),(35*7,10*7)),pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gamePlayer3Hearts.png"),(35*7,10*7))]
tempHeart = pygame.transform.scale(pygame.image.load("assets/player/UI/NNN_gamePlayer3Hearts.png"),(35*7,10*7))

class Player:
    def __init__(self, pos):
        self.type = -1
        self.pos = Vec2(pos)
        self.offset = Vec2((0,0))
        self.dim = (50,100)
        self.life = 3
        self.vec = Vec2((0, 0))
        self.hitbox = pygame.Rect(self.pos.position[0], self.pos.position[1], 50,100)
        self.mainImage = playerImage
        self.SFX = sound.playerSFXHandler()

        self.Image = self.mainImage

        # self.surface.fill((255,0,0))

        self.jumpTimer = 5
        self.speed = 20
        self.grounded = False
        self.reachCheckpoint = False
        self.bullets = pygame.sprite.Group()
        self.gun = Gun(self.pos.position, self.bullets)
        self.keysPressed = pygame.key.get_pressed()
        self.keysPressed_once = self.get_key_presses()
        self.running = False
        self.runAnimationFrame = 0
        self.reloadAnimationFrame = 0
        self.direction = 0
        self.health = 100
        self.healthBarHealth = 100
        self.canDoubleJump = False
        self.doubleJump = False
        self.heldSpace = False
        self.justDoubledJumped = False
        self.takenDamage = False
        self.respawnPos = 0
        self.getHitParalysis = 0
        self.regenTimer = 0
        self.regenCooldown = 300
        self.iFrames = 0
        self.getHitTimer = 0

        self.lives = 3
        self.dead = False
        self.justDiedTimer = 0

        self.completedLevel = False
        self.respawnSFX = sound.SFX("assets/SFX/general/respawn.mp3")



    def draw(self, screen):


        if self.runAnimationFrame >= len(runningAnimationFrames):
            self.runAnimationFrame = 1


        randomOffset = Vec2((0,0))
        self.getHitTimer -= 1


        if self.running:
            self.Image = runningAnimationFrames[int(self.runAnimationFrame)]
        else:
            self.Image = self.mainImage

        if self.gun.reloadingTime >= self.gun.reloadTime-1:
            self.reloadAnimationFrame = 0

        if self.gun.reloading:
            # self.SFX.reloadSFX.play(-1)
            self.Image = reloadAnimationFrames[int(self.reloadAnimationFrame)]
            self.reloadAnimationFrame += 0.2

        if self.getHitParalysis > 0:
            self.Image = getHitImage
            randomOffset = Vec2((0,50))


        screen.blit(pygame.transform.flip(self.Image,self.direction,0), (self.pos+self.offset+randomOffset).position)
        if self.getHitParalysis > 0:
            getHitMask = (getSilouhette(getHitImage))
            getHitMask.convert_alpha()
            # getHitMask.set_alpha(100)
            getHitMask.set_alpha(200*self.getHitTimer/30)
            screen.blit(pygame.transform.flip(getHitMask, self.direction, 0), (self.pos + self.offset + randomOffset).position)

        if not self.gun.reloading:
            self.gun.draw(screen, self.offset)
        # pygame.draw.rect(screen, (255,0,0), self.hitbox)

    def reset(self, position):
        self.health = 100
        self.respawnPos = Vec2((position.position))
        self.pos = Vec2(position.position)
        self.reachCheckpoint = False
        self.vec = Vec2((0, 0))
        self.getHitParalysis = 0
        self.lives = 3
        self.takenDamage = False
        self.reachCheckpoint = False
        self.completedLevel = False
        self.gun.ammoAmount = 10

    def die(self):
        self.health = 100
        self.pos = Vec2(self.respawnPos.position)
        self.reachCheckpoint = True
        self.vec = Vec2((0,0))
        self.getHitParalysis = 0
        self.iFrames = 60
        self.lives -= 1
        self.respawnSFX.playOnce(-1)

    def drawUI(self, screen):
        if self.healthBarHealth>self.health:
            self.healthBarHealth -= 1
        else:
            self.healthBarHealth = self.health


        if self.health < 25 and self.health > 0:
            healthScreenShake = Vec2((random.randint(-5,5), random.randint(-5,5)))
        else:
            healthScreenShake = Vec2((0,0))

        screen.blit(playerHealthBar, (35+healthScreenShake.x, 26+healthScreenShake.y))
        if self.health > 0:
            pygame.draw.rect(screen, (224, 206, 192), pygame.Rect(50+healthScreenShake.x,41+healthScreenShake.y, self.healthBarHealth/100*195,20))
            screen.blit(clip(playerHealthBar_green,0,0,int(self.health/100*195),20), (50+healthScreenShake.x,41+healthScreenShake.y))

        screen.blit(font.render(f"{self.gun.ammoAmount}x",1,(0,0,0)), (1085, 8))
        screen.blit(bulletImage, (1162, 14))
        screen.blit(heartImages[self.lives], (548, 18))

    def gunUpdates(self):
        if not self.completedLevel:
            self.gun.update(self.pos, self.offset)
            self.gun.shoot(self.bullets)
        else:
            self.gun.vec = Vec2((20,0))

    def updateBullets(self):
        for bullet in self.bullets:
            bullet.update(self.offset, self)

    def drawBullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def get_key_presses(self):
        list = [False]
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    list[0] = True


        return tuple(list)

    def takeDamage(self, damage, damageDirection):
        if self.completedLevel:
            return 0

        if self.iFrames <= 0:
            self.health -= damage
            self.takenDamage = True
            self.getHitParalysis = damage
            self.direction = not damageDirection
            self.iFrames = 10
            self.regenTimer =self.regenCooldown
            if damageDirection:
                self.vec = Vec2((10,-20))
            else:
                self.vec = Vec2((-10, -20))
            self.getHitTimer = 30
            getHitMask.set_alpha(100)



    def move(self):
        if self.lives <= 0:
            return 0

        self.keysPressed = pygame.key.get_pressed()
        self.keysPressed_once = self.get_key_presses()
        # self.vec = self.vec*0.1
        if self.keysPressed[pygame.K_a]:
            self.running = True
            self.direction = 1
            self.runAnimationFrame += 0.2
            self.vec.decrement(Vec2((2,0)))
        elif self.keysPressed[pygame.K_d]:
            self.running = True
            self.direction = 0
            self.runAnimationFrame += 0.2
            self.vec.increment(Vec2((2,0)))
        else:
            self.running = False
            self.runAnimationFrame = 0

        if self.keysPressed[pygame.K_LCTRL]:
            self.speed = 25
        else:
            self.speed = 20


        if abs(self.vec.x) > self.speed:
            if self.vec.x < 0:
                self.vec.update_x(-self.speed)
            else:
                self.vec.update_x(self.speed)

        if not self.keysPressed[pygame.K_LCTRL]:
            self.vec.update_x(self.vec.x/1.1)

        if self.keysPressed[pygame.K_SPACE]:
            self.justDoubledJumped = False
            if self.jumpTimer < -10 and self.grounded:
                self.grounded = False
                self.jumpTimer = 10


            elif self.jumpTimer <= 0 and self.doubleJump and not self.heldSpace and self.canDoubleJump:
                self.justDoubledJumped = True
                self.vec.update_y(0)
                self.jumpTimer = 10
                self.doubleJump = False
            self.heldSpace = True

        else:
            self.heldSpace = False

        if self.pos.y > 1200:
            self.health -= 100




        if self.jumpTimer > 0:
            self.vec.increment(Vec2((0, -self.jumpTimer)))

        self.jumpTimer -= 1

        if abs(self.vec.x) > 0 and self.grounded:
            self.SFX.grassWalkSFX.play(self.vec.x*10)


    def update(self):
        self.SFX.update()
        if self.completedLevel:
            self.vec = Vec2((10,0))
            self.running = True
            self.gun.angle = 90
            self.runAnimationFrame += 0.2

        self.takenDamage = False
        self.reachCheckpoint = False
        self.iFrames -= 1
        if self.getHitParalysis <= 0 and not self.completedLevel:
            self.move()
        else:
            self.getHitParalysis -= 1
        self.gravity()

        self.updateHitbox()
        if self.pos.position[1] + self.dim[1] > 720 and self.completedLevel:
            self.pos.update(self.pos.x, 720-100)
            self.vec.update(self.vec.x, 0)

        self.regenTimer -= 1
        if self.regenTimer <= 0 and self.health<100:
            self.health += 0.5

        self.hitbox = pygame.Rect(self.pos.position[0], self.pos.position[1], 50, 100)
        self.dead = self.health<=0

        if self.dead:
            self.die()
            self.justDiedTimer = 120

        self.justDiedTimer -= 1

        # self.pos.increment(self.vec)

    def updateHitbox(self):
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, 50, 100)

    def gravity(self):
        self.vec.increment(Vec2((0,GRAVITY)))