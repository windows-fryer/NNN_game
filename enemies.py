import random

import pygame
from vector import Vec2
from settings import *
import sound
from functions import *
from bullet import PeanutBullet

masks = {}

class EnemyContainer():
    def __init__(self):
        self.enemies = pygame.sprite.Group()


    def update(self, player):
        self.enemies.update(player)

    def add(self, type, pos, layout):
        if type == 0:
            enemy = Pistachio(pos*100, layout)
        elif type == 1:
            enemy = Macadamia(pos * 100, layout)
        elif type == 2:
            enemy = Peanut(pos * 100, layout)
        elif type == 3:
            enemy = Cashew(pos * 100, layout)
        elif type == 4:
            enemy = BabyPistachio(pos*100)


        self.enemies.add(enemy)

    def collisionUpdate(self, level):
        for enemy in self.enemies:

            if enemy.type == 3 or enemy.type == 4:
                continue
            if not enemy.awakened:
                continue
            level.collision(enemy)

    def bulletCollision(self, bullets):
        for enemy in self.enemies:
            if enemy.type == 4:
                continue

            if enemy.bulletCollision(bullets):
                continue

    def peanutBulletCollision(self, level):
        for enemy in self.enemies:
            if enemy.type == 2:
                for bullet in enemy.bullets:
                    surroundingElementsList = []
                    for x in range(-1, 2):
                        for y in range(-1, 3):

                            position = (translateWorldtoTileSpace(bullet.pos) + Vec2((x, y)))

                            if position.x < 0 or position.y < 0:
                                continue
                            elif position.x >= level.layoutSize[0] or position.y >= level.layoutSize[0]:
                                continue

                            position *= TILE_SIZE

                            hashValue = hash(position)

                            try:
                                for tile in level.tileHashMap[hashValue]:
                                    surroundingElementsList.append(tile)
                            except:
                                continue

                    for tile in surroundingElementsList:
                        if tile.rect.colliderect(bullet.hitbox):
                            bullet.Delete = True
                            break

    def draw(self, screen, offset):
        for enemy in self.enemies:
            enemy.draw(screen, offset)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, health, size, speed, walkAnimationLength, layout):
        super().__init__()
        self.pos = pos
        self.vec = Vec2((0,0))
        self.tilePos = self.convert_SelfPostoTilePos()
        self.direction = 1
        self.dim = size
        self.health = health
        self.awakened = False
        self.toPlayerVec = Vec2((0,0))
        self.direction = 0
        self.jumpTimer = 5
        self.grounded = True
        self.speed = speed
        self.takenDamage = False
        self.takeDamageTimer = 10
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.dim[0], self.dim[1])
        self.rect = self.hitbox
        self.layout = layout
        self.delete = False
        self.walkAnimationFrame = 0
        self.hitmarkerSFX = sound.SFX("assets/SFX/general/hitmarker.mp3")
        self.deathSFX = sound.SFX("assets/SFX/general/death.mp3")
        self.walkAnimationLength = walkAnimationLength

    def getAwakened(self, player):
        if (player.pos-self.pos).mag <= 1200:
            self.awakened = True

    def moveToPlayer(self, player):
        if player.pos.x > self.pos.x:
            self.toPlayerVec = Vec2((1,0))
        else:
            self.toPlayerVec = Vec2((-1, 0))

    def convert_SelfPostoTilePos(self):
        return self.pos // TILE_SIZE

    def getTilefromTilePos(self, tilepos):
        if tilepos.x >= len(self.layout[0]) or tilepos.y >= len(self.layout):
            return " "
        elif tilepos.x < 0 or tilepos.y < 0:
            return " "


        return self.layout[int(tilepos.y)][int(tilepos.x)]

    def generalUpdates(self):
        if self.pos.y > 1200 and self.type != 3:
            self.health -= 100
        self.deathSFX.update()
        self.hitmarkerSFX.update()

    def standardMovement(self, player):
        self.moveToPlayer(player)
        self.tilePos = self.convert_SelfPostoTilePos()
        self.direction = self.toPlayerVec.x == 1

        self.vec += self.toPlayerVec * self.speed

        if self.getTilefromTilePos(self.tilePos+Vec2((self.toPlayerVec.x,2))) == " ": # checks whether the block below infront
            self.jump()
        if self.getTilefromTilePos(self.tilePos+self.toPlayerVec) == "X": # checks whether there is a block infront of it
            self.jump()

        if abs(self.vec.x) > self.speed:
            if self.vec.x < 0:
                self.vec.update_x(-self.speed)
            else:
                self.vec.update_x(self.speed)

        if self.jumpTimer > 0:
            self.vec.increment(Vec2((0, -self.jumpTimer)))

        self.jumpTimer -= 1
        self.walkAnimationFrame += 0.2
        if self.walkAnimationFrame >= self.walkAnimationLength:
            self.walkAnimationFrame = 1


    def bulletCollision(self, bullets):
        for bullet in bullets:
            if bullet.hitbox.colliderect(self.hitbox):
                self.hitmarkerSFX.playOnce(-1)
                self.takeDamage(bullet.damage)
                bullet.Delete = True
                return True
            return False

    def takeDamage(self, damage):
        self.health -= damage
        self.takenDamage = True
        self.takeDamageTimer = 10



    def jump(self):
        if self.jumpTimer < -10 and self.grounded:
            self.grounded = False
            self.jumpTimer = 10



    def updateHitbox(self):
        self.hitbox = pygame.Rect(self.pos.x, self.pos.y, self.dim[0], self.dim[1])

    def attack(self):
        pass

    def gravity(self):
        self.vec.increment(Vec2((0, GRAVITY)))

    def getMask(self):
        hash = hashSurface(self.Image)
        if hash in masks:
            return masks[hash]
        else:
            ImageMask = getSilouhette(self.Image)
            masks[hash] = ImageMask
        return ImageMask

    def drawHash(self, screen, offset):
        image = self.getMask()
        screen.blit(image, (self.pos-offset).position)

    def drawHitbox(self, screen, offset):
        pygame.draw.rect(screen, (255,0,0), self.hitbox.move(-offset.x, -offset.y))

