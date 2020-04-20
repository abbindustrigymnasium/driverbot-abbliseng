import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    health: 100,
    popularity: 50,
    influence: 25
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  }
})

export default store