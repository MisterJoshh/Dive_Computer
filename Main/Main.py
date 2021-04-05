import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer,QDateTime
from ms5803py import MS5803
from db import Database



#***************Welcome screen Class***********************
class Welcome(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("UI/Dive2.ui",self)
        self.Button_enter.clicked.connect(self.gotohome)

    def gotohome(self):
        home=HomeScreen()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)



#***************Home screen class**************************
class HomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('UI/homescreen.ui',self)
        self.divebutton.clicked.connect(self.divefunction)
        self.log_button.clicked.connect(self.gotoLog)

    def gotoLog(self):
        log=Logbook()
        widget.addWidget(log)
        widget.setCurrentIndex(widget.currentIndex()+2)


    def divefunction(self):
        dive=Divescreen()
        widget.addWidget(dive)
        widget.setCurrentIndex(widget.currentIndex()+1)



#*************Dive Screen class****************************
class Divescreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('UI/divescreen.ui',self)
        self.sens = MS5803()
        self.atmos = float(self.sens.read()[0])
        self.dive_list = []
        self.dt, self.dtm, self.dth = 0,0,0
        self.press = 0
        self.seconds = 0
        self.flag1,self.flag2,self.flag3= False,False,False
        self.dive_time.setText('00:00:00')
        self.dive_depth.setText('0')
        self.start_button.clicked.connect(self.start) #method
        self.end_button.clicked.connect(self.end)
        self.back_button.clicked.connect(self.backtoHome)
        self.db = Database('dive_log.db')
        self.dive_number = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.timeout.connect(self.showDepth)
        self.timer.timeout.connect(self.showTemp)
        self.timer.timeout.connect(self.rec)
        self.timer.start(1000)


    def showTime(self):
        if self.flag1:
            if self.dt==59 and not self.dtm==59:
                self.dt=0
                self.dtm+=1
                self.seconds+=1
            elif self.dtm==59 and self.dt==59:
                self.dtm=0
                self.dt=0
                self.dth+=1
                self.seconds+=1
            else:
                self.dt+=1
                self.seconds+=1
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

    def rec(self):
        if self.flag3:
            self.dive_list.append((self.dive_number,
            int(round((self.sens.read()[0]-self.atmos)/1000,0)),
            self.seconds,
            int(round(self.sens.read()[1],0))))

            
    
    def end(self):
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.dth,self.dtm,self.dt=0,0,0
        self.db.insert(self.dive_list)
        self.dive_list=[]
        self.seconds=0


    def start(self):
        self.flag1 = True
        self.flag2 = True
        self.flag3 = True
        self.dive_number = self.db.diveNum()
        print(self.dive_number)
    
    def backtoHome(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

class Logbook(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('UI/logbook.ui',self)
        self.db = Database('dive_log.db')
        self.list_dives.addItems(self.db.popLog())
        self.back_button.clicked.connect(self.backtoMain)

    def backtoMain(self):
        widget.setCurrentIndex(widget.currentIndex()-2)
        

        
    




app=QApplication(sys.argv)
welcomewindow=Welcome()
widget=QtWidgets.QStackedWidget()
widget.addWidget(welcomewindow)
widget.setFixedWidth(680)
widget.setFixedHeight(320)
widget.show()
app.exec_()

