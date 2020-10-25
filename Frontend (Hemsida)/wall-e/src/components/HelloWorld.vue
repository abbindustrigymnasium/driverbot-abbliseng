<template>
  <div class="row justify-center" style="margin-top: 10px">
    <div class="row col-12">
      <v-btn style="height: 60px; margin-left: 20px; margin-right: 10px" color="primary" @click="send()">Update</v-btn>
      <v-text-field label="Desired Speed" style="margin-right: 10px" v-model="dSpeed"></v-text-field>
      <v-text-field label="Deriving Constant" style="margin-right: 10px" v-model="kd"></v-text-field>
      <v-text-field label="Intregral Constant" style="margin-right: 20px" v-model="ki"></v-text-field>
    </div>
    <apexchart
      class="col-12 trial"
      type="line"
      height="500"
      :options="chartOptions"
      :series="serie"
    ></apexchart>
  </div>
</template>

<script>
import firebase from "firebase";

var mqtt = require("mqtt"),
  /* eslint-disable no-unused-vars */
  url = require("url");

var client = mqtt.connect("mqtt://maqiatto.com", {
  port: 8883,
  clientId: "VueSite10923",
  username: "lisa.engstrom@abbindustrigymnasium.se",
  password: "driverbot",
});
var data = "";

client.on("connect", function () {
  client.unsubscribe("lisa.engstrom@abbindustrigymnasium.se/ctrl")
  client.subscribe("lisa.engstrom@abbindustrigymnasium.se/ctrl", function (
    error
  ) {
    if (!error) {
      client.publish(
        "lisa.engstrom@abbindustrigymnasium.se/info",
        "Website Connected!"
      );
    }
  });
});
client.on("message", function (topic, message) {
  data = message.toString();
});

export default {
  name: "HelloWorld",
  data: () => ({
    display: "",
    dSpeed: "",
    kd: "",
    ki: "",
    series: [
      {
        name: "Desired speed",
        data: [],
      },
      {
        name: "Actual speed",
        data: [],
      },
    ],
    chartOptions: {
      chart: {
        height: 350,
        type: "line",
        zoom: {
          enabled: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "smooth",
      },
      title: {
        text: "Driverbot Speeds",
        align: "center",
      },
      grid: {
        row: {
          colors: ["#f3f3f3", "transparent"], // takes an array which will be repeated on columns
          opacity: 0.5,
        },
      },
      xaxis: {
        labels: {
          show: false
        }
      }
    },
  }),
  methods: {
    send() {
      if (this.dSpeed == ""){
        this.dSpeed = '0'
      }
      if (this.kd == ""){
        this.kd = '0'
      }
      if (this.ki == ""){
        this.ki = '0'
      }
      firebase
        .database()
        .ref('kd')
        .set(Number(this.kd))
      firebase
        .database()
        .ref('ki')
        .set(Number(this.ki))
      let msg = String('('+this.dSpeed+':'+this.kd+':'+this.ki+')');
      client.publish("lisa.engstrom@abbindustrigymnasium.se/info", msg);
    },
    data(newDataPoints) {
      let x = []
      this.series.forEach(line => {
        x.push({name: line["name"], data: []})
        line["data"].forEach(element => {
          x[x.length-1]["data"].push(element)
        });
      });
      x[0]["data"].push(newDataPoints[0])
      x[1]["data"].push(newDataPoints[1])
      this.series = x
    },
  },
  watch: {
    display: function (value, oldValue) {
      if (value != ""){
        let formatted = value.replace('(','')
        formatted = formatted.replace(')','')
        const vars = formatted.split(',')
        console.log(Number(vars[0]))
        console.log(Number(vars[1]))
        this.data([Number(vars[0]),Number(vars[1])])
      }
    },
  },
  computed: {
    serie() {
      return this.series;
    },
  },
  created: function () {
    setInterval(() => {
      this.display = data;
    }, 1);
  },
  beforeDestroyed: function () {
    client.end();
  },
};
</script>
