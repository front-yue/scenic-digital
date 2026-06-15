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

    <!-- 底部操作区 -->
    <div class="mt-auto shrink-0 flex flex-col gap-2">
       <!-- 对话记录（输入框上方） -->
       <div ref="chatListRef" v-if="avatarStore.chatMessages.length" class="max-h-[200px] overflow-y-auto custom-scrollbar pr-1">
         <TransitionGroup name="chat-msg" tag="div" class="flex flex-col gap-1.5">
           <div
             v-for="(msg, i) in avatarStore.chatMessages.slice(-8)"
             :key="msg.role + '-' + i"
             class="flex items-start gap-1.5"
             :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
           >
             <span v-if="msg.role === 'ai'" class="shrink-0 mt-1 w-1 h-1 rounded-full bg-emerald-400 shadow-[0_0_3px_#34d399]"></span>
             <p
               class="text-[11px] leading-relaxed max-w-[88%] px-2.5 py-1.5 rounded-lg"
               :class="msg.role === 'user'
                 ? 'bg-emerald-500/15 text-emerald-100/90 border border-emerald-500/25'
                 : 'bg-black/20 text-emerald-200/70 border border-emerald-500/10'"
             >{{ msg.content }}</p>
             <span v-if="msg.role === 'user'" class="shrink-0 mt-1 w-1 h-1 rounded-full bg-emerald-300/60"></span>
           </div>
         </TransitionGroup>
       </div>

       <!-- 消息输入区 -->
       <div class="h-11 w-full flex relative group">
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
import { ref, watch, nextTick } from 'vue'
import { Send, MapPin } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import { useAvatarStore } from '@/stores/avatar'
import { sendFayMessage } from '@/api/fay'
import { Message } from '@/utils/message'

const store = useScenicStore()
const avatarStore = useAvatarStore()

// 自动滚动到底部
const chatListRef = ref(null)
watch(() => avatarStore.chatMessages.length, () => {
  nextTick(() => {
    if (chatListRef.value) {
      chatListRef.value.scrollTop = chatListRef.value.scrollHeight
    }
  })
})

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
  const text = chatMessage.value.trim()

  isSending.value = true
  try {
    const res = await sendFayMessage(text)
    if (res && res.result === 'successful') {
      avatarStore.addChatMessage('user', text)
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
/* 对话消息动画 */
.chat-msg-enter-active { transition: all 0.3s ease-out; }
.chat-msg-leave-active { transition: all 0.2s ease-in; }
.chat-msg-enter-from { opacity: 0; transform: translateY(6px); }
.chat-msg-leave-to { opacity: 0; transform: translateY(-4px); }
.chat-msg-move { transition: transform 0.3s ease; }
</style>
