<template>
  <section class="flex-1 w-full lg:w-[40%] relative flex flex-col items-center justify-center bg-[#061226]/40 backdrop-blur-md rounded-2xl tech-center-panel shadow-[inset_0_0_60px_rgba(0,240,255,0.05)] transform-style-3d transition-transform duration-500 mt-[60px] mb-[30px] h-[calc(100%-90px)] mx-4">
    <!-- 内部实际展示区边框 -->
    <div class="absolute inset-x-0 top-0 bottom-0 border border-cyan-500/50 rounded-2xl pointer-events-none"></div>

    <!-- 四角高亮装饰 -->
    <div class="absolute top-0 left-0 w-12 h-12 border-t-2 border-l-2 border-cyan-400 rounded-tl-2xl pointer-events-none opacity-50"></div>
    <div class="absolute top-0 right-0 w-12 h-12 border-t-2 border-r-2 border-cyan-400 rounded-tr-2xl pointer-events-none opacity-50"></div>
    <div class="absolute bottom-0 left-0 w-12 h-12 border-b-2 border-l-2 border-cyan-400 rounded-bl-2xl pointer-events-none opacity-50"></div>
    <div class="absolute bottom-0 right-0 w-12 h-12 border-b-2 border-r-2 border-cyan-400 rounded-br-2xl pointer-events-none opacity-50"></div>

    <!-- 顶部标签 -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 bg-cyan-400/20 border border-cyan-400/50 px-8 py-1 rounded-b-lg backdrop-blur-sm">
      <span class="text-sm font-bold text-cyan-300 tracking-[0.3em]">全息展示舱</span>
    </div>

    <!-- 左侧悬浮挂件 -->
    <div class="absolute z-40 left-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
       <!-- 麦克风状态 -->
       <div id="guide-mic-btn" class="relative group cursor-pointer" @click="handleToggleMic" title="麦克风开关">
         <div class="tech-hex-btn transition-colors" :class="audioConfig.mic ? 'border-emerald-400/50 bg-emerald-400/10' : 'border-red-400/50 bg-red-400/10'">
            <MicIcon v-if="audioConfig.mic" class="w-5 h-5 text-emerald-300 group-hover:scale-110 transition-transform" />
            <MicOffIcon v-else class="w-5 h-5 text-red-400 group-hover:scale-110 transition-transform" />
         </div>
       </div>
       <!-- 启停 Fay 服务 -->
       <div id="guide-fay-btn" class="relative group cursor-pointer" @click="handleToggleFay" :title="isFayRunning ? '关闭 Fay 服务' : '开启 Fay 服务'">
          <div class="tech-hex-btn transition-colors" :class="isFayRunning ? 'border-emerald-400/50 bg-emerald-400/10 shadow-[0_0_15px_#34d399]' : 'border-red-400/50 bg-red-400/10'">
            <PowerIcon v-if="isFayRunning" class="w-5 h-5 text-emerald-300 group-hover:scale-110 transition-transform" />
            <PowerOffIcon v-else class="w-5 h-5 text-red-400 group-hover:scale-110 transition-transform" />
          </div>
       </div>
    </div>

    <!-- 右侧悬浮挂件 -->
    <div class="absolute z-40 right-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
       <!-- 获取当前位置雷达 -->
       <div id="guide-location-btn" class="relative group cursor-pointer" @click="showCurrentLocation" title="当前位置雷达">
          <div class="tech-hex-btn transition-colors border-cyan-400/50 bg-cyan-400/10 hover:shadow-[0_0_15px_#00f0ff]">
            <MapPinIcon class="w-5 h-5 text-cyan-300 group-hover:scale-110 transition-transform" />
          </div>
       </div>
       <!-- 启停数字人渲染 -->
       <div id="guide-avatar-btn" class="relative group cursor-pointer" @click="handleToggleXmov" :title="avatarStore.isXmovRunning ? '关闭数字人' : '开启数字人'">
          <div class="tech-hex-btn transition-colors" :class="avatarStore.isXmovRunning ? 'border-amber-400/50 bg-amber-400/10 shadow-[0_0_15px_#fbbf24]' : 'border-cyan-400/50 bg-cyan-400/10'">
            <MonitorPlayIcon class="w-5 h-5 transition-transform group-hover:scale-110" :class="avatarStore.isXmovRunning ? 'text-amber-300' : 'text-cyan-400'" />
          </div>
       </div>
    </div>

    <!-- 数字人模型占位区 -->
    <div class="relative z-20 h-[80%] w-full flex flex-col items-center justify-end">
       <div id="sdk" class="w-[342px] h-[100%] scale-110 origin-bottom flex flex-col items-center justify-center mix-blend-screen relative animate-float z-30 pointer-events-auto">
          <!-- 当 SDK 未就绪时显示占位符 -->
          <template v-if="!avatarStore.isReady">
            <UserIcon class="w-32 h-32 mb-4 opacity-70 filter drop-shadow-[0_0_15px_#00f0ff] text-cyan-300/50" />
            <span class="font-mono font-bold tracking-[0.3em] text-lg text-shadow-glow text-cyan-300/50">
              {{ avatarStore.isXmovRunning ? '3D AVATAR LOADING...' : '数字向导尚未唤醒' }}
            </span>
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
    
    <!-- 引入地图弹窗组件 -->
    <MapModal 
      :visible="isMapVisible" 
      @update:visible="isMapVisible = $event"
      :originCoord="mapOriginCoord"
      :destCoord="mapDestCoord"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import {   User as UserIcon,  MapPin as MapPinIcon,  Mic as MicIcon,  MicOff as MicOffIcon,  Power as PowerIcon,  PowerOff as PowerOffIcon,  MonitorPlay as MonitorPlayIcon} from 'lucide-vue-next'
