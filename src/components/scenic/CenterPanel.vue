<template>
  <section class="flex-1 w-full lg:w-[40%] relative flex flex-col transform-style-3d transition-transform duration-500 h-full mx-4">

    <!-- ========== 顶部系统状态指示条 ========== -->
    <div class="absolute inset-x-0 top-0 h-[86px] pointer-events-none z-5 flex items-center justify-center">
      <div class="flex items-center gap-6 text-[11px] font-mono tracking-[0.2em] opacity-70">
        <!-- 状态项 1 -->
        <div class="flex items-center gap-2">
          <div class="w-1.5 h-1.5 bg-cyan-400 rotate-45 shadow-[0_0_6px_#00f0ff] animate-pulse"></div>
          <span class="text-cyan-400/80">SCENIC MONITOR</span>
          <span class="text-cyan-300 font-bold">ACTIVE</span>
        </div>
        <!-- 分隔线 -->
        <div class="w-[1px] h-3 bg-cyan-500/30"></div>
        <!-- 状态项 2 -->
        <div class="flex items-center gap-2">
          <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_#34d399] animate-pulse" style="animation-delay: 0.5s;"></div>
          <span class="text-emerald-400/80">SPOTS ONLINE</span>
          <span class="text-emerald-300 font-bold">{{ scenicStore.spotList.length }}</span>
        </div>
        <!-- 分隔线 -->
        <div class="w-[1px] h-3 bg-cyan-500/30"></div>
        <!-- 状态项 3 -->
        <div class="flex items-center gap-2">
          <div class="w-1.5 h-1.5 bg-cyan-400 rotate-45 shadow-[0_0_6px_#00f0ff] animate-pulse" style="animation-delay: 1s;"></div>
          <span class="text-cyan-400/80">REALTIME SYNC</span>
        </div>
      </div>
    </div>

    <!-- ========== 卡片容器（所有内容在此内部） ========== -->
    <div class="flex-1 relative flex flex-col min-h-0 mt-[86px] mb-[38px] bg-[#061226]/40 backdrop-blur-md rounded-2xl tech-center-panel shadow-[inset_0_0_60px_rgba(0,240,255,0.05)] border border-cyan-500/50 overflow-hidden">
      <!-- 四角高亮装饰 -->
      <div class="absolute top-0 left-0 w-12 h-12 border-t-2 border-l-2 border-cyan-400 rounded-tl-2xl pointer-events-none opacity-50 z-30"></div>
      <div class="absolute top-0 right-0 w-12 h-12 border-t-2 border-r-2 border-cyan-400 rounded-tr-2xl pointer-events-none opacity-50 z-30"></div>
      <div class="absolute bottom-0 left-0 w-12 h-12 border-b-2 border-l-2 border-cyan-400 rounded-bl-2xl pointer-events-none opacity-50 z-30"></div>
      <div class="absolute bottom-0 right-0 w-12 h-12 border-b-2 border-r-2 border-cyan-400 rounded-br-2xl pointer-events-none opacity-50 z-30"></div>

      <!-- ========== 模式切换 Tab（浮在内容上方） ========== -->
      <div class="absolute top-3 left-1/2 -translate-x-1/2 z-40">
        <div class="flex bg-[#061226]/80 backdrop-blur-md rounded-full border border-cyan-500/30 p-0.5 gap-0.5">
          <button
            @click="centerMode = 'map'"
            class="flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-bold tracking-wider transition-all"
            :class="centerMode === 'map'
              ? 'bg-cyan-500/20 text-cyan-300 shadow-[0_0_12px_rgba(0,240,255,0.25)]'
              : 'text-cyan-500/60 hover:text-cyan-400'"
          >
            <MapIcon class="w-3.5 h-3.5" /> 景区地图
          </button>
          <button
            @click="centerMode = 'avatar'"
            class="flex items-center gap-1.5 px-4 py-1.5 rounded-full text-xs font-bold tracking-wider transition-all"
            :class="centerMode === 'avatar'
              ? 'bg-cyan-500/20 text-cyan-300 shadow-[0_0_12px_rgba(0,240,255,0.25)]'
              : 'text-cyan-500/60 hover:text-cyan-400'"
          >
            <UserIcon class="w-3.5 h-3.5" /> 数字向导
          </button>
        </div>
      </div>

      <!-- ========== 地图/数字人内容区（填满卡片） ========== -->
      <div class="absolute inset-0">
        <!-- 地图模式 -->
        <Transition name="mode-switch">
          <div v-if="centerMode === 'map'" class="absolute inset-0 rounded-b-2xl overflow-hidden z-10">
            <el-amap
              :center="mapCenter"
              :zoom="mapZoom"
              map-style="amap://styles/darkblue"
              class="w-full h-full"
              @init="onMapInit"
            />
            <!-- 地图蒙版 -->
            <div class="absolute inset-0 pointer-events-none shadow-[inset_0_0_60px_rgba(0,0,0,0.85)] z-10"></div>
            <div class="absolute inset-0 pointer-events-none bg-cyan-400/3 mix-blend-screen z-10"></div>

            <!-- 地图底部信息栏 -->
            <div class="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
              <div class="flex items-center gap-2 px-5 py-2 rounded-full bg-[#061226]/80 backdrop-blur-md border border-cyan-500/30 shadow-[0_0_20px_rgba(0,240,255,0.1)]">
                <div class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_6px_#00f0ff]"></div>
                <span class="text-xs text-cyan-300 font-bold tracking-wider">{{ mapStatusText }}</span>
              </div>
            </div>
          </div>
        </Transition>

        <!-- 数字人模式 -->
        <Transition name="mode-switch">
          <div v-if="centerMode === 'avatar'" class="absolute inset-0 z-10 flex items-center justify-center">
            <!-- 数字人模型占位区 -->
            <div class="relative z-20 h-[80%] w-full flex flex-col items-center justify-end">
              <div id="sdk" class="w-[342px] h-[100%] scale-110 origin-bottom flex flex-col items-center justify-center mix-blend-screen relative animate-float z-30 pointer-events-auto">

                <!-- ========== 加载中状态 ========== -->
                <template v-if="!avatarStore.isReady && avatarStore.isXmovRunning">
                  <div class="relative flex flex-col items-center">
                    <!-- 旋转扫描环 -->
                    <div class="relative w-28 h-28 mb-6">
                      <div class="absolute inset-0 rounded-full border-2 border-cyan-500/10"></div>
                      <div class="absolute inset-0 rounded-full border-2 border-transparent border-t-cyan-400 border-r-cyan-400/50 animate-spin-slow"></div>
                      <div class="absolute inset-2 rounded-full border border-transparent border-b-emerald-400/60 border-l-emerald-400/30 animate-spin-reverse"></div>
                      <!-- 中心图标 -->
                      <div class="absolute inset-0 flex items-center justify-center">
                        <UserIcon class="w-12 h-12 text-cyan-300/60 animate-pulse" />
                      </div>
                    </div>
                    <!-- 文字提示 -->
                    <span class="font-mono font-bold tracking-[0.3em] text-sm text-cyan-300/70 mb-3">3D AVATAR LOADING</span>
                    <!-- 加载动画点 -->
                    <div class="flex gap-1.5">
                      <div class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style="animation-delay: 0s;"></div>
                      <div class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style="animation-delay: 0.15s;"></div>
                      <div class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style="animation-delay: 0.3s;"></div>
                    </div>
                  </div>
                </template>

                <!-- ========== 未唤醒状态 ========== -->
                <template v-else-if="!avatarStore.isReady">
                  <div class="relative flex flex-col items-center cursor-pointer group" @click="handleToggleXmov">
                    <!-- 外圈呼吸光环 -->
                    <div class="relative w-36 h-36 mb-6">
                      <div class="absolute inset-0 rounded-full bg-cyan-400/5 animate-breathe"></div>
                      <div class="absolute inset-3 rounded-full border border-cyan-500/20 animate-breathe" style="animation-delay: 0.5s;"></div>
                      <div class="absolute inset-6 rounded-full border border-cyan-400/10"></div>
                      <!-- 中心图标 -->
                      <div class="absolute inset-0 flex items-center justify-center">
                        <div class="flex flex-col items-center gap-1">
                          <UserIcon class="w-14 h-14 text-cyan-300/40 group-hover:text-cyan-300/70 transition-colors duration-500" />
                          <div class="w-8 h-[2px] bg-gradient-to-r from-transparent via-cyan-400/40 to-transparent group-hover:via-cyan-400/80 transition-colors"></div>
                        </div>
                      </div>
                    </div>
                    <!-- 文字提示 -->
                    <span class="font-mono font-bold tracking-[0.2em] text-sm text-cyan-300/40 group-hover:text-cyan-300/70 transition-colors duration-500 mb-2">数字向导待命中</span>
                    <span class="text-[10px] font-mono tracking-[0.15em] text-cyan-500/30 group-hover:text-cyan-400/60 transition-colors duration-500">CLICK TO ACTIVATE</span>
                  </div>
                </template>

              </div>
            </div>

            <!-- 底部全息投影底座 -->
            <div class="absolute bottom-[80px] left-1/2 -translate-x-1/2 w-[350px] sm:w-[450px] h-[30px] flex items-center justify-center z-10">
              <div class="relative w-full h-full flex items-center justify-center">
                <div class="absolute w-[120%] h-[150%] rounded-[50%] border border-cyan-500/50 opacity-0 animate-ripple-1"></div>
                <div class="absolute w-[120%] h-[150%] rounded-[50%] border border-cyan-500/30 opacity-0 animate-ripple-2"></div>
                <div class="absolute w-full h-full rounded-[50%] bg-cyan-500/30 blur-2xl"></div>
                <div class="absolute w-[90%] h-[80%] rounded-[50%] border-[2px] border-cyan-300 shadow-[0_0_15px_#00f0ff,inset_0_0_15px_#00f0ff]"></div>
                <div class="absolute w-[60%] h-[50%] rounded-[50%] bg-cyan-400/40 blur-md animate-pulse-core"></div>
                <div class="absolute w-[70%] h-[30%] top-[20%] rounded-[50%] bg-gradient-to-b from-white/30 to-transparent blur-[2px]"></div>
              </div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- ========== 悬浮控件（卡片内绝对定位） ========== -->
      <!-- 左侧 -->
      <div class="absolute z-40 left-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
        <div id="guide-mic-btn" class="relative group cursor-pointer" @click="handleToggleMic" title="麦克风开关">
          <div class="tech-hex-btn transition-colors" :class="audioConfig.mic ? 'border-emerald-400/50 bg-emerald-400/10' : 'border-red-400/50 bg-red-400/10'">
            <MicIcon v-if="audioConfig.mic" class="w-5 h-5 text-emerald-300 group-hover:scale-110 transition-transform" />
            <MicOffIcon v-else class="w-5 h-5 text-red-400 group-hover:scale-110 transition-transform" />
          </div>
        </div>
        <div id="guide-fay-btn" class="relative group cursor-pointer" @click="handleToggleFay" :title="isFayRunning ? '关闭 Fay 服务' : '开启 Fay 服务'">
          <div class="tech-hex-btn transition-colors" :class="isFayRunning ? 'border-emerald-400/50 bg-emerald-400/10 shadow-[0_0_15px_#34d399]' : 'border-red-400/50 bg-red-400/10'">
            <PowerIcon v-if="isFayRunning" class="w-5 h-5 text-emerald-300 group-hover:scale-110 transition-transform" />
            <PowerOffIcon v-else class="w-5 h-5 text-red-400 group-hover:scale-110 transition-transform" />
          </div>
        </div>
      </div>

      <!-- 右侧 -->
      <div class="absolute z-40 right-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
        <div id="guide-location-btn" class="relative group cursor-pointer" @click="showCurrentLocation" title="当前位置雷达">
          <div class="tech-hex-btn transition-colors border-cyan-400/50 bg-cyan-400/10 hover:shadow-[0_0_15px_#00f0ff]">
            <MapPinIcon class="w-5 h-5 text-cyan-300 group-hover:scale-110 transition-transform" />
          </div>
        </div>
        <div id="guide-avatar-btn" class="relative group cursor-pointer" @click="handleToggleXmov" :title="avatarStore.isXmovRunning ? '关闭数字人' : '开启数字人'">
          <div class="tech-hex-btn transition-colors" :class="avatarStore.isXmovRunning ? 'border-amber-400/50 bg-amber-400/10 shadow-[0_0_15px_#fbbf24]' : 'border-cyan-400/50 bg-cyan-400/10'">
            <MonitorPlayIcon class="w-5 h-5 transition-transform group-hover:scale-110" :class="avatarStore.isXmovRunning ? 'text-amber-300' : 'text-cyan-400'" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import {
  User as UserIcon, Map as MapIcon, MapPin as MapPinIcon,
  Mic as MicIcon, MicOff as MicOffIcon,
  Power as PowerIcon, PowerOff as PowerOffIcon,
  MonitorPlay as MonitorPlayIcon
} from 'lucide-vue-next'
import { useAvatarStore } from '@/stores/avatar'
import { useScenicStore } from '@/stores/scenic'
import { getAudioConfig, toggleMicrophone, startFayLive, stopFayLive, getFayStatus } from '@/api/fay'
import { getGeocode } from '@/api/map'
import { Message } from '@/utils/message'
import { useWebSocket } from '@vueuse/core'
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const avatarStore = useAvatarStore()
const scenicStore = useScenicStore()
const audioConfig = ref({ mic: false, speaker: false })
const isFayRunning = ref(false)
const message = ref('')

