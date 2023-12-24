import random

import pygame

import functions
import settings
import sound
from tile import Tile
from vector import Vec2
from enemies import EnemyContainer
from LevelInteractables import LevelInterectableContainer
from functions import *
import Interactable


levelImage = pygame.image.load("assets/miscellaneous/NNN_gameLevelImages.png")
levelImageSelected = pygame.image.load("assets/miscellaneous/NNN_gameLevelImagesSelected.png")
levelImages = [pygame.image.load("assets/player/NNN_gamePlayerCharacterImage.png")]
levelImagesSelected = [pygame.image.load("assets/player/NNN_gamePlayerCharacterImage.png")]
levelLockImage = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameLevelLock.png"),(140,140))
LevelBackBoardScreen = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameLevelScreen.png"), (22*23, 29*23))
HorizontalLevelBackBoardScreen = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameScreen.png"),(int(36*35.5),int(19*35.5)))

starImageArray = [pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameOneStart.png"), (64*4,20*4)),pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameOneStart.png"), (64*4,20*4)),pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameTwoStar.png"), (64*4,20*4)),pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameThreeStar.png"), (64*4,20*4))]



size = (147,140)
for i in range(10):
    levelImages.append(pygame.transform.scale(functions.clip(levelImage, i*21, 0, 21, 20), size))
    levelImagesSelected.append(pygame.transform.scale(functions.clip(levelImageSelected, i*21, 0, 21, 20), size))

posList = (Vec2((0,0)),Vec2((145,100)),Vec2((420,100)),Vec2((695,100)),Vec2((970,100)),Vec2((970,300)),Vec2((695,300)),Vec2((420,300)),Vec2((145,300)),Vec2((145,500)),Vec2((420,500)))
nameList = ("NA", " NutVille|needs help!","Maca...what?","Growing Up|Fast","Nutty|Parkour!","GO!!!","There is|Pea in my| Nuts","Peanut Hell","There is|More!?","Doubly|Nutty|Parkour","The|Last|Stretch")


