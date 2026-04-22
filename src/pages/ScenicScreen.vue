 <template>
  <div class="h-screen w-full bg-[#021114] text-[#a7f3d0] font-sans relative overflow-hidden tech-bg flex flex-col">
    
    <!-- 全局 Canvas 粒子背景 -->
    <canvas ref="particleCanvas" class="absolute inset-0 z-0 opacity-60"></canvas>

    <!-- 全局背景光晕与网格特效 -->
    <div class="absolute inset-0 pointer-events-none z-0">
      <div class="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[80%] h-[600px] bg-[#0d9488]/20 blur-[150px] rounded-[100%]"></div>
      <div class="absolute bottom-[-10%] left-1/2 -translate-x-1/2 w-[100%] h-[400px] bg-[#10b981]/15 blur-[150px] rounded-[100%]"></div>
    </div>

    <!-- ================= 顶部标题栏 ================= -->
    <header class="w-full flex items-start justify-center relative z-20 shrink-0 h-[100px]">
      <div class="relative w-full h-full max-w-[1920px] flex justify-between items-start">
        
        <div class="relative w-[30%] h-full">
           <div class="absolute top-0 left-0 w-full h-[60px] bg-gradient-to-r from-[#00f0ff]/10 to-transparent skew-x-[-30deg] origin-top border-b border-cyan-500/30"></div>
           <div class="absolute top-0 left-0 w-full h-full flex flex-col items-start justify-center px-8">
              <div class="flex items-center gap-3 text-cyan-300">
                <ClockIcon class="w-5 h-5 animate-pulse" />
                <span class="text-xl md:text-2xl font-mono font-bold tracking-wider text-shadow-glow">{{ currentTime }}</span>
              </div>
              <span class="text-sm text-cyan-500/80 tracking-widest font-mono mt-1 ml-8">{{ currentDate }}</span>
           </div>
        </div>

        <div class="relative flex flex-col justify-start items-center w-[40%] h-full pt-4">
          <div class="relative w-full max-w-[600px] h-[50px] flex items-center justify-center">
            <div class="absolute inset-0 bg-[#061226]/90 backdrop-blur-md border-x-2 border-cyan-400 shadow-[0_0_30px_rgba(0,240,255,0.15)]" style="clip-path: polygon(5% 0, 95% 0, 100% 50%, 95% 100%, 5% 100%, 0% 50%);"></div>
            
            <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[80%] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent"></div>
            <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[80%] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent"></div>

            <h1 class="relative text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-emerald-300 tracking-[0.2em] z-10 filter drop-shadow-[0_0_12px_rgba(52,211,153,0.8)]">
              智慧文旅数字人体验平台
            </h1>
            
            <div class="absolute left-6 w-2 h-2 bg-cyan-400 rotate-45 shadow-[0_0_8px_#00f0ff] animate-pulse"></div>
            <div class="absolute right-6 w-2 h-2 bg-cyan-400 rotate-45 shadow-[0_0_8px_#00f0ff] animate-pulse"></div>
          </div>

          <div class="relative w-full max-w-[400px] h-[20px] mt-2 flex justify-center items-center gap-4 opacity-70">
            <div class="flex-1 h-[1px] bg-cyan-500/50 relative">
               <div class="absolute right-0 top-1/2 -translate-y-1/2 w-16 h-[3px] bg-cyan-400"></div>
            </div>
            <div class="cursor-pointer group" @click="versionVisible = true">
              <div class="flex items-center gap-1.5 px-3 py-1 rounded-full border border-cyan-500/30 bg-cyan-900/20 backdrop-blur-md group-hover:bg-cyan-500/20 transition-all shadow-[0_0_10px_rgba(0,240,255,0.08)] group-hover:shadow-[0_0_15px_rgba(0,240,255,0.25)]">
                <div class="w-1.5 h-1.5 bg-cyan-400 rotate-45 shadow-[0_0_8px_#00f0ff]"></div>
                <span class="text-xs text-cyan-400/80 tracking-[0.2em] font-mono group-hover:text-cyan-300">SYS KERNEL V3.0</span>
                <div class="w-1.5 h-1.5 bg-cyan-400 rotate-45 shadow-[0_0_8px_#00f0ff]"></div>
              </div>
            </div>
            <div class="flex-1 h-[1px] bg-cyan-500/50 relative">
               <div class="absolute left-0 top-1/2 -translate-y-1/2 w-16 h-[3px] bg-cyan-400"></div>
            </div>
          </div>
        </div>

        <div class="relative w-[30%] h-[60px]">
           <div class="absolute top-0 right-0 w-full h-[60px] bg-gradient-to-l from-[#00f0ff]/10 to-transparent skew-x-[30deg] origin-top border-b border-cyan-500/30"></div>
           <div class="absolute top-0 right-0 w-full h-full flex flex-col items-end justify-center px-8">
              <div class="cursor-pointer group" @click="adminVisible = true">
                <div class="flex items-center gap-2 px-4 py-1.5 rounded-full border border-cyan-500/30 bg-cyan-900/20 backdrop-blur-md group-hover:bg-cyan-500/20 transition-all shadow-[0_0_15px_rgba(0,240,255,0.1)] group-hover:shadow-[0_0_20px_rgba(0,240,255,0.3)]">
                  <DatabaseIcon class="w-4 h-4 text-cyan-300 group-hover:text-white" />
                  <span class="text-sm font-bold text-cyan-300 tracking-widest group-hover:text-white">控制台</span>
                </div>
              </div>
           </div>
        </div>
      </div>
    </header>

    <!-- ================= 顶部弧形装饰线 ================= -->
    <div class="absolute top-0 left-0 w-full h-[150px] pointer-events-none z-0 overflow-hidden flex justify-center">
      <div class="w-[120%] h-[300px] border-b-[2px] border-cyan-500/50 rounded-[50%] absolute top-[-165px] shadow-[0_10px_20px_rgba(0,240,255,0.2)]"></div>
      <div class="absolute top-[134px] w-[50%] max-w-[600px] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent shadow-[0_0_15px_#00f0ff]"></div>
    </div>

    <!-- ================= 底部弧形装饰线 ================= -->
    <div class="absolute bottom-0 left-0 w-full h-[150px] pointer-events-none z-0 overflow-hidden flex justify-center">
      <div class="w-[120%] h-[300px] border-t-[2px] border-cyan-500/50 rounded-[50%] absolute bottom-[-260px] shadow-[0_-10px_20px_rgba(0,240,255,0.2)]"></div>
      <div class="absolute bottom-[39px] w-[50%] max-w-[600px] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent shadow-[0_0_15px_#00f0ff]"></div>
    </div>

    <!-- ================= 主体内容区 ================= -->
    <main class="flex-1 w-full max-w-[1800px] mx-auto p-4 lg:p-6 flex flex-col lg:flex-row items-stretch gap-10 relative z-10 perspective-[1500px] min-h-0 pb-8 pt-4">
      
      <LeftPanel />
      <CenterPanel />
      <RightPanel />

    </main>

    <!-- 管理后台弹窗组件 -->
    <AdminOverlay v-model:visible="adminVisible" @data-updated="store.refreshAllData" />

    <!-- 版本信息弹窗 -->
    <VersionModal  :visible="versionVisible"  @update:visible="versionVisible = $event"/>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { Clock as ClockIcon, Database as DatabaseIcon } from 'lucide-vue-next'

