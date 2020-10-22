#include "EspMQTTClient.h"
#include "Servo.h"

Servo servo1;

#define defaulturl "abbexpectmore@gmail.com"
#define motorPinRightDir  0//D3
#define motorPinRightSpeed 5//D1
#define motorPinLeftDir 2
#define motorPinLeftSpeed 4
#define GPIO 12
#define PI 3.1415926535897932384626433832795

int dir = 0;
int spd = 0;

bool timer = false;
float bor = 0;
float err = 0;
int velo = 0;
int last_time = 0;
int dT = 100;
float kp = 2;
float vel = 0;
float deck = 3.5 * PI;

int servo1_pin = 14;
int turn = 90;
int pulse = 0;

bool neg = false;

void onConnectionEstablished();

EspMQTTClient client(
  "ABB_Indgym_Guest",           // Wifi ssid
  "Welcome2abb",           // Wifi password
/*  "#Telia-53E8F8",
  "JAH@=-wauM231rnt", */
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
  // Motors
  pinMode(motorPinRightDir, OUTPUT);
  pinMode(motorPinRightSpeed, OUTPUT);
  pinMode(motorPinLeftDir, OUTPUT);
  pinMode(motorPinLeftSpeed, OUTPUT);
  servo1.attach(servo1_pin);
  //Reset wheels before start
  servo1.write(turn);
  pinMode(GPIO, INPUT);
  attachInterrupt(digitalPinToInterrupt(GPIO), IntCallback, RISING);
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
  digitalWrite(Dirpin, Direction);
  analogWrite(Speedpin, Speed);
}
void loop() {
  //Loop through and catch imcoming messages
 client.loop();
 millis_check(last_time);
 if (timer == true) {
  vel = pulse*(1/60)*deck* 1000 / dT;
  last_time = millis();
  err = bor - vel;
  velo += kp * err;
  String message = String(last_time)+", Error: "+String(err)+", Velo: "+String(velo)+", Vel: "+String(vel)+", Bor: "+String(bor)+", Pusles: "+String(pulse);
  pulse = 0;
  client.publish("abbexpectmore@gmail.com/light", message);
 }
 // Add speed diff for turning
 DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, dir, velo);
 DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, dir, velo);
}

ICACHE_RAM_ATTR void IntCallback() {
  pulse += 1;
}
bool millis_check(int last) {
  if ((millis() - last)>=dT) {
    timer = true;
  } else {
    timer = false;
  }
}
