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
int turn = 90;
bool neg = false;

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
  // Useful for debugging
  pinMode(LED_BUILTIN, OUTPUT);
  analogWrite(LED_BUILTIN, 0);
  Serial.begin(115200);
  // Actually useful stuff xD
  pinMode(motorPinRightDir, OUTPUT);
  pinMode(motorPinRightSpeed, OUTPUT);
  pinMode(motorPinLeftDir, OUTPUT);
  pinMode(motorPinLeftSpeed, OUTPUT);
  servo1.attach(servo1_pin);
  //Reset wheels before start
  servo1.write(turn);
}

void onConnectionEstablished(){
  client.subscribe("abbexpectmore@gmail.com/ctrl", [] (const String &payload)
  {
    //Parse incoming message and seperate useful information
    dir = payload.substring(payload.indexOf('(')+1,payload.indexOf(':')).toInt();
    spd = payload.substring(payload.indexOf(':')+1,payload.lastIndexOf(':')).toInt();
    turn = payload.substring(payload.lastIndexOf(':')+1).toInt();
    // If the turn is negative remeber this and make it an absolute value
    // This needs to be saved to later determine if right or left turn.
    //Calculate speed diff between inner and outer wheel
    float placeholder = -0.0082*turn+1;
    int spd1 = spd * placeholder;
    DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, dir, spd1);
    DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, dir, spd);
    servo1.write(turn);
    
  });
  //Make sure your actually here (Good way to know if lost connection issue is present)
  client.publish("abbexpectmore@gmail.com/light", "I'm online!");

  client.executeDelayed(5 * 1000, []() {
    //client.publish("joakim.flink@abbindustrigymnasium.se/lampa", "This is a message sent 5 seconds later");
  });
}
// Function to simplify code and avoid repeditiveness.
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
  //Loop through and catch imcoming messages
 client.loop();
}
