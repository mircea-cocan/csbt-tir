#----------------------------------------------
# Class pour toutes les series
#----------------------------------------------
class Serie():
    def __init__(self, title, duration, load_duration, target, sound, sound_file, target_run=True, auto_pause=True):
        self.title = title
        self.duration = duration
        self.load_duration = load_duration
        self.index = 1
        self.sound_file = sound_file
        self.target_run = target_run
        self.auto_pause = auto_pause
        self.action = 0 # 0 - new, 1 - chargez, 2 - attention, 3 - tirez, 4 - stop, 5 - tir terminé
        self.counter = 0
        self.target = target
        self.inProgress = False
        self.sound = sound


    #----------------------------------------------
    # Reset la serie
    #----------------------------------------------
    def reset(self):
        self.index = 1
        self.action = 0 # 0 - new, 1 - chargez, 2 - attention, 3 - tirez, 4 - stop, 5 - tir terminé
        self.counter = 0
        self.inProgress = False

    #----------------------------------------------
    # Retourne le texte correspondant à l'action en cours
    #----------------------------------------------
    def getActionText(self):
        match self.action:
            case 0:
                return ""
            case 1:
                return "CHARGEZ"
            case 2:
                return "ATTENTION"
            case 3:
                return "TIREZ"
            case 4:
                return "STOP"
            case 5:
                return "TIR TERMINE"

    #----------------------------------------------
    # Retourne la couleur correspondant à l'action en cours
    #----------------------------------------------
    def getActionColor(self):
        match self.action:
            case 0:
                return "#008000" # New - green
            case 1:
                return "#D70040" # CHARGEZ - red
            case 2:
                return "#D70040" # ATTENTION - red
            case 3:
                return "#008000 " # TIREZ - green
            case 4:
                return "#D70040" # STOP - red
            case 5:
                return "#D70040" # TIR TERMINE - red
            case 6:
                return "#D70040" # TIR TERMINE - red

    #----------------------------------------------
    # Retourne la couleur correspondant à l'action en cours
    #----------------------------------------------
    def getCounterColor(self):
        match self.action:
            case 0:
                return "#3DDC84" # New - green
            case 1:
                return "#D70040" # CHARGEZ - red
            case 2:
                return "#D70040" # ATTENTION - red
            case 3:
                return "#3DDC84 " # TIREZ - green
            case 4:
                return "#D70040" # STOP - red
            case 5:
                return "#D70040" # TIR TERMINE - red
            case 6:
                return "#D70040" # TIR TERMINE - red

    #----------------------------------------------
    # Fonction appelée chaque seconde
    #----------------------------------------------
    def step(self):
        self.inProgress = True
        if self.counter <= 1:
            self.action = self.action + 1
            match self.action:
                case 0:
                    self.counter = 0 # CHARGEZ - green
                    if self.target_run:
                        self.target.start()
                    self.sound.playSerieSound(self.sound_file)
                case 1:
                    self.counter = self.load_duration # CHARGEZ - red
                    if self.target_run:
                        self.target.start()
                    self.sound.playSerieSound(self.sound_file)
                case 2:
                    self.counter = 7 # ATTENTION - red
                    if self.target_run:
                        self.target.off()
                    self.sound.playAttention()
                case 3:
                    self.counter = self.duration # TIREZ - green
                    if self.target_run:
                        self.target.on()
                    self.sound.playShoot()
                case 4:
                    self.counter = 3 # STOP - red
                    if self.target_run:
                        self.target.off()
                    self.sound.playStop()
                case 5:
                    self.counter = 5 # TIR TERMINE - red
                    if self.target_run:
                        self.target.on()
                    self.sound.playShootEnd()
                case 6:
                    self.inProgress = False
                    self.counter = 5 # TIR TERMINE - red
                case _:
                    self.action = 6
                    self.counter = 0
                    self.inProgress = False
        else:
            if self.counter <= 4 and self.action in [1, 2, 3]:
                self.sound.playBeep()
            self.counter = self.counter - 1