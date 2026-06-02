<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <div class="flex-shrink-0 flex justify-between items-center p-4 md:p-6 border-b border-emerald-500/10">
      <h3 class="text-base md:text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3 tracking-wider">互动控制台</h3>
    </div>

    <div class="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar">
      <div class="max-w-4xl mx-auto pb-12 flex flex-col gap-6 md:gap-8">

        <!-- 主题切换 -->
        <section class="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-4 md:p-5">
          <h4 class="text-emerald-100 font-bold flex items-center gap-2 mb-3 md:mb-4"><Palette class="w-5 h-5 text-emerald-400" /> 全局主题切换</h4>
          <div class="flex gap-2 md:gap-4 flex-wrap">
            <button @click="setTheme('default')" :class="['px-4 md:px-6 py-2 md:py-3 rounded-lg border flex flex-col items-center gap-1 md:gap-2 transition-all', currentTheme === 'default' ? 'border-emerald-400 bg-emerald-500/20 shadow-[0_0_15px_rgba(52,211,153,0.3)] text-emerald-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
              <Moon class="w-5 h-5 md:w-6 md:h-6" />
              <span class="text-xs md:text-sm">极夜模式</span>
            </button>
            <button @click="setTheme('spring_season')" :class="['px-4 md:px-6 py-2 md:py-3 rounded-lg border flex flex-col items-center gap-1 md:gap-2 transition-all', currentTheme === 'spring_season' ? 'border-lime-400 bg-lime-500/20 shadow-[0_0_15px_rgba(132,204,22,0.3)] text-lime-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
              <Leaf class="w-5 h-5 md:w-6 md:h-6" />
              <span class="text-xs md:text-sm">春季主题</span>
            </button>
            <button @click="setTheme('summer')" :class="['px-4 md:px-6 py-2 md:py-3 rounded-lg border flex flex-col items-center gap-1 md:gap-2 transition-all', currentTheme === 'summer' ? 'border-sky-400 bg-sky-500/20 shadow-[0_0_15px_rgba(56,189,248,0.3)] text-sky-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
              <Sun class="w-5 h-5 md:w-6 md:h-6" />
              <span class="text-xs md:text-sm">夏季主题</span>
            </button>
            <button @click="setTheme('autumn')" :class="['px-4 md:px-6 py-2 md:py-3 rounded-lg border flex flex-col items-center gap-1 md:gap-2 transition-all', currentTheme === 'autumn' ? 'border-orange-400 bg-orange-500/20 shadow-[0_0_15px_rgba(249,115,22,0.3)] text-orange-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
              <Wind class="w-5 h-5 md:w-6 md:h-6" />
              <span class="text-xs md:text-sm">秋季主题</span>
            </button>
            <button @click="setTheme('winter')" :class="['px-4 md:px-6 py-2 md:py-3 rounded-lg border flex flex-col items-center gap-1 md:gap-2 transition-all', currentTheme === 'winter' ? 'border-slate-400 bg-slate-500/20 shadow-[0_0_15px_rgba(148,163,184,0.3)] text-slate-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
              <Snowflake class="w-5 h-5 md:w-6 md:h-6" />
              <span class="text-xs md:text-sm">冬季主题</span>
            </button>
          </div>
        </section>

        <!-- 数字人广播 -->
        <section class="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-4 md:p-5">
          <h4 class="text-emerald-100 font-bold flex items-center gap-2 mb-3 md:mb-4"><Mic class="w-5 h-5 text-emerald-400" /> 数字人主动广播</h4>
          <div class="flex flex-col sm:flex-row gap-2">
            <input v-model="broadcastMsg" @keyup.enter="handleBroadcast" type="text" placeholder="输入要让 Fay 播报的紧急通知或导览词..." class="flex-1 bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40" />
            <button @click="handleBroadcast" class="px-4 sm:px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_10px_rgba(52,211,153,0.3)] flex items-center justify-center gap-2 whitespace-nowrap">
              <Send class="w-4 h-4" /> 立即播报
            </button>
          </div>
        </section>

        <!-- 客流模拟器 -->
        <section class="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-4 md:p-5">
          <h4 class="text-emerald-100 font-bold flex items-center gap-2 mb-3 md:mb-4"><Activity class="w-5 h-5 text-emerald-400" /> 客流压力模拟器</h4>
          <p class="text-xs text-emerald-100/50 mb-3 md:mb-4">调整以下景点人数并保存，以在右侧面板及地图上观察拥挤预警联动效果。</p>
          <div class="flex flex-col gap-3">
            <div v-if="loadingSpots" class="text-emerald-400/60 flex items-center gap-2">
              <Loader2 class="w-5 h-5 animate-spin" /> 加载景点数据中...
            </div>
            <div v-else v-for="spot in spotList" :key="spot.id" class="bg-[#020b14] border border-emerald-500/10 p-3 rounded space-y-2 sm:space-y-0 sm:flex sm:items-center sm:gap-4">
              <!-- 景点名称 -->
              <div class="flex items-center justify-between sm:w-32 sm:flex-shrink-0">
                <span class="text-sm font-medium text-emerald-100 truncate">{{ spot.spot_name }}</span>
                <span class="text-[10px] text-emerald-500/50 sm:hidden">{{ spot.temp_visitors }}/{{ spot.max_capacity }}</span>
              </div>
              <!-- 滑动条 -->
              <input type="range" v-model.number="spot.temp_visitors" :max="spot.max_capacity * 1.5" min="0" class="w-full sm:flex-1 accent-emerald-500" />
              <!-- 数值 + 按钮 -->
              <div class="flex items-center gap-2">
                <input type="number" v-model.number="spot.temp_visitors" class="w-20 bg-emerald-900/30 border border-emerald-500/30 rounded px-2 py-1.5 text-sm text-emerald-100 text-center" />
                <span class="text-xs text-emerald-500/60 hidden sm:inline flex-1">/ {{ spot.max_capacity }} MAX</span>
                <button @click="applyFlow(spot)" class="px-3 py-1.5 bg-emerald-500/20 hover:bg-emerald-500/40 border border-emerald-400/50 rounded text-emerald-300 text-xs transition-colors ml-auto sm:ml-0">
                  应用
                </button>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Palette, Moon, Sun, Leaf, Wind, Snowflake, Mic, Send, Activity, Loader2 } from 'lucide-vue-next'
