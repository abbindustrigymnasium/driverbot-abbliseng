<template>
  <div class="row justify-center" style="margin-top: 10px;">
    <v-btn :disabled=connected @click="connect()" style="margin-right: 10px">Connect</v-btn>
    <v-btn :disabled=subscribed @click="subscribe()" style="margin-right: 10px">subscribe</v-btn>
    <v-text class="col-12">{{this.display}}</v-text>
  </div>
</template>

<script>
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
    topic1: 'abbexpectmore@gmail.com/ctrl',
    last_payload: false,
    subscribed: false,
    display: 'Nada',
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
      this.connected = true
    },
    send() {
      let msg = String(this.message)
      this.client.publish(this.topic1, msg);
      this.last_payload = msg
      this.message = !this.message
    },
    subscribe(){
      var test = ''
      this.client.subscribe(this.topic, function(err, granted){
        console.log("Hello")
      })
      this.client.on('message', function(topic, message){
        test = String.fromCharCode.apply(null, message)
        console.log(test)
      })
      this.subscribed = true
    },
  },
  mounted: function(){
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
      this.connected = true
    this.subscribe()
  }
}
</script>
