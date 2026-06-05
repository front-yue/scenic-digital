import { defineStore } from 'pinia'
import { getScenicInfo, getScenicSpots } from '../api/scenic'

export const useScenicStore = defineStore('scenic', {
  state: () => ({
    scenicInfo: {},
    spotList: [],
    loadingInfo: false,
    loadingSpots: false,
    isInteractMode: false // 控制是否进入 AI 照相馆沉浸模式
  }),
  getters: {},
  actions: {
    async fetchScenicInfo() {
      this.loadingInfo = true
      try {
        const res = await getScenicInfo()
        if (res && res.status === 'success') {
          this.scenicInfo = res.data || {}
        }
      } catch (error) {
        console.error('获取景区信息失败:', error)
      } finally {
        this.loadingInfo = false
      }
    },
    async fetchSpotList() {
      this.loadingSpots = true
      try {
        const res = await getScenicSpots()
        if (res && res.status === 'success') {
          this.spotList = res.data || []
        }
      } catch (error) {
        console.error('获取景点列表失败:', error)
      } finally {
        this.loadingSpots = false
      }
    },
    async refreshAllData() {
      await Promise.all([this.fetchScenicInfo(), this.fetchSpotList()])
    }
  }
})