import LeftPanel from '@/components/scenic/LeftPanel.vue'
import CenterPanel from '@/components/scenic/CenterPanel.vue'
import RightPanel from '@/components/scenic/RightPanel.vue'
import AdminOverlay from '@/components/admin/AdminOverlay.vue'
import VersionModal from '@/components/common/VersionModal.vue'

import { useScenicStore } from '@/stores/scenic'

const store = useScenicStore()

// 动态时间
const currentTime = ref('');
const currentDate = ref('');
let timeInterval;

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false });
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
};

// 弹窗状态
const adminVisible = ref(false);
const versionVisible = ref(false);

// =========== Canvas 背景粒子特效 ===========
const particleCanvas = ref(null)
let animationFrameId = null
let handleResize = null 

const initParticleCanvas = () => {
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
      this.size = Math.random() * 2 + 0.5
      this.speedX = Math.random() * 1 - 0.5
      this.speedY = Math.random() * 1 - 0.5
      this.color = Math.random() > 0.5 ? '#10b981' : '#34d399'
      this.opacity = Math.random() * 0.5 + 0.2
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
    const numberOfParticles = (canvas.width * canvas.height) / 15000
    for (let i = 0; i < numberOfParticles; i++) {
      particlesArray.push(new Particle())
    }
  }
  
  const connect = () => {
    for (let a = 0; a < particlesArray.length; a++) {
      for (let b = a; b < particlesArray.length; b++) {
        const dx = particlesArray[a].x - particlesArray[b].x
        const dy = particlesArray[a].y - particlesArray[b].y
        const distance = dx * dx + dy * dy
        
        if (distance < 12000) {
          ctx.globalAlpha = 1 - distance / 12000
          ctx.strokeStyle = '#10b981'
          ctx.lineWidth = 0.5
          ctx.beginPath()
          ctx.moveTo(particlesArray[a].x, particlesArray[a].y)
          ctx.lineTo(particlesArray[b].x, particlesArray[b].y)
          ctx.stroke()
        }
      }
    }
    ctx.globalAlpha = 1
  }
  
  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for (let i = 0; i < particlesArray.length; i++) {
      particlesArray[i].update()
      particlesArray[i].draw()
    }
    connect()
    animationFrameId = requestAnimationFrame(animate)
  }
  
  init()
  animate()
}