class Level:
    def __init__(self, type, playerSpawnPos):
        self.name = nameList[type]
        self.nameRendered = self.renderString(self.name)
        self.layout = None
        self.unlocked = False
        self.selected = False
        self.completed = False
        self.type = type
        self.playerSpawnPos = playerSpawnPos
        self.mainImage = levelImages[self.type]
        self.selectedImage = levelImagesSelected[self.type]
        self.Image = self.mainImage
        self.levelStats = {
            'stars' : 0,
            'time' : 1000000,
        }
        self.button = Interactable.Button(Vec2((515,477)),"PLAY", self.type)
        self.cancelButton = Interactable.CancelButton(Vec2((823, 58)))
        self.pos = posList[self.type]
        self.pressSFX = sound.SFX("assets/SFX/general/button.mp3")
        self.rect = pygame.Rect(self.pos.x, self.pos.y, size[0], size[1])
        self.buttonReset = Interactable.BackButton(Vec2((-1000,0)))

        self.localCompleted = False
        self.completedTimer = 0
        self.tempCompletedVariable = False
        self.achivementSFX = sound.SFX("assets/SFX/general/ability_unlock.mp3")

        self.currentStars = 1
        self.displayTime = 0
        self.currentTime = 0


        self.tileSize = 100
        self.tileHashMap = {}
        self.EnemyContainer = EnemyContainer()
        self.levelInteractables = LevelInterectableContainer()
        self.layoutSize = None
        self.scrollPos = Vec2((0,0))
        self.scrollVec = Vec2((0,0))
        self.screenShake = Vec2((0,0))
        self.finalOffset = Vec2((0,0))
        self.screenShakeDuration = 10


    def renderString(self, string):
        list1 = string.split("|")
        renderedText = []
        counter = 0
        for text in list1:
            renderedText.append((counter,font.render(text, 1, (0,0,0))))
            counter += 1
        return renderedText

    def reset(self, player):
        self.EnemyContainer.enemies.empty()

        self.init_level(self.layout)
        self.levelInteractables.reset()

        self.buttonReset = Interactable.BackButton(Vec2((-1000, 0)))
        self.buttonReset.activated = False
        self.localCompleted = False
        self.completedTimer = 0
        self.displayTime = 0
        self.currentTime = 0
        self.currentStars = 0
        self.scrollPos.x = self.playerSpawnPos.x

        player.reset(self.playerSpawnPos)



    def drawTitle(self, screen):
        for row, text in self.nameRendered:
            screen.blit(text, (508,108+row*50))

    def drawIcon(self, screen):
        if self.type != 1:
            pygame.draw.line(screen, (0,0,0), *((self.pos+Vec2(size)*0.5).position,(posList[self.type-1]+Vec2(size)*0.5).position),10)
        screen.blit(self.Image, self.pos.position)

        if not self.unlocked:
            screen.blit(levelLockImage, self.pos.position)

    def drawUI(self, screen):
        screen.blit(LevelBackBoardScreen, (412, 17))
        # screen.blit(self.nameRendered[0][1], pygame.mouse.get_pos())
        self.drawTitle(screen)
        if self.completed:
            screen.blit(starImageArray[self.levelStats['stars']], (529, 232))
            secondsTime = self.levelStats['time']//settings.FRAMERATE
            screen.blit(font.render(f"Time {secondsTime//60}:{secondsTime%60}",1,(0,0,0)),(535, 331))
        else:
            screen.blit(font.render("UNCOMPLETED",1,(207,24,113)),(503, 340))

        self.cancelButton.update()
        self.button.update()
        self.button.draw(screen)
        self.cancelButton.draw(screen)

        if self.cancelButton.activated:
            self.selected = False

        # print(pygame.mouse.get_pos())

    def drawCompletedLevelScreen(self, player, screen):
        # self.localCompleted = True
        if self.localCompleted:
            self.completedTimer += 2

            # screen.blit(starImageArray[self.levelStats['stars']-1], (529, 232))
            # secondsTime = self.levelStats['time']//settings.FRAMERATE
            # screen.blit(font.render(f"Time {secondsTime//60}:{secondsTime%60}",1,(0,0,0)),(535, 331))

            screen.blit(HorizontalLevelBackBoardScreen, (0,0))
            screen.blit(font.render(f"LEVEL COMPLETED", 1, (0, 0, 0)), (200, 153))
            # self.achivementSFX.update()
            if self.completedTimer > 30 and self.completedTimer <= 180:
                if self.completedTimer % 60 == 0:
                    # print(player.lives, self.currentStars)
                    if player.lives > self.currentStars:

                        self.achivementSFX.playOnce(-1)


                        self.currentStars += 1

            if self.completedTimer > 210:
                if self.displayTime < self.currentTime:
                    self.displayTime += 180

                else:
                    if self.currentTime <= self.levelStats["time"]:
                        self.levelStats["time"] = self.currentTime
                        screen.blit(font.render("NEW HIGHSCORE!", 1, (0, 0, 0)), (509, 345))

                    if self.currentStars >= self.levelStats["stars"]:
                        self.levelStats["stars"] = self.currentStars
                        screen.blit(font.render("NEW HIGHSCORE!", 1, (0, 0, 0)), (509, 254))

                    self.buttonReset.updatePosition(Vec2((959, 423)))



            # self.buttonReset = Interactable.BackButton(Vec2((959, 423)))
            secondsTime = self.displayTime//60

            screen.blit(starImageArray[self.currentStars], (211, 242))
            screen.blit(font.render(f"Time {secondsTime // 60}:{secondsTime % 60}", 1, (0, 0, 0)), (211, 335))
            self.buttonReset.update()
            self.buttonReset.draw(screen)
            # print(pygame.mouse.get_pos())

    def drawFailedLevelScreen(self, screen):
        screen.blit(HorizontalLevelBackBoardScreen, (0, 0))
        screen.blit(font.render(f"LEVEL FAILED", 1, (0, 0, 0)), (200, 153))
        self.buttonReset.updatePosition(Vec2((959, 423)))

        self.buttonReset.update()
        self.buttonReset.draw(screen)



    def updateUI(self):
        mousePos = pygame.mouse.get_pos()
        # self.pressSFX.update()
        if self.rect.collidepoint(mousePos[0], mousePos[1]) and self.unlocked:
            self.Image = self.selectedImage
            if pygame.mouse.get_pressed()[0]:
                if not self.selected:
                    self.pressSFX.playOnce(-1)
                self.selected = True
        else:
            self.Image = self.mainImage



    def getType(self, row_index, col_index, layout):
        adjacency_list = []
        self.layoutSize = (len(layout[0]), len(layout))
        for x in range(-1,2):
            for y in range(-1,2):
                if row_index+x < 0 or row_index+x >= len(layout):
                    adjacency_list.append(0)
                    continue
                elif col_index+y < 0 or col_index+y >= len(layout[0]):
                    adjacency_list.append(0)
                    continue
                if layout[row_index+x][col_index+y] == "X":
                    adjacency_list.append(1)
                else:
                    adjacency_list.append(0)

        if adjacency_list[1]: # there is something on the top
            if adjacency_list[7]: # there is something on the bottom
                if not adjacency_list[3]: # there is nothing on the left
                    return 3
                else: # there is something on the left
                    if adjacency_list[5]: # there is something on the right
                        return 4 # middle
                    return 5 # there is nothing on the right so right
            else: #there is nothing on the bottom
                if not adjacency_list[3]: # there is nothing on the left
                    return 6
                else: # there is something on the left
                    if adjacency_list[6]: # there is something on the right
                        return 7 # middle
                    return 8 # there is nothing on the right so right
        else: # there is nothing on the top
            if not adjacency_list[3]:  # there is nothing on the left
                if not adjacency_list[7]:# if there is nothing on the bottom
                    return 9
                return 0
            else:  # there is something on the left
                if adjacency_list[5]:  # there is something on the right
                    return 1  # middle
                if not adjacency_list[7]:  # if there is nothing on the bottom
                    return 10
                return 2  # there is nothing on the right so right

    def addToHashMap(self, key, value):
        if key not in self.tileHashMap:
            self.tileHashMap[key] = []
        self.tileHashMap[key].append(value)

    def init_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.layout = layout

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == "X":


                    type = self.getType(row_index, col_index, layout)

                    tile1 = Tile((col_index, row_index),100, type)

                    self.addToHashMap(hash(tile1), tile1)
                    self.tiles.add(tile1)

                if cell == "P":
                    self.EnemyContainer.add(0,Vec2((col_index, row_index)), layout)
                elif cell == "M":
                    self.EnemyContainer.add(1, Vec2((col_index, row_index)), layout)
                elif cell == "R":
                    self.EnemyContainer.add(2, Vec2((col_index, row_index)), layout)
                elif cell == "C":
                    self.EnemyContainer.add(3, Vec2((col_index, row_index)), layout)
                elif cell == "B":
                    self.EnemyContainer.add(4, Vec2((col_index, row_index)), layout)
                elif cell == "K":
                    self.levelInteractables.add(0, Vec2((col_index, row_index)))
                elif cell == "E":
                    self.levelInteractables.add(-1, Vec2((col_index, row_index)))
                elif cell == "U":
                    self.levelInteractables.add(-2, Vec2((col_index, row_index)))

    def add_enemies(self):

        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                if cell == "P":
                    self.EnemyContainer.add(0,Vec2((col_index, row_index)), self.layout)
                elif cell == "M":
                    self.EnemyContainer.add(1, Vec2((col_index, row_index)), self.layout)
                elif cell == "R":
                    self.EnemyContainer.add(2, Vec2((col_index, row_index)), self.layout)
                elif cell == "C":
                    self.EnemyContainer.add(3, Vec2((col_index, row_index)), self.layout)
                elif cell == "B":
                    self.EnemyContainer.add(4, Vec2((col_index, row_index)), self.layout)
                # elif cell == "K":
                #     self.levelInteractables.add(0, Vec2((col_index, row_index)))
                # elif cell == "E":
                #     self.levelInteractables.add(-1, Vec2((col_index, row_index)))


        # for tile in self.tiles:
        #     print((tile.pos*0.01).position)
        #
        # for tile in self.tileHashMap:
        #     print(self.tileHashMap[tile])
        #     # for tile2 in tile:
        #     #     print((tile2), (self.tileHashMap[tile2].pos*0.01).position)
        # print(len(self.tileHashMap), len(self.tiles))


    def collision(self, player):

        player.pos.x_increment(player.vec.x)
        surroundingElementsList = []
        for x in range(-1,2):
            for y in range(-1,3):

                position = (functions.translateWorldtoTileSpace(player.pos) + Vec2((x, y)))

                if position.x < 0 or position.y < 0:
                    continue
                elif position.x >= self.layoutSize[0] or position.y >= self.layoutSize[0]:
                    continue

                position *= TILE_SIZE


                hashValue = hash(position)

                try:
                    for tile in self.tileHashMap[hashValue]:
                        surroundingElementsList.append(tile)
                except:
                    continue

        # for tile in self.tiles:
        #     tile.playerCollision_x(player)
        for tile in surroundingElementsList:
            tile.playerCollision_x(player)

        player.pos.y_increment(player.vec.y)
        surroundingElementsList = []
        for x in range(-1, 2):
            for y in range(-1, 3):
                position = (functions.translateWorldtoTileSpace(player.pos) + Vec2((x, y)))

                if position.x < 0 or position.y < 0:
                    continue
                elif position.x >= self.layoutSize[0] or position.y >= self.layoutSize[0]:
                    continue

                position *= TILE_SIZE
                hashValue = hash(position)

                try:
                    for tile in self.tileHashMap[hashValue]:
                        surroundingElementsList.append(tile)
                except:
                    continue

        # for tile in self.tiles:
        #     tile.playerCollision_y(player)

        for tile in surroundingElementsList:
            tile.playerCollision_y(player)




    def LevelInteractableUpdates(self, player):
        self.levelInteractables.update(player)

    def LevelInteractableDraw(self, screen):
        self.levelInteractables.draw(screen, self.finalOffset)

    def EnemyCollision(self):
        self.EnemyContainer.collisionUpdate(self)

    def EnemyBulletCollision(self,bullets):
        self.EnemyContainer.bulletCollision(bullets)

    def PeanutCollision(self):
        self.EnemyContainer.peanutBulletCollision(self)

    def EnemyUpdate(self, player):
        self.EnemyContainer.update(player)
        self.PeanutCollision()

    def DrawEnemy(self, screen):
        self.EnemyContainer.draw(screen, self.finalOffset)


    def bulletCollision(self, bullets):

        for bullet in bullets:
            for tile in self.tiles:
                if bullet.hitbox.colliderect(tile.rect):
                    if (bullet.pos-bullet.vec).y < tile.pos.y: #the bullet was above the tile
                        bullet.angle = 0

                    bullet.SFX.play(-1)


                    bullet.Delete = True
                    break

    def scroll(self, player):
        self.tempCompletedVariable = False
        if not self.localCompleted:
            self.currentTime += 1
        if player.completedLevel:
            if not self.localCompleted:
                self.tempCompletedVariable = True
            self.completed = True
            self.localCompleted = True
            if self.tempCompletedVariable:
                self.completedTimer = 0



        offScreen = player.pos.x+player.offset.x

        if offScreen < SCROLL_LEFT and player.vec.x < 0:
            self.scrollPos.x_increment(player.vec.x)
            # player.offset.x_increment(10)

        elif offScreen > SCROLL_RIGHT and player.vec.x > 0:
            self.scrollPos.x_increment(player.vec.x)
            # player.offset.x_increment(-10)

        player.offset = -self.finalOffset
        # self.scrollPos += self.scrollVec
        # self.scrollPos.update_x(player.pos.x)
        # player.offset = -self.scrollPos
        # self.scrollVec.update_x(self.scrollVec.x/1.2)
        # player.offset = -self.scrollPos
        # self.screenShake = Vec2((random.randint(-3, 3), random.randint(-3, 3)))
        if player.justDiedTimer > 0:
            if player.pos.x < self.scrollPos.x:
                self.scrollPos.x = self.scrollPos.x - (self.scrollPos.x-player.pos.x)*0.1
            else:
                self.scrollPos.x = player.pos.x-200

        if player.takenDamage:
            self.screenShakeDuration = 10

        if self.screenShakeDuration > 0:
            screenShakeMag = int(self.screenShakeDuration/10*20)

            self.screenShake = Vec2((random.randint(-screenShakeMag,screenShakeMag), random.randint(-screenShakeMag,screenShakeMag)))

            self.screenShakeDuration -= 1
        self.finalOffset = self.scrollPos+self.screenShake


        for tile in self.tiles:
            tile.offset = -self.finalOffset
            tile.update()



    def draw(self, screen):

        for tile in self.tiles:
            tile.draw(screen)