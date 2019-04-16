import Vue from 'vue'
import App from './App.vue'
import store from "./store";

Vue.config.productionTip = false

const TranslationPlugin = {
    install(Vue) {
        Vue.prototype.$t = function(name) {
            return this.$root.ts[name] || name;
        };
    }
}
Vue.use(TranslationPlugin);

new Vue({
    store,
    render: h => h(App),
    data: {
        ts: {}
    }
}).$mount('#app')