// ========== 模式切换 ==========
const centerMode = ref('map') // 'map' | 'avatar'
const mapStatusText = computed(() => {
  if (navActive.value) return '导航模式 · 步行路线'
  if (locationActive.value) return '当前位置雷达'
  return `${scenicStore.spotList.length} 个景点标记`
})

// ========== 地图核心 ==========
const mapCenter = ref([120.15, 30.28])
const mapZoom = ref(14)
let amapInstance = null
let spotMarkers = []
let highlightMarker = null
let locationMarker = null
let walkingRoute = null
const navActive = ref(false)
const locationActive = ref(false)

const onMapInit = (map) => {
  amapInstance = map
  addSpotMarkers()
}

const addSpotMarkers = () => {
  if (!amapInstance || !window.AMap) return
  spotMarkers.forEach(m => amapInstance.remove(m))
  spotMarkers = []

  const spots = scenicStore.spotList || []
  spots.forEach((spot) => {
    const lat = Number(spot.latitude)
    const lng = Number(spot.longitude)
    if (!lat || !lng) return

    const markerContent = `
      <div class="relative flex items-center justify-center w-8 h-8">
        <div class="absolute w-full h-full rounded-full bg-cyan-400/15 animate-pulse"></div>
        <div class="absolute w-5 h-5 rounded-full border border-cyan-400/40"></div>
        <div class="absolute w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_8px_#00f0ff]"></div>
      </div>
    `
    const marker = new AMap.Marker({
      position: [lng, lat],
      content: markerContent,
      offset: new AMap.Pixel(-16, -16),
      title: spot.spot_name
    })
    amapInstance.add(marker)
    spotMarkers.push(marker)
  })
}

