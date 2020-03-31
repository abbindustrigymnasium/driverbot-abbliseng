#include "EspMQTTClient.h"
#include "Servo.h"
Servo servo1;
#define defaulturl "abbexpectmore@gmail.com"
#define motorPinRightDir  0//D3
#define motorPinRightSpeed 5//D1
#define motorPinLeftDir 2
#define motorPinLeftSpeed 4

int dir = 0;
int spd = 0;

int servo1_pin = 14;
int initial_position = 90;

void onConnectionEstablished();

EspMQTTClient client(
/* "ABB_Indgym_Guest",           // Wifi ssid
  "Welcome2abb",           // Wifi password */
  "#Telia-53E8F8",
  "JAH@=-wauM231rnt",
  "maqiatto.com",  // MQTT broker ip
  1883,             // MQTT broker port
  "abbexpectmore@gmail.com",            // MQTT username
  "hej",       // MQTT password
  "Node",          // Client name
  onConnectionEstablished, // Connection established callback
  true,             // Enable web updater
  true              // Enable debug messages
);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  analogWrite(LED_BUILTIN, 0);
  Serial.begin(115200);
  pinMode(motorPinRightDir, OUTPUT);
  pinMode(motorPinRightSpeed, OUTPUT);
  pinMode(motorPinLeftDir, OUTPUT);
  pinMode(motorPinLeftSpeed, OUTPUT);
  servo1.attach(servo1_pin);
  servo1.write(initial_position);
  startSeq();
}

void onConnectionEstablished(){
  client.subscribe("abbexpectmore@gmail.com/light", [] (const String &payload)
  {
    //Serial.println(payload);
    if (payload == "on"){
      Serial.println("on: " + payload);
      digitalWrite(motorPinRightDir, 1);
      analogWrite(motorPinRightSpeed, 1024);
    } else if (payload == "off"){
      digitalWrite(motorPinRightDir, 1);
      analogWrite(motorPinRightSpeed, 0);
    }
    else if(payload == "I'm online!"){
      Serial.println("Nah fam");
    }
    else {
      Serial.println(payload);
      int a = payload.toInt();
      servo1.write(a);
      delay(15);
    }
    
  });
  client.subscribe("abbexpectmore@gmail.com/ctrl", [] (const String &payload1)
  {
    dir = payload1.substring(payload1.indexOf('(')+1,payload1.lastIndexOf(':')).toInt();
    spd = payload1.substring(payload1.lastIndexOf(':')+1).toInt();
    spd = map(spd, 0, 100, 0, 1024);
    DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, dir, spd);
  });
  
  client.publish("abbexpectmore@gmail.com/light", "I'm online!");

  client.executeDelayed(5 * 1000, []() {
    //client.publish("joakim.flink@abbindustrigymnasium.se/lampa", "This is a message sent 5 seconds later");
  });
}
void Drivetest3(int Dirpin, int Speedpin) {
  int Direction = 0;
  while (Direction <= 1)
  {
    int Speed = 0;
    while (Speed < 1020)
    {
      Speed += 100;
      DriveDirSpeed(Dirpin, Speedpin, Direction, Speed);
      delay(2200);
    }
    Direction++;
  }

}
void DriveDirSpeed(int Dirpin, int Speedpin, int Direction, int Speed) {
  if (Direction == 1)
    Serial.println("Framåt");
  else
    Serial.println("Bakåt");
  Serial.println("Hastighet: " + String(Speed));
  digitalWrite(Dirpin, Direction);
  analogWrite(Speedpin, Speed);
}
void loop() {
  // put your main code here, to run repeatedly:
 client.loop();
}

void startSeq(){
  delay(5000);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 1, 1024);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 1, 1024);
  delay(1000);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 0, 1024);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 0, 1024);
  delay(1000);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 1, 0);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 1, 0);
  delay(100);
  servo1.write(90);
  delay(1000);
  servo1.write(45);
  delay(1000);
  servo1.write(135);
  delay(1000);
  servo1.write(90);
  delay(1000);

  servo1.write(135);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 1, 1024);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 1, 1024);
  delay(10000);
  servo1.write(135);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 0, 1024);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 0, 1024);
  delay(10000);
  servo1.write(45);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 1, 1024);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 1, 1024);
  delay(10000);
  servo1.write(45);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 0, 1024);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 0, 1024);
  delay(10000);
  servo1.write(90);
  DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, 0, 0);
  DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, 0, 0);
}
