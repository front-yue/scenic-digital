import { ref, watch, onUnmounted } from 'vue'
import { useWebSocket } from '@vueuse/core'
import { useAvatarStore } from '@/stores/avatar'

// 全局唯一的 FAY WebSocket 连接（应用根组件调用一次即可）
// 严格沿用原 CenterPanel 的实时消息逻辑：human_text -> 用户消息；text(IsEnd) -> 数字人回复并播报
export function useFaySocket() {
  const avatarStore = useAvatarStore()
  const message = ref('')

  const { data: wsData, send: wsSend } = useWebSocket('ws://127.0.0.1:10002', {
    autoReconnect: { retries: 5, delay: 3000, onFailed() { console.warn('Fay WebSocket 重连失败') } },
    onConnected() {
      console.log('✅ Fay WebSocket 已成功连接 (10002端口)')
      wsSend(JSON.stringify({ Output: false }))
    },
    onDisconnected() { console.log('❌ Fay WebSocket 连接已断开') },
  })

  watch(() => avatarStore.voiceStatus, (newStatus) => {
    if (newStatus == 'end') message.value = ''
  })

  watch(wsData, (newData) => {
    if (!newData) return
    try {
      const msg = JSON.parse(newData)
      if (msg?.Data?.Key === 'human_text') {
        avatarStore.addChatMessage('user', msg.Data.Value)
      } else if (msg?.Data?.Key === 'text') {
        message.value += msg.Data.Value
        if (msg.Data.IsEnd == 1) {
          avatarStore.addChatMessage('ai', message.value)
          avatarStore.speak(message.value, true, true)
          message.value = ''
        }
      }
    } catch {
      console.log('📩 收到非 JSON 格式的实时消息:', newData)
    }
  })

  onUnmounted(() => {
    // useWebSocket 会在组件卸载时自动关闭连接
  })
}
