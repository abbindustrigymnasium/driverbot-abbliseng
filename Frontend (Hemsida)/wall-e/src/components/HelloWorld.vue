<template>
  <div>
    <v-btn :disabled=connected @click="connect()">Connect</v-btn>
    <v-btn @click="subscribe()">subscribe</v-btn>
    <v-btn @click="send()">Send</v-btn>
  </div>
</template>

<script>
// import mqtt from "mqtt"
var mqtt = require("mqtt"),
  /* eslint-disable no-unused-vars */
  url = require("url")

export default {
  name: 'HelloWorld',
  data: () => ({
    connected: false,
    client: undefined,
    user: "abbexpectmore@gmail.com",
    pass: "hej",
    message: true,
    once: false,
    topic: 'abbexpectmore@gmail.com/light',
    last_payload: false
  }),
  methods: {
    connect() {
      var mqtt_url = "maqiatto.com"
      var url = "mqtt://"+mqtt_url;
      var options = {
        port: 8883,
        clientId: "mqttjs_"+Math.random().toString(16).substr(2,8),
        username: this.user,
        password: this.pass
      }
      console.log("Connecting")
      this.client = mqtt.connect(url, options)
      console.log("Connected?")
      this.client
        .on("error", function(){
          console.log("no")
          this.connected = false
        })
        .on("close", function(){
          console.log("no")
          this.connected = false
        })
    },
    publish() {
      // this.$mqtt.publish('VueMqtt/publish', "Hello World")
    },
    send() {
      let msg = String(this.message)
      this.client.publish(this.topic, msg);
      this.last_payload = msg
      this.message = !this.message
    },
    subscribe(){
      this.client.subscribe(this.topic, function(err, granted){
        console.log(granted)
      })
    },
  },
  // mqtt: {
  //   'VueMqtt/publish' (data, topic) {
  //     console.log(topic+': '+String.fromCharCode.apply(null, data));
  //   }
  // }
}
</script>
