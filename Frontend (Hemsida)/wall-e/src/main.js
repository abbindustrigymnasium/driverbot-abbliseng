import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import VueApexCharts from 'vue-apexcharts';
import firebase from 'firebase';

Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)

Vue.config.productionTip = false

const config = {
  apiKey: "AIzaSyDxVCoKjLTKoyn5LCpQU90ARJHnhfWA-vs",
  authDomain: "driverbotliseng.firebaseapp.com",
  databaseURL: "https://driverbotliseng.firebaseio.com",
  projectId: "driverbotliseng",
  storageBucket: "driverbotliseng.appspot.com",
  messagingSenderId: "78698869973",
  appId: "1:78698869973:web:a8a74a495b9672a6fd9e5c"
}
firebase.initializeApp(config)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
