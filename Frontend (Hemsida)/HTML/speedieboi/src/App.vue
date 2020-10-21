<template>
  <div>
    <q-btn @click="connect()">Connect</q-btn>
  </div>
</template>

<script>
import mqtt from "paho-mqtt"

// let client = new mqtt.MQTT.Client("maqiatto.com", 1883, "Testieboi")
let client = mqtt

export default {
  name: 'LayoutDefault',

  components: {
  },

  data () {
    return {
      leftDrawerOpen: false
    }
  },
  methods: {
    connect() {
      client.connect({
        userName: "abbexpectmore@gmail.com",
        password: "hej",
      })
    },
  },
}
</script>

<style>
</style>