// 公开方法：定位到指定景点
const locateSpot = ({ latitude, longitude, name }) => {
  centerMode.value = 'map'
  nextTick(() => {
    if (!amapInstance) return
    clearOverlays()

    const hlContent = `
      <div class="relative flex items-center justify-center w-12 h-12">
        <div class="absolute w-full h-full rounded-full bg-cyan-400/20 animate-ping"></div>
        <div class="absolute w-8 h-8 rounded-full border-2 border-cyan-400/60 animate-pulse"></div>
        <div class="absolute w-4 h-4 rounded-full bg-cyan-400 shadow-[0_0_15px_#00f0ff]"></div>
      </div>
    `
    highlightMarker = new AMap.Marker({
      position: [longitude, latitude],
      content: hlContent,
      offset: new AMap.Pixel(-24, -24),
      title: name,
      animation: 'AMAP_ANIMATION_DROP'
    })
    amapInstance.add(highlightMarker)
    amapInstance.setZoomAndCenter(16, [longitude, latitude], false, 500)
  })
}

defineExpose({ locateSpot })

watch(() => scenicStore.spotList, () => {
  nextTick(() => addSpotMarkers())
}, { deep: true })

// 清除地图上的覆盖物（定位标记、路线等）
const clearOverlays = () => {
  if (highlightMarker && amapInstance) { amapInstance.remove(highlightMarker); highlightMarker = null }
  if (locationMarker && amapInstance) { amapInstance.remove(locationMarker); locationMarker = null }
  if (walkingRoute) { walkingRoute.clear(); walkingRoute = null }
  navActive.value = false
  locationActive.value = false
}

