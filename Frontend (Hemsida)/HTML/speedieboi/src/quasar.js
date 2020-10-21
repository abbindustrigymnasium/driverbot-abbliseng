import Vue from 'vue'

import './styles/quasar.sass'
import iconSet from 'quasar/icon-set/mdi-v4.js'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/mdi-v4/mdi-v4.css'
import '@quasar/extras/eva-icons/eva-icons.css'
import { Quasar } from 'quasar'

Vue.use(Quasar, {
  config: {},
  plugins: {
  },
  iconSet: iconSet
 })