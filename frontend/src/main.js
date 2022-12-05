import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import axios from 'axios'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import Apis from './services/api'

import {
  CanvasRenderer
} from 'echarts/renderers'
import {
  ScatterChart,
  LineChart
} from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  ScatterChart,
  LineChart,
  GridComponent,
  TooltipComponent
]);

Vue.component('v-chart', ECharts)

axios.defaults.baseURL = Apis.backendBaseUrl
Vue.prototype.$axios = axios

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
