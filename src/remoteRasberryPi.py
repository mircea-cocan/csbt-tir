from rpi_rf import RFDevice
from PyQt5.QtCore import QTimer

#----------------------------------------------
# Class pour la gestion de la télécommande
#----------------------------------------------
class Remote():
    def __init__(self, remoteHandler, pin):
        # remote rx device
        self.remoteHandler = remoteHandler
        self.remote_rx_rfdevice = RFDevice(pin)
        self.remote_rx_rfdevice.enable_rx()
        self.remote_rx_timestamp = None

        self.remote_rx_timer=QTimer()
        self.remote_rx_timer.timeout.connect(self.remoteRxReceive)
        self.remote_rx_timer.start(10)

    #----------------------------------------------
    # Fonction appelée toutes les 10 millisecondes 
    # pour vérifier la réception d'un ordre à partir 
    # de la télécommande
    #----------------------------------------------
    def remoteRxReceive(self):
        if self.remote_rx_rfdevice.rx_code_timestamp != self.remote_rx_timestamp:
            self.remote_rx_timestamp = self.remote_rx_rfdevice.rx_code_timestamp
            match self.remote_rx_rfdevice.rx_code:
                case 2386725632:
                    self.remoteHandler(1)
                case 2168621824:
                    self.remoteHandler(2)
                case 2789378816:
                    self.remoteHandler(3)
                case 2923596544:
                    self.remoteHandler(4)
