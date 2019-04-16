import Vue from 'vue'
import Vuex from 'vuex'
import meeting from './modules/meeting'
import projector from './modules/projector'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    meeting,
    projector
  },
  strict: debug
});
