<template>
  <div class="h-screen w-full font-sans relative overflow-hidden flex flex-col" style="background-color: var(--app-bg); color: var(--app-text);">

    <!-- Canvas 粒子背景（移动端减少数量） -->
    <canvas ref="particleCanvas" class="absolute inset-0 z-0 opacity-40"></canvas>

    <!-- 景区封面背景图 + 模糊暗色蒙版 -->
    <div
      v-if="store.scenicInfo.cover_image"
      class="absolute inset-0 z-0 bg-cover bg-center"
      :style="{ backgroundImage: `url(${store.scenicInfo.cover_image})` }"
    ></div>
    <div class="absolute inset-0 z-0 bg-black/35 backdrop-blur-[2px]"></div>

    <!-- 背景光晕（简化） -->
    <div class="absolute inset-0 pointer-events-none z-0">
      <div class="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[80%] h-[400px] blur-[120px] rounded-[100%]" style="background-color: var(--app-glow-1);"></div>
      <div class="absolute bottom-[-10%] left-1/2 -translate-x-1/2 w-[100%] h-[300px] blur-[120px] rounded-[100%]" style="background-color: var(--app-glow-2);"></div>
    </div>

    <!-- ================= 简化顶栏 ================= -->
    <header class="w-full flex items-center relative z-20 shrink-0 h-14 px-5">
      <div class="flex items-center gap-2 text-cyan-300">
        <ClockIcon class="w-4 h-4 animate-pulse" />
        <span class="text-base font-mono font-bold tracking-wider">{{ currentTime }}</span>
      </div>
      <h1 class="absolute left-0 right-0 mx-auto w-fit text-sm font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-emerald-300 tracking-[0.1em] drop-shadow-[0_0_10px_rgba(52,211,153,0.6)] truncate max-w-[50vw] text-center whitespace-nowrap pointer-events-none">
        {{ store.scenicInfo.scenic_name || '智慧文旅' }}
      </h1>
      <div class="flex items-center gap-2 ml-auto">
        <button @click="configVisible = true" class="p-2 rounded-lg border border-white/10 bg-white/5 backdrop-blur-md active:bg-white/10 transition-all">
          <SettingsIcon class="w-4 h-4 text-white/60" />
        </button>
        <button @click="router.push('/admin')" class="p-2 rounded-lg border border-cyan-500/30 bg-cyan-900/20 backdrop-blur-md active:bg-cyan-500/20 transition-all">
          <DatabaseIcon class="w-4 h-4 text-cyan-300" />
        </button>
      </div>
    </header>

    <!-- ================= 数字人全屏展示 ================= -->
    <div class="flex-1 relative z-10 flex flex-col items-center justify-center">

        <!-- 数字人模型 -->
        <div class="relative flex-1 w-full flex items-center justify-center">
          <div id="sdk" class="w-full h-full flex items-center justify-center mix-blend-screen relative z-30 pointer-events-auto">
          </div>

          <!-- SDK 未就绪时的占位符（独立于 SDK 容器，避免被挤偏） -->
          <div v-if="!avatarStore.isReady" class="absolute inset-0 flex flex-col items-center justify-center z-20 pointer-events-none">
            <div class="flex flex-col items-center gap-5">
              <!-- 脉冲环 + 人形图标 -->
              <div class="relative">
                <div class="absolute inset-[-8px] rounded-full border border-cyan-400/30 animate-pulse"></div>
                <div class="absolute inset-[-16px] rounded-full border border-cyan-400/15 animate-ping"></div>
                <div class="w-20 h-20 rounded-full bg-cyan-500/10 border border-cyan-400/30 flex items-center justify-center">
                  <UserIcon class="w-10 h-10 text-cyan-300/60 drop-shadow-[0_0_8px_#00f0ff]" />
                </div>
              </div>
              <div class="flex flex-col items-center gap-1.5">
                <span class="font-mono font-bold tracking-[0.15em] text-sm text-cyan-300/60 whitespace-nowrap">
                  {{ avatarStore.isXmovRunning ? '3D AVATAR LOADING...' : '数字向导尚未唤醒' }}
                </span>
                <span v-if="!avatarStore.isXmovRunning" class="text-[11px] text-cyan-400/40 font-mono tracking-wider">
                  点击右下角「数字人」按钮启动
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部控制工具栏 -->
        <div class="w-full shrink-0 pb-5 pt-3 px-4 bg-gradient-to-t from-black/40 to-transparent">
          <!-- Fay 语音播报文字 -->
          <div v-if="fayMessage" class="mb-3 mx-auto max-w-sm rounded-lg border border-cyan-500/30 bg-[#061226]/80 backdrop-blur-md px-4 py-2">
            <p class="text-xs text-cyan-100/80 leading-relaxed">{{ fayMessage }}</p>
          </div>

          <!-- 控制按钮行 -->
          <div class="flex items-center justify-center gap-5">
            <!-- 麦克风 -->
            <button @click="handleToggleMic" class="flex flex-col items-center gap-1.5 active:scale-90 transition-transform">
              <div class="w-11 h-11 rounded-full flex items-center justify-center border backdrop-blur-md transition-all"
                :class="audioConfig.mic
                  ? 'border-emerald-400/50 bg-emerald-400/15 shadow-[0_0_12px_rgba(52,211,153,0.3)]'
                  : 'border-white/15 bg-white/5'">
                <MicIcon v-if="audioConfig.mic" class="w-5 h-5 text-emerald-300" />
                <MicOffIcon v-else class="w-5 h-5 text-white/50" />
              </div>
              <span class="text-[10px] text-white/50">麦克风</span>
            </button>

            <!-- Fay 服务 -->
            <button @click="handleToggleFay" class="flex flex-col items-center gap-1.5 active:scale-90 transition-transform">
              <div class="w-11 h-11 rounded-full flex items-center justify-center border backdrop-blur-md transition-all"
                :class="isFayRunning
                  ? 'border-emerald-400/50 bg-emerald-400/15 shadow-[0_0_12px_rgba(52,211,153,0.3)]'
                  : 'border-white/15 bg-white/5'">
                <PowerIcon v-if="isFayRunning" class="w-5 h-5 text-emerald-300" />
                <PowerOffIcon v-else class="w-5 h-5 text-white/50" />
              </div>
              <span class="text-[10px] text-white/50">Fay</span>
            </button>

            <!-- 定位雷达 -->
            <button @click="showCurrentLocation" class="flex flex-col items-center gap-1.5 active:scale-90 transition-transform">
              <div class="w-11 h-11 rounded-full flex items-center justify-center border border-cyan-400/40 bg-cyan-400/10 backdrop-blur-md transition-all active:shadow-[0_0_12px_rgba(0,240,255,0.3)]">
                <MapPinIcon class="w-5 h-5 text-cyan-300" />
              </div>
              <span class="text-[10px] text-white/50">定位</span>
            </button>

            <!-- 数字人开关 -->
            <button @click="handleToggleXmov" class="flex flex-col items-center gap-1.5 active:scale-90 transition-transform">
              <div class="w-11 h-11 rounded-full flex items-center justify-center border backdrop-blur-md transition-all"
                :class="avatarStore.isXmovRunning
                  ? 'border-amber-400/50 bg-amber-400/15 shadow-[0_0_12px_rgba(251,191,36,0.3)]'
                  : 'border-cyan-400/40 bg-cyan-400/10'">
                <MonitorPlayIcon class="w-5 h-5" :class="avatarStore.isXmovRunning ? 'text-amber-300' : 'text-cyan-400'" />
              </div>
              <span class="text-[10px] text-white/50">数字人</span>
            </button>
          </div>

          <!-- 消息输入框 -->
          <div class="mt-4 mx-auto max-w-sm flex relative">
            <input
              v-model="chatMessage"
              @keyup.enter="handleSendMessage"
              type="text"
              placeholder="向 Fay 发送消息..."
              class="w-full h-11 bg-white/8 border border-white/15 backdrop-blur-md rounded-xl pl-4 pr-11 text-sm text-white/90 tracking-wider placeholder-white/30 focus:outline-none focus:border-cyan-400/50 focus:bg-white/10 transition-all"
            />
            <button
              @click="handleSendMessage"
              :disabled="isSending || !chatMessage.trim()"
              class="absolute right-1.5 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg text-cyan-300 disabled:opacity-30 transition-all active:scale-90"
            >
              <SendIcon class="w-4 h-4" :class="{ 'animate-pulse': isSending }" />
            </button>
          </div>
        </div>
      </div>

    <!-- 地图弹窗 -->
    <MapModal
      :visible="isMapVisible"
      @update:visible="isMapVisible = $event"
      :originCoord="mapOriginCoord"
      :destCoord="mapDestCoord"
    />

    <!-- AI 照相馆弹窗 -->
    <AIPhotoOverlay />

    <!-- 版本信息弹窗 -->
    <VersionModal :visible="versionVisible" @update:visible="versionVisible = $event" />

    <!-- 系统配置弹窗 -->
    <ConfigPanel :visible="configVisible" @update:visible="configVisible = $event" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  Clock as ClockIcon,
  Database as DatabaseIcon,
  User as UserIcon,
  MapPin as MapPinIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  Power as PowerIcon,
  PowerOff as PowerOffIcon,
  MonitorPlay as MonitorPlayIcon,
  Send as SendIcon,
  Settings as SettingsIcon,
  Sun,
  MapPin
} from 'lucide-vue-next'
import { useWebSocket } from '@vueuse/core'
import { useScenicStore } from '@/stores/scenic'
import { useAvatarStore } from '@/stores/avatar'
import { getConfig } from '@/api/config'
import { getAudioConfig, toggleMicrophone, startFayLive, stopFayLive, getFayStatus, sendFayMessage } from '@/api/fay'
import { getGeocode } from '@/api/map'
import { Message } from '@/utils/message'
import MapModal from '@/components/scenic/MapModal.vue'
import AIPhotoOverlay from '@/components/photo/AIPhotoOverlay.vue'
import VersionModal from '@/components/common/VersionModal.vue'
import ConfigPanel from '@/components/common/ConfigPanel.vue'

