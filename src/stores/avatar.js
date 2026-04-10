import { defineStore } from 'pinia'
import { ref } from 'vue'
import { Message } from '../utils/message'

export const useAvatarStore = defineStore('avatar', () => {
  const sdkInstance = ref(null)
  const isReady = ref(false)
  const currentStatus = ref('')
  const voiceStatus = ref('')
  const renderState = ref('')
  const isXmovRunning = ref(false)

  const initSDK = async () => {
    if (typeof window.XmovAvatar === 'undefined') {
      Message.error('XmovAvatar SDK 未加载，请检查 index.html')
      return
    }

    try {
      const url = new URL('https://nebula-agent.xingyun3d.com/user/v1/ttsa/session')
      url.searchParams.append('data_source', '2')
      url.searchParams.append('custom_id', 'demo')

      const avatar = new window.XmovAvatar({
        containerId: '#sdk',
        appId: import.meta.env.VITE_XMOV_APP_ID,
        appSecret: import.meta.env.VITE_XMOV_APP_SECRET,
        gatewayServer: url.toString(),
        enableDebugger: false,
        onStateChange(state) {
          if (state === 'online') isReady.value = true
        },
        onStatusChange(status) {
          currentStatus.value = status
        },
        onVoiceStateChange(status) {
          console.log('XmovAvatar 语音状态变化:', status)
          voiceStatus.value = status
        }
      })
      
      sdkInstance.value = avatar
      isXmovRunning.value = true
      
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      await avatar.init({
        onDownloadProgress: (progress) => {
          if (progress >= 100) isReady.value = true
        },
        onClose: () => {
          isReady.value = false
          isXmovRunning.value = false
        }
      })

    } catch (error) {
      console.error('初始化 XmovAvatar 失败:', error)
      Message.error('初始化数字人失败')
      isXmovRunning.value = false
    }
  }

  const speak = (text, is_start = false, is_end = false) => {
    if (!sdkInstance.value || !isReady.value) {
      Message.warning('数字人尚未就绪，请稍后再试')
      return
    }
    if (!text) return

    try {
      if (typeof sdkInstance.value.speak === 'function') {
        sdkInstance.value.speak(text, is_start, is_end)
      } else if (typeof sdkInstance.value.sendText === 'function') {
        sdkInstance.value.sendText(text)
      }
    } catch (error) {
      console.error('数字人播报失败:', error)
    }
  }

  const destroySDK = () => {
    if (sdkInstance.value) {
      try {
        if (typeof sdkInstance.value.destroy === 'function') {
          sdkInstance.value.destroy()
        } else if (typeof sdkInstance.value.dispose === 'function') {
          sdkInstance.value.dispose()
        }
      } catch (error) {
        console.error('销毁 SDK 失败:', error)
      } finally {
        sdkInstance.value = null
        isReady.value = false
        isXmovRunning.value = false
      }
    }
  }

  return {
    sdkInstance,
    isReady,
    currentStatus,
    voiceStatus,
    renderState,
    isXmovRunning,
    initSDK,
    speak,
    destroySDK
  }
})
