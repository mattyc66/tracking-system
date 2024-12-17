#include <Arduino.h>
#include <TinyGPSPlus.h>
#include <PubSubClient.h>
#include "SoftwareSerial.h"
#include <WiFiClient.h>
#include <GyverOLED.h>
#include <WiFi.h>
#include <Wire.h>

GyverOLED<SSH1106_128x64> display;

const long Baudrate = 9600;
const char RX_Pin = 17;
const char TX_Pin = 16;


const char* Wifi_ID = "BT-H2CWHH";
const char* Wifi_pass = "U3K94X4PCrEkHN";
//const char* Wifi_ID = "xprmx15";
//const char* Wifi_pass = "password22";
const char* Broker = "broker.hivemq.com";

TinyGPSPlus GPS;
SoftwareSerial Port;

WiFiClient Wifi_Client;
PubSubClient MQTT(Wifi_Client);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup() 
{

  Serial.begin(115200);
  delay(10000);
  Port.begin(Baudrate, SWSERIAL_8N1, RX_Pin, TX_Pin);

  WiFi.begin(Wifi_ID, Wifi_pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  MQTT.setServer(Broker, 1883);
  MQTT.setCallback(callback);
  MQTT.connect("MC-GPS-Tracking-System");
  Serial.println("MQTT connected");

  display.init();
  display.clear();
  display.update();

}


void upload()
{
  Serial.println("setup is executing");
  if (GPS.location.isValid() && MQTT.connected())
  {
    String Latitude = String(GPS.location.lat(),6);
    String Longitude = String(GPS.location.lng(),6);
    String timestamp = String(millis());
    int Hour = GPS.time.hour();
    int Minute = GPS.time.minute();

    Serial.printf("Satellites: %i\n", GPS.satellites.value());
    Serial.println("GPS coordinates");
    Serial.println(Latitude);
    Serial.println(Longitude);

    MQTT.publish("MC-Project-Lat", Latitude.c_str());
    MQTT.publish("MC-Project-Lng", Longitude.c_str());
    MQTT.publish("MC-Project-Sat", String(GPS.satellites.value()).c_str());
    display.clear();

    display.setCursorXY(25, 5);
    display.print("Lat: ");
    display.setCursorXY(50, 5);
    display.print(GPS.location.lat(),6);

    display.setCursorXY(25, 20);
    display.print("Lng: ");
    display.setCursorXY(50, 20);
    display.print(GPS.location.lng(),6);

    display.setCursorXY(0, 50);
    display.print("Sat: ");
    display.setCursorXY(25, 50);
    display.print(GPS.satellites.value());   

    display.setCursorXY(70, 50); 
    display.printf("%02d : %02d", Hour, Minute);
    display.update();
  } 
  else 
  {
    Serial.println("Waiting for satellite lock");
    MQTT.publish("MC-Project-Sat", "Waiting for satellite lock");
    display.clear();
    display.setCursorXY(0, 20);
    display.print("waiting for sat lock");
    display.update();
  }

}

void reconnect ()
{
  while (!MQTT.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (MQTT.connect("MC-GPS-Tracking-System")) {
      Serial.println("MQTT connected");
      MQTT.subscribe("MC-Project-Lat");
      MQTT.subscribe("MC-Project-Lng");
      MQTT.subscribe("MC-Project-Sat");
    } else {
      Serial.print("MQTT connection failed, rc=");
      Serial.print(MQTT.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}



void loop()
{
  if (!MQTT.connected()) {
    //Serial.println("No broker connection");   
    reconnect();
  }

  MQTT.loop()
  
  while (Port.available() > 0)
  if (GPS.encode(Port.read()))
  upload();
}  