const store = useScenicStore()
const avatarStore = useAvatarStore()
const router = useRouter()

// =========== 状态 ===========
const currentTime = ref('')
const currentDate = ref('')
const versionVisible = ref(false)
const configVisible = ref(false)
const audioConfig = ref({ mic: false, speaker: false })
const isFayRunning = ref(false)
const fayMessage = ref('')
const chatMessage = ref('')
const isSending = ref(false)

// 地图弹窗
const isMapVisible = ref(false)
const mapOriginCoord = ref('')
const mapDestCoord = ref('')

// =========== 时间 ===========
let timeInterval
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

// =========== Fay WebSocket ===========
const { data: wsData, send: wsSend } = useWebSocket('ws://127.0.0.1:10002', {
  autoReconnect: {
    retries: 5,
    delay: 3000,
    onFailed() {
      console.warn('Fay WebSocket 重连失败')
    }
  },
  onConnected() {
    console.log('Fay WebSocket 已连接')
    wsSend(JSON.stringify({ Output: false }))
  }
})

watch(() => avatarStore.voiceStatus, (newStatus) => {
  if (newStatus === 'end') {
    fayMessage.value = ''
  }
})

watch(wsData, (newData) => {
  if (!newData) return
  try {
    const msg = JSON.parse(newData)
    if (msg?.Data?.Key === 'text') {
      const text = msg.Data.Value
      fayMessage.value += text
      if (msg.Data.IsEnd === 1) {
        avatarStore.speak(fayMessage.value, true, true)
        const routeMatch = fayMessage.value.match(/从【(.*?)】到【(.*?)】/)
        fayMessage.value = ''
        if (routeMatch) {
          triggerMapNav(routeMatch[1], routeMatch[2])
        }
      }
    }
  } catch (error) {
    console.log('收到非 JSON 消息:', newData)
  }
})

