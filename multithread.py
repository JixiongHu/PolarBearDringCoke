from PyQt5.QtCore    import QCoreApplication, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QLineEdit

from time import sleep as tmSleep

class Processor(QObject):
    sigCount = pyqtSignal(int)

    def __init__(self):
        QObject.__init__(self)
        self.Connected = True
        self.StreamRdy = False
        self.Count = 0
        self.Delay = 0
        
        print('From within Thread')

    def ProcessRunner(self):
        print('Starting Thread Process')
        while self.Connected:
            if self.StreamRdy:
                self.Count += 1
                self.sigCount.emit(self.Count)
                tmSleep(0.5)
            else:
                self.Delay -= 1
                self.sigCount.emit(self.Delay)
                tmSleep(0.5)
            QCoreApplication.processEvents()

    @pyqtSlot()
    def CountUp(self):
        print('..... Counting Up')
        self.StreamRdy = True

    @pyqtSlot()
    def CountDown(self):
        print('..... Counting Down')
        self.StreamRdy = False

    @pyqtSlot()
    def StopCount(self):
        print('..... Stopped Counting')
        self.Connected = False

    @pyqtSlot()
    def RestartCount(self):
        print('..... Restarted Counting')
        if not self.Connected:
            self.Connected = True
            self.ProcessRunner()
        self.Delay = 0
        self.Count = 0


class MainWindow(QWidget):
    sigCntUp  = pyqtSignal()
    sigCntDn  = pyqtSignal()
    sigStpCnt = pyqtSignal()
    sigRestrt = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Main Window')    
        self.setGeometry(150, 150, 200, 200)

        self.btnCntUp = QPushButton('Up')
        self.btnCntUp.clicked.connect(self.CountUp)

        self.btnCntDn = QPushButton('Down')
        self.btnCntDn.clicked.connect(self.CountDwn)

        self.btnStopCnt = QPushButton('Stop')
        self.btnStopCnt.clicked.connect(self.StopCnt)

        self.btnRestart = QPushButton('Restart')
        self.btnRestart.clicked.connect(self.RestrtCnt)

        self.btnTermnat = QPushButton('Quit')
        self.btnTermnat.clicked.connect(self.TerminateThread)
        
        self.lneOutput = QLineEdit()
        
        HBox = QHBoxLayout()
        HBox.addWidget(self.btnCntUp)
        HBox.addWidget(self.btnCntDn)
        HBox.addWidget(self.btnStopCnt)
        HBox.addWidget(self.btnRestart)
        HBox.addWidget(self.btnTermnat)
        HBox.addStretch(1)
        
        VBox = QVBoxLayout()
        VBox.addWidget(self.lneOutput)
        VBox.addLayout(HBox)
        
        self.setLayout(VBox)
        
        self.EstablishThread()

    def EstablishThread(self):
      # Create the Object from Class
        self.Prcssr = Processor()
      # Assign the Database Signals to Slots
        self.Prcssr.sigCount.connect(self.CountRecieve)
      # Assign Signals to the Database Slots
        self.sigCntUp.connect(self.Prcssr.CountUp)
        self.sigCntDn.connect(self.Prcssr.CountDown)
        self.sigStpCnt.connect(self.Prcssr.StopCount)
        self.sigRestrt.connect(self.Prcssr.RestartCount)

      # Create the Thread
        self.ThredHolder = QThread()
      # Move the Listener to the Thread
        self.Prcssr.moveToThread(self.ThredHolder)
      # Assign the Listener Starting Function to the Thread Call
        self.ThredHolder.started.connect(self.Prcssr.ProcessRunner)
      # Start the Thread which launches Listener.Connect( )
        self.ThredHolder.start()

    @pyqtSlot(int)
    def CountRecieve(self, Count):
        self.lneOutput.setText('Count : ' + str(Count))

    def CountUp(self):
        print('Count Up')
        self.sigCntUp.emit()

    def CountDwn(self):
        print('Count Down')
        self.sigCntDn.emit()

    def StopCnt(self):
        print('Stop Counting')
        self.sigStpCnt.emit()

    def RestrtCnt(self):
        print('Restart Counting')
        self.sigRestrt.emit()

    def TerminateThread(self):
        print('Close Thread')
        self.ThredHolder.quit()
        if not self.ThredHolder.isRunning():
            self.ThredHolder.wait()
            print('Thread Active ',self.ThredHolder.isRunning())
        else:
            print('Thread is still Active cannot Quit')
            QCoreApplication.processEvents()

if __name__ == '__main__':
    MainThred = QApplication([])

    MainApplication = MainWindow()
    MainApplication.show()

    MainThred.exec()
