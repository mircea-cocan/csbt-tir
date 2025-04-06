import pygame

#----------------------------------------------
# Class pour la gestion des sons
#----------------------------------------------
class Sound():
    def __init__(self):
        # remote rx device
        pygame.init()
        self.load_sound = pygame.mixer.Sound('chargez.mp3')
        self.attention_sound = pygame.mixer.Sound('attention.mp3')
        self.shoot_sound = pygame.mixer.Sound('tirez.mp3')
        self.stop_sound = pygame.mixer.Sound('stop.mp3')
        self.shoot_end_sound = pygame.mixer.Sound('tir_termine.mp3')
        self.beep = pygame.mixer.Sound('beep.mp3')

    def loadSerieSound(self, sound_file_name):
        return pygame.mixer.Sound(sound_file_name)

    def playSerieSound(self, sound_file):
        sound_file.play()

    def playAttention(self):
        self.attention_sound.play()

    def playShoot(self):
        self.shoot_sound.play()

    def playStop(self):
        self.stop_sound.play()

    def playShootEnd(self):
        self.shoot_end_sound.play()

    def playBeep(self):
        self.beep.play()