// =========== 地图导航 ===========
const triggerMapNav = async (origin, dest) => {
  if (origin === '当前位置') origin = store.scenicInfo?.address
  if (dest === '当前位置') dest = store.scenicInfo?.address
  const [originRes, destRes] = await Promise.all([getGeocode(origin), getGeocode(dest)])
  if (originRes.code === 200 && destRes.code === 200) {
    mapOriginCoord.value = originRes.data.location
    mapDestCoord.value = destRes.data.location
    isMapVisible.value = true
  }
}

const showCurrentLocation = async () => {
  const currentAddress = store.scenicInfo?.address
  if (!currentAddress) {
    Message.warning('景区位置未配置')
    return
  }
  Message.info('正在定位...')
  const res = await getGeocode(currentAddress)
  if (res && res.code === 200) {
    mapOriginCoord.value = res.data.location
    mapDestCoord.value = ''
    isMapVisible.value = true
  } else {
    Message.error('定位失败')
  }
}

// =========== 控制按钮 ===========
const handleToggleMic = async () => {
  try {
    const targetStatus = !audioConfig.value.mic
    const res = await toggleMicrophone(targetStatus)
    if (res && res.status === 'success') {
      audioConfig.value.mic = res.enabled
    } else {
      Message.warning('切换麦克风失败')
    }
  } catch (error) {
    Message.error('调用麦克风失败')
  }
}

const handleToggleFay = async () => {
  try {
    if (isFayRunning.value) {
      const res = await stopFayLive()
      if (res && res.result === 'successful') {
        isFayRunning.value = false
        Message.info('已关闭 Fay 服务')
      } else {
        Message.warning('关闭失败')
      }
    } else {
      const res = await startFayLive()
      if (res && res.result === 'successful') {
        isFayRunning.value = true
        Message.success('已开启 Fay 服务')
      } else {
        Message.warning('开启失败')
      }
    }
  } catch (error) {
    Message.error('请求 Fay 服务失败')
  }
}

