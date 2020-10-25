#include "EspMQTTClient.h"
#include "Servo.h"

Servo servo1;

#define defaulturl "lisa.engstrom@abbindustrigymnasium.se"
#define motorPinRightDir  0//D3
#define motorPinRightSpeed 5//D1
#define motorPinLeftDir 2
#define motorPinLeftSpeed 4
#define GPIO 12
#define PI 3.1415926535897932384626433832795

int dir = 0;
int spd = 0;

const float wheelCircumference = 3.5 * PI;
const int interval = 100; //Interval
const float exchange = 0.016666666667;

bool timer = false;
int last_time = 0;

float setpoint = 0; // Speed to reach
float currentVelocity = 0;
int velocityOut = 0;
float err = 0;
float dT = 0; // Delta time
float kp = 2; // constant proportional
float ki = 0; // constant integral
float kd = 0; //constant derive

int servo1_pin = 14;
int turn = 90;
int pulse = 0;

bool neg = false;

void onConnectionEstablished();

EspMQTTClient client(
/*  "ABB_Indgym_Guest",           // Wifi ssid
  "Welcome2abb",           // Wifi password*/
  "#Telia-53E8F8",
  "JAH@=-wauM231rnt", 
  "maqiatto.com",  // MQTT broker ip
  1883,             // MQTT broker port
  "lisa.engstrom@abbindustrigymnasium.se",            // MQTT username
  "driverbot",       // MQTT password
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
  client.subscribe("lisa.engstrom@abbindustrigymnasium.se/ctrl", [] (const String &payload)
  {
    //Parse incoming message and seperate useful information
    setpoint = payload.substring(payload.indexOf('(')+1,payload.indexOf(':')).toInt();
    kd = payload.substring(payload.indexOf(':')+1,payload.lastIndexOf(':')).toInt();
    ki = payload.substring(payload.lastIndexOf(':')+1).toInt();
    // kp = payload.substring(payload.indexOf('(')+1,payload.indexOf(':')).toInt();
    // setpoint = payload.substring(payload.indexOf(':')+1,payload.lastIndexOf(':')).toInt();
    // turn = payload.substring(payload.lastIndexOf(':')+1).toInt();
    /* If the turn is negative remeber this and make it an absolute value
    // This needs to be saved to later determine if right or left turn.
    //Calculate speed diff between inner and outer wheel
    float placeholder = -0.0082*turn+1;
    int spd1 = spd * placeholder;
    DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, dir, spd1);
    DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, dir, spd);
    servo1.write(turn); */
  });
  //Make sure your actually here (Good way to know if lost connection issue is present)
  client.publish("lisa.engstrom@abbindustrigymnasium.se/info", "I'm online!");
}
void DriveDirSpeed(int Dirpin, int Speedpin, int Direction, int Speed) {
  digitalWrite(Dirpin, Direction);
  analogWrite(Speedpin, Speed);
}
void loop() {
 client.loop();
 millis_check(last_time);
 if (timer == true) {
  currentVelocity = (pulse*exchange*wheelCircumference)/(dT/1000); // unit cm/s
  last_time = millis();
  err = setpoint - currentVelocity;
  //kp * err => Proportional
  velocityOut += err+(kd * err);
  String message = String(last_time)+", Current Velocity: "+String(currentVelocity)+", Pulses: "+String(pulse)+", Exchange: "+String(exchange)+", Wheel Circumference: "+String(wheelCircumference)+", dT: "+String(dT);
  String mes = String(last_time)+", Error: "+String(err)+", Velocity Out: "+String(velocityOut)+", Current Velocity: "+String(currentVelocity)+", Setpoint: "+String(setpoint)+", Pusles: "+String(pulse);
  pulse = 0;
  client.publish("abbexpectmore@gmail.com/light", message);
  client.publish("abbexpectmore@gmail.com/light", mes);
 }
 // Add speed diff for turning
 DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, dir, velocityOut);
 DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, dir, velocityOut);
}

ICACHE_RAM_ATTR void IntCallback() {
  pulse += 1;
}
bool millis_check(int last) {
  if ((millis() - last)>=interval) {
    dT = millis() - last;
    timer = true;
  } else {
    timer = false;
  }
}