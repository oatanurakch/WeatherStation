from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from GUI import Ui_MainWindow
from threading import Thread as th
import csv
import Send_s_t
import serial
from serial import Serial
import pyqtgraph as pg
import numpy as np
import time as tm
from datetime import datetime
 
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

#Obj to send to Uno
Send = Send_s_t.send_s()

#Create CSV for Write Data
with open('CSVData.csv', 'w',newline='') as f:
    x = csv.writer(f)
    x.writerow(['Date','DATE','TIME','PRESSURE(hPa)','Temperature(Celcius)','Humidity(%)'])

#GUI with QTimer
class Work(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)
        
        self.Datanowshow.setReadOnly(True)
        self.datacsv.setReadOnly(True)
        
        self.dl = 0
        self.ci = 0

        self.tmtx1 = QtCore.QTimer()
        self.tmtx1.timeout.connect(self.sendS)

        self.tmtx4 = QtCore.QTimer()
        self.tmtx4.timeout.connect(self.showst_ON)
    
        self.ST.clicked.connect(self.read_tick)
        self.SP.clicked.connect(self.stop_tick)
        self.readnow.clicked.connect(self.readdatanow)
        self.cleardata.clicked.connect(self.cleardatanow)

    #Read time to tick s to Uno nano
    def read_tick(self):
        self.dl = (float(self.t_tick.text()))*60000
        self.t_tick.setEnabled(False)
        self.tupdate = float(self.t_tick.text())
        self.tmtx4.setInterval(200)
        self.tmtx4.start()
      
        self.tmtx1.setInterval(self.dl)
        self.tmtx1.start()

        self.ST.setEnabled(False)
        self.SP.setEnabled(True)

    #Show time
    def Timeonline(self):
        while True:
            self.timex = datetime.now()
            self.datenow.setText(self.timex.strftime('%a, %b, %Y'))
            self.HOUR.display(self.timex.hour)
            self.Minute.display(self.timex.minute)
            self.Second.display(self.timex.second)
            tm.sleep(0.2)

    #Show status logger on
    def showst_ON(self):
        self.loggerset.setText("ON")
        if self.ci==0:
            self.loggerset.setStyleSheet("background-color: rgb(0, 255, 0);")
            self.ci=1
        elif self.ci==1:
            self.loggerset.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.ci=0

    #Read now
    def readdatanow(self):
        Send.send_t_to_uno()
        self.Datanowshow.append(tm.ctime() + '\nPressure:' + Send.PS1 + ' Tempereture: ' + Send.Temp1 + ' Humidity: ' + Send.Humid1)

    #Clear data
    def cleardatanow(self):
        self.Datanowshow.clear()

    #Show status logger off
    def showst_OFF(self):
        self.loggerset.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.loggerset.setText("OFF")

    #Read data to Write CSV
    def sendS(self):
        Send.send_s_to_uno()
        self.udplot()
        self.WriteDataOnGui()
        self.show_online()

    #show on texteditonline
    def show_online(self):
        self.datacsv.append('Date: ' + Send.Date + ' Time: ' + Send.Time + ' \nPressure: ' + str(Send.Pressure) + ' Tempereture: ' + str(Send.Temperature) + ' Humidity: ' + str(Send.Humidity))

    #Update plot Temp,Pressure,Humidity
    def udplot(self):
        self.x = np.append(self.x[1:],self.x[-1]+self.tupdate)
        self.y1 = np.append(self.y1[1:],(Send.Temperature))
        self.y2 = np.append(self.y2[1:],(Send.Pressure))
        self.y3 = np.append(self.y3[1:],(Send.Humidity))
        self.dataline1.setData(self.x,self.y1)
        self.dataline2.setData(self.x,self.y2)
        self.dataline3.setData(self.x,self.y3)

    #stop tick to uno
    def stop_tick(self):
        self.tmtx1.stop()
        self.tmtx4.stop()
        self.showst_OFF()
        self.ST.setEnabled(True)
        self.SP.setEnabled(False)
        self.t_tick.setEnabled(True)
        self.Temp.display(0)
        self.PS.display(0)
        self.Humi.display(0)

    #Show data on GUI
    def WriteDataOnGui(self):
        self.Temp.display(float(Send.Temperature))
        self.PS.display(float(Send.Pressure))
        self.Humi.display(float(Send.Humidity))

    #Graph Temp
    def gpsetting1(self):
        
        self.x = np.zeros(30)
        self.y1 = np.zeros(30)
        self.mygp_Temp = pg.PlotWidget(self.centralwidget)
        self.mygp_Temp.setGeometry(QtCore.QRect(415,510,400,340))
        self.mygp_Temp.setObjectName("Graph_Temp")
        self.mygp_Temp.setTitle('Temperature', color = (0,0,0), size = '15pt', bold = True)
        self.style1 = {'color' : (0,0,0), 'font-size' : '14px'}
        self.mygp_Temp.setLabel('bottom','Time(Min)', **self.style1)
        self.mygp_Temp.setLabel('left','Temp(\u25E6C)', **self.style1)
        self.mygp_Temp.showGrid(x=True,y=True)
        self.mygp_Temp.setBackground((0,255,157))
        self.mypen = pg.mkPen(color = (255,0,0), width = 2, style = QtCore.Qt.SolidLine)
        self.dataline1 = self.mygp_Temp.plot(pen = self.mypen)

    #Graph Pressure
    def gpsetting2(self):

        self.y2 = np.zeros(30)
        self.mygp_PS = pg.PlotWidget(self.centralwidget)
        self.mygp_PS.setGeometry(QtCore.QRect(5,510,400,340))
        self.mygp_PS.setObjectName("Graph_PS")
        self.mygp_PS.setTitle('Pressure', color = (0,0,0), size = '15pt', bold = True)
        self.mygp_PS.setLabel('bottom','Time(Min)', **self.style1)
        self.mygp_PS.setLabel('left','Pressure(hPa)', **self.style1)
        self.mygp_PS.showGrid(x=True,y=True)
        self.mygp_PS.setBackground((85,255,255))
        self.dataline2 = self.mygp_PS.plot(pen = self.mypen)

    #Graph Humidity
    def gpsetting3(self):

        self.y3 = np.zeros(30)
        self.mygp_HM = pg.PlotWidget(self.centralwidget)
        self.mygp_HM.setGeometry(QtCore.QRect(825,510,400,340))
        self.mygp_HM.setObjectName("Graph_HM")
        self.mygp_HM.setTitle('Humidity', color = (0,0,0), size = '15pt', bold = True)
        self.mygp_HM.setLabel('bottom','Time(Min)', **self.style1)
        self.mygp_HM.setLabel('left','Humidity(%)', **self.style1)
        self.mygp_HM.showGrid(x=True,y=True)
        self.mygp_HM.setBackground((255,248,149))
        self.dataline3 = self.mygp_HM.plot(pen = self.mypen)

#Object to superclass and setgraph
mywork = Work()
mywork.gpsetting1()
mywork.gpsetting2()
mywork.gpsetting3()

#Thread for showtime
class mythread(th):
    def __init__(self,func):
        th.__init__(self)
        self.func = func

    def run(self):
        if self.func == 1:
            mywork.Timeonline()
            
thr1 = mythread(1)
thr1.start()

MainWindow.show()
sys.exit(app.exec_())