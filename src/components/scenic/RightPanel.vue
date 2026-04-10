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
      <div v-for="(spot, index) in store.spotList" :key="index" class="tech-panel flex items-center gap-4 p-3 cursor-pointer group hover:bg-emerald-500/10 transition-all border border-emerald-500/20 bg-[#021815]/40 rounded-lg relative overflow-hidden shrink-0">
         <div class="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-400/5 to-transparent -translate-x-[100%] group-hover:translate-x-[100%] transition-transform duration-700 z-0"></div>
         <!-- 景点缩略图 -->
         <div class="w-16 h-16 rounded-md bg-emerald-900/50 border border-emerald-500/30 flex items-center justify-center shrink-0 z-10 group-hover:border-emerald-400 transition-colors overflow-hidden relative">
            <img :src="spot.image_url" alt="spot" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500" />
            <div class="absolute inset-0 bg-emerald-500/20 mix-blend-overlay"></div>
         </div>
         <div class="flex flex-col flex-1 z-10">
           <div class="flex justify-between items-start">
              <span class="text-base font-bold text-emerald-50 tracking-wider group-hover:text-emerald-300 transition-colors">{{ spot.spot_name }}</span>
              <span :class="['text-[10px] px-2 py-0.5 rounded-sm border whitespace-nowrap', spot.status === '良好畅通' ? 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10' : (spot.status === '拥挤预警' ? 'text-red-400 border-red-400/30 bg-red-400/10' : 'text-amber-400 border-amber-400/30 bg-amber-400/10')]">{{ spot.status }}</span>
           </div>
           <span class="text-[10px] text-emerald-500/60 font-mono tracking-widest mt-0.5">{{ spot.en_name }}</span>
           <p class="text-xs text-emerald-100/60 mt-1 line-clamp-1">{{ spot.description }}</p>
         </div>
      </div>
    </div>

    <!-- 底部操作按钮 -->
    <button @click="handleManualSpeak" class="mt-auto shrink-0 h-14 w-full bg-gradient-to-r from-teal-600 to-emerald-500 rounded-lg font-bold text-white tracking-[0.2em] shadow-[0_0_20px_rgba(52,211,153,0.4)] hover:shadow-[0_0_30px_rgba(52,211,153,0.6)] hover:scale-[1.02] transition-all flex items-center justify-center gap-2 relative overflow-hidden group">
       <div class="absolute inset-0 bg-white/20 -translate-x-full group-hover:translate-x-full transition-transform duration-700 skew-x-[-20deg]"></div>
       <Navigation class="w-5 h-5" />
       <span>唤醒伴游向导</span>
    </button>

  </aside>
</template>

<script setup>
import { Navigation } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import { useAvatarStore } from '@/stores/avatar'
import { Message } from '@/utils/message'

const store = useScenicStore()
const avatarStore = useAvatarStore()

const handleManualSpeak = () => {
  if (avatarStore.isReady) {
    const statusText = store.overallStatus.replace(/🟢|🟡|🔴|\s/g, '')
    const greeting = `欢迎来到${store.scenicInfo.scenic_name || '智慧文旅大屏'}，我是您的专属数字向导。当前在园人数为${store.totalVisitors}人，游览环境${statusText}。祝您游玩愉快！`
    avatarStore.speak(greeting)
  } else {
    Message.warning('数字人引擎尚未就绪，请稍后再试。')
  }
}
</script>
