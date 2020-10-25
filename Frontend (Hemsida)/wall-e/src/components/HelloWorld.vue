<template>
  <div class="row justify-center" style="margin-top: 10px;">
    <v-btn @click="send()" style="margin-right: 10px">Send</v-btn>
    <h1 class="col-12">{{display}}</h1>
  </div>
</template>

<script>
var mqtt = require("mqtt"),
  /* eslint-disable no-unused-vars */
  url = require("url")
var client = mqtt.connect('mqtt://maqiatto.com',{port: 8883, clientId: 'VueSite10923', username: "lisa.engstrom@abbindustrigymnasium.se", password: 'driverbot'})
var data = "No recieved messages"

client.on('connect', function () {
  client.subscribe('lisa.engstrom@abbindustrigymnasium.se/info', function (error) {
    if (!error){
      client.publish('lisa.engstrom@abbindustrigymnasium.se/info', 'Hello MQTT')
    }
  })
})
client.on('message', function(topic, message) {
  data = message.toString()
})

export default {
  name: 'HelloWorld',
  data: () => ({
    display: data,
  }),
  methods: {
    send() {
      let msg = String("Hello")
      client.publish('lisa.engstrom@abbindustrigymnasium.se/info', msg);
    },
  },
  watch: {
    display: function(value, oldValue) {
      // console.log(oldValue)
    }
  },
  created: function(){
    setInterval(() => {
      this.display = data
    }, 1);
  }
}
</script>
