#include "EspMQTTClient.h"
#include "FirebaseESP8266.h"
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
const int interval = 1000; //Interval
// const float exchange = 0.01666666666666666666666666666667; // 1/60
const float exchange = 0.00833333333333333333333333333333;

bool timer = false;
int last_time = 0;
int last_setpoint = 0;

float setpoint = 0; // Speed to reach
float currentVelocity = 0;
float velocityOut = 0;
float err = 0;
float dT = 0; // Delta time
float kp = 2; // constant proportional
float ki = 0; // constant integral
float kd = 1; //constant derive
float last_error = 0;
float sumError = 0;

int servo1_pin = 14;
int turn = 90;
int pulse = 0;

bool neg = false;

// EspMQTTClient client(
//   "#Telia-53E8F8",
//   "JAH@=-wauM231rnt",
//   "maqiatto.com",
//   // 1883,
//   "lisa.engstrom@abbindustrigymnasium.se"
// )

void onConnectionEstablished();
EspMQTTClient client(
/*  "ABB_Indgym_Guest",           // Wifi ssid
  "Welcome2abb",           // Wifi password*/
  "#Telia-53E8F8",
  "JAH@=-wauM231rnt", 
  "maqiatto.com",  // MQTT broker ip
  "lisa.engstrom@abbindustrigymnasium.se",            // MQTT username
  "driverbot",       // MQTT password
  "Node",          // Client name
  1883
);

ICACHE_RAM_ATTR void IntCallback() {
  pulse += 1;
}

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
  client.subscribe("lisa.engstrom@abbindustrigymnasium.se/set", [] (const String &payload)
  {
    //Parse incoming message and seperate useful information
    setpoint = payload.substring(payload.indexOf('(')+1,payload.indexOf(':')).toInt();
    kd = payload.substring(payload.indexOf(':')+1,payload.lastIndexOf(':')).toFloat();
    ki = payload.substring(payload.lastIndexOf(':')+1,payload.lastIndexOf(',')).toFloat();
    kp = payload.substring(payload.lastIndexOf(',')+1).toFloat();
    client.publish("lisa.engstrom@abbindustrigymnasium.se/info", (String(kd)+':'+String(ki)+':'+String(kp)));
    // velocityOut = setpoint*10;
    // if (setpoint<last_setpoint){
    //   velocityOut = 5*setpoint;
    //   last_setpoint = setpoint;
    // }

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
  client.subscribe("lisa.engstrom@abbindustrigymnasium.se/turn", [] (const String &payload){
    turn = payload.substring(payload.indexOf('(')+1,payload.indexOf(')')).toInt(); //140 - 30
    turn = map(turn,-60,60,30,140);
    servo1.write(turn);
  });
  //Make sure your actually here (Good way to know if lost connection issue is present)
  client.publish("lisa.engstrom@abbindustrigymnasium.se/info", "I'm online!");
}
void DriveDirSpeed(int Dirpin, int Speedpin, int Direction, int Speed) {
  digitalWrite(Dirpin, Direction);
  analogWrite(Speedpin, Speed);
}

void millis_check(int last) {
  if ((millis() - last)>=interval) {
    dT = millis() - last;
    timer = true;
  } else {
    timer = false;
  }
}

void loop() {
 client.loop();
 millis_check(last_time);
 if (timer == true) {
    dT = dT/1000;
    currentVelocity = (pulse*exchange*wheelCircumference)/dT; // unit cm/s
    last_time = millis();
    err = setpoint - currentVelocity;
    if (setpoint < 1){
      velocityOut = 0;
    }else{
      sumError += err*dT;
      velocityOut = (currentVelocity*5)+(err*kp)+(ki*sumError)+(kd*((err-last_error)/dT));
      // if (velocityOut>max_vOut){
      //   max_vOut = velocityOut;
      // }
      // velocityOut = map(velocityOut,0,3000,0,1023);
    }
    // if (velocityOut > 1020){
    //   velocityOut = 1023;
    // }
    last_error = err;

    String message = "("+String(setpoint)+','+String(currentVelocity)+','+String(velocityOut/10)+','+String(last_time/1000)+')';
    pulse = 0;
    client.publish("lisa.engstrom@abbindustrigymnasium.se/ctrl", message);
  // client.publish("lisa.engstrom@abbindustrigymnasium.se/info", mes);
 }
 // Add speed diff for turning
 DriveDirSpeed(motorPinRightDir, motorPinRightSpeed, dir, int(velocityOut));
 DriveDirSpeed(motorPinLeftDir, motorPinLeftSpeed, dir, int(velocityOut));
}
