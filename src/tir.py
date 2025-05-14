import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel, QStackedLayout, QVBoxLayout, QTabWidget
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer,QDateTime

from target import Target
from remote import Remote
from serie import Serie
from sound import Sound
from config import Config

#----------------------------------------------
# Classe de la fenêtre principale d'affichage
#----------------------------------------------
class MainWindow(QMainWindow):
    #----------------------------------------------
    # Construteur de la classe
    #----------------------------------------------
    def __init__(self):
        super().__init__()
        # -----------------------------------------------
        # Configuration
        # -----------------------------------------------
        self.config = Config()

        self.pinRemote = 18
        self.pinTarget = 17

        self.match = None

        # -----------------------------------------------
        # init sound
        self.sound = Sound()

        # init Remote
        self.remote = Remote(self.remoteHandler, self.pinRemote)

        # init Target
        self.target = Target(self.pinTarget)

        # chargement des matches
        self.config.loadMatches(self.target, self.sound)

        # init fenêtre
        self.setWindowTitle("Tir")
        self.setWindowIcon(QtGui.QIcon('tir.png'))

        # count timer
        self.timer=QTimer()
        self.timer.timeout.connect(self.timerStep)

        self.stakedLayout = QStackedLayout()

        self.stakedLayout.addWidget(self.createMenuWidget())
        self.stakedLayout.addWidget(self.createRunWidget())

        self.stakedLayout.setCurrentIndex(0)        
        stackedPanel = QWidget()
        stackedPanel.setFixedHeight(480)
        stackedPanel.setFixedWidth(800)
        stackedPanel.setLayout(self.stakedLayout)
        self.setCentralWidget(stackedPanel)

    #----------------------------------------------
    # Creation de la page "menu"
    #----------------------------------------------
    def createMenuWidget(self):
        menuAllLayout = QGridLayout()
        menuAllLayout.setSpacing(20)

        menuTab = QTabWidget()
        tabStyle = "QTabBar { height: 50px; font-size:18pt;}"
        menuTab.setStyleSheet(tabStyle)

        for tab in self.getTabNames():
            menuTab.addTab(self.createTabPage(tab), tab)

        menuAllLayout.addWidget(menuTab, 0, 0, 4, 9)
        self.addImageButton(menuAllLayout, 0, "exit.png", lambda x: self.close())

        # Init panneau central de la fenêtre
        menuAllPanel = QWidget()
        menuAllPanel.setLayout(menuAllLayout)

        return menuAllPanel

    #----------------------------------------------
    # Retourne les noms des pages dans le menu
    #----------------------------------------------
    def getTabNames(self):
        tabs = []
        
        for group in self.config.groups:
            if not group.tab in tabs:
                tabs.append(group.tab)

        return tabs

    #----------------------------------------------
    # Creation d'une page dans le "menu"
    #----------------------------------------------
    def createTabPage(self, tab):
        menuPage = QWidget()
        pageLayout = QVBoxLayout()
        pageLayout.setSpacing(20)

        for group in self.config.groups:
            if tab == group.tab:
                pageLayout.addWidget(self.createGroupWidget(group))

        menuPage.setLayout(pageLayout)

        return menuPage

    #----------------------------------------------
    # Creation de la page "menu"
    #----------------------------------------------
    def createGroupWidget(self, group):
        groupLayout = QGridLayout()
        #groupLayout.setSpacing(20)

        groupLayout.addWidget(QLabel(group.title), 0, 0, 1, 10)

        position = 0
        for match in group.matches:
            m = match
            self.addMatchButton(groupLayout, position, match)
            position = position + 1
        
        # Init panneau central de la fenêtre
        groupWidget = QWidget()
        groupWidget.setLayout(groupLayout)

        return groupWidget

    #----------------------------------------------
    # Createion de la page run
    #----------------------------------------------
    def createRunWidget(self):
        # controls
        layout = QGridLayout()
        #layout.setSpacing(20)

        self.labelSerieTitle = QLabel("") 
        self.labelSerieTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSerieTitle.setStyleSheet("font: 35px; color: #000080; ")
        layout.addWidget(self.labelSerieTitle, 0, 0, 1, 10)

        self.labelMessage = QLabel("") 
        self.labelMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMessage.setStyleSheet("font: 80px; color: #3DDC84; ")
        layout.addWidget(self.labelMessage, 1, 0, 1, 10)

        self.labelSerie = QLabel("")
        self.labelSerie.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSerie.setStyleSheet("font: 100px; color: #00BFFF; background-color:black")
        layout.addWidget(self.labelSerie, 2, 0, 3, 4)

        self.labelCount = QLabel("")
        self.labelCount.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCount.setStyleSheet("font: 180px; color: #D70040; background-color:black")

        layout.addWidget(self.labelCount, 2, 4, 3, 6)
        
        self.buttonPlay = self.addImageButton(layout, 4, "play.png", lambda x: self.play())
        self.buttonStop = self.addImageButton(layout, 5, "stop.png", lambda x: self.stop())
        self.buttonReset = self.addImageButton(layout, 6, "reset.png", lambda x: self.reset())
        self.buttonEndAction = self.addImageButton(layout, 7, "eaction.png", lambda x: self.endAction())
        self.buttonPrev = self.addImageButton(layout, 8, "prev.png", lambda x: self.prev())
        self.buttonNext = self.addImageButton(layout, 9, "next.png", lambda x: self.next())

        #self.addSerieButton(layout, 4, "Standard\n150", lambda x: self.createSerie("Standard 150", 150))
        #self.addSerieButton(layout, 5, "Standard\n20", lambda x: self.createSerie("Standard 20", 20))
        #self.addSerieButton(layout, 6, "Standard\n10", lambda x: self.createSerie("Standard 10", 10))

        self.buttonTargetSwitch = self.addImageButton(layout, 2, "switch.png", lambda x: self.targetSwitch())
        self.addImageButton(layout, 0, "exit.png", lambda x: self.closeRun())

        self.setRunning(False)
        self.dispalyInfo()

        # Init panneau central de la fenêtre
        runPanel = QWidget()
        runPanel.setLayout(layout)

        return runPanel

    #----------------------------------------------
    # Ajoute un bouton de type "icon" 
    #----------------------------------------------
    def addImageButton(self, layout, position, image, connect):
        button = QPushButton("")
        button.setFixedHeight(75)
        button.setFixedWidth(75)
        button.setIcon(QtGui.QIcon(image))
        button.setIconSize(QtCore.QSize(50, 50))

        button.clicked.connect(connect)
        layout.addWidget(button, 5, position)
        return button

    #----------------------------------------------
    # Ajoute un bouton de type "texte" 
    #----------------------------------------------
    def addMatchButton(self, layout, position, match):
        button = QPushButton(match.title)
        button.setFixedHeight(70)
        button.setFixedWidth(220)

        button.setStyleSheet("font: 16px;")
        button.clicked.connect(lambda x: self.startMatch(match))
        layout.addWidget(button, 2, position)
        return button

    #----------------------------------------------
    # Affiche les informations en cours
    #----------------------------------------------
    def dispalyInfo(self):
        if self.match is not None and self.match.currentSerie is not None:
            self.labelSerieTitle.setText(self.match.currentSerie.title)
            self.labelSerie.setText(self.match.getLoopText())
            self.labelMessage.setText(self.match.currentSerie.getActionText())

            if self.match.currentSerie.action == 0:
                if self.match.currentSerie.duration > 60:
                    self.labelCount.setText("{}:{:02d}".format(self.match.currentSerie.duration // 60, self.match.currentSerie.duration % 60))
                else:
                    self.labelCount.setText("{}".format(self.match.currentSerie.duration))
            else:
                if self.match.currentSerie.counter > 60:
                    self.labelCount.setText("{}:{:02d}".format(self.match.currentSerie.counter // 60, self.match.currentSerie.counter % 60))
                else:
                    self.labelCount.setText("{}".format(self.match.currentSerie.counter))

            self.labelMessage.setStyleSheet("font: 80px; color: "+self.match.currentSerie.getActionColor())
            self.labelCount.setStyleSheet("font: 180px; background-color:black; color: "+self.match.currentSerie.getCounterColor())
        else:
            self.labelSerieTitle.setText("")
            self.labelSerie.setText("")
            self.labelMessage.setText("FIN MATCH")
            self.labelCount.setText("")
            self.labelMessage.setStyleSheet("font: 80px; color: #D70040")
            self.labelCount.setStyleSheet("font: 180px; background-color:black; color: #D70040")

    #----------------------------------------------
    # Fonction appelée toutes les secondes par le timer
    #----------------------------------------------
    def timerStep(self):
        self.match.currentSerie.step()
        if not self.match.currentSerie.inProgress:
            self.stop()

        if self.match.currentSerie.action >= 6:
            self.match.setNextSerie()

        self.dispalyInfo()
        

    #----------------------------------------------
    # Fonction appelée à l'appui d'une touche 
    # sur la télécommande
    #----------------------------------------------
    def remoteHandler(self, buttonCode):
            match buttonCode:
                case 1:
                    self.play()
                case 2:
                    self.stop()
                case 3:
                    self.prev()
                case 4:
                    if self.isRunning:
                        self.endAction()
                    else:    
                        self.next()

    #----------------------------------------------
    # set running status (on, off)
    #----------------------------------------------
    def setRunning(self, status):
        self.isRunning = status
        if status:
            self.buttonPlay.setEnabled(False)
            self.buttonStop.setEnabled(True)
            self.buttonReset.setEnabled(True)
            self.buttonEndAction.setEnabled(True)
            
            self.buttonTargetSwitch.setEnabled(False)
        else:
            self.buttonPlay.setEnabled(True)
            self.buttonStop.setEnabled(False)
            self.buttonReset.setEnabled(False)
            self.buttonEndAction.setEnabled(False)

            self.buttonTargetSwitch.setEnabled(True)
              

    #----------------------------------------------
    # Fermeture de la page run
    #----------------------------------------------
    def closeRun(self):
        self.stop()
        self.stakedLayout.setCurrentIndex(0)

    #----------------------------------------------
    # Démarrage de la série
    #----------------------------------------------
    def play(self):
        if not self.isRunning and self.match.currentSerie != None :
            if self.match.currentSerie.action >= 5:
                self.reset()

            self.setRunning(True)
            self.timer.start(1000)

    #----------------------------------------------
    # Fin de l'action en cours
    #----------------------------------------------
    def endAction(self):
        if self.isRunning and self.match.currentSerie != None :
            self.match.currentSerie.endAction()

    #----------------------------------------------
    # Arrêt de la série
    #----------------------------------------------
    def stop(self):
        if self.isRunning :
            self.setRunning(False)
            self.timer.stop()

    #----------------------------------------------
    # Réinitialise la série
    #----------------------------------------------
    def reset(self):
        if self.isRunning :
            self.setRunning(False)
            self.timer.stop()
            self.match.currentSerie.reset()
            self.dispalyInfo()

    #----------------------------------------------
    # Initialise la série précédente
    #----------------------------------------------
    def prev(self):
        self.stop()
        self.match.setPrevSerie()
        self.dispalyInfo()

    #----------------------------------------------
    # Initialise la série suivante
    #----------------------------------------------
    def next(self):
        self.stop()
        self.match.setNextSerie()
        self.dispalyInfo()

    #----------------------------------------------
    # Start match
    #----------------------------------------------
    def startMatch(self, match):
        self.match = match
        self.match.reset()
        self.dispalyInfo()
        self.stakedLayout.setCurrentIndex(1)

    #----------------------------------------------
    # Retourne manuellement la cible
    #----------------------------------------------
    def targetSwitch(self):
        self.target.switch()

#----------------------------------------------
# Main code
#----------------------------------------------
app = QApplication(sys.argv)

window = MainWindow()

window.showFullScreen()
#window.setFixedSize(800, 480)
window.show()

app.exec()
