<template>
  <div class="min-h-screen bg-gray-100 p-6 flex flex-col md:flex-row gap-6 pb-20">
    <!-- 左侧：数字人与对话区 -->
    <div class="w-full md:w-1/3 flex flex-col gap-4">
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden flex flex-col h-[500px]">
        <!-- 数字人展示区 -->
        <div class="relative h-2/3 bg-blue-50 flex items-center justify-center">
          
          <!-- WS 连接状态与直播状态 -->
          <div class="absolute top-4 left-4 flex gap-2">
            <div 
              class="flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-white/80 backdrop-blur-sm shadow-sm"
              :class="wsConnected ? 'text-green-600' : 'text-red-500'"
            >
              <Wifi v-if="wsConnected" class="w-3 h-3" />
              <WifiOff v-else class="w-3 h-3" />
              {{ wsConnected ? 'Fay 已连接' : '未连接' }}
            </div>
            <div 
              v-if="wsConnected"
              class="flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-white/80 backdrop-blur-sm shadow-sm"
              :class="isLive ? 'text-red-500' : 'text-gray-500'"
            >
              <span class="w-2 h-2 rounded-full" :class="isLive ? 'bg-red-500 animate-pulse' : 'bg-gray-400'"></span>
              {{ isLive ? '直播中' : '休息中' }}
            </div>
          </div>

          <!-- 简单用一个 CSS 动画模拟数字人说话 -->
          <div class="flex flex-col items-center">
            <div 
              class="w-32 h-32 rounded-full border-4 shadow-md overflow-hidden transition-all duration-300"
              :class="[isSpeaking ? 'border-blue-500 scale-105' : 'border-gray-200']"
            >
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Fay&style=circle" alt="Fay Avatar" class="w-full h-full object-cover bg-white" />
            </div>
            <h2 class="mt-4 text-xl font-bold text-gray-700">Fay 智能管家</h2>
            <div class="mt-2 text-sm text-gray-500 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full" :class="[isSpeaking ? 'bg-green-500 animate-pulse' : 'bg-gray-400']"></span>
              {{ isSpeaking ? '正在讲话...' : panelStatus }}
            </div>
          </div>
        </div>
        
        <!-- 对话记录区 -->
        <div class="flex-1 p-4 bg-gray-50 overflow-y-auto flex flex-col gap-2" ref="chatContainer">
          <div v-for="(msg, index) in messages" :key="index" class="flex flex-col" :class="[msg.role === 'user' ? 'items-end' : 'items-start']">
            <div 
              class="max-w-[80%] px-4 py-2 rounded-2xl text-sm"
              :class="[msg.role === 'user' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-white text-gray-800 border shadow-sm rounded-bl-none']"
            >
              {{ msg.content }}
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="bg-white rounded-2xl shadow-lg p-4 flex gap-2">
        <input 
          v-model="userInput" 
          @keyup.enter="handleSend"
          type="text" 
          placeholder="对 Fay 说点什么吧..." 
          class="flex-1 px-4 py-2 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
        />
        <button 
          @click="handleSend"
          class="bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 transition-colors flex items-center gap-2"
          :disabled="isSpeaking"
        >
          <Send class="w-4 h-4" />
          发送
        </button>
      </div>
    </div>

    <!-- 右侧：物联网中控面板 -->
    <div class="w-full md:w-2/3 bg-white rounded-2xl shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <LayoutDashboard class="w-6 h-6 text-blue-500" />
          智能家居中控大屏
        </h1>
        <div class="flex items-center gap-4 text-sm">
          <div class="flex items-center gap-1 bg-blue-50 px-3 py-1 rounded-full text-blue-700">
            <Thermometer class="w-4 h-4" />
            <span>{{ mockIotDevices.temperature }}°C</span>
          </div>
          <div class="flex items-center gap-1 bg-cyan-50 px-3 py-1 rounded-full text-cyan-700">
            <Droplets class="w-4 h-4" />
            <span>{{ mockIotDevices.humidity }}%</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <!-- 客厅灯 -->
        <DeviceCard 
          title="客厅灯" 
          :active="mockIotDevices.livingRoomLight" 
          icon="Lightbulb"
          @toggle="toggleDevice('livingRoomLight')"
        />
        
        <!-- 卧室灯 -->
        <DeviceCard 
          title="卧室灯" 
          :active="mockIotDevices.bedroomLight" 
          icon="Lightbulb"
          @toggle="toggleDevice('bedroomLight')"
        />

        <!-- 空调 -->
        <DeviceCard 
          title="空调" 
          :active="mockIotDevices.airConditioner" 
          icon="Wind"
          @toggle="toggleDevice('airConditioner')"
        />

        <!-- 门锁 -->
        <DeviceCard 
          title="智能门锁" 
          :active="mockIotDevices.doorLock" 
          icon="Lock"
          activeColor="text-green-500"
          activeBg="bg-green-50"
          activeGlow="bg-green-400"
          activeDot="bg-green-500"
          inactiveIcon="Unlock"
          @toggle="toggleDevice('doorLock')"
        />

        <!-- 窗户 -->
        <DeviceCard 
          title="智能窗户" 
          :active="mockIotDevices.window" 
          icon="AppWindow"
          @toggle="toggleDevice('window')"
        />

        <!-- 窗帘 -->
        <DeviceCard 
          title="智能窗帘" 
          :active="mockIotDevices.curtain" 
          icon="Blinds"
          @toggle="toggleDevice('curtain')"
        />
      </div>

      <div class="mt-8 p-4 bg-gray-50 rounded-xl border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-500 mb-2 flex items-center gap-2">
          <Terminal class="w-4 h-4" />
          系统运行日志
        </h3>
        <div class="h-32 overflow-y-auto font-mono text-xs text-gray-600 space-y-1" ref="logContainer">
          <div v-for="(log, idx) in systemLogs" :key="idx" class="flex gap-2">
            <span class="text-gray-400">[{{ log.time }}]</span>
            <span :class="log.type === 'error' ? 'text-red-500' : 'text-green-600'">{{ log.msg }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted, onUnmounted } from 'vue'
