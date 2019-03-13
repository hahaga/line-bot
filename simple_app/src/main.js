import Vue from 'vue'       //vue library
import App from './App.vue' //app component

Vue.config.productionTip = false

new Vue({
  render: f => f(App),
}).$mount('#app') // mount our application to the element with id of 'app'
