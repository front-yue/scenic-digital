<template>
  <aside class="w-full lg:w-[28%] flex flex-col justify-between transform-style-3d rotate-y-[15deg] origin-left transition-transform duration-500 h-full relative z-20">
    <!-- 模块标题 -->
    <div class="flex items-center gap-3 h-[40px]">
       <div class="flex gap-1">
         <div class="w-1.5 h-6 bg-emerald-400 skew-x-[-15deg] shadow-[0_0_8px_#34d399]"></div>
         <div class="w-1.5 h-6 bg-teal-500 skew-x-[-15deg]"></div>
         <div class="w-1.5 h-6 bg-teal-800 skew-x-[-15deg]"></div>
       </div>
       <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">景区全景概况</h2>
    </div>

    <!-- 卡片 1：景区封面与天气 -->
    <div class="tech-card p-0 flex flex-col relative group border-emerald-500/20 bg-[#021815]/60 overflow-hidden min-h-[160px] shrink-0">
      <div class="absolute inset-0 bg-cover bg-center opacity-40 group-hover:opacity-60 transition-opacity duration-700 group-hover:scale-105" :style="{ backgroundImage: `url(${store.scenicInfo.cover_image})` }"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-[#021815] via-[#021815]/70 to-transparent"></div>
      
      <div class="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-emerald-400 z-10"></div>
      <div class="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-emerald-400 z-10"></div>
      
      <div class="relative z-10 p-5 flex flex-col justify-between h-full">
        <div class="flex justify-end">
           <div class="flex items-center gap-2 text-amber-400 bg-black/40 px-3 py-1.5 rounded-full backdrop-blur-md border border-emerald-500/30">
              <Sun class="w-4 h-4" />
              <span class="text-sm font-bold">{{ store.scenicInfo.weather_temp }}°C</span>
              <div class="w-px h-3 bg-emerald-500/50 mx-1"></div>
              <span class="text-xs text-emerald-100/80">{{ store.scenicInfo.weather_desc }}</span>
           </div>
        </div>
        <div class="mt-auto pt-6">
          <h3 class="text-2xl font-black text-emerald-300 tracking-widest filter drop-shadow-[0_0_5px_#34d399]">{{ store.scenicInfo.scenic_name }}</h3>
          <div class="flex items-center justify-between gap-2 mt-1">
             <p class="text-[10px] text-emerald-400/80 font-mono tracking-widest">{{ store.scenicInfo.scenic_en_name}}</p>
             <div v-if="store.scenicInfo.address" class="flex items-center justify-end gap-1 text-emerald-100/60 text-[11px] group cursor-default max-w-[60%]">
                <MapPin class="w-3 h-3 shrink-0 group-hover:text-emerald-300 transition-colors" />
                <span class="truncate group-hover:text-emerald-300 transition-colors" :title="store.scenicInfo.address">{{ store.scenicInfo.address }}</span>
             </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 卡片 2：详细介绍 -->
    <div class="tech-card flex-1 min-h-[150px] max-h-[250px] p-6 relative flex flex-col gap-3 border-emerald-500/20 bg-[#021815]/60 shrink-0">
      <div class="flex items-center gap-2 mb-2 shrink-0">
        <div class="w-2 h-4 bg-emerald-400"></div>
        <h3 class="text-lg font-bold text-white tracking-wider shrink-0">景区简介</h3>
      </div>
      
      <div 
        ref="introScrollContainer"
        class="overflow-y-auto custom-scrollbar flex-1 pr-2 relative z-10"
        @mouseenter="pauseIntroScroll"
        @mouseleave="resumeIntroScroll"
        @touchstart="pauseIntroScroll"
        @touchend="resumeIntroScroll"
      >
        <div 
          ref="introScrollContent" 
          class="text-sm leading-relaxed text-emerald-50/80 font-light text-justify whitespace-pre-wrap"
        >{{ store.scenicInfo.introduction || '暂无简介' }}</div>
      </div>
      <div class="absolute bottom-0 left-0 w-full h-[30px] bg-gradient-to-t from-[#021815] to-transparent pointer-events-none z-20"></div>
      <div class="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-50 z-20"></div>
    </div>

    <!-- 卡片 3：票务信息 -->
    <div class="flex gap-4 h-[100px] shrink-0">
      <div class="flex-1 tech-card border-emerald-500/20 bg-[#021815]/60 hover:border-emerald-400/80 p-4 flex flex-col justify-center relative overflow-hidden group cursor-pointer transition-all">
        <div class="absolute inset-0 bg-emerald-500/5 group-hover:bg-emerald-500/10 transition-colors"></div>
        <span class="text-xs text-emerald-400/80 font-mono tracking-widest relative z-10 mb-1">成人票价 TICKET</span>
        <div class="flex items-baseline gap-1 relative z-10">
          <span class="text-2xl font-bold text-amber-400 drop-shadow-[0_0_5px_#fbbf24]">¥{{ store.scenicInfo.ticket_price}}</span>
          <span class="text-xs text-emerald-100/50">/人</span>
        </div>
        <Ticket class="absolute right-[-10px] bottom-[-10px] w-16 h-16 text-emerald-500/10 group-hover:text-emerald-500/20 group-hover:scale-110 transition-all -rotate-12" />
      </div>
      
      <div class="flex-1 tech-card border-teal-500/20 bg-[#021815]/60 hover:border-teal-400/80 p-4 flex flex-col justify-center relative overflow-hidden group cursor-pointer transition-all">
        <div class="absolute inset-0 bg-teal-500/5 group-hover:bg-teal-500/10 transition-colors"></div>
        <span class="text-xs text-teal-400/80 font-mono tracking-widest relative z-10 mb-1">营业时间 OPENING</span>
        <div class="text-lg font-bold text-emerald-100 relative z-10 drop-shadow-[0_0_5px_#10b981]">
          {{ store.scenicInfo.opening_hours }}
        </div>
        <ClockIcon class="absolute right-[-10px] bottom-[-10px] w-16 h-16 text-teal-500/10 group-hover:text-teal-500/20 group-hover:scale-110 transition-all rotate-12" />
      </div>
    </div>

    <!-- 卡片 4：推荐游览路线 -->
    <div class="tech-card p-5 flex flex-col gap-3 relative border-emerald-500/20 bg-[#021815]/60 shrink-0 overflow-hidden">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-2 h-4 bg-emerald-400"></div>
          <h3 class="text-md font-bold text-white tracking-wider">推荐游览路线</h3>
        </div>
        <Compass class="w-4 h-4 text-emerald-400/60" />
      </div>

      <!-- 路线 1：经典一日游 -->
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-2">
          <div class="px-2 py-0.5 rounded border border-emerald-400/40 bg-emerald-400/10 text-[10px] text-emerald-300 font-bold">经典线</div>
          <span class="text-[10px] text-emerald-100/50 font-mono">约 3 小时</span>
        </div>
        <div class="flex items-center gap-1 flex-wrap">
          <span v-for="(spot, i) in routeClassic" :key="'c' + i" class="text-xs text-emerald-100/80">
            {{ spot }}<span v-if="i < routeClassic.length - 1" class="text-emerald-500/40 mx-1">→</span>
          </span>
        </div>
      </div>

      <!-- 路线 2：文化深度游 -->
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-2">
          <div class="px-2 py-0.5 rounded border border-teal-400/40 bg-teal-400/10 text-[10px] text-teal-300 font-bold">文化线</div>
          <span class="text-[10px] text-emerald-100/50 font-mono">约 2 小时</span>
        </div>
        <div class="flex items-center gap-1 flex-wrap">
          <span v-for="(spot, i) in routeCulture" :key="'w' + i" class="text-xs text-emerald-100/80">
            {{ spot }}<span v-if="i < routeCulture.length - 1" class="text-emerald-500/40 mx-1">→</span>
          </span>
        </div>
      </div>

      <!-- 底部波浪装饰条 -->
      <div class="h-4 w-full flex items-end gap-[2px] opacity-50 mt-1">
        <div v-for="i in 40" :key="`wave-${i}`" class="flex-1 bg-emerald-500/40 rounded-t-sm" :style="`height: ${20 + Math.random() * 80}%; animation: wave ${0.5 + Math.random()}s infinite alternate;`"></div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Sun, Ticket, Clock as ClockIcon, MapPin, Compass } from 'lucide-vue-next'