// ========== 当前位置雷达 ==========
const showCurrentLocation = async () => {
  try {
    const currentAddress = scenicStore.scenicInfo?.address
    if (!currentAddress) {
      Message.warning('景区位置未配置，请先在管理后台设置地理位置')
      return
    }

    Message.info('正在定位当前位置...')
    const res = await getGeocode(currentAddress)
    if (res && res.code == 200) {
      const [lng, lat] = res.data.location.split(',').map(Number)

      // 切到地图模式
      centerMode.value = 'map'
      await nextTick()

      if (!amapInstance) return
      clearOverlays()

      const markerContent = `
        <div class="relative flex items-center justify-center w-12 h-12">
          <div class="absolute w-full h-full rounded-full bg-cyan-400/20 animate-ping"></div>
          <div class="absolute w-8 h-8 rounded-full border border-cyan-400/50 animate-pulse"></div>
          <div class="absolute w-4 h-4 rounded-full bg-cyan-400 shadow-[0_0_15px_#00f0ff]"></div>
        </div>
      `
      locationMarker = new AMap.Marker({
        position: [lng, lat],
        content: markerContent,
        offset: new AMap.Pixel(-24, -24),
        title: '当前位置',
        animation: 'AMAP_ANIMATION_DROP'
      })
      amapInstance.add(locationMarker)
      amapInstance.setZoomAndCenter(15, [lng, lat])
      locationActive.value = true
    } else {
      Message.error('定位失败')
    }
  } catch (error) {
    console.error('定位异常:', error)
    Message.error('雷达系统异常')
  }
}

