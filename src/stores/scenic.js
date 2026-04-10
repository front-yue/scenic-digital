import { defineStore } from 'pinia'
import { getScenicInfo, getScenicSpots } from '../api/scenic'

export const useScenicStore = defineStore('scenic', {
  state: () => ({
    scenicInfo: {},
    spotList: [],
    loadingInfo: false,
    loadingSpots: false
  }),
  getters: {
    totalVisitors: (state) => {
      return state.spotList.reduce((sum, spot) => sum + (spot.current_visitors || 0), 0)
    },
    overallStatus: (state) => {
      if (!state.spotList.length) return '未知'
      const sumVisitors = state.spotList.reduce((sum, spot) => sum + (spot.current_visitors || 0), 0)
      const sumCapacity = state.spotList.reduce((sum, spot) => sum + (spot.max_capacity || 0), 0)
      
      if (sumCapacity === 0) return '未知'
      const ratio = sumVisitors / sumCapacity
      
      if (ratio < 0.4) return '🟢 良好畅通'
      if (ratio < 0.8) return '🟡 适中平稳'
      return '🔴 拥挤预警'
    }
  },
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