def explosionDamage(n):
    return -(n**6)+1

PistachioExplodeImage = pygame.image.load("assets/enemys/pistachio/NNN_gamePistachioEnemyAttackAnimationFrames.png")
PistachioExplodeAnimationFrames = []
for i in range(13):
    PistachioExplodeAnimationFrames.append(pygame.transform.scale(clip(PistachioExplodeImage, i*20, 0, 20, 20),(100,100)))

PistachioWalkImage = pygame.image.load("assets/enemys/pistachio/NNN_gamePistachioEnemyWalkAnimationFrames.png")
PistachioWalkAnimationFrames = []
for i in range(5):
    PistachioWalkAnimationFrames.append(pygame.transform.scale(clip(PistachioWalkImage, i*10, 0, 10, 20),(50,100)))



class Pistachio(Enemy):
    def __init__(self, pos, layout):
        super().__init__(pos,60, (50,100),6,5,layout)
        self.type = 1
        self.explosionDamageDist = 300
        self.damage = 150
        self.mainImage = pygame.transform.scale(pygame.image.load("assets/enemys/pistachio/NNN_gamePistachioEnemy.png"),(50,100))
        self.SFX = sound.pistachioSFXHandler()
        self.Image = self.mainImage
        self.exploding = False
        self.attackTimer = 0



    def attack(self, player):
        playerToSelf = (player.pos - self.pos).mag
        self.exploding = True
        if playerToSelf < self.explosionDamageDist and self.attackTimer >= 10:
            player.takeDamage(self.damage*explosionDamage(playerToSelf/self.explosionDamageDist), self.direction)

        # self.delete = True

    def update(self, player):

        self.vec.update_x(self.vec.x / 1.1)

        if self.awakened:

            super().generalUpdates()

            self.takenDamage = False
            self.takeDamageTimer -= 1

            if self.delete:
                self.SFX.explodeSFX.playOnce(-1)
                self.deathSFX.playOnce(-1)
                self.kill()

            if not self.exploding:
                self.standardMovement(player)
            self.gravity()

            if (player.pos-self.pos).mag <= self.explosionDamageDist/3 or self.exploding:
                self.attack(player)

            if self.health <= 0:
                self.delete = True




        else:
            super().getAwakened(player)

    def draw(self, screen, offset):
        # pygame.draw.rect(screen, (255,0,0), self.hitbox.move(-offset.x, -offset.y))

        self.Image = PistachioWalkAnimationFrames[int(self.walkAnimationFrame)]

        if self.exploding:
            self.Image = PistachioExplodeAnimationFrames[int(self.attackTimer)]
            self.attackTimer += 0.5
            if self.attackTimer >= 12:
                self.delete = True

        screen.blit(pygame.transform.flip(self.Image, self.direction,0), (self.pos-offset).position)

        if self.takeDamageTimer > 0:
            screen.blit(pygame.transform.flip(self.getMask(), self.direction,0), (self.pos-offset).position)

