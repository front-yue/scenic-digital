import { createRouter, createWebHistory } from 'vue-router'
import ScenicScreen from '../pages/ScenicScreen.vue'

const routes = [
  {
    path: '/',
    name: 'ScenicScreen',
    component: ScenicScreen
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
