import pygame
from bullet import Bullet
from vector import Vec2
from sound import playerSFXHandler

class Gun:
    def __init__(self, pos, bulletArray):
        self.pos = Vec2(pos)
        self.vec = Vec2((0,0))
        self.angle = 0
        self.bulletArray = bulletArray
        self.image = pygame.transform.scale(pygame.image.load("assets/player/gun/NNN_gameWaterGun.png"),(60,40))
        self.bulletSpeed = 20
        self.ammoAmount = 10
        self.reloadTime = 78
        self.reloadingTime = 0
        self.firerate = 60/5
        self.fireCooldown = 0
        self.damage = 20
        self.reloading = False
        self.SFX = playerSFXHandler()
        self.mouseStuff = self.getMouseStuff()


    def getMouseStuff(self):
        return (pygame.mouse.get_pressed(), Vec2(pygame.mouse.get_pos()))

    def update(self, pos, offset):
        self.SFX.update()
        self.mouseStuff = self.getMouseStuff()
        self.pos = pos
        self.angle = (self.mouseStuff[1] - self.pos-offset).get_angle()
        self.vec = (self.mouseStuff[1] - self.pos-offset).normalise()*self.bulletSpeed
        if self.ammoAmount <= 0:
            if not self.reloading:
                self.reloadingTime = self.reloadTime

            self.reloading = True


        else:
            self.reloading = False

        if self.reloading:
            self.SFX.reloadSFX.play(-1)
            self.reloadingTime -= 1
            if self.reloadingTime <= 0:
                self.reload()

    def reload(self):
        self.reloading = False
        self.ammoAmount = 10

    def draw(self, screen, offset):
        angleOffset = 0
        if self.angle < 0:
            image = pygame.transform.flip(self.image,1,0)
            angleOffset = 180
        else:
            image = self.image

        rotImage = pygame.transform.rotate(image,(self.angle-90+angleOffset))
        offsetVector = Vec2(rotImage.get_size()) * 0.5



        screen.blit(rotImage, (self.pos+self.vec-offsetVector+offset+Vec2((25,50))).position)

    def shoot(self, bulletArray):
        if self.mouseStuff[0][0] and self.ammoAmount > 0 and self.fireCooldown <= 0:
            self.SFX.fireProjectileSFX.playOnce(-1)
            self.ammoAmount -= 1
            self.fireCooldown = self.firerate
            bulletArray.add(Bullet(self.pos+Vec2((0,50))+self.vec,self.vec))
        self.fireCooldown -= 1

