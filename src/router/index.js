import { createRouter, createWebHistory } from 'vue-router'
import CyberBoard from '../components/CyberBoard.vue'
import IotPanel from '../views/IotPanel.vue'

const routes = [
  {
    path: '/',
    name: 'CyberBoard',
    component: CyberBoard
  },
  {
    path: '/iot',
    name: 'IotPanel',
    component: IotPanel
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
