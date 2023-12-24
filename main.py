import pygame

import functions
import particles
import settings
import sound
from player import Player
from level import Level
from foreground import foreGroundContainer
import Interactable
from sound import Music
from vector import Vec2

pygame.init()
pygame.display.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
player = Player((1200,-100))

clock = pygame.time.Clock()
running = True

# level1 = Level()
# level1.init_level([
#     "                                           ",
#     "    X         xx                x          ",
#     "   XX      XXXXXXX        C   XXXX         ",
#     "            XXXX      B         XXX        ",
#     "   XXX       XX      XXX         X         ",
#     " XXXXXX   R        XXXXXX  XXX    K        ",
#     "XXXXXXXXXXX   K  XXXXXXXXXXXXXX   XX    E  ",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
# ])

level1 = Level(1, Vec2((0,0)))
level1.init_level([
    "                                                                                                              ",
    "                                                                                                              ",
    "                                                                                                              ",
    "            XXXX                                                                                              ",
    "   XXX       XX      XXX    B              K                                                                  ",
    " XXXXXX            XXXXXX  XXX            XXXXXXXXX      XXXXXX     XX             BB                         ",
    "XXXXXXXXXXX      XXXXXXXXXXXXXX   XX  XXXXXXXXXXXXX       XXXX      XXX         XXXXXXX                    E  ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
])

level2 = Level(2, Vec2((0,0)))
level2.init_level([
    "                                                                                                                ",
    "                                                                                                                ",
    "                            K                                                                                   ",
    "                         XXXXX           XXXXXX                                                                 ",
    "                          XXX               XX                      M                                           ",
    "         X      XXXX                                 X             XXX                                 X        ",
    "        XX      XXXXXXXX              M          XXXXXX   K       XXXX      XXXXX      BBB      MMMMM  X    E   ",
    "XXXXXXXXXX      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXX      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX       XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
])

level3 = Level(3, Vec2((0,0)))
level3.init_level([
    "                                                                                                                ",
    "                                                                                                                ",
    "                                            BB                 P                                                ",
    "                           BBB        K XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           BBB                           ",
    "          MM        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                   X   ",
    "    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                            PP      X  E",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      P          MMM    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
])

level4 = Level(4, Vec2((0,0)))
level4.init_level([
    "         K             X         XXXXXXX      P                                                                            ",
    "         X     XXXXX   X            XXX    XXXXXX                 XXX                                                      ",
    "         X     X       X                    XXXX                  X                                                        ",
    "        XXX    X     XXX                                          X      B                       XXX     XXX               ",
    "         X  P  X                                     B      B     X     XX                   X                   B         ",
    "    BBXXXXXXX  X            B        K    BBBB       X      X           PX    M B     B      B K               XXXXX   E   ",
    "XXXXXXXXXXXXXXXXX      XXXXXX      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXX    XXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX         X XXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXX",
])

level5 = Level(5, Vec2((0,0)))
level5.init_level([
    "                                                                                                                                 ",
    "                                                    BP                                                                           ",
    "        K                              XXP          XX                                                                           ",
    "        X                  XXPX      XXXXX    XXXXXXXX                                                      B                    ",
    "       XX          P    XXXXXXX                   P          B              XX                X            XX               X    ",
    "        X     P  XXXX   P    P    P    P    P  XXXX   P    P X  K    P   XXXXXX P    P    P XXX PPPPPPPPPPP XX P  PPPPP    PX  E ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
])

level6 = Level(6, Vec2((0,0)))
level6.init_level([
    "                                                                                                                                 ",
    "                                                                                       XXXR                                      ",
    "                                                                                         XX                                      ",
    "              R              X                                                  X    X    X                   B            X     ",
    "      M     XXXX             X                                                 XX    XX   X                  XX           XX     ",
    "      XXXXXXXXXXXXX      BBB     K                           P  BB       P   P  X K PP   XX        RRR        X         P  X E   ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX       XXXX           XXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           M  XXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
])

level7 = Level(7, Vec2((0,0)))
level7.init_level([
    "                                                              X                                                                  ",
    "                       B       MM                B            X           XXXXX                                                  ",
    "                     XXX     XXXXXX             XX            XRR         XXX                                                    ",
    "                      XX       XX               XX            XXXX    XX           XXXXXX      K                           B     ",
    "           BBXXXXXX                 B          XXX                  XXXX             XX       XX                          XX     ",
    "      XXXXXXXXXXXXXX            P  XXX       R XX   K            P   XXXBBBBBBBBBBBBBBBBBBBBBXXX       RRRRRRRRR           X  E  ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   B  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   MMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
])

