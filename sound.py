import math

import pygame

frameRate = 60

pygame.mixer.init()

class SFXHandler():
    def __init__(self):
        self.grassWalkSFX = SFX("assets/running-in-grass-6237 (mp3cut.net).mp3")
        self.pistachioExplode = SFX("assets/rock-destroy-6409.mp3")

    def update(self):
        self.grassWalkSFX.update()
        self.pistachioExplode.update()

class playerSFXHandler:
    def __init__(self):
        self.grassWalkSFX = SFX("assets/SFX/general/running-in-grass-6237 (mp3cut.net).mp3")
        self.reloadSFX = SFX("assets/SFX/player/reload.mp3")
        self.fireProjectileSFX = SFX("assets/SFX/player/player_projectile_fire.mp3")
        self.projectileExplodeSFX = SFX("assets/SFX/player/projectile/player_projectile_explode.mp3")
        self.landOnGrassSFX = SFX("assets/SFX/general/land_on_grass.mp3")
        self.respawnSFX = SFX("assets/SFX/general/respawn.mp3")

    def update(self):
        self.grassWalkSFX.update()
        self.reloadSFX.update()
        self.fireProjectileSFX.update()
        self.projectileExplodeSFX.update()
        self.landOnGrassSFX.update()
        self.respawnSFX.update()

class pistachioSFXHandler:
    def __init__(self):
        self.grassWalkSFX = SFX("assets/SFX/general/running-in-grass-6237 (mp3cut.net).mp3")
        self.deathSFX = SFX("assets/SFX/general/death.mp3")
        self.explodeSFX = SFX("assets/SFX/pistachio/pistachio_explode.mp3")
        self.hitMarkerSFX = SFX("assets/SFX/general/hitmarker.mp3")

    def update(self):
        self.grassWalkSFX.update()
        self.explodeSFX.update()



class peanutSFXHandler:
    def __init__(self):
        self.grassWalkSFX = SFX("assets/SFX/general/running-in-grass-6237 (mp3cut.net).mp3")
        self.deathSFX = SFX("assets/SFX/general/death.mp3")
        self.projectileFireSFX = SFX("assets/SFX/peanut/peanut_projectile_fire.mp3")
        self.projectileExplodeSFX = SFX("assets/SFX/peanut/projectile/peanut_projectile_explode.mp3")
        self.hitMarkerSFX = SFX("assets/SFX/general/hitmarker.mp3")
        self.openUpSFX = SFX("assets/SFX/peanut/peanut_open.mp3")

    def update(self):
        self.grassWalkSFX.update()
        self.projectileFireSFX.update()
        self.projectileExplodeSFX.update()
        self.openUpSFX.update()

class macadamiaSFXHandler:
    def __init__(self):
        self.grassWalkSFX = SFX("assets/SFX/general/running-in-grass-6237 (mp3cut.net).mp3")
        self.deathSFX = SFX("assets/SFX/general/death.mp3")
        self.moveSFX = SFX("assets/SFX/macadamia/macadamia_move.mp3")
        self.hitMarkerSFX = SFX("assets/SFX/general/hitmarker.mp3")

    def update(self):
        self.grassWalkSFX.update()
        self.moveSFX.update()

class cashewSFXHandler:
    def __init__(self):
        self.moveSFX = SFX("assets/SFX/cashew/cashew_spinning.mp3")
        self.moveSFX.soundVolume = 0.3
        self.deathSFX = SFX("assets/SFX/general/death.mp3")
        self.chargeSFX = SFX("assets/SFX/cashew/cashew_charge.mp3")
        self.hitMarkerSFX = SFX("assets/SFX/general/hitmarker.mp3")

    def update(self):
        self.moveSFX.update()
        self.chargeSFX.update()

class GeneralSFXHandler:
    def __init__(self):
        self.abilityUnlockSFX = SFX("assets/SFX/general/ability_unlock.mp3")
        self.buttonPressSFX = SFX("assets/SFX/general/button.mp3")
        self.checkpointSFX = SFX("assets/SFX/general/checkpoint.mp3")

    def update(self):
        self.abilityUnlockSFX.update()
        self.buttonPressSFX.update()
        self.checkpointSFX.update()

class Music:
    def __init__(self):
        self.track1 = 'assets/SFX/music/retro-and-groovy-fun-21952.mp3'
        self.track2 = 'assets/SFX/music/mobile-phone-ringtone-6769.mp3'
        self.currentTrack = self.track1
        self.volumeMultiplier = 0.05
        self.aimedVolume = 0.5
        self.volume = 0.5*self.volumeMultiplier
        self.playing = False
        self.transitioning = False
        pygame.mixer.music.load(self.currentTrack)

    def changeTrack(self):
        if self.currentTrack == self.track1:
            self.currentTrack = self.track2
        else:
            self.currentTrack = self.track1
        self.playing = False
        pygame.mixer.music.load(self.currentTrack)

    def update(self):
        if self.transitioning:
            if self.volume > 0:
                self.aimedVolume = 0
            else:
                self.aimedVolume = 0.5*self.volumeMultiplier
                self.changeTrack()
                self.transitioning = False



        if self.volume > self.aimedVolume:
            self.volume -= 0.01
        elif self.volume < self.aimedVolume:
            self.volume += 0.01

    def updateVolume(self):
        self.volume = self.aimedVolume

    def play(self):
        pygame.mixer.music.set_volume(self.volume)
        if not self.playing:
            self.playing = True
            pygame.mixer.music.play(-1)


soundVolume = 1

class SFX:
    def __init__(self, path):
        self.path = path
        self.sfx = pygame.mixer.Sound(path)
        self.currentDuration = 0
        self.duration = self.sfx.get_length()* frameRate
        self.volume = 1
        self.volumeMultiplierConstant = 0.001
        self.soundVolume = soundVolume
        self.playing = False
        self.playOnceBool = False

    def update(self):
        self.soundVolume = soundVolume
        if not self.playing and not self.playOnceBool:
            self.currentDuration = 0
            self.sfx.stop()
        self.sfx.set_volume(self.volume*self.soundVolume)
        self.playing = False

    def SoundDropOff(self, dist):
        dist *= self.volumeMultiplierConstant

        amount = (4*math.pi*(dist**2))
        if amount < 1:
            amount = 1

        self.volume = 1/amount


    def playOnce(self, dist):
        self.playing = True
        self.playOnceBool = True
        self.soundVolume = soundVolume
        if dist != -1:
            self.SoundDropOff(dist)
            self.sfx.set_volume(self.volume*self.soundVolume)
        else:
            self.sfx.set_volume(self.soundVolume)

        pygame.mixer.Sound.play(self.sfx)

    def play(self, dist):
        if dist != -1:
            self.SoundDropOff(dist)
            self.sfx.set_volume(self.volume*self.soundVolume)
        else:
            self.sfx.set_volume(self.soundVolume)
        self.playing = True
        if self.currentDuration > 0:
            self.currentDuration -= 1
            return 0

        self.currentDuration = self.duration-10
        pygame.mixer.Sound.play(self.sfx)

    def playSimple(self):
        self.sfx = pygame.mixer.Sound(self.path)
        pygame.mixer.Sound.play(self.sfx)