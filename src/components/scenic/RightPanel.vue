<template>
  <aside class="w-full lg:w-[28%] flex flex-col justify-between transform-style-3d rotate-y-[-15deg] origin-right transition-transform duration-500 h-full relative z-20">
    <!-- 模块标题 -->
    <div class="flex items-center gap-3 justify-end h-[40px] shrink-0">
       <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">景区景点列表</h2>
       <div class="flex gap-1">
         <div class="w-1.5 h-6 bg-teal-800 skew-x-[15deg]"></div>
         <div class="w-1.5 h-6 bg-teal-500 skew-x-[15deg]"></div>
         <div class="w-1.5 h-6 bg-emerald-400 skew-x-[15deg] shadow-[0_0_8px_#34d399]"></div>
       </div>
    </div>

    <!-- 内容区：景点列表 (滚动) -->
    <div class="flex-1 flex flex-col gap-3 min-h-[300px] overflow-y-auto custom-scrollbar pr-2 mt-4 mb-4">
      <div
        v-for="(spot, index) in store.spotList"
        :key="index"
        class="tech-panel flex items-center gap-4 p-3 cursor-pointer group hover:bg-emerald-500/10 transition-all border border-emerald-500/20 bg-[#021815]/40 rounded-lg relative overflow-hidden shrink-0"
        :class="{ 'border-cyan-400/60 bg-cyan-900/20': activeSpotIndex === index }"
        @click="handleLocateSpot(spot, index)"
      >
         <div class="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-400/5 to-transparent -translate-x-[100%] group-hover:translate-x-[100%] transition-transform duration-700 z-0"></div>
         <!-- 景点缩略图 -->
         <div class="w-16 h-16 rounded-md bg-emerald-900/50 border border-emerald-500/30 flex items-center justify-center shrink-0 z-10 group-hover:border-emerald-400 transition-colors overflow-hidden relative">
            <img :src="spot.image_url" alt="spot" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500" />
            <div class="absolute inset-0 bg-emerald-500/20 mix-blend-overlay"></div>
         </div>
         <div class="flex flex-col flex-1 z-10 min-w-0">
           <div class="flex justify-between items-start gap-2">
              <span class="text-base font-bold text-emerald-50 tracking-wider group-hover:text-emerald-300 transition-colors truncate">{{ spot.spot_name }}</span>
              <!-- 定位按钮 -->
              <button
                class="shrink-0 w-7 h-7 flex items-center justify-center rounded border border-emerald-500/30 bg-emerald-900/30 hover:bg-cyan-500/20 hover:border-cyan-400/50 transition-all group/loc"
                :class="{ 'bg-cyan-500/20 border-cyan-400/50': activeSpotIndex === index }"
                @click.stop="handleLocateSpot(spot, index)"
                title="在地图上定位"
              >
                <MapPin class="w-3.5 h-3.5 text-emerald-400 group-hover/loc:text-cyan-300 transition-colors" :class="{ 'text-cyan-300': activeSpotIndex === index }" />
              </button>
           </div>
           <span class="text-[10px] text-emerald-500/60 font-mono tracking-widest mt-0.5">{{ spot.en_name }}</span>
           <p class="text-xs text-emerald-100/60 mt-1 line-clamp-1">{{ spot.description }}</p>
         </div>
      </div>
    </div>

    <!-- 底部操作按钮 -> 消息输入区与互动按钮 -->
    <div class="mt-auto shrink-0 flex flex-col gap-3">
       <!-- 互动体验区 -->
       <div class="flex items-center gap-2 mb-1">
          <div class="w-1.5 h-1.5 rotate-45" style="background-color: var(--app-primary); box-shadow: 0 0 8px var(--app-primary);"></div>
          <span class="text-xs font-bold tracking-widest" style="color: var(--app-primary);">互动体验</span>
       </div>
       <button
          @click="store.isInteractMode = true"
          class="w-full relative group/btn overflow-hidden rounded-lg border bg-black/30 p-3 transition-all duration-300 hover-border-primary"
          style="border-color: rgba(var(--app-primary-rgb), 0.3);"
       >
          <div class="absolute inset-0 bg-gradient-to-r from-transparent via-[rgba(var(--app-primary-rgb),0.1)] to-transparent -translate-x-full group-hover/btn:translate-x-full transition-transform duration-700"></div>
          <div class="flex items-center gap-3">
             <div class="w-10 h-10 rounded bg-black/50 border flex items-center justify-center group-hover/btn:scale-110 transition-transform" style="border-color: rgba(var(--app-primary-rgb), 0.5);">
                <Camera class="w-5 h-5" style="color: var(--app-primary);" />
             </div>
             <div class="text-left">
                <h3 class="font-bold text-sm" style="color: var(--app-text);">AI 穿越照相馆</h3>
                <p class="text-[10px] mt-0.5 opacity-70" style="color: var(--app-primary);">一键生成景区实景融合海报</p>
             </div>
          </div>
       </button>

       <!-- 消息输入区 -->
       <div class="h-12 w-full flex relative group mt-1">
         <input
            v-model="chatMessage"
            @keyup.enter="handleSendMessage"
            type="text"
            placeholder="向 Fay 发送消息..."
            class="w-full h-full bg-[#021815]/80 border-2 border-emerald-500/30 rounded-lg pl-4 pr-12 text-sm text-emerald-100 tracking-wider placeholder-emerald-500/50 focus:outline-none focus:border-emerald-400 focus:shadow-[0_0_15px_rgba(52,211,153,0.3)] transition-all"
         />
         <button
            @click="handleSendMessage"
            :disabled="isSending || !chatMessage.trim()"
            class="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center bg-emerald-500/20 hover:bg-emerald-500/40 rounded text-emerald-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
         >
            <Send class="w-4 h-4" :class="{'animate-pulse': isSending}" />
         </button>
       </div>
    </div>

  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { Send, Camera, MapPin } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import { useAvatarStore } from '@/stores/avatar'
import { sendFayMessage } from '@/api/fay'
import { Message } from '@/utils/message'

const store = useScenicStore()
const avatarStore = useAvatarStore()

const emit = defineEmits(['locate-spot'])

const chatMessage = ref('')
const isSending = ref(false)
const activeSpotIndex = ref(-1)

const handleLocateSpot = (spot, index) => {
  if (spot.latitude && spot.longitude) {
    activeSpotIndex.value = index
    emit('locate-spot', {
      latitude: Number(spot.latitude),
      longitude: Number(spot.longitude),
      name: spot.spot_name
    })
  } else {
    Message.info('该景点暂无坐标数据')
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
    console.error('发送消息失败:', error)
    Message.error('服务连接异常')
  } finally {
    isSending.value = false
  }
}
</script>

<style scoped>
.hover-border-primary:hover {
  border-color: var(--app-primary) !important;
}
</style>
