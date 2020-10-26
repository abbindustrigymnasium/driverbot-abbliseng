<template>
  <div class="row justify-center" style="margin-top: 10px">
    <div class="row col-12">
      <v-btn style="height: 60px; margin-left: 20px; margin-right: 10px" color="primary" @click="send()">Update</v-btn>
      <v-text-field label="Desired Speed" style="margin-right: 10px" v-model="dSpeed"></v-text-field>
      <v-text-field label="Proportional Constant" style="margin-right: 10px" v-model="kp"></v-text-field>
      <v-text-field label="Deriving Constant" style="margin-right: 10px" v-model="kd"></v-text-field>
      <v-text-field label="Intregral Constant" style="margin-right: 20px" v-model="ki"></v-text-field>
    </div>
    <apexchart
      class="col-12 trial"
      type="line"
      height="500"
      :options="chartOption"
      :series="serie"
    ></apexchart>
    <div class="row col-12">
      <!-- <v-btn style="height: 60px; margin-left: 20px; margin-right: 10px" color="primary" @click="send()">Update</v-btn> -->
      <v-slider max="60" min="-60" thumb-label="always" v-model="turn" style="margin-left: 20px ;margin-right: 20px" @change="turns()"></v-slider>
    </div>
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
    kp: "",
    lastValue: "",
    ph: [],
    turn: 0,
    series: [
      {
        name: "Desired speed",
        data: [],
      },
      {
        name: "Actual speed",
        data: [],
      },
      {
        name: "Velocity Out",
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
        categories: ["Error"],
        labels: {
          show: true
        }
      }
    },
  }),
  methods: {
    send() {
      if (this.dSpeed == ""){
        this.dSpeed = '0'
      }
      if (this.kd != ""){
        firebase
        .database()
        .ref('kd')
        .set(Number(this.kd))
      }
      if (this.ki != ""){
        firebase
        .database()
        .ref('ki')
        .set(Number(this.ki))
      }
      if (this.kp != ""){
        firebase
        .database()
        .ref('kp')
        .set(Number(this.kp))
      }
      let msg = String('('+this.dSpeed+':'+this.kd+':'+this.ki+','+this.kp+')');
      client.publish("lisa.engstrom@abbindustrigymnasium.se/set", msg);
    },
    turns(){
      client.publish("lisa.engstrom@abbindustrigymnasium.se/turn", ('('+String(this.turn)+')'));
    },
    data(newDataPoints) {
      this.series[0]["data"].push(newDataPoints[0])
      this.series[1]["data"].push(newDataPoints[1])
      this.series[2]["data"].push(newDataPoints[2])
      let x = this.chartOptions["xaxis"]["categories"]
      this.ph.push(newDataPoints[3])
      this.chartOptions = {...this.chartOptions, ...{
        xaxis: {
          categories: this.ph
        }
      }}
    },
  },
  watch: {
    display: function (value, oldValue) {
      if (value != ""){
        let formatted = value.replace('(','')
        formatted = formatted.replace(')','')
        const vars = formatted.split(',')
        this.data([Number(vars[0]),Number(vars[1]),Number(vars[2]),Number(vars[3])])
      }
    },
  },
  computed: {
    serie() {
      return this.series;
    },
    chartOption() {
      return this.chartOptions;
    }
  },
  created: function () {
    firebase.database().ref('kp').on("value", (snapshot)=>{
      this.kp = snapshot.val()
    })
    firebase.database().ref('ki').on("value", (snapshot)=>{
      this.ki = snapshot.val()
    })
    firebase.database().ref('kd').on("value", (snapshot)=>{
      this.kd = snapshot.val()
    })
    setInterval(() => {
      this.display = data;
    }, 1);
  },
};
</script>