import { 
  Send, 
  LayoutDashboard, 
  Thermometer, 
  Droplets, 
  Terminal,
  Wifi,
  WifiOff
} from 'lucide-vue-next'
import DeviceCard from '../components/DeviceCard.vue'

// === 模拟：所有智能家居设备状态 ===
const mockIotDevices = reactive({
  livingRoomLight: false, // 客厅灯
  bedroomLight: false,    // 卧室灯
  airConditioner: false,  // 空调
  temperature: 24,        // 温度
  humidity: 46,           // 湿度
  doorLock: true,         // 门锁 (true为锁定)
  window: false,          // 窗户
  curtain: false          // 窗帘
})

const isSpeaking = ref(false)
const userInput = ref('')
const messages = ref([
  { role: 'assistant', content: '您好！我是您的智能管家 Fay，有什么可以帮您？' }
])
const systemLogs = ref([
  { time: new Date().toLocaleTimeString(), type: 'info', msg: '系统初始化成功，Fay 核心已加载。' }
])
const panelStatus = ref('待命中')
const isLive = ref(false)
const wsConnected = ref(false)

const chatContainer = ref(null)
const logContainer = ref(null)

const addLog = (msg, type = 'info') => {
  systemLogs.value.push({ time: new Date().toLocaleTimeString(), type, msg })
  nextTick(() => {
    if (logContainer.value) logContainer.value.scrollTop = logContainer.value.scrollHeight
  })
}

