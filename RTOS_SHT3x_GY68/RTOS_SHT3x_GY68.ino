#include <Arduino_FreeRTOS.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include "SHTSensor.h"
#include <EasyScheduler.h>
#include <avr/wdt.h>
SHTSensor sht;

float PTH[3] = {0,0,0}; 

Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

char serialData;

void displaySensorDetails(void)
{
  sensor_t sensor;
  bmp.getSensor(&sensor);
}

void setup(void) 
{
  Wire.begin();
  Serial.begin(9600);
  Serial.setTimeout(50);
  sht.setAccuracy(SHTSensor::SHT_ACCURACY_MEDIUM);
  if(!bmp.begin())
  {
    Serial.print("Ooops, no BMP085 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  displaySensorDetails();
  if (sht.init()) {
      //Serial.print("init(): success\n");
  } else {
     //Serial.print("init(): failed\n");
  }
  xTaskCreate(SendPressure, "Pressure", 128, NULL, 1, NULL);
  xTaskCreate(SendTemp_Humidity, "Temp_Humidity", 128, NULL, 1, NULL);
  xTaskCreate(SEND, "SEND", 128, NULL, 1, NULL);
}
void SendPressure(){
  while(1){
    sensors_event_t event;
    bmp.getEvent(&event);
    PTH[0] = (event.pressure);
    //Serial.println(PTH[0]);
    vTaskDelay(1000/portTICK_PERIOD_MS);
  }
}

void SendTemp_Humidity(){
  while(1){
    if(sht.readSample()){
      PTH[1] = (sht.getTemperature());
      PTH[2] = (sht.getHumidity());
      //Serial.println(PTH[1]);
      //Serial.println(PTH[2]);
    }
    vTaskDelay(1000/portTICK_PERIOD_MS); 
  }
}

void SEND(){
  while(1){
  if(Serial.available() > 0){
    serialData = Serial.read();
  }
  if(serialData == 's'){
    if(PTH[0] == 0 and PTH[1] == 0 and PTH[2] == 0){
      serialData = "";
      continue;
    }
    else{
      Serial.println(PTH[0]);
      Serial.println(PTH[1]);
      Serial.println(PTH[2]);
      serialData = "";
    }
  }else if(serialData == 't'){
      Serial.println(PTH[0]);
      Serial.println(PTH[1]);
      Serial.println(PTH[2]);
      serialData = "";
  }
  } 
}
void loop(){}
