import pygame

#----------------------------------------------
# Class pour la gestion des sons
#----------------------------------------------
class Sound():
    def __init__(self):
        # remote rx device
        pygame.init()

    def setFolder(self, sound_folder):
        self.sound_folder = sound_folder
        self.attention_sound = pygame.mixer.Sound(self.sound_folder + '/'+ 'attention.mp3')
        self.shoot_sound = pygame.mixer.Sound(self.sound_folder + '/'+ 'tirez.mp3')
        self.stop_sound = pygame.mixer.Sound(self.sound_folder + '/'+ 'stop.mp3')
        self.shoot_end_sound = pygame.mixer.Sound(self.sound_folder + '/'+ 'tir_termine.mp3')
        self.beep = pygame.mixer.Sound(self.sound_folder + '/'+ 'beep.mp3')

    def loadSerieSound(self, sound_file_name):
        return pygame.mixer.Sound(self.sound_folder + '/'+ sound_file_name)

    def playSerieSound(self, sound_file_name):
        sound_file = self.loadSerieSound(sound_file_name)
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