const addMessage = (role, content) => {
  messages.value.push({ role, content })
  nextTick(() => {
    if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}

// WebSocket 连接
let ws = null
let lastFayInitPayload = null // 缓存初始化消息
let currentSpeakBuffer = ''   // 用于拼接流式下发的完整句子

const connectWebSocket = () => {
  ws = new WebSocket('ws://127.0.0.1:10002')

  ws.onopen = () => {
    wsConnected.value = true
    addLog('已连接到 Fay 数字人 WebSocket 服务端 (10002端口)')
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      console.log('WS 接收到消息:', data)
      
      // 适配 10002 端口的数据格式 (数字人专用)
      if (data.Topic === 'human' && data.Data) {
        const key = data.Data.Key
        const value = data.Data.Value
        
        // 1. 处理状态提示 (如：思考中...)
        if (key === 'log') {
          panelStatus.value = value
          addLog(`[Fay状态] ${value}`)
        }
        
        // 2. 处理 Fay 回复语音及文本
        // 根据您最新的日志，Fay 下发的是 Key: 'text' 而不是 'audio'
        if (key === 'text' && value) {
          const isFirst = data.Data.IsFirst === 1
          const isEnd = data.Data.IsEnd === 1
          
          if (isFirst) {
            // 新的一句开始，清空缓存
            currentSpeakBuffer = value
          } else {
            // 继续拼接
            currentSpeakBuffer += value
          }
          
          if (isEnd) {
            // 一整句话接收完毕，开始统一展示和播报
            const finalSentence = currentSpeakBuffer
            console.log('[完整句子接收完毕]', finalSentence)
            
            simulateSpeak(finalSentence)
            
            // 如果同时需要解析 IoT 意图（如果 Fay 自己决定要开灯）
            const intent = parseIntent(finalSentence)
            if (intent.type !== 'chat') {
              executeIntent(intent)
            }
            
            // 清空缓存准备迎接下一句
            currentSpeakBuffer = ''
          }
        }
        
        // 3. 处理音频数据与播放 (Key: 'audio')
        // 这是 Fay 数字人驱动端的核心！当 Fay 开启 TTS 时，它会通过这个字段把生成的音频文件路径发过来。
        // 我们可以在浏览器中直接播放这个 HttpValue 提供的音频 URL。
        if (key === 'audio') {
          console.log('[接收到音频数据]', data.Data)
          
          const audioUrl = data.Data.HttpValue
          if (audioUrl) {
            // 播放音频
            const audio = new Audio(audioUrl)
            audio.play().then(() => {
              addLog(`[语音播放] 正在播放 Fay 的语音`)
            }).catch(e => {
              console.error('播放音频失败:', e)
            })
          }
          
          // 解析唇形数据
          if (data.Data.Lips && data.Data.Lips.length > 0) {
             console.log(`[唇形] 收到 ${data.Data.Lips.length} 帧唇形数据`)
             // 在真实的3D数字人项目中，我们会根据 Lips 数据来驱动嘴型 BlendShape
          }
          
          // 解析动作与情绪
          if (data.Data.Action) {
             console.log(`[动作] 触发动作: ${data.Data.Action.behavior}`)
          }
          if (data.Data.Sentiment !== undefined) {
             console.log(`[情绪] 当前情绪值: ${data.Data.Sentiment}`)
          }
        }
        
        // 3. 处理控制指令 (Key: 'control')
        if (key === 'control') {
           if (value === 'speak_end') {
             // 收到说话结束指令
             console.log('[播报] 语音播报结束')
             isSpeaking.value = false
           } else if (value === 'speak_start') {
             console.log('[播报] 语音播报开始')
             isSpeaking.value = true
           }
        }
      }
    } catch (e) {
      addLog(`[WS解析错误] ${e.message}`, 'error')
    }
  }

  ws.onclose = () => {
    wsConnected.value = false
    addLog('Fay WebSocket 连接已断开，尝试重连...', 'error')
    setTimeout(connectWebSocket, 3000)
  }

  ws.onerror = (error) => {
    addLog(`Fay WebSocket 错误: 连接失败`, 'error')
  }
}

// 发送初始化消息
const sendInitMessage = () => {
  // 修改：尝试将 Output 设置为 false，并注释掉发送逻辑，看看是否可行
  const initData = { Username: "User", Output: false }
  const payload = JSON.stringify(initData)
  lastFayInitPayload = payload // 缓存供重连使用
  
  if (wsConnected.value && ws && ws.readyState === WebSocket.OPEN) {
    try {
      ws.send(payload)
      console.log(`[Fay WS] 发送初始化消息: ${payload}`)
      addLog(`[Fay WS] 发送初始化消息`)
    } catch (e) {
      console.error(`[Fay WS] 发送初始化消息失败: ${e.message}`)
    }
  }
}

onMounted(() => {
  connectWebSocket()
  
  // 模拟建立连接后，稍作延迟发送初始化消息
  setTimeout(() => {
    sendInitMessage()
  }, 1000)
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})
const simulateSpeak = async (text) => {
  isSpeaking.value = true
  addMessage('assistant', text)
  // 简单根据字数模拟讲话时间
  const speakTime = Math.max(2000, text.length * 150)
  await new Promise(resolve => setTimeout(resolve, speakTime))
  isSpeaking.value = false
}

// 手动切换设备状态 (供面板点击使用)
const toggleDevice = (deviceKey) => {
  mockIotDevices[deviceKey] = !mockIotDevices[deviceKey]
  const status = mockIotDevices[deviceKey] ? '开启' : '关闭'
  addLog(`[面板操作] 设备 [${deviceKey}] 状态变更为: ${status}`)
}

// === 核心：模拟执行物联网指令 ===
const controlDevice = (device, action) => {
  const cmd = `${device}_${action}`
  addLog(`[Fay指令下发] 接收到控制指令: ${cmd}`)
  
  switch (cmd) {
    case "livingRoomLight_on":
      mockIotDevices.livingRoomLight = true
      return "客厅灯已打开"
    case "livingRoomLight_off":
      mockIotDevices.livingRoomLight = false
      return "客厅灯已关闭"
    case "bedroomLight_on":
      mockIotDevices.bedroomLight = true
      return "卧室灯已打开"
    case "bedroomLight_off":
      mockIotDevices.bedroomLight = false
      return "卧室灯已关闭"
    case "airConditioner_on":
      mockIotDevices.airConditioner = true
      return "空调已开启"
    case "airConditioner_off":
      mockIotDevices.airConditioner = false
      return "空调已关闭"
    case "doorLock_lock":
      mockIotDevices.doorLock = true
      return "家门已锁定"
    case "doorLock_unlock":
      mockIotDevices.doorLock = false
      return "家门已解锁"
    case "window_on":
      mockIotDevices.window = true
      return "窗户已打开"
    case "window_off":
      mockIotDevices.window = false
      return "窗户已关闭"
    case "curtain_on":
      mockIotDevices.curtain = true
      return "窗帘已打开"
    case "curtain_off":
      mockIotDevices.curtain = false
      return "窗帘已关闭"
    default:
      return null
  }
}

// === 核心：模拟 Fay 意图解析 (NLP) ===
const parseIntent = (text) => {
  addLog(`[Fay大脑] 正在分析用户意图: "${text}"`)
  
  // 简单关键词匹配模拟 NLP 实体提取
  const actions = {
    '打开': 'on', '开': 'on', '开启': 'on', '解锁': 'unlock',
    '关闭': 'off', '关': 'off', '锁定': 'lock', '锁上': 'lock', '锁': 'lock'
  }
  
  const devices = {
    '客厅灯': 'livingRoomLight',
    '卧室灯': 'bedroomLight',
    '灯': 'livingRoomLight', // 默认匹配客厅灯
    '空调': 'airConditioner',
    '门': 'doorLock', '门锁': 'doorLock',
    '窗户': 'window', '窗': 'window',
    '窗帘': 'curtain'
  }

  // 场景模式
  if (text.includes('出门') || text.includes('离家')) {
    addLog('[Fay大脑] 匹配到场景模式：离家模式')
    return { type: 'scene', scene: 'leave_home' }
  }
  
  if (text.includes('回家')) {
    addLog('[Fay大脑] 匹配到场景模式：回家模式')
    return { type: 'scene', scene: 'go_home' }
  }

  // 查询状态
  if (text.includes('温度') || text.includes('多热') || text.includes('多冷')) {
    return { type: 'query', target: 'temperature' }
  }
  if (text.includes('状态') || text.includes('安全') || text.includes('安防')) {
    return { type: 'query', target: 'security' }
  }

  // 提取动作和设备
  let matchedAction = null
  let matchedDevice = null

  for (const [key, val] of Object.entries(actions)) {
    if (text.includes(key)) matchedAction = val
  }
  for (const [key, val] of Object.entries(devices)) {
    if (text.includes(key)) matchedDevice = val
  }

  // 特殊处理门锁的 开/关 为 解锁/锁定
  if (matchedDevice === 'doorLock') {
    if (matchedAction === 'on') matchedAction = 'unlock'
    if (matchedAction === 'off') matchedAction = 'lock'
  }

  if (matchedAction && matchedDevice) {
    addLog(`[Fay大脑] 意图解析成功 -> 设备: ${matchedDevice}, 动作: ${matchedAction}`)
    return { type: 'control', device: matchedDevice, action: matchedAction }
  }

  addLog(`[Fay大脑] 未能识别明确的设备控制意图`)
  return { type: 'chat' }
}

const executeIntent = (intent) => {
  if (intent.type === 'scene') {
    if (intent.scene === 'leave_home') {
      controlDevice('livingRoomLight', 'off')
      controlDevice('bedroomLight', 'off')
      controlDevice('airConditioner', 'off')
      controlDevice('window', 'off')
      controlDevice('curtain', 'off')
      controlDevice('doorLock', 'lock')
    } else if (intent.scene === 'go_home') {
      controlDevice('livingRoomLight', 'on')
      controlDevice('airConditioner', 'on')
      controlDevice('curtain', 'on')
      controlDevice('doorLock', 'unlock')
    }
  } 
  else if (intent.type === 'control') {
    controlDevice(intent.device, intent.action)
  }
}

const handleSend = async () => {
  const text = userInput.value.trim()
  if (!text || isSpeaking.value) return
  
  userInput.value = ''

  if (wsConnected.value && ws && ws.readyState === WebSocket.OPEN) {
    // WebSocket 只用于接收消息，发送消息调用 HTTP 接口
    const apiHost = 'http://127.0.0.1:5000'
    
    try {
      addMessage('user', text)
      
      // 调用 Fay 官方的 /api/send 接口来发送消息
      const payload = {
        username: "User",
        msg: text
      }
      
      fetch(`${apiHost}/api/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'data=' + encodeURIComponent(JSON.stringify(payload))
      }).then(response => response.json())
        .then(data => {
          if (data.result === 'successful') {
            console.log('消息已通过 HTTP 成功发送给 Fay:', payload)
            addLog(`[HTTP发送] 消息发送成功: ${text}`)
          } else {
            console.error('Fay 返回错误:', data)
            addLog(`[HTTP发送错误] 消息发送失败: ${data.message}`, 'error')
          }
        }).catch(err => {
          console.error('HTTP 请求异常:', err)
          addLog(`[HTTP请求异常] 无法连接到 Fay HTTP 服务: ${err.message}`, 'error')
        })
        
    } catch (err) {
      console.error('消息发送异常:', err)
      addLog(`[HTTP发送异常] 消息发送失败: ${err.message}`, 'error')
    }
    
    return
  }

  // ==== 以下为离线断网时的本地降级模拟处理 ====
  addMessage('user', text)
  // 模拟网络延迟
  await new Promise(r => setTimeout(r, 500))

  // 解析意图
  const intent = parseIntent(text)
  
  let responseText = ''

  if (intent.type === 'scene') {
    if (intent.scene === 'leave_home') {
      controlDevice('livingRoomLight', 'off')
      controlDevice('bedroomLight', 'off')
      controlDevice('airConditioner', 'off')
      controlDevice('window', 'off')
      controlDevice('curtain', 'off')
      controlDevice('doorLock', 'lock')
      responseText = '已为您开启离家模式，灯光空调已关闭，门窗已锁定，祝您一路平安！'
    } else if (intent.scene === 'go_home') {
      controlDevice('livingRoomLight', 'on')
      controlDevice('airConditioner', 'on')
      controlDevice('curtain', 'on')
      controlDevice('doorLock', 'unlock')
      responseText = '欢迎回家！已为您打开客厅灯和空调，并解锁了门锁。'
    }
  } 
  else if (intent.type === 'query') {
    if (intent.target === 'temperature') {
      responseText = `当前室内温度 ${mockIotDevices.temperature} 度，湿度 ${mockIotDevices.humidity}%，环境非常舒适～`
    } else if (intent.target === 'security') {
      const lockStatus = mockIotDevices.doorLock ? '已锁定' : '未锁定'
      const windowStatus = mockIotDevices.window ? '开启' : '关闭'
      responseText = `当前门锁状态为${lockStatus}，窗户处于${windowStatus}状态。`
      if (!mockIotDevices.doorLock) {
        responseText += ' 提醒您注意关门哦。'
      }
    }
  }
  else if (intent.type === 'control') {
    const result = controlDevice(intent.device, intent.action)
    if (result) {
      responseText = result + '啦～'
    } else {
      responseText = '抱歉，设备操作失败。'
    }
  }
  else {
    // 闲聊兜底
    const chatResponses = [
      '好的呢，我听懂啦！',
      '嗯嗯，Fay在听哦～',
      '您说的很有意思呢。',
      '如果您需要控制家电，可以直接告诉我哦！'
    ]
    responseText = chatResponses[Math.floor(Math.random() * chatResponses.length)]
  }

  // 数字人播报
  simulateSpeak(responseText)
}
</script>