level8 = Level(8, Vec2((0,0)))
level8.init_level([
    "                                                                                                                                  ",
    "                                        BM                      X                           C                                     ",
    "                                  XXXXXXXXXXXX                 XX               K           B              X       XXXXXX         ",
    "XXXX B         R                  XXXXXXXXXXXX                XXX            XXXXXX        XX              X            X         ",
    "XXXXXXXX     XXX                XXXX                          XXX     XXX             XXX  XX              X            X         ",
    "XXXXXXXX     XXXX   PP  BBBB    XXXXP  P         K         R XXXXB                         XX       U      X            X    E    ",
    "XXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXX    XXXXXXXXXXX        XXXXXXXXXXXXXX",
    "XXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXX    XXXXXXXXXXX        XXXXXXXXXXXXXX",
    "XXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXX    XXXXXXXXXXX        XXXXXXXXXXXXXX",
])

level9 = Level(9, Vec2((0,0)))
level9.init_level([
    "                     XXXXXX             BBB                                                                                          ",
    "                      X                 XXXX                                                                          B              ",
    "                      X                  XXX            B                                     B K                     XXX            ",
    "                     XX  P   B                          X                XX                   XXX          XXX   C    X X            ",
    "                  R   X XXXXXXXXX              K       XXXX        B      XX                  XX                      X X        E   ",
    "XXXXXXX          XXXXXX   XXXXX            XXXXXX      XX       XXXX           XXXX        XXXX     XXXX              XXXXXXXXXXXXXXX",
    "XXXXXXX          XXXXXX                    XXXXXX     R                 R             R    XXXX                  XXX  XXXXXXXXXXXXX  ",
    "XXXXXXX          XXXXXX                    XXXXXXBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBXXXX           XXX         XXXXXXXXXXXXX  ",
    "XXXXXXX          XXXXXX                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                       XXXXXXXXXXXXXX ",
])
level10 = Level(10, Vec2((0,0)))
level10.init_level([
    "                 BB                                                                                                                            ",
    "                 XX                                                                                                XXXX                        ",
    "                 XX                B          B        B   XXXX                     B             XXXX        K                                ",
    "                 XX                X          X        X    XX        C   XXXX      X                      CCCXXXX                   B         ",
    "                            PPP    X   MMM    X  RRR K X        XXXX       XX       X    XXXXX PPP    MM        PPP  XXXX  PPP       X       E ",
    "XXXXXX   B             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         XX   XXXX          X               XXXXXXX                          XXXXXXXXXX",
    "XXXXXXXXXXX            XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX               XX           X    RRR   BBB                XXXXXXX            XXXXXXXXXX",
    "XXXXXXXXXXXXX         XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXBBBBBBBBBBBBBBBBBBBBBBBBBBBBXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXX     XXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXX         XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXXXXXX     XXXXXXXXXXXXXXX",
])

# level11 = Level(11)
# level1.init_level([
#     "                                           ",
#     "    X         xx                x          ",
#     "   XX      XXXXXXX        C   XXXX         ",
#     "            XXXX      B         XXX        ",
#     "   XXX       XX      XXX         X         ",
#     " XXXXXX   R        XXXXXX  XXX    K        ",
#     "XXXXXXXXXXX   K  XXXXXXXXXXXXXX   XX    E  ",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
# ])


levelArray = (level1, level2, level3, level4, level5, level6, level7, level8, level9, level10)
unlockedTo = 1
currentLevel = level1

foreGroundContainer1 = foreGroundContainer()

titleImage = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameTitle.png"), (720,260))
bg_image = pygame.transform.scale(pygame.image.load("assets/NNN_backgroundImage.png"),(1395,720))
DisplayBackboard = pygame.transform.scale(pygame.image.load("assets/miscellaneous/NNN_gameScreen.png"),(int(36*35.5),int(19*35.5)))


ButtonHandler1 = Interactable.ButtonHandler((Interactable.Button(Vec2((490,338)), "PLAY", 0),Interactable.Button(Vec2((490,488)), "SETTING", 1)),-1)
ButtonHandler2 = Interactable.ButtonHandler((),Interactable.BackButton(Vec2((1146, 610))))
ButtonHandler3 = Interactable.ButtonHandler((),Interactable.BackButton(Vec2((1146, 610))))

volumeControl1 = Interactable.Slider(Vec2((338,263)), 200, 1, "SFX Vol")
volumeControl2 = Interactable.Slider(Vec2((338,362)), 200, 0.5, "Music Vol")
particleControl = Interactable.TrueFalseButton((Vec2((954, 226))))
backgroundControl = Interactable.TrueFalseButton((Vec2((954, 326))))

music = Music()

gamestate = "menu"
previousGamestate = "menu"

drawHighQualityBackgrund = True

def changeGamestate(toGamestate):
    global gamestate
    global previousGamestate

    previousGamestate = gamestate
    gamestate = toGamestate

def goBackToPreviousGamestate():
    global gamestate
    global previousGamestate

    gamestate = previousGamestate
    previousGamestate = gamestate