// ========== 导航路线绘制 ==========
const triggerMapNav = async (origin, dest) => {
  if (origin === '当前位置') origin = scenicStore.scenicInfo?.address
  if (dest === '当前位置') dest = scenicStore.scenicInfo?.address

  const [originRes, destRes] = await Promise.all([getGeocode(origin), getGeocode(dest)])
  if (originRes.code !== 200 || destRes.code !== 200) return

  const [lng1, lat1] = originRes.data.location.split(',').map(Number)
  const [lng2, lat2] = destRes.data.location.split(',').map(Number)

  // 切到地图模式
  centerMode.value = 'map'
  await nextTick()

  if (!amapInstance || !window.AMap) return
  clearOverlays()

  AMap.plugin('AMap.Walking', () => {
    walkingRoute = new AMap.Walking({
      map: amapInstance,
      panel: '',
      outlineColor: '#00f0ff',
      isOutline: true,
      autoFitView: true
    })
    walkingRoute.search([lng1, lat1], [lng2, lat2], (status) => {
      if (status === 'complete') {
        navActive.value = true
      } else {
        console.warn('绘制路线失败')
      }
    })
  })
}

// ========== Fay WebSocket ==========
const { data: wsData, send: wsSend } = useWebSocket('ws://127.0.0.1:10002', {
  autoReconnect: { retries: 5, delay: 3000, onFailed() { console.warn('Fay WebSocket 重连失败') } },
  onConnected() {
    console.log('✅ Fay WebSocket 已成功连接 (10002端口)')
    wsSend(JSON.stringify({ Output: false }))
  },
  onDisconnected() { console.log('❌ Fay WebSocket 连接已断开') }
})

watch(() => avatarStore.voiceStatus, (newStatus) => {
  if (newStatus == 'end') message.value = ''
})

watch(wsData, (newData) => {
  if (!newData) return
  try {
    const msg = JSON.parse(newData)
    if (msg?.Data.Key == 'text') {
      message.value += msg.Data.Value
      if (msg.Data.IsEnd == 1) {
        avatarStore.speak(message.value, true, true)
        const routeMatch = message.value.match(/从【(.*?)】到【(.*?)】/)
        message.value = ''
        if (routeMatch) triggerMapNav(routeMatch[1], routeMatch[2])
      }
    }
  } catch { console.log('📩 收到非 JSON 格式的实时消息:', newData) }
})

// ========== 控制按钮 ==========
const handleToggleMic = async () => {
  try {
    const res = await toggleMicrophone(!audioConfig.value.mic)
    if (res && res.status === 'success') audioConfig.value.mic = res.enabled
    else Message.warning('切换麦克风失败')
  } catch { Message.error('调用麦克风切换接口失败') }
}

