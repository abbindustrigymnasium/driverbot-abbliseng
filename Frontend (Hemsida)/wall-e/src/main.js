import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
// import VueMqtt from 'vue-mqtt'

// Vue.use(VueMqtt, "maqiatto.com",
//   {clientId: 'WebClient-' + parseInt(Math.random() * 100000),
//   username: "abbexpectmore@gmail.com",
//   password: "hej",
//   port: 1883,
// })

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
