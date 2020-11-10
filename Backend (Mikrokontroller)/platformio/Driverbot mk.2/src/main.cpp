#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "Servo.h"
#include <DNSServer.h>
#include <PubSubClient.h>
#include "WiFiManager.h"

const char *mqtt_server = "maqiatto.com";
const char *topic = "lisa.engstrom@abbindustrigymnasium.se/info";
const char *user = "lisa.engstrom@abbindustrigymnasium.se";
const char *pass = "driverbot";

WiFiClient espClient;
PubSubClient client(espClient);
Servo servo1;

void reconnect()
{
  // Loop until we're reconnected
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), user, pass))
    {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish(topic, "hello world");
      // ... and resubscribe
      client.subscribe(topic);
      // client.subscribe(topic2);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char *topic, byte *payload, unsigned int length)
{
  String topicStr;
  String payloadStr;
}
void setup() {
  Serial.begin(115200);
  WiFiManager wifiManager;
  if (!wifiManager.autoConnect("imtired", "testo123")) // wifiManager saker
  {
    Serial.println("failed to connect, we should reset as see if it connects");
    delay(3000);
    ESP.reset();
    delay(5000);
  }
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback); // kopplar till server
}

void loop() {
  if (!client.connected()) // altid upkopplad
  {
    reconnect();
  }
  client.loop();
}