const initFayAudio = async () => {
  try {
    const res = await getAudioConfig()
    if (res) { audioConfig.value.mic = res.mic || false; audioConfig.value.speaker = res.speaker || false }
  } catch (e) { console.error('获取音频配置状态失败:', e) }
}

const handleToggleFay = async () => {
  try {
    if (isFayRunning.value) {
      const res = await stopFayLive()
      if (res?.result === 'successful') { isFayRunning.value = false; Message.info('已成功关闭后端 Fay 服务') }
      else Message.warning('关闭失败，请检查 Fay 服务端状态')
    } else {
      const res = await startFayLive()
      if (res?.result === 'successful') { isFayRunning.value = true; Message.success('已成功开启后端 Fay 服务') }
      else Message.warning('开启失败，请检查 Fay 服务端状态')
    }
  } catch { Message.error('请求 Fay 服务端接口失败，请检查网络连接') }
}

const handleToggleXmov = () => {
  if (avatarStore.isXmovRunning) {
    avatarStore.destroySDK()
    Message.info('已关闭前端Xmov数字人渲染')
  } else {
    avatarStore.initSDK()
    Message.success('已启动前端Xmov数字人渲染，请稍候...')
    centerMode.value = 'avatar'
  }
}

const initFayStatus = async () => {
  try {
    const res = await getFayStatus()
    if (res && res.status !== undefined) isFayRunning.value = res.status
  } catch (e) { console.error('获取 Fay 服务初始状态失败:', e) }
}

// ========== 新手引导 ==========
const initGuide = () => {
  const isFirstVisit = localStorage.getItem('scenic_digital_guide_shown')
  if (!isFirstVisit) {
    const driverObj = driver({
      showProgress: true, animate: true, allowClose: false,
      doneBtnText: '开启探索', closeBtnText: '跳过', nextBtnText: '下一步', prevBtnText: '上一步',
      popoverClass: 'driverjs-theme-scifi', overlayOpacity: 0.3,
      steps: [
        { element: '#guide-fay-btn', popover: { title: '核心引擎', description: '点击这里启动或关闭 Fay 数字人 AI 引擎。', side: 'right', align: 'start' } },
        { element: '#guide-mic-btn', popover: { title: '语音输入', description: '控制麦克风收音，直接与数字向导对话。', side: 'right', align: 'start' } },
        { element: '#guide-avatar-btn', popover: { title: '全息投影', description: '启动/关闭数字人的 3D 模型渲染。', side: 'left', align: 'start' } },
        { element: '#guide-location-btn', popover: { title: '位置雷达', description: '在地图上精准定位当前景区位置。', side: 'left', align: 'start' } }
      ],
      onDestroyed: () => localStorage.setItem('scenic_digital_guide_shown', 'true')
    })
    setTimeout(() => driverObj.drive(), 1000)
  }
}

onMounted(() => {
  initFayAudio()
  initFayStatus()
  initGuide()
})
</script>

<style lang="scss" scoped>
#sdk {
  canvas {
    inset: auto;
  }
}
</style>

<style scoped>
:deep(.amap-copyright) { display: none !important; }
:deep(.amap-logo) { opacity: 0.6 !important; }
:deep(.amap-call) { display: none !important; }
:deep(.amap-marker) {
  filter: hue-rotate(180deg) brightness(1.1) drop-shadow(0 0 3px rgba(0,240,255,0.3));
}
:deep(.amap-info) { display: none !important; }

/* 模式切换动画 */
.mode-switch-enter-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.mode-switch-leave-active { transition: opacity 0.25s ease, transform 0.25s ease; }
.mode-switch-enter-from { opacity: 0; transform: scale(0.97); }
.mode-switch-leave-to { opacity: 0; transform: scale(0.97); }

/* 数字人占位区动画 */
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
@keyframes spin-reverse {
  from { transform: rotate(360deg); }
  to   { transform: rotate(0deg); }
}
@keyframes breathe {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50%      { opacity: 0.8; transform: scale(1.06); }
}
.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}
.animate-spin-reverse {
  animation: spin-reverse 2s linear infinite;
}
.animate-breathe {
  animation: breathe 3s ease-in-out infinite;
}

</style>