BabyPistachioClosedImage = pygame.transform.scale(pygame.image.load("assets/enemys/babyPistachio/NNN_gameBabyPistachioEnemy_closed.png"),(100,100))
BabyPistachioIdleAnimationImage = pygame.image.load("assets/enemys/babyPistachio/NNN_gameBabyPistachioEnemyIdleAnimationFrames.png")
BabyPistachioIdleAnimationFrames = []
for i in range(9):
    BabyPistachioIdleAnimationFrames.append(pygame.transform.scale(clip(BabyPistachioIdleAnimationImage, i*20, 0, 20, 20),(100,100)))



class BabyPistachio(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.vec = Vec2((0,0))
        self.grounded = False
        self.type = 4
        self.mainImage = pygame.transform.scale(pygame.image.load("assets/enemys/babyPistachio/NNN_gameBabyPistachioEnemy.png"), (TILE_SIZE, TILE_SIZE))
        self.Image = self.mainImage
        self.idleAnimationFrame = 0
        self.attackTimer = 0
        self.rect = pygame.Rect(self.pos.x, self.pos.y, TILE_SIZE, TILE_SIZE)
        self.hitbox = self.rect
        self.damage = 35
        self.delete = False
        self.awakened = False
        self.SFX = sound.SFX("assets/SFX/babypistachio/fresh_snap-37385.mp3")


    def update(self, player):
        self.SFX.update()
        if player.hitbox.colliderect(self.rect):
            self.SFX.playOnce(-1)
            player.takeDamage(self.damage, player.pos.x>self.pos.x)
            self.attackTimer = 20

        self.idleAnimationFrame += 0.33
        if self.idleAnimationFrame >= len(BabyPistachioIdleAnimationFrames):
            self.idleAnimationFrame = 0


        self.attackTimer -= 1

    def draw(self, screen, offset):

        self.Image = BabyPistachioIdleAnimationFrames[int(self.idleAnimationFrame)]
        if self.attackTimer > 0:
            self.Image = BabyPistachioClosedImage


        screen.blit(self.Image, (self.pos-offset).position)



MacadamiaAttackImage = pygame.image.load("assets/enemys/macadamia/NNN_gameMacadamiaEnemyAttackAnimation.png")
MacadamiaAttackAnimationFrames = []
for i in range(9):
    MacadamiaAttackAnimationFrames.append(pygame.transform.scale(clip(MacadamiaAttackImage, i*30, 0, 30, 20),(150,100)))

MacadamiaWalkImage = pygame.image.load("assets/enemys/macadamia/NNN_gameMacadamiaEnemyMovingAnimation.png")
MacadamiaWalkAnimationFrames = []
for i in range(5):
    MacadamiaWalkAnimationFrames.append(pygame.transform.scale(clip(MacadamiaWalkImage, i*20, 0, 20, 20),(100,100)))




class Macadamia(Enemy):
    def __init__(self, pos, layout):
        super().__init__(pos,80, (100,100),6,5,layout)
        self.type = 0
        self.attackDist = 400
        self.damage = 20
        self.mainImage = pygame.transform.scale(pygame.image.load("assets/enemys/macadamia/NNN_gameMacadamiaEnemy.png"),(100,100))
        self.SFX = sound.macadamiaSFXHandler()
        self.Image = self.mainImage
        self.attacking = False
        self.attackOffset = Vec2((50,0))
        self.attackFrames = 0
        self.attackCooldown = 60
        self.attackCooldownTimer = 0
        self.inflictDamageTimer = 0
        self.inflictDamageCooldown = 20



    def attack(self, player):
        playerToSelf = (player.pos - self.pos).mag
        self.attackOffset = Vec2((50,0))
        self.attacking = True
        if playerToSelf < self.attackDist and self.inflictDamageTimer<=0:
            self.inflictDamageTimer = self.inflictDamageCooldown
            player.takeDamage(self.damage, self.direction)

        # self.delete = True

    def update(self, player):
        self.vec.update_x(self.vec.x / 1.1)
        if self.awakened:
            super().generalUpdates()
            self.takenDamage = False
            self.takeDamageTimer -= 1
            self.SFX.update()

            self.SFX.moveSFX.play((player.pos-self.pos).mag)

            if self.delete:
                self.deathSFX.playOnce(-1)
                self.kill()

            if not self.attacking:
                self.standardMovement(player)
            self.gravity()

            if ((player.pos-self.pos).mag <= self.attackDist/3 or self.attacking) and self.attackCooldownTimer <= 0:
                self.attack(player)
            else:
                self.attackOffset = Vec2((0, 0))

            if self.health <= 0:
                self.delete = True
            self.attackCooldownTimer -= 1
            self.inflictDamageTimer -= 1




        else:
            super().getAwakened(player)

    def draw(self, screen, offset):
        # pygame.draw.rect(screen, (255,0,0), self.hitbox.move(-offset.x, -offset.y))

        self.Image = MacadamiaWalkAnimationFrames[int(self.walkAnimationFrame)]

        if self.attacking:
            self.Image = MacadamiaAttackAnimationFrames[int(self.attackFrames)]

            self.attackFrames += 0.2
            if self.attackFrames > 8:
                self.attackFrames = 0
                self.attacking = False
                self.attackCooldownTimer = self.attackCooldown

        screen.blit(pygame.transform.flip(self.Image, self.direction,0), (self.pos-offset+(self.attackOffset*self.toPlayerVec.x)).position)

        if self.takeDamageTimer > 0:
            screen.blit(pygame.transform.flip(self.getMask(), self.direction,0), (self.pos-offset+(self.attackOffset*self.toPlayerVec.x)).position)


PeanutAttackImage = pygame.image.load("assets/enemys/peanut/NNN_gamePeanutEnemyAttackAnimation.png")
PeanutAttackAnimationFrames = []
for i in range(13):
    PeanutAttackAnimationFrames.append(pygame.transform.scale(clip(PeanutAttackImage, i*20, 0, 20, 20),(100,100)))

PeanutWalkImage = pygame.image.load("assets/enemys/peanut/NNN_gamePeanutEnemyWalkingAnimation.png")
PeanutWalkAnimationFrames = []
for i in range(6):
    PeanutWalkAnimationFrames.append(pygame.transform.scale(clip(PeanutWalkImage, i*10, 0, 10, 20),(50,100)))

class Peanut(Enemy):
    def __init__(self, pos, layout):
        super().__init__(pos,80, (50,100),3,6,layout)
        self.type = 2
        self.attackDist = 1000
        self.runDist = 500
        self.damage = 20
        self.still = False
        self.mainImage = pygame.transform.scale(pygame.image.load("assets/enemys/peanut/NNN_gamePeanutEnemy.png"),(50,100))
        self.Image = self.mainImage
        self.attacking = False
        self.attackOffset = Vec2((50,0))
        self.attackFrames = 0
        self.attackCooldown = 60
        self.attackCooldownTimer = 0
        self.bulletShootNumber = 5
        self.bullets = pygame.sprite.Group()
        self.SFX = sound.peanutSFXHandler()



    def attack(self, player):
        self.attackOffset = Vec2((50,0))
        self.attacking = True
        self.SFX.openUpSFX.play((player.pos-self.pos).mag)

        if self.attackFrames >= 6 and self.attackFrames <= 8 and self.bulletShootNumber > 0:
            self.SFX.projectileFireSFX.playOnce((player.pos-self.pos).mag)
            self.bullets.add(PeanutBullet(self.pos, Vec2((0,-20)), random.randint(5,15)))
            self.bulletShootNumber -= 1
        else:
            self.bulletShootNumber = 1

        # self.delete = True

    def standardMovement(self, player):
        self.moveToPlayer(player)


        if (player.pos - self.pos).mag < self.runDist:
            self.toPlayerVec = -self.toPlayerVec

        self.tilePos = self.convert_SelfPostoTilePos()
        self.direction = self.toPlayerVec.x == 1

        self.vec += self.toPlayerVec * self.speed

        if self.getTilefromTilePos(self.tilePos+Vec2((self.toPlayerVec.x,2))) == " ": # checks whether the block below infront
            self.jump()
        if self.getTilefromTilePos(self.tilePos+self.toPlayerVec) == "X": # checks whether there is a block infront of it
            self.jump()

        if abs(self.vec.x) > self.speed:
            if self.vec.x < 0:
                self.vec.update_x(-self.speed)
            else:
                self.vec.update_x(self.speed)

        if self.jumpTimer > 0:
            self.vec.increment(Vec2((0, -self.jumpTimer)))

        self.jumpTimer -= 1
        self.walkAnimationFrame += 0.2
        if self.walkAnimationFrame >= self.walkAnimationLength:
            self.walkAnimationFrame = 1



    def update(self, player):
        if self.awakened:
            super().generalUpdates()
            self.SFX.update()
            self.takenDamage = False
            self.takeDamageTimer -= 1
            self.vec.update_x(self.vec.x / 1.1)

            if self.delete:
                self.deathSFX.playOnce(-1)
                self.kill()

            fromPlayerDist = (player.pos-self.pos).mag

            if fromPlayerDist > self.runDist and fromPlayerDist < self.attackDist:
                self.still = True
            else:
                self.still = False

            if not self.attacking and not self.still:
                self.standardMovement(player)
            self.gravity()

            if ((player.pos-self.pos).mag <= self.attackDist or self.attacking) and self.attackCooldownTimer <= 0:
                self.attack(player)
            else:
                self.attackOffset = Vec2((0, 0))

            if self.health <= 0:
                self.delete = True

            for bullet in self.bullets:
                bullet.update(player)
                if bullet.hitbox.colliderect(player.hitbox):
                    player.takeDamage(self.damage, bullet.direction)
                    bullet.Delete = True

            self.attackCooldownTimer -= 1






        else:
            super().getAwakened(player)

    def draw(self, screen, offset):
        # pygame.draw.rect(screen, (255,0,0), self.hitbox.move(-offset.x, -offset.y))

        if self.still:
            self.Image = self.mainImage
        else:

            self.Image = PeanutWalkAnimationFrames[int(self.walkAnimationFrame)]

        if self.attacking:
            self.Image = PeanutAttackAnimationFrames[int(self.attackFrames)]

            self.attackFrames += 0.2
            if self.attackFrames > 13:
                self.attackFrames = 0
                self.attacking = False
                self.attackCooldownTimer = self.attackCooldown

        screen.blit(pygame.transform.flip(self.Image, self.direction,0), (self.pos-offset+(self.attackOffset*self.toPlayerVec.x)).position)

        if self.takeDamageTimer > 0:
            screen.blit(pygame.transform.flip(self.getMask(), self.direction,0), (self.pos-offset+(self.attackOffset*self.toPlayerVec.x)).position)

        for bullet in self.bullets:
            bullet.draw(screen)


        # super().drawHitbox(screen,offset)

class Cashew(Enemy):
    def __init__(self, pos, layout):
        super().__init__(pos,150, (150,150),30,6,layout)
        self.type = 3
        self.damage = 40
        self.mainImage = pygame.transform.scale(pygame.image.load("assets/enemys/cashew/NNN_gameCashewEnemy.png"),(105,140))
        self.rotImageArray = []
        for i in range(17):
            self.rotImageArray.append(pygame.transform.rotate(self.mainImage, i*20))
        self.Image = self.mainImage
        self.attacking = False
        self.attackCooldown = 60
        self.attackCooldownTimer = 0
        self.inflictDamageTimer = 0
        self.inflictDamageCooldown = 40
        self.goToPos = Vec2((0,0))
        self.rotateAngle = 0
        self.SFX = sound.cashewSFXHandler()




    def update(self, player):

        if self.awakened:
            super().generalUpdates()
            self.SFX.update()
            self.takenDamage = False
            self.takeDamageTimer -= 1
            self.grounded = False
            self.rotateAngle += 1
            if self.rotateAngle >= 17:
                self.rotateAngle = 0

            self.SFX.moveSFX.play((player.pos-self.pos).mag)





            if self.attacking:

                if (self.pos - self.goToPos).mag <= 100:
                    self.attackCooldownTimer = self.attackCooldown
                    self.attacking = False
                self.vec += (self.goToPos-self.pos).normalise()

                if self.vec.mag > self.speed:
                    self.vec *= 0.9

            else:
                self.vec *= 0.9
                self.attackCooldownTimer -= 1
                if self.attackCooldownTimer <= 0:
                    self.attacking = True
                    self.SFX.chargeSFX.playOnce((player.pos-self.pos).mag)
                    self.goToPos = Vec2(player.pos.position)+(player.pos-self.pos).normalise()*100

            if self.health <= 0:
                self.deathSFX.playOnce(-1)
                self.kill()

            self.direction = self.vec.x > 0
            self.pos += self.vec
            self.hitbox = pygame.Rect(self.pos.x-self.dim[0]/2, self.pos.y-self.dim[1]/2, self.dim[0], self.dim[1])

            if self.hitbox.colliderect(player.hitbox):
                if self.inflictDamageTimer <= 0:
                    player.takeDamage(self.damage, self.direction)
                    self.inflictDamageTimer = self.inflictDamageCooldown

            self.inflictDamageTimer -= 1

        else:
            super().getAwakened(player)
            self.goToPos = player.pos

    def draw(self, screen, offset):

        self.Image = self.rotImageArray[self.rotateAngle]
        imageRotOffset = Vec2(self.Image.get_size())*0.5

        screen.blit(pygame.transform.flip(self.Image, self.direction,0), (self.pos-offset-imageRotOffset).position)

        if self.takeDamageTimer > 0:
            screen.blit(pygame.transform.flip(self.getMask(), self.direction, 0), (self.pos - offset - imageRotOffset).position)

        # super().drawHitbox(screen,offset)












