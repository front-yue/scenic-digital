import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import VueAMap, { initAMapApiLoader } from '@vuemap/vue-amap'
import '@vuemap/vue-amap/dist/style.css'

// 初始化高德地图 API
initAMapApiLoader({
  key: import.meta.env.VITE_AMAP_KEY, 
  securityJsCode: import.meta.env.VITE_AMAP_SECURITY_CODE, 
  plugins: ['AMap.Walking', 'AMap.Driving', 'AMap.Transfer'],
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(VueAMap)
app.mount('#app')