import { useScenicStore } from '../../stores/scenic'

const store = useScenicStore()

// 推荐路线数据
const routeClassic = ['断桥残雪', '白堤', '孤山', '苏堤春晓', '雷峰塔']
const routeCulture = ['岳王庙', '西泠印社', '曲院风荷', '三潭印月']

// 自动滚动逻辑
const introScrollContainer = ref(null);
const introScrollContent = ref(null);
let introScrollAnimationId = null;
let isIntroScrolling = true;
let currentScrollTop = 0;

const startIntroAutoScroll = () => {
  const scroll = () => {
    if (isIntroScrolling && introScrollContainer.value && introScrollContent.value) {
      currentScrollTop += 0.2; 
      introScrollContainer.value.scrollTop = currentScrollTop;
      
      const maxScrollTop = introScrollContainer.value.scrollHeight - introScrollContainer.value.clientHeight;
      if (introScrollContainer.value.scrollTop >= maxScrollTop - 1) {
        currentScrollTop = 0;
        introScrollContainer.value.scrollTop = 0;
      }
    }
    introScrollAnimationId = requestAnimationFrame(scroll);
  };
  introScrollAnimationId = requestAnimationFrame(scroll);
};

const pauseIntroScroll = () => {
  isIntroScrolling = false;
};

const resumeIntroScroll = () => {
  isIntroScrolling = true;
  if (introScrollContainer.value) {
    currentScrollTop = introScrollContainer.value.scrollTop;
  }
};

onMounted(() => {
  startIntroAutoScroll();
})

onUnmounted(() => {
  if (introScrollAnimationId) cancelAnimationFrame(introScrollAnimationId);
})
</script>