const startClock = () => {
  updateTime();
  timeInterval = setInterval(updateTime, 1000);
}

onMounted(() => {
  store.refreshAllData();
  initParticleCanvas();
  startClock();
})

onUnmounted(() => {
  if (handleResize) window.removeEventListener('resize', handleResize)
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  if (timeInterval) clearInterval(timeInterval);
})
</script>

<style scoped>
.tech-bg {
  background-image: 
    linear-gradient(rgba(0, 150, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 150, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: center center;
}

.text-shadow-glow {
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.8), 0 0 20px rgba(0, 100, 255, 0.5);
}

/* 3D */
.perspective-\[1500px\] {
  perspective: 1500px;
}
</style>

<style>
/* 包含原来提取到子组件的公共样式 */
.tech-card {
  background: linear-gradient(135deg, rgba(6, 18, 38, 0.8) 0%, rgba(2, 9, 26, 0.9) 100%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  box-shadow: inset 0 0 20px rgba(0, 150, 255, 0.05);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  clip-path: polygon(0 15px, 15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%);
}

.tech-hex-btn {
  width: 44px;
  height: 48px;
  background: rgba(0, 240, 255, 0.05);
  border: 1px solid rgba(0, 240, 255, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
}
.tech-hex-btn:hover {
  background: rgba(0, 240, 255, 0.2);
  border-color: #00f0ff;
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
}

.transform-style-3d {
  transform-style: preserve-3d;
}
.origin-left { transform-origin: left center; }
.origin-right { transform-origin: right center; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
.animate-float { animation: float 4s ease-in-out infinite; }

@keyframes scanline {
  0% { top: 0; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
.animate-scanline { animation: scanline 3s linear infinite; }

@keyframes ripple {
  0% { transform: scale(0.8); opacity: 1; border-width: 2px; }
  100% { transform: scale(1.5); opacity: 0; border-width: 0px; }
}
.animate-ripple-1 { animation: ripple 3s cubic-bezier(0.4, 0, 0.2, 1) infinite; }
.animate-ripple-2 { animation: ripple 3s cubic-bezier(0.4, 0, 0.2, 1) infinite 1.5s; }

@keyframes pulseCore {
  0%, 100% { transform: scale(0.9); opacity: 0.6; }
  50% { transform: scale(1.1); opacity: 1; }
}
.animate-pulse-core { animation: pulseCore 2s ease-in-out infinite; }

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(16, 185, 129, 0.05); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(16, 185, 129, 0.3); border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(16, 185, 129, 0.6); }
</style>