import { useAvatarStore } from '@/stores/avatar'
import { useScenicStore } from '@/stores/scenic'
import { getAudioConfig, toggleMicrophone, startFayLive, stopFayLive, getFayStatus } from '@/api/fay'
import { getGeocode } from '@/api/map'
import { Message } from '@/utils/message'
import { useWebSocket } from '@vueuse/core'
import MapModal from './MapModal.vue'
import { driver } from 'driver.js'
import 'driver.js/dist/driver.css'

const avatarStore = useAvatarStore()
const scenicStore = useScenicStore() 
const audioConfig = ref({ mic: false, speaker: false })
const isFayRunning = ref(false)
const message = ref('')

// 地图弹窗相关状态
const isMapVisible = ref(false)
const mapOriginCoord = ref('')
const mapDestCoord = ref('')

// 接入 Fay WebSocket 监听
const { status: wsStatus, data: wsData, send: wsSend } = useWebSocket('ws://127.0.0.1:10002', {
  autoReconnect: {
    retries: 5,
    delay: 3000,
    onFailed() {
      console.warn('Fay WebSocket 重连失败')
    }
  },
  onConnected() {
    console.log('✅ Fay WebSocket 已成功连接 (10002端口)')
    // 连接成功时发送初始化指令
    const initMsg = JSON.stringify({ Output: false })
    wsSend(initMsg)
    console.log('📤 发送初始化消息:', initMsg)
  },
  onDisconnected() {
    console.log('❌ Fay WebSocket 连接已断开')
  }
})
watch(() => avatarStore.voiceStatus, (newStatus) => {
  console.log('XmovAvatar 语音状态变化:', newStatus)
  if (newStatus == 'end') {
    message.value = ''
  } else if (newStatus === 'start') {
  }
})
// 监听接收到的 Fay WebSocket 消息
watch(wsData, (newData) => {
  if (!newData) return
  try {
    const msg = JSON.parse(newData)
    // console.log('📩 收到 Fay 实时消息:', msg)
    
    // 解析 Fay 返回的结构并调用数字人播报
    if (msg?.Data.Key == 'text') {
      let text = msg.Data.Value
      message.value += text
      if(msg.Data.IsEnd == 1) {
        avatarStore.speak(message.value, true, true)
         // 匹配 "从【起点】到【终点】"
        message.value = ''
        const routeMatch = message.value.match(/从【(.*?)】到【(.*?)】/)
        if (routeMatch) {
          triggerMapNav(routeMatch[1], routeMatch[2])
        }
      }
    }
  } catch (error) {
    console.log('📩 收到非 JSON 格式的实时消息:', newData)
  }
})
const triggerMapNav = async (origin, dest) => {
  if(origin == "当前位置") {
    origin = scenicStore.scenicInfo?.address
  }
  if(dest == "当前位置") {
    dest = scenicStore.scenicInfo?.address
  }
  alert(origin + dest)
  const [originRes, destRes] = await Promise.all([
    getGeocode(origin),
    getGeocode(dest)
  ])
  if (originRes.code == 200 && destRes.code == 200) {
    mapOriginCoord.value = originRes.data.location
    mapDestCoord.value = destRes.data.location
    isMapVisible.value = true
  }
}