import { getScenicSpots, updateSpotFlow } from '@/api/scenic'
import { sendFayMessage } from '@/api/fay'
import { getConfig, updateConfig } from '@/api/config'
import { Message } from '@/utils/message'

// ================== 主题切换 ==================
const currentTheme = ref(document.documentElement.getAttribute('data-theme') || 'default')

const fetchThemeConfig = async () => {
  try {
    const res = await getConfig('theme')
    if (res && res.status === 'success' && res.data && res.data.value) {
      const theme = res.data.value
      currentTheme.value = theme
      if (theme === 'default') {
        document.documentElement.removeAttribute('data-theme')
      } else {
        document.documentElement.setAttribute('data-theme', theme)
      }
    }
  } catch (error) {
    console.error('获取主题配置失败:', error)
  }
}

const setTheme = async (theme) => {
  currentTheme.value = theme
  if (theme === 'default') {
    document.documentElement.removeAttribute('data-theme')
  } else {
    document.documentElement.setAttribute('data-theme', theme)
  }

  try {
    await updateConfig('theme', theme)
    Message.success('主题已保存')
  } catch (error) {
    Message.error('主题配置保存失败')
  }
}

// ================== 数字人广播 ==================
const broadcastMsg = ref('')

const handleBroadcast = async () => {
  if (!broadcastMsg.value.trim()) return
  try {
    const res = await sendFayMessage(`[系统广播] ${broadcastMsg.value}`)
    if (res && res.result === 'successful') {
      Message.success('广播发送成功，Fay 即将开始播报')
      broadcastMsg.value = ''
    } else {
      Message.warning('广播发送失败')
    }
  } catch (error) {
    Message.error('无法连接到 Fay 服务')
  }
}

// ================== 客流模拟器 ==================
const loadingSpots = ref(false)
const spotList = ref([])

const fetchSpotList = async () => {
  loadingSpots.value = true
  try {
    const res = await getScenicSpots()
    if (res && res.status === 'success') {
      spotList.value = (res.data || []).map(spot => ({
        ...spot,
        temp_visitors: spot.current_visitors || 0
      }))
    }
  } catch (error) {
    console.error('获取景点列表失败:', error)
  } finally {
    loadingSpots.value = false
  }
}

const applyFlow = async (spot) => {
  try {
    const res = await updateSpotFlow(spot.id, spot.temp_visitors)
    if (res && res.status === 'success') {
      Message.success(`${spot.spot_name} 客流更新成功`)
    } else {
      Message.error('客流更新失败')
    }
  } catch (error) {
    Message.error('网络异常，客流更新失败')
  }
}

onMounted(() => {
  fetchThemeConfig()
  fetchSpotList()
})
</script>
