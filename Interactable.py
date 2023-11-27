import settings
import pygame
from vector import Vec2
import sound


font = pygame.font.Font("assets/fonts/Inconsolata,Lexend_Peta,Pixelify_Sans/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 50)

buttonImage1 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameButtonUnpressed.png"),(300,100))
buttonImage2 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameButtonPressed.png"), (300,100))

backButtonImage1 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameBackButtonUnpressed.png"),(100,100))
backButtonImage2 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameBackButtonPressed.png"), (100,100))

cancelButtonImage1 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameCancelButton.png"),(50,50))
cancelButtonImage2 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameCancelButtonSelected.png"), (50,50))

menuButtonImage1 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameMenuButtton.png"),(50,50))
menuButtonImage2 = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameMenuButttonSelected.png"), (50,50))


class ButtonHandler:
    def __init__(self, buttons, backButton):
        self.buttons = buttons
        if not backButton == -1:
            self.backButton = backButton
        else:
            self.backButton = BackButton(Vec2((-300, -300)))
        self.activatedButton = None
        self.goBack = self.backButton.update()

    def update(self):
        for button in self.buttons:
            button.update()

        for button in self.buttons:
            if button.activated:
                self.activatedButton = button.id
                break
        self.backButton.update()
        self.goBack = self.backButton.activated

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
        self.backButton.draw(screen)


class Button():
    def __init__(self, pos, text, id):
        self.pos = pos
        self.pressSFX = sound.SFX("assets/SFX/general/button.mp3")
        self.size = Vec2((300,100))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.text = text
        self.unPressedImage = buttonImage1
        self.PressedImage = buttonImage2
        self.Image = self.unPressedImage
        self.textRendered = font.render(self.text,1,(0,0,0))
        self.textOffset = (self.size-Vec2(self.textRendered.get_size()))*0.5
        self.id = id
        self.activated = False

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.activated = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            self.Image = self.PressedImage
            if pygame.mouse.get_pressed()[0]:
                self.pressSFX.playOnce(-1)
                self.activated = True
        else:
            self.Image = self.unPressedImage

    def draw(self, screen):
        screen.blit(self.Image, self.pos.position)
        screen.blit(self.textRendered, (self.pos+self.textOffset).position)

class BackButton:
    def __init__(self, pos):
        self.pos = pos
        self.size = Vec2((100, 100))
        self.pressSFX = sound.SFX("assets/SFX/general/button.mp3")
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.unPressedImage = backButtonImage1
        self.PressedImage = backButtonImage2
        self.Image = self.unPressedImage
        self.activated = False

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.activated = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            self.Image = self.PressedImage
            if pygame.mouse.get_pressed()[0]:
                self.pressSFX.playOnce(-1)
                self.activated = True
        else:
            self.Image = self.unPressedImage

    def updatePosition(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def draw(self, screen):
        screen.blit(self.Image, self.pos.position)

class CancelButton:
    def __init__(self, pos):
        self.pos = pos
        self.size = Vec2((50, 50))
        self.pressSFX = sound.SFX("assets/SFX/general/button.mp3")
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.unPressedImage = cancelButtonImage1
        self.PressedImage = cancelButtonImage2
        self.Image = self.unPressedImage
        self.activated = False

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.activated = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            self.Image = self.PressedImage
            if pygame.mouse.get_pressed()[0]:
                self.pressSFX.playOnce(-1)
                self.activated = True
        else:
            self.Image = self.unPressedImage

    def draw(self, screen):
        screen.blit(self.Image, self.pos.position)

class TrueFalseButton():
    def __init__(self, pos):
        self.pos = pos
        self.size = Vec2((70, 70))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.pressSFX = sound.SFX("assets/SFX/general/button.mp3")
        self.borderSize = 10
        self.coloredRect = pygame.Rect(self.pos.x+self.borderSize, self.pos.y+self.borderSize, self.size.x-self.borderSize*2, self.size.y-self.borderSize*2)
        self.colors = ((212, 10, 84), (116, 189, 79))
        self.color = self.colors[0]
        self.unPressedImage = menuButtonImage1
        self.PressedImage = menuButtonImage2
        self.Image = self.unPressedImage
        self.state = True

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.activated = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pressSFX.playOnce(-1)
                    self.state = not self.state
        else:
            self.Image = self.unPressedImage

        if self.state:
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), self.rect)
        pygame.draw.rect(screen, self.color, self.coloredRect)


class MenuButton:
    def __init__(self, pos):
        self.pos = pos
        self.size = Vec2((50, 50))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.unPressedImage = menuButtonImage1
        self.PressedImage = menuButtonImage2
        self.Image = self.unPressedImage
        self.activated = False

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.activated = False
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            self.Image = self.PressedImage
            if pygame.mouse.get_pressed()[0]:
                self.activated = True
        else:
            self.Image = self.unPressedImage

    def draw(self, screen):
        screen.blit(self.Image, self.pos.position)

class Slider:
    def __init__(self, pos, len, sliderPos, name):
        self.pos = pos
        self.sliderPos = sliderPos
        self.len = len
        self.name = name
        self.name_rendered = font.render(name, 1, (0, 0, 0))
        self.height = 40
        self.rect = pygame.Rect(self.pos.x, self.pos.y-self.height/2, self.len, self.height)


    def update(self):

        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos[0], mousePos[1]) and pygame.mouse.get_pressed()[0]:
            self.sliderPos = (mousePos[0]-self.pos.x) / self.len
        self.textRendered = font.render(str(int(self.sliderPos*100)), 1, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.line(screen, (0,0,0), *(self.pos.position, (self.pos+Vec2((self.len,0))).position), 10)
        pygame.draw.circle(screen, (232, 32, 129), (self.pos+Vec2((self.len*self.sliderPos,0))).position,20)
        screen.blit(self.textRendered, (self.pos+Vec2((self.len+20,-self.textRendered.get_height()/2))).position)
        screen.blit(self.name_rendered, (self.pos+Vec2((-self.name_rendered.get_width(),-self.textRendered.get_height()/2))).position)