// 触发当前位置雷达（单点定位模式）
const showCurrentLocation = async () => {
  try {
    // 从 Vuex/Pinia Store 获取后台配置的最新地理位置
    const currentAddress = scenicStore.scenicInfo?.address
    
    if (!currentAddress) {
      Message.warning('景区位置未配置，请先在管理后台设置地理位置')
      return
    }

    Message.info('正在定位当前位置...')
    const res = await getGeocode(currentAddress)
    
    if (res && res.code == 200) {
      mapOriginCoord.value = res.data.location
      mapDestCoord.value = '' 
      isMapVisible.value = true
    } else {
      Message.error('定位失败')
    }
  } catch (error) {
    console.error('定位异常:', error)
    Message.error('雷达系统异常')
  }
}

const handleToggleMic = async () => {
  try {
    const targetStatus = !audioConfig.value.mic;
    const res = await toggleMicrophone(targetStatus);
    if (res && res.status === 'success') {
      audioConfig.value.mic = res.enabled;
    } else {
      Message.warning('切换麦克风失败')
    }
  } catch (error) {
    Message.error('调用麦克风切换接口失败')
  }
};

const initFayAudio = async () => {
  try {
    const audioRes = await getAudioConfig();
    if (audioRes) {
      audioConfig.value.mic = audioRes.mic || false;
      audioConfig.value.speaker = audioRes.speaker || false;
    }
  } catch (error) {
    console.error('获取音频配置状态失败:', error);
  }
};

const handleToggleFay = async () => {
  try {
    if (isFayRunning.value) {
      const res = await stopFayLive()
      if (res && res.result === 'successful') {
        isFayRunning.value = false
        Message.info('已成功关闭后端 Fay 服务')
      } else {
        Message.warning('关闭失败，请检查 Fay 服务端状态')
      }
    } else {
      const res = await startFayLive()
      if (res && res.result === 'successful') {
        isFayRunning.value = true
        Message.success('已成功开启后端 Fay 服务')
      } else {
        Message.warning('开启失败，请检查 Fay 服务端状态')
      }
    }
  } catch (error) {
    console.error('调用启停接口失败:', error)
    Message.error('请求 Fay 服务端接口失败，请检查网络连接')
  }
}

const handleToggleXmov = () => {
  if (avatarStore.isXmovRunning) {
    avatarStore.destroySDK()
    Message.info('已关闭前端Xmov数字人渲染')
  } else {
    avatarStore.initSDK()
    Message.success('已启动前端Xmov数字人渲染，请稍候...')
  }
}

const initFayStatus = async () => {
  try {
    const res = await getFayStatus()
    if (res && res.status !== undefined) {
      isFayRunning.value = res.status
    }
  } catch (error) {
    console.error('获取 Fay 服务初始状态失败:', error)
  }
}

// 初始化新手引导
const initGuide = () => {
  const isFirstVisit = localStorage.getItem('scenic_digital_guide_shown')
  if (!isFirstVisit) {
    const driverObj = driver({
      showProgress: true,
      animate: true,
      allowClose: false,
      doneBtnText: '开启探索',
      closeBtnText: '跳过',
      nextBtnText: '下一步',
      prevBtnText: '上一步',
      popoverClass: 'driverjs-theme-scifi', 
      overlayOpacity: 0.3, 
      steps: [
        {
          element: '#guide-fay-btn',
          popover: {
            title: '核心引擎',
            description: '点击这里启动或关闭 Fay 数字人 AI 引擎。这是整个对话系统的大脑。',
            side: 'right',
            align: 'start'
          }
        },
        {
          element: '#guide-mic-btn',
          popover: {
            title: '语音输入',
            description: '控制麦克风收音。当引擎启动后，你可以通过麦克风直接与数字向导对话。',
            side: 'right',
            align: 'start'
          }
        },
        {
          element: '#guide-avatar-btn',
          popover: {
            title: '全息投影',
            description: '启动/关闭数字人的 3D 模型渲染。关闭后可节省性能，仅保留语音。',
            side: 'left',
            align: 'start'
          }
        },
        {
          element: '#guide-location-btn',
          popover: {
            title: '位置雷达',
            description: '点击即可在地图上精准定位当前景区的具体位置。',
            side: 'left',
            align: 'start'
          }
        }
      ],
      onDestroyed: () => {
        // 记录已展示，下次不再弹出
        localStorage.setItem('scenic_digital_guide_shown', 'true')
      }
    })
    
    // 稍微延迟一下等 DOM 完全渲染好再弹出
    setTimeout(() => {
      driverObj.drive()
    }, 1000)
  }
}

onMounted(() => {
  initFayAudio()
  initFayStatus()
  initGuide()
})
</script>
<style lang="scss" scoped>
#sdk{
  canvas{
    inset: auto;
  }
}
</style>