def drawLowPolyBackgroundImage():
    screen.fill((37,195,232))
    offset = -currentLevel.scrollPos.x / 100
    pygame.draw.circle(screen, (39, 100, 18), (50+offset , 700), 250)
    pygame.draw.circle(screen, (42, 110, 15), (750 + offset, 700), 200)
    pygame.draw.circle(screen, (50,130,18),(400+offset ,700),300)
    pygame.draw.circle(screen, (50,130,18),(1100+offset ,700),400)


    pygame.draw.rect(screen, (66,171,23), pygame.Rect(0,600,1280,200))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # x = 1/0
            pygame.quit()

    music.play()
    music.update()
    screen.fill((100,100,100))
    keys = pygame.key.get_pressed()



    if gamestate == "menu":
        screen.blit(bg_image, (0, 0))
        screen.blit(titleImage, (272, 46))
        ButtonHandler1.update()
        ButtonHandler1.draw(screen)

        if ButtonHandler1.activatedButton == 0:
            changeGamestate("levelsscreen")
            ButtonHandler1.activatedButton = None

        elif ButtonHandler1.activatedButton == 1:
            changeGamestate("settings")
            ButtonHandler1.activatedButton = None

    elif gamestate == "settings":
        screen.blit(bg_image, (0, 0))
        screen.blit(DisplayBackboard, (0,0))

        screen.blit(settings.font.render("SOUND", 1, (0, 0, 0)), (174,160))
        screen.blit(settings.font.render("PARTICLES", 1, (0, 0, 0)), (688, 233))
        screen.blit(settings.font.render("HD BACKGND", 1, (0, 0, 0)), (688, 333))
        ButtonHandler2.update()
        volumeControl1.update()
        volumeControl2.update()
        particleControl.update()
        backgroundControl.update()

        particleControl.draw(screen)
        backgroundControl.draw(screen)



        music.aimedVolume = volumeControl2.sliderPos*0.1
        sound.soundVolume = volumeControl1.sliderPos

        particles.drawParticles = particleControl.state
        drawHighQualityBackgrund = backgroundControl.state

        music.updateVolume()

        ButtonHandler2.draw(screen)
        volumeControl1.draw(screen)
        volumeControl2.draw(screen)

        if ButtonHandler2.goBack:
            previousGamestate = "menu"
            goBackToPreviousGamestate()
        # print(pygame.mouse.get_pos())

    elif gamestate == "levelsscreen":
        screen.blit(bg_image, (0, 0))

        for i in range(unlockedTo):
            if i>9:
                break
            levelArray[i].unlocked = True

        for level in levelArray:
            level.updateUI()

        index = 9
        while index >= 0:
            levelArray[index].drawIcon(screen)
            index -= 1

        for level in levelArray:
            if level.selected:
                level.drawUI(screen)
                if level.button.activated:
                    changeGamestate("playlevel")
                    # currentLevel = level1
                    currentLevel = levelArray[level.type-1]
                    currentLevel.reset(player)

        ButtonHandler3.update()
        ButtonHandler3.draw(screen)
        if ButtonHandler3.goBack:
            previousGamestate = "menu"
            goBackToPreviousGamestate()





    elif gamestate == "playlevel":
        if drawHighQualityBackgrund:
            screen.blit(bg_image, (-currentLevel.scrollPos.x / 100, 0))
        else:
            drawLowPolyBackgroundImage()
        player.update()
        player.gunUpdates()
        player.updateBullets()

        currentLevel.EnemyUpdate(player)
        currentLevel.EnemyCollision()
        currentLevel.EnemyBulletCollision(player.bullets)
        currentLevel.LevelInteractableUpdates(player)


        player.draw(screen)
        currentLevel.DrawEnemy(screen)

        player.drawBullets(screen)

        currentLevel.scroll(player)
        currentLevel.draw(screen)
        currentLevel.collision(player)
        currentLevel.bulletCollision(player.bullets)

        currentLevel.LevelInteractableDraw(screen)

        foreGroundContainer1.add(currentLevel, player)
        foreGroundContainer1.update()
        foreGroundContainer1.draw(screen, currentLevel.scrollPos)
        player.drawUI(screen)

        if currentLevel.localCompleted:
            currentLevel.drawCompletedLevelScreen(player, screen)

        if currentLevel.tempCompletedVariable:
            music.transitioning = True


        if currentLevel.buttonReset.activated:
            if currentLevel.localCompleted:
                music.transitioning = True
                unlockedTo = currentLevel.type + 1
            gamestate = "levelsscreen"



        if player.health < 25:
            functions.get_TransRect((0,0,1280,720),100, (255,0,0), screen)

        if player.lives <= 0:
            currentLevel.drawFailedLevelScreen(screen)



    clock.tick(60)
    pygame.display.set_caption(f"NN Game - fps:{int(clock.get_fps())}")
    pygame.display.flip()
















