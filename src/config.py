import json
from serie import Serie
from match import Match
from group import Group

#----------------------------------------------
# Class pour la gestion de la configuration
#----------------------------------------------
class Config():
    #----------------------------------------------
    # Construteur de la classe
    #----------------------------------------------
    def __init__(self):
        # Open and read the JSON file
        with open('config.json', 'r') as file:
            self.data = json.load(file)

        # load groups
        self.groups = []

        self.soundTitles = []
        self.soundFolders = []

        for s in self.data['sounds']:
             self.soundTitles.append(s['title'])
             self.soundFolders.append(s['folder'])
  
    #----------------------------------------------
    # Chargement des matches à partir du fichier config.json
    #----------------------------------------------
    def loadMatches(self, target, sound):
        for g in self.data['groups']:
            tab = 'Match'
            if 'tab' in g:
                tab = g['tab']

            group = Group(g['title'], tab)    
            # load matches
            for m in g['matches']:
                match = Match(m['title'])
                # load series
                for s in m['series']:
                    # series count
                    nbSeries = 1
                    if 'loop' in s:
                        nbSeries = s['loop']

                    # serie sound file
                    soundFileName = 'chargez.mp3'
                    if 'sound' in s:
                        soundFileName = s['sound']

                    #soundFile = sound.loadSerieSound(soundFileName)

                    # load duration
                    load_duration = 60
                    if 'load' in s:
                        load_duration = s['load']

                    # target run On/Off
                    targetRun = True
                    if 'target' in s:
                        targetRun = eval(s['target'])

                    # speed loop (pour vitesse 25m)
                    speedLoop = 1
                    if 'speed_loop' in s:
                        speedLoop = s['speed_loop']

                    # action attention
                    attentionAction = True
                    if 'attention_action' in s:
                        attentionAction = eval(s['attention_action'])

                    # beep
                    beep = True
                    if 'beep' in s:
                        beep = eval(s['beep'])

                    #create series
                    for i in range(nbSeries):
                        title = s['title']
                        if nbSeries > 1:
                            title = title + " (" + str(i+1) + "/" + str(nbSeries) + ")"

                        serie = Serie(title, s['duration'], load_duration, target, beep, sound, soundFileName, speedLoop, attentionAction, targetRun)
                        match.series.append(serie)

                group.matches.append(match)
            self.groups.append(group)