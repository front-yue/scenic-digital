import { createRouter, createWebHistory } from 'vue-router'
import ScenicScreen from '../pages/ScenicScreen.vue'

const MobileScreen = () => import('../pages/MobileScreen.vue')
const AdminLayout = () => import('../pages/admin/AdminLayout.vue')
const ScenicInfo = () => import('../pages/admin/ScenicInfo.vue')
const SpotList = () => import('../pages/admin/SpotList.vue')
const ControlPanel = () => import('../pages/admin/ControlPanel.vue')

const routes = [
  {
    path: '/',
    name: 'ScenicScreen',
    component: ScenicScreen,
    beforeEnter: (to, from, next) => {
      // 自动检测屏幕宽度，移动端跳转到移动端页面
      if (typeof window !== 'undefined' && window.innerWidth < 1024) {
        next('/mobile')
      } else {
        next()
      }
    }
  },
  {
    path: '/mobile',
    name: 'MobileScreen',
    component: MobileScreen
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', redirect: '/admin/scenic' },
      { path: 'scenic', name: 'AdminScenic', component: ScenicInfo },
      { path: 'spots', name: 'AdminSpots', component: SpotList },
      { path: 'control', name: 'AdminControl', component: ControlPanel }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