const handleToggleXmov = () => {
  if (avatarStore.isXmovRunning) {
    avatarStore.destroySDK()
    Message.info('已关闭数字人渲染')
  } else {
    avatarStore.initSDK()
    Message.success('已启动数字人渲染，请稍候...')
  }
}

const handleSendMessage = async () => {
  if (!chatMessage.value.trim() || isSending.value) return
  isSending.value = true
  try {
    const res = await sendFayMessage(chatMessage.value)
    if (res && res.result === 'successful') {
      Message.success('消息发送成功')
      chatMessage.value = ''
    } else {
      Message.warning('消息发送失败')
    }
  } catch (error) {
    Message.error('服务连接异常')
  } finally {
    isSending.value = false
  }
}

// =========== 初始化 ===========
const initFayAudio = async () => {
  try {
    const audioRes = await getAudioConfig()
    if (audioRes) {
      audioConfig.value.mic = audioRes.mic || false
      audioConfig.value.speaker = audioRes.speaker || false
    }
  } catch (error) {
    console.error('获取音频状态失败:', error)
  }
}

const initFayStatus = async () => {
  try {
    const res = await getFayStatus()
    if (res && res.status !== undefined) {
      isFayRunning.value = res.status
    }
  } catch (error) {
    console.error('获取 Fay 状态失败:', error)
  }
}

// =========== 粒子背景（移动端减少数量） ===========
const particleCanvas = ref(null)
let animationFrameId = null
let handleResize = null

const initParticleCanvas = () => {
  if (handleResize) window.removeEventListener('resize', handleResize)
  if (animationFrameId) cancelAnimationFrame(animationFrameId)

  const canvas = particleCanvas.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  let particlesArray = []

  handleResize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  window.addEventListener('resize', handleResize)
  handleResize()

  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width
      this.y = Math.random() * canvas.height
      this.size = Math.random() * 1.5 + 0.5
      this.speedX = Math.random() * 0.6 - 0.3
      this.speedY = Math.random() * 0.6 - 0.3
      const theme = document.documentElement.getAttribute('data-theme')
      if (theme === 'spring_season') this.color = Math.random() > 0.5 ? '#84cc16' : '#22c55e'
      else if (theme === 'summer') this.color = Math.random() > 0.5 ? '#38bdf8' : '#3b82f6'
      else if (theme === 'autumn') this.color = Math.random() > 0.5 ? '#f97316' : '#f59e0b'
      else if (theme === 'winter') this.color = Math.random() > 0.5 ? '#94a3b8' : '#818cf8'
      else this.color = Math.random() > 0.5 ? '#10b981' : '#34d399'
      this.opacity = Math.random() * 0.4 + 0.2
    }
    update() {
      this.x += this.speedX
      this.y += this.speedY
      if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX
      if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY
    }
    draw() {
      ctx.globalAlpha = this.opacity
      ctx.fillStyle = this.color
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
      ctx.fill()
      ctx.globalAlpha = 1
    }
  }

  const init = () => {
    particlesArray = []
    // 移动端粒子数大幅减少（/40000 vs 大屏 /15000），且不做连线
    const numberOfParticles = Math.floor((canvas.width * canvas.height) / 40000)
    for (let i = 0; i < numberOfParticles; i++) {
      particlesArray.push(new Particle())
    }
  }

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (let i = 0; i < particlesArray.length; i++) {
      particlesArray[i].update()
      particlesArray[i].draw()
    }
    // 移动端不做粒子连线，节省性能
    animationFrameId = requestAnimationFrame(animate)
  }

  init()
  animate()
}

const loadSystemConfig = async () => {
  try {
    const res = await getConfig('theme')
    if (res && res.status === 'success' && res.data && res.data.value) {
      const theme = res.data.value
      if (theme === 'default') {
        document.documentElement.removeAttribute('data-theme')
      } else {
        document.documentElement.setAttribute('data-theme', theme)
      }
      initParticleCanvas()
    }
  } catch (error) {
    console.error('获取系统配置失败:', error)
  }
}

onMounted(() => {
  loadSystemConfig()
  store.refreshAllData()
  initParticleCanvas()
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  initFayAudio()
  initFayStatus()
})

onUnmounted(() => {
  if (handleResize) window.removeEventListener('resize', handleResize)
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  if (timeInterval) clearInterval(timeInterval)
})
</script>

<style scoped>
</style>