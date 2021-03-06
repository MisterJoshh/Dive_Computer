import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer,QDateTime
from ms5803py import MS5803



#***************Welcome screen Class***********************
class Welcome(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Dive2.ui",self)
        self.Button_enter.clicked.connect(self.gotohome)

    def gotohome(self):
        home=HomeScreen()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)



#***************Home screen class**************************
class HomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('homescreen.ui',self)
        self.divebutton.clicked.connect(self.divefunction)


    def divefunction(self):
        dive=Divescreen()
        widget.addWidget(dive)
        widget.setCurrentIndex(widget.currentIndex()+1)



#*************Dive Screen class****************************
class Divescreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('divescreen.ui',self)
        self.sens = MS5803()
        self.atmos = float(self.sens.read()[0])
        self.dt, self.dtm, self.dth = 0,0,0
        self.press = 0
        self.flag1,self.flag2,= False,False
        self.dive_time.setText('00:00:00')
        self.dive_depth.setText('0')
        self.start_button.clicked.connect(self.Start) #method
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.timeout.connect(self.showDepth)
        self.timer.timeout.connect(self.showTemp)
        self.timer.start(1000)


    def showTime(self):
        if self.flag1:
            if self.dt==59 and not self.dtm==59:
                self.dt=0
                self.dtm+=1
            elif self.dtm==59 and self.dt==59:
                self.dtm=0
                self.dt=0
                self.dth+=1
            else:
                self.dt+=1
        if self.dt>9 and self.dtm>9:
            text = f'0{self.dth}:{self.dtm}:{self.dt}'
        elif self.dt>9 and not self.dtm>9:
            text = f'0{self.dth}:0{self.dtm}:{self.dt}'
        elif not self.dt>9 and self.dtm>9:
            text = f'0{self.dth}:{self.dtm}:0{self.dt}'
        else:
            text = f'0{self.dth}:0{self.dtm}:0{self.dt}'
        self.dive_time.setText(text)


    def showDepth(self):
        if self.flag2:
            text2 = int(round((self.sens.read()[0]-self.atmos)/1000,0))
        else:
            text2 = 0
        self.dive_depth.setText(f'{text2}')

    def showTemp(self):
        text3 = int(round(self.sens.read()[1],0))
        self.dive_temp.setText(f'{text3}')

    def Start(self):
        self.flag1 = True
        self.flag2 = True



app=QApplication(sys.argv)
welcomewindow=Welcome()
widget=QtWidgets.QStackedWidget()
widget.addWidget(welcomewindow)
widget.setFixedWidth(680)
widget.setFixedHeight(320)
widget.show()
app.exec_()


#testing file
