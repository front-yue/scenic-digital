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
       <div class="relative group cursor-pointer" @click="handleToggleMic" title="麦克风开关">
         <div class="tech-hex-btn transition-colors" :class="audioConfig.mic ? 'border-emerald-400/50 bg-emerald-400/10' : 'border-red-400/50 bg-red-400/10'">
            <MicIcon v-if="audioConfig.mic" class="w-5 h-5 text-emerald-300 group-hover:scale-110 transition-transform" />
            <MicOffIcon v-else class="w-5 h-5 text-red-400 group-hover:scale-110 transition-transform" />
         </div>
       </div>
       <!-- 启停 Fay 服务 -->
       <div class="relative group cursor-pointer" @click="handleToggleFay" :title="isFayRunning ? '关闭 Fay 服务' : '开启 Fay 服务'">
          <div class="tech-hex-btn transition-colors" :class="isFayRunning ? 'border-emerald-400/50 bg-emerald-400/10 shadow-[0_0_15px_#34d399]' : 'border-red-400/50 bg-red-400/10'">
            <PowerIcon v-if="isFayRunning" class="w-5 h-5 text-emerald-300 group-hover:scale-110 transition-transform" />
            <PowerOffIcon v-else class="w-5 h-5 text-red-400 group-hover:scale-110 transition-transform" />
          </div>
       </div>
    </div>

    <!-- 右侧悬浮挂件 -->
    <div class="absolute z-40 right-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
       <div class="tech-hex-btn">
          <FileTextIcon class="w-5 h-5 text-cyan-300" />
       </div>
       <!-- 启停数字人渲染 -->
       <div class="relative group cursor-pointer" @click="handleToggleXmov" :title="avatarStore.isXmovRunning ? '关闭数字人' : '开启数字人'">
          <div class="tech-hex-btn transition-colors" :class="avatarStore.isXmovRunning ? 'border-amber-400/50 bg-amber-400/10 shadow-[0_0_15px_#fbbf24]' : 'border-cyan-400/50 bg-cyan-400/10'">
            <MonitorPlayIcon class="w-5 h-5 transition-transform group-hover:scale-110" :class="avatarStore.isXmovRunning ? 'text-amber-300' : 'text-cyan-400'" />
          </div>
       </div>
    </div>

    <!-- 数字人模型占位区 -->
    <div class="relative z-20 h-[65%] w-full flex flex-col items-center justify-end pb-[100px]">
       <div id="sdk" class="w-[550px] h-[800px] scale-110 origin-bottom flex flex-col items-center justify-center mix-blend-screen relative animate-float z-30 pointer-events-auto">
          <!-- 当 SDK 未就绪时显示占位符 -->
          <template v-if="!avatarStore.isReady">
            <UserIcon class="w-32 h-32 mb-4 opacity-70 filter drop-shadow-[0_0_15px_#00f0ff] text-cyan-300/50" />
            <span class="font-mono font-bold tracking-[0.3em] text-lg text-shadow-glow text-cyan-300/50">
              {{ avatarStore.isXmovRunning ? '3D AVATAR LOADING...' : '数字向导尚未唤醒' }}
            </span>
          </template>
          
          <!-- 扫描线动画 -->
          <div class="absolute top-0 left-0 w-full h-[2px] bg-cyan-400/80 shadow-[0_0_10px_#00f0ff] animate-scanline pointer-events-none"></div>
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
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { 
  User as UserIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  FileText as FileTextIcon,
  Power as PowerIcon,
  PowerOff as PowerOffIcon,
  MonitorPlay as MonitorPlayIcon
} from 'lucide-vue-next'
import { useAvatarStore } from '@/stores/avatar'
import { getAudioConfig, toggleMicrophone, startFayLive, stopFayLive, getFayStatus } from '@/api/fay'
import { Message } from '@/utils/message'
import { useWebSocket } from '@vueuse/core'

const avatarStore = useAvatarStore()
const audioConfig = ref({ mic: false, speaker: false })
const isFayRunning = ref(false)
const message = ref('')
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
  if (newStatus === 'end') {
    message.value = ''
  } else if (newStatus === 'start') {
  }
})
// 监听接收到的 Fay WebSocket 消息
watch(wsData, (newData) => {
  if (!newData) return
  try {
    const msg = JSON.parse(newData)
    console.log('📩 收到 Fay 实时消息:', msg)
    // 解析 Fay 返回的结构并调用数字人播报
    if (msg?.Data.Key === 'text') {
      const text = msg.Data.Value
      message.value += text
      if(msg.Data.IsEnd == 1) {
        avatarStore.speak(message.value, true, true)
      }
    }
  } catch (error) {
    console.log('📩 收到非 JSON 格式的实时消息:', newData)
  }
})

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

onMounted(() => {
  initFayAudio()
  initFayStatus()
})
</script>
