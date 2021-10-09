import serial
from serial import Serial
import time
from datetime import datetime
import WriteCSV

ser = serial.Serial('com3',9600,timeout=1)

writeData = WriteCSV.WriteCSVforData()

class send_s():
    def __init__(self):
        self.Pressure = 0
        self.Temperature = 0
        self.Humidity = 0
        self.Date = ''
        self.Time = ''
        self.DateforPlot = ''
    def send_s_to_uno(self):
        ser.write('s'.encode())
        writeData.Pressure = ser.readline().decode()
        self.Pressure = writeData.Pressure[0:len(writeData.Pressure)-2]
        self.Pressure = float(writeData.Pressure)
        writeData.Pressure = self.Pressure
        writeData.Temperature = ser.readline().decode()
        writeData.Temperature = writeData.Temperature[0:len(writeData.Temperature)-2]
        self.Temperature = float(writeData.Temperature)
        writeData.Temperature = self.Temperature
        writeData.Humidity = ser.readline().decode()
        writeData.Humidity = writeData.Humidity[0:len(writeData.Humidity)-2]
        self.Humidity = float(writeData.Humidity)
        writeData.Humidity = self.Humidity
        self.Date = time.strftime("%d"+","+"%b"+","+"%Y")
        writeData.Date = self.Date
        self.Time = time.strftime("%H"+"."+"%M"+"."+"%S")
        writeData.Time = self.Time
        writeData.DateforPlot = time.strftime("%d"+","+"%m"+","+"%Y")
        writeData.WriteinCSVData()

    def send_t_to_uno(self):
        ser.write('t'.encode())
        self.PS1 = ser.readline().decode()
        self.PS1 = self.PS1[0:len(self.PS1)-2]
        self.Temp1 = ser.readline().decode()
        self.Temp1 = self.Temp1[0:len(self.Temp1)-2]
        self.Humid1 = ser.readline().decode()
        self.Humid1 = self.Humid1[0:len(self.Humid1)-2]