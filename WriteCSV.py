import csv

class WriteCSVforData:
    def __init__(self):
        self.Pressure = 0
        self.Temperature = 0
        self.Humidity = 0
        self.Date = ''
        self.Time = ''
        self.DateforPlot = ''
    def WriteinCSVData(self):
        with open('CSVData.csv', 'a',newline='') as f:
            x = csv.writer(f)
            x.writerow([self.DateforPlot,self.Date,self.Time,self.Pressure,self.Temperature,self.Humidity])