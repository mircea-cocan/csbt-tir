#----------------------------------------------
# Class pour toutes les matchs
#----------------------------------------------
class Match():
    def __init__(self, title):
        self.title = title
        self.series = []
        self.currentSerie = None
    
    def addSerie(self, serie):
        self.series.append(serie)

    #----------------------------------------------
    # Retourne le texte correspondant à l'action en cours
    #----------------------------------------------
    def getLoopText(self):
        if self.currentSerie is None:
            return "0/" + str(len(self.series))
        else:
            return str(self.series.index(self.currentSerie)+1) + "/" + str(len(self.series))

    #----------------------------------------------
    # Initialise la serie suivante comme la serie active
    #----------------------------------------------
    def setNextSerie(self):
        if self.currentSerie is None:
            self.currentSerie = self.series[0]
        else:
            pos = self.series.index(self.currentSerie)
            if pos < len(self.series)-1:
                pos = pos + 1
                self.currentSerie = self.series[pos]
            else:
                self.currentSerie = None
        
        if self.currentSerie is not None:
            self.currentSerie.reset()

    #----------------------------------------------
    # Initialise la serie suivante comme la serie active
    #----------------------------------------------
    def setPrevSerie(self):
        if self.currentSerie is None:
            self.currentSerie = self.series[0]
        else:
            pos = self.series.index(self.currentSerie)
            if pos > 0:
                pos = pos - 1
                self.currentSerie = self.series[pos]
            else:
                self.currentSerie = self.series[0]
        
        if self.currentSerie is not None:
            self.currentSerie.reset()

    #----------------------------------------------
    # Reset le match
    #----------------------------------------------
    def reset(self):
        self.currentSerie = None
        self.setNextSerie()
        