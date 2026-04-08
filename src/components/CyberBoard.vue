<template>
  <div class="h-screen w-full bg-[#070b19] text-[#a5f3ff] font-sans relative overflow-hidden tech-bg flex flex-col">
    
    <!-- 全局 Canvas 粒子背景 -->
    <canvas ref="particleCanvas" class="absolute inset-0 z-0 opacity-60"></canvas>

    <!-- 全局背景光晕与网格特效 -->
    <div class="absolute inset-0 pointer-events-none z-0">
      <div class="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[80%] h-[600px] bg-[#0055ff]/10 blur-[150px] rounded-[100%]"></div>
      <div class="absolute bottom-[-10%] left-1/2 -translate-x-1/2 w-[100%] h-[400px] bg-[#00e5ff]/10 blur-[150px] rounded-[100%]"></div>
    </div>

    <!-- ================= 顶部标题栏 ================= -->
    <header class="w-full flex items-start justify-center relative z-20 shrink-0 h-[100px]">
      <div class="relative w-full h-full max-w-[1920px] flex justify-between items-start">
        
        <!-- 左侧装饰与动态时间 (向下延伸填补空档) -->
        <div class="relative w-[30%] h-full">
           <!-- 背景装饰面 -->
           <div class="absolute top-0 left-0 w-full h-[60px] bg-gradient-to-r from-[#00f0ff]/10 to-transparent skew-x-[-30deg] origin-top border-b border-cyan-500/30"></div>
           <div class="absolute top-0 left-0 w-full h-full flex flex-col items-start justify-center px-8">
              <div class="flex items-center gap-3 text-cyan-300">
                <ClockIcon class="w-5 h-5 animate-pulse" />
                <span class="text-xl md:text-2xl font-mono font-bold tracking-wider text-shadow-glow">{{ currentTime }}</span>
              </div>
              <span class="text-sm text-cyan-500/80 tracking-widest font-mono mt-1 ml-8">{{ currentDate }}</span>
           </div>
        </div>

        <!-- 中间标题区域 (悬浮下压) -->
        <div class="relative flex flex-col justify-start items-center w-[40%] h-full pt-4">
          <!-- 标题主体 (六边形切割) -->
          <div class="relative w-full max-w-[600px] h-[50px] flex items-center justify-center">
            <!-- 复杂的六边形背景框 -->
            <div class="absolute inset-0 bg-[#061226]/90 backdrop-blur-md border-x-2 border-cyan-400 shadow-[0_0_30px_rgba(0,240,255,0.15)]" style="clip-path: polygon(5% 0, 95% 0, 100% 50%, 95% 100%, 5% 100%, 0% 50%);"></div>
            
            <!-- 顶部高光线 -->
            <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[80%] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent"></div>
            <!-- 底部高光线 -->
            <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[80%] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent"></div>

            <!-- 标题文字 -->
            <h1 class="relative text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-cyan-300 tracking-[0.2em] z-10 filter drop-shadow-[0_0_12px_rgba(0,255,255,0.8)]">
              智慧数字人视界
            </h1>
            
            <!-- 左右装饰点 -->
            <div class="absolute left-6 w-2 h-2 bg-cyan-400 rotate-45 shadow-[0_0_8px_#00f0ff] animate-pulse"></div>
            <div class="absolute right-6 w-2 h-2 bg-cyan-400 rotate-45 shadow-[0_0_8px_#00f0ff] animate-pulse"></div>
          </div>

          <!-- 标题下方的科幻排线装饰 (向下延伸填补空档) -->
          <div class="relative w-full max-w-[400px] h-[20px] mt-2 flex justify-center items-center gap-4 opacity-70">
            <div class="flex-1 h-[1px] bg-cyan-500/50 relative">
               <div class="absolute right-0 top-1/2 -translate-y-1/2 w-16 h-[3px] bg-cyan-400"></div>
            </div>
            <div class="flex gap-1">
              <div class="w-1.5 h-1.5 bg-blue-500 rotate-45"></div>
              <div class="w-1.5 h-1.5 bg-cyan-400 rotate-45"></div>
              <div class="w-1.5 h-1.5 bg-blue-500 rotate-45"></div>
            </div>
            <div class="flex-1 h-[1px] bg-cyan-500/50 relative">
               <div class="absolute left-0 top-1/2 -translate-y-1/2 w-16 h-[3px] bg-cyan-400"></div>
            </div>
          </div>
        </div>

        <!-- 右侧装饰与系统状态 (向下延伸填补空档) -->
        <div class="relative w-[30%] h-full">
           <!-- 背景装饰面 -->
           <div class="absolute top-0 right-0 w-full h-[60px] bg-gradient-to-l from-[#00f0ff]/10 to-transparent skew-x-[30deg] origin-top border-b border-cyan-500/30"></div>
           <div class="absolute top-0 right-0 w-full h-full flex flex-col items-end justify-center px-8">
              <div class="flex items-center gap-3">
                <div class="w-2.5 h-2.5 rounded-full bg-green-400 animate-pulse shadow-[0_0_10px_#4ade80]"></div>
                <span class="text-lg font-bold text-green-400 tracking-wider">SYSTEM ONLINE</span>
              </div>
              <span class="text-sm text-cyan-500/80 tracking-widest font-mono mt-1 mr-6">FAY KERNEL V3.0</span>
           </div>
        </div>

      </div>
    </header>

    <!-- ================= 顶部弧形装饰线 ================= -->
    <div class="absolute top-0 left-0 w-full h-[150px] pointer-events-none z-0 overflow-hidden flex justify-center">
      <div class="w-[120%] h-[300px] border-b-[2px] border-cyan-500/50 rounded-[50%] absolute top-[-165px] shadow-[0_10px_20px_rgba(0,240,255,0.2)]"></div>
      <!-- 装饰光点/线段 -->
      <div class="absolute top-[134px] w-[50%] max-w-[600px] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent shadow-[0_0_15px_#00f0ff]"></div>
    </div>

    <!-- ================= 底部弧形装饰线 ================= -->
    <div class="absolute bottom-0 left-0 w-full h-[150px] pointer-events-none z-0 overflow-hidden flex justify-center">
      <div class="w-[120%] h-[300px] border-t-[2px] border-cyan-500/50 rounded-[50%] absolute bottom-[-260px] shadow-[0_-10px_20px_rgba(0,240,255,0.2)]"></div>
      <!-- 装饰光点/线段 -->
      <div class="absolute bottom-[39px] w-[50%] max-w-[600px] h-[2px] bg-gradient-to-r from-transparent via-cyan-300 to-transparent shadow-[0_0_15px_#00f0ff]"></div>
    </div>

    <!-- ================= 主体内容区 (内容区铺满剩余高度) ================= -->
    <main class="flex-1 w-full max-w-[1800px] mx-auto p-4 lg:p-6 flex flex-col lg:flex-row items-stretch gap-10 relative z-10 perspective-[1500px] min-h-0 pb-8 pt-4">
      
      <!-- 【左侧面板】：品牌/项目信息区 (向内翻转) -->
      <aside class="w-full lg:w-[28%] flex flex-col gap-4 transform-style-3d rotate-y-[15deg] origin-left transition-transform duration-500 hover:rotate-y-[5deg] h-full relative z-20">
        <!-- 模块标题 (固定高度占位，确保两侧标题高度一致) -->
        <div class="flex items-center gap-3 h-[40px]">
           <div class="flex gap-1">
             <div class="w-1.5 h-6 bg-cyan-400 skew-x-[-15deg] shadow-[0_0_8px_#00f0ff]"></div>
             <div class="w-1.5 h-6 bg-blue-500 skew-x-[-15deg]"></div>
             <div class="w-1.5 h-6 bg-blue-800 skew-x-[-15deg]"></div>
           </div>
           <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">核心介绍</h2>
        </div>

        <!-- 卡片 1：LOGO与名称 -->
        <div class="tech-card p-6 flex flex-col items-center justify-center gap-4 relative group">
          <!-- 装饰角 -->
          <div class="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-cyan-400"></div>
          <div class="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-cyan-400"></div>
          
          <div class="relative w-20 h-20 flex items-center justify-center">
            <!-- 旋转六边形 -->
            <div class="absolute inset-0 border border-cyan-400/50 rounded-full animate-[spin_10s_linear_infinite] border-t-cyan-300 border-b-cyan-300"></div>
            <div class="absolute inset-2 border border-blue-500/50 rounded-full animate-[spin_6s_linear_infinite_reverse] border-l-blue-400 border-r-blue-400"></div>
            <HexagonIcon class="w-12 h-12 text-cyan-300 filter drop-shadow-[0_0_8px_#00f0ff]" />
          </div>
          <div class="text-2xl font-black text-white tracking-widest uppercase filter drop-shadow-[0_0_5px_#fff]">BRAND LOGO</div>
        </div>

        <!-- 卡片 2：详细信息 -->
        <div class="tech-card flex-1 p-6 relative flex flex-col gap-3">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-2 h-4 bg-cyan-400"></div>
            <h3 class="text-lg font-bold text-white tracking-wider">项目愿景</h3>
          </div>
          <p class="text-sm leading-relaxed text-blue-100/80 font-light text-justify">
            本展示平台致力于提供前沿的 AI 数字人交互体验。通过先进的虚拟现实技术与大语言模型深度融合，我们为品牌展示、智能导览、沉浸式互动等场景提供全方位的数字孪生解决方案。科技赋能，开启智能未来新纪元。
          </p>
          <p class="text-sm leading-relaxed text-blue-100/80 font-light text-justify mt-2">
            采用模块化架构设计，支持高度定制化的交互场景，无论是企业展厅还是元宇宙入口，皆能完美适配。
          </p>
          <!-- 装饰扫光 -->
          <div class="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-cyan-400 to-transparent opacity-50"></div>
        </div>

        <!-- 卡片 3：数据/里程碑 -->
        <div class="flex gap-4 h-[100px]">
          <div class="flex-1 tech-card-alt border-cyan-500/30 hover:border-cyan-400/80 p-3 flex flex-col justify-center items-center gap-1 group cursor-pointer">
            <div class="text-xs text-cyan-400/60 font-mono tracking-widest">USERS</div>
            <div class="text-2xl font-bold text-cyan-100 group-hover:text-white transition-colors drop-shadow-[0_0_5px_#00f0ff]">12,500+</div>
          </div>
          <div class="flex-1 tech-card-alt border-blue-500/30 hover:border-blue-400/80 p-3 flex flex-col justify-center items-center gap-1 group cursor-pointer">
            <div class="text-xs text-blue-400/60 font-mono tracking-widest">UPTIME</div>
            <div class="text-2xl font-bold text-blue-100 group-hover:text-white transition-colors drop-shadow-[0_0_5px_#3b82f6]">99.9%</div>
          </div>
        </div>

        <!-- 卡片 4：动态系统监控 (填补空白区域) -->
        <div class="tech-card flex-1 p-5 relative flex flex-col gap-4 overflow-hidden">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-2 h-4 bg-blue-500"></div>
              <h3 class="text-md font-bold text-white tracking-wider">系统监控</h3>
            </div>
            <div class="flex gap-1">
              <div class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></div>
              <span class="text-xs text-cyan-400 font-mono">LIVE</span>
            </div>
          </div>
          
          <div class="flex-1 flex flex-col gap-3 justify-center">
             <!-- CPU 负载条 -->
             <div>
               <div class="flex justify-between text-xs font-mono text-cyan-300/70 mb-1">
                 <span>CPU 算力分配</span>
                 <span class="text-cyan-300">68%</span>
               </div>
               <div class="w-full h-1.5 bg-blue-900/50 rounded overflow-hidden">
                 <div class="h-full bg-gradient-to-r from-cyan-500 to-blue-400 w-[68%] relative">
                   <div class="absolute top-0 right-0 bottom-0 w-4 bg-white/50 blur-[2px]"></div>
                 </div>
               </div>
             </div>
             <!-- 内存占用条 -->
             <div>
               <div class="flex justify-between text-xs font-mono text-cyan-300/70 mb-1">
                 <span>模型显存占用</span>
                 <span class="text-cyan-300">42%</span>
               </div>
               <div class="w-full h-1.5 bg-blue-900/50 rounded overflow-hidden">
                 <div class="h-full bg-gradient-to-r from-blue-500 to-indigo-400 w-[42%] relative">
                   <div class="absolute top-0 right-0 bottom-0 w-4 bg-white/50 blur-[2px]"></div>
                 </div>
               </div>
             </div>
             <!-- 动态波形图 (纯CSS实现) -->
             <div class="mt-2 h-10 w-full flex items-end gap-1 opacity-60">
                <div v-for="i in 30" :key="`wave-${i}`" class="flex-1 bg-cyan-500/50 rounded-t-sm" :style="`height: ${Math.random() * 100}%; animation: wave ${0.5 + Math.random()}s infinite alternate;`"></div>
             </div>
          </div>
        </div>
      </aside>

      <!-- 【中间面板】：数字人全息展示区 (内容区内铺满高度，顶部与两侧卡片内部持平) -->
      <section class="flex-1 w-full lg:w-[40%] relative flex flex-col items-center justify-center bg-[#061226]/40 backdrop-blur-md rounded-2xl tech-center-panel shadow-[inset_0_0_60px_rgba(0,240,255,0.05)] transform-style-3d transition-transform duration-500 mt-[60px] mb-[30px] h-[calc(100%-90px)] mx-4">
        
        <!-- 内部实际展示区边框 (根据红线要求，向内收缩对齐左右卡片的实际内边框) -->
        <div class="absolute inset-x-0 top-0 bottom-0 border border-cyan-500/50 rounded-2xl pointer-events-none"></div>

        <!-- 四角高亮装饰 (经典的 UI 准星设计) -->
        <div class="absolute top-0 left-0 w-12 h-12 border-t-2 border-l-2 border-cyan-400 rounded-tl-2xl pointer-events-none opacity-50"></div>
        <div class="absolute top-0 right-0 w-12 h-12 border-t-2 border-r-2 border-cyan-400 rounded-tr-2xl pointer-events-none opacity-50"></div>
        <div class="absolute bottom-0 left-0 w-12 h-12 border-b-2 border-l-2 border-cyan-400 rounded-bl-2xl pointer-events-none opacity-50"></div>
        <div class="absolute bottom-0 right-0 w-12 h-12 border-b-2 border-r-2 border-cyan-400 rounded-br-2xl pointer-events-none opacity-50"></div>

        <!-- 顶部标签 -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2 bg-cyan-400/20 border border-cyan-400/50 px-8 py-1 rounded-b-lg backdrop-blur-sm">
          <span class="text-sm font-bold text-cyan-300 tracking-[0.3em]">全息展示舱</span>
        </div>

        <!-- 左侧悬浮挂件 -->
        <div class="absolute left-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
           <div class="tech-hex-btn">
              <SettingsIcon class="w-5 h-5 text-cyan-300" />
           </div>
           <div class="tech-hex-btn">
              <CpuIcon class="w-5 h-5 text-cyan-300" />
           </div>
        </div>

        <!-- 右侧悬浮挂件 -->
        <div class="absolute right-4 top-1/2 -translate-y-1/2 flex flex-col gap-4">
           <div class="tech-hex-btn">
              <FileTextIcon class="w-5 h-5 text-cyan-300" />
           </div>
           <div class="tech-hex-btn">
              <ActivityIcon class="w-5 h-5 text-cyan-300" />
           </div>
        </div>

        <!-- 数字人模型占位区 (核心视觉焦点) -->
        <div class="relative z-20 h-[65%] w-full flex flex-col items-center justify-end pb-[100px]">
           <div class="w-64 h-[400px] flex flex-col items-center justify-center text-cyan-300/50 mix-blend-screen relative animate-float">
              <!-- 移除粗糙的光柱，保持干净 -->
              <UserIcon class="w-32 h-32 mb-4 opacity-70 filter drop-shadow-[0_0_15px_#00f0ff]" />
              <span class="font-mono font-bold tracking-[0.3em] text-lg text-shadow-glow">3D AVATAR</span>
              
              <!-- 扫描线动画保留 -->
              <div class="absolute top-0 left-0 w-full h-[2px] bg-cyan-400/80 shadow-[0_0_10px_#00f0ff] animate-scanline pointer-events-none"></div>
           </div>
        </div>

        <!-- 底部全息投影底座 (稳定无穿模的同心涟漪发光基座) -->
        <div class="absolute bottom-[80px] left-1/2 -translate-x-1/2 w-[350px] sm:w-[450px] h-[30px] flex items-center justify-center z-10">
          <div class="relative w-full h-full flex items-center justify-center">
            <!-- 最底层：向外扩散的极光涟漪动画 -->
            <div class="absolute w-[120%] h-[150%] rounded-[50%] border border-cyan-500/50 opacity-0 animate-ripple-1"></div>
            <div class="absolute w-[120%] h-[150%] rounded-[50%] border border-cyan-500/30 opacity-0 animate-ripple-2"></div>
            
            <!-- 底座主发光阴影 (大范围光晕) -->
            <div class="absolute w-full h-full rounded-[50%] bg-cyan-500/30 blur-2xl"></div>

            <!-- 底座边缘主亮线 (扁平椭圆) -->
            <div class="absolute w-[90%] h-[80%] rounded-[50%] border-[2px] border-cyan-300 shadow-[0_0_15px_#00f0ff,inset_0_0_15px_#00f0ff]"></div>
            
            <!-- 底盘中央能量核心 (呼吸缩放) -->
            <div class="absolute w-[60%] h-[50%] rounded-[50%] bg-cyan-400/40 blur-md animate-pulse-core"></div>
            
            <!-- 表面高光反射 (增强材质感) -->
            <div class="absolute w-[70%] h-[30%] top-[20%] rounded-[50%] bg-gradient-to-b from-white/30 to-transparent blur-[2px]"></div>
          </div>
        </div>
      </section>

      <!-- 【右侧面板】：交互操作区 (向内翻转) -->
      <aside class="w-full lg:w-[28%] flex flex-col gap-4 transform-style-3d rotate-y-[-15deg] origin-right transition-transform duration-500 hover:rotate-y-[-5deg] h-full relative z-20">
        <!-- 模块标题 (固定高度占位，确保两侧标题高度一致) -->
        <div class="flex items-center gap-3 justify-end h-[40px]">
           <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">交互入口</h2>
           <div class="flex gap-1">
             <div class="w-1.5 h-6 bg-blue-800 skew-x-[15deg]"></div>
             <div class="w-1.5 h-6 bg-blue-500 skew-x-[15deg]"></div>
             <div class="w-1.5 h-6 bg-cyan-400 skew-x-[15deg] shadow-[0_0_8px_#00f0ff]"></div>
           </div>
        </div>

        <!-- 九宫格功能面板 (强制拉伸撑满容器高度) -->
        <div class="tech-card p-6 flex-1 flex flex-col">
           <div class="grid grid-cols-2 gap-6 flex-1">
             <div v-for="(item, index) in featureMenu" :key="index" class="relative tech-btn group flex flex-col items-center justify-center gap-4 bg-[#0a1930]/50 border border-blue-500/20 hover:border-cyan-400/60 hover:bg-cyan-900/20 transition-all duration-300 cursor-pointer overflow-hidden rounded-lg min-h-[120px]">
               <!-- 背景扫光特效 -->
               <div class="absolute inset-0 bg-gradient-to-br from-cyan-400/0 via-cyan-400/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
               <div class="absolute top-0 left-[-100%] w-[50%] h-full bg-gradient-to-r from-transparent via-white/10 to-transparent skew-x-[-45deg] group-hover:animate-[sweep_1s_ease-in-out]"></div>
               
               <!-- 图标与文字 -->
               <component :is="item.icon" class="w-12 h-12 text-cyan-500 group-hover:text-cyan-300 group-hover:scale-110 transition-all duration-300 filter group-hover:drop-shadow-[0_0_8px_#00f0ff]" />
               <span class="text-base md:text-lg font-bold text-blue-100 group-hover:text-white tracking-widest">{{ item.title }}</span>
               
               <!-- 装饰角 -->
               <div class="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-cyan-500/50 group-hover:border-cyan-300"></div>
               <div class="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-cyan-500/50 group-hover:border-cyan-300"></div>
             </div>
           </div>
        </div>

        <!-- 底部高亮按钮组 -->
        <div class="flex flex-col gap-3 mt-4">
          <button class="relative w-full py-5 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-cyan-500 hover:to-blue-400 text-white font-bold text-xl tracking-[0.3em] rounded-md overflow-hidden group shadow-[0_0_15px_rgba(0,240,255,0.4)] transition-all">
             <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20 mix-blend-overlay"></div>
             <div class="absolute top-0 left-[-100%] w-1/2 h-full bg-gradient-to-r from-transparent via-white/30 to-transparent skew-x-[-45deg] group-hover:animate-sweep"></div>
             <span class="relative z-10 flex items-center justify-center gap-2">
                <PowerIcon class="w-5 h-5" /> 启动数字人
             </span>
          </button>
        </div>
      </aside>
    </main>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { 
  Settings as SettingsIcon, 
  Headphones as HeadphonesIcon,
  Activity as ActivityIcon,
  User as UserIcon,
  FileText as FileTextIcon,
  Power as PowerIcon,
  Cpu as CpuIcon,
  Mic as MicIcon,
  MessageSquare as MessageSquareIcon,
  Video as VideoIcon,
  Clock as ClockIcon
} from 'lucide-vue-next'

// 动态时间
const currentTime = ref('');
const currentDate = ref('');
const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false });
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
};
let timeInterval;

// 定义右侧交互入口的数据结构
const featureMenu = [
  { title: '控制面板', icon: SettingsIcon },
  { title: '语音设置', icon: HeadphonesIcon },
  { title: '大语言模型', icon: CpuIcon },
  { title: '麦克风接入', icon: MicIcon },
  { title: '剧本配置', icon: MessageSquareIcon },
  { title: '视频流推流', icon: VideoIcon }
]

// =========== Canvas 背景粒子特效 ===========
const particleCanvas = ref(null)
let animationFrameId = null

onMounted(() => {
  const canvas = particleCanvas.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  let particlesArray = []
  
  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  window.addEventListener('resize', resize)
  resize()
  
  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width
      this.y = Math.random() * canvas.height
      this.size = Math.random() * 2 + 0.5
      this.speedX = Math.random() * 1 - 0.5
      this.speedY = Math.random() * 1 - 0.5
      this.color = Math.random() > 0.5 ? '#00f0ff' : '#3b82f6'
      this.opacity = Math.random() * 0.5 + 0.2
    }
    update() {
      this.x += this.speedX
      this.y += this.speedY
      
      // 边界检测回弹
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
          ctx.strokeStyle = '#00f0ff'
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

  // 启动时间更新
  updateTime();
  timeInterval = setInterval(updateTime, 1000);
})

onUnmounted(() => {
  window.removeEventListener('resize', () => {})
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  if (timeInterval) clearInterval(timeInterval);
})
</script>

<style scoped>
/* =========== 核心科技感背景与排版 =========== */
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

/* =========== 顶部标题梯形裁剪 =========== */
.tech-title-clip {
  clip-path: polygon(10% 0, 90% 0, 100% 100%, 0% 100%);
}

/* =========== 通用科技卡片 =========== */
.tech-card {
  background: linear-gradient(135deg, rgba(6, 18, 38, 0.8) 0%, rgba(2, 9, 26, 0.9) 100%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  box-shadow: inset 0 0 20px rgba(0, 150, 255, 0.05);
  backdrop-filter: blur(8px);
  border-radius: 8px;
  /* 左上角与右下角切角效果 */
  clip-path: polygon(
    0 15px, 
    15px 0, 
    100% 0, 
    100% calc(100% - 15px), 
    calc(100% - 15px) 100%, 
    0 100%
  );
}

/* 包含红色/黄色的特殊小卡片 */
.tech-card-alt {
  background: rgba(6, 18, 38, 0.6);
  border-width: 1px;
  border-style: solid;
  border-radius: 6px;
  backdrop-filter: blur(4px);
  transition: all 0.3s ease;
}

/* 列表项 */
.tech-list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid rgba(59, 130, 246, 0.3);
  background: rgba(6, 18, 38, 0.6);
  border-radius: 4px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.tech-list-item:hover {
  background: rgba(0, 240, 255, 0.1);
  border-color: rgba(0, 240, 255, 0.6);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
}

/* =========== 悬浮六边形按钮 =========== */
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

/* =========== 3D 透视与投影 =========== */
.perspective-\[1500px\] {
  perspective: 1500px;
}
.perspective-\[800px\] {
  perspective: 800px;
}
.transform-style-3d {
  transform-style: preserve-3d;
}
.rotate-x-\[80deg\] {
  transform: rotateX(80deg);
}
.rotate-x-\[-20deg\] {
  transform: rotateX(-20deg);
}
.rotate-z-\[20deg\] {
  transform: rotateZ(20deg);
}
.rotate-y-\[15deg\] {
  transform: rotateY(15deg);
}
.rotate-y-\[-15deg\] {
  transform: rotateY(-15deg);
}
.rotate-y-\[5deg\] {
  transform: rotateY(5deg);
}
.rotate-y-\[-5deg\] {
  transform: rotateY(-5deg);
}
.translate-z-\[-50px\] {
  transform: translateZ(-50px);
}
.translate-z-0 {
  transform: translateZ(0);
}
.origin-left {
  transform-origin: left center;
}
.origin-right {
  transform-origin: right center;
}

.clip-light-beam {
  clip-path: polygon(30% 0, 70% 0, 100% 100%, 0% 100%);
}

/* =========== 关键帧动画 =========== */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
.animate-float {
  animation: float 4s ease-in-out infinite;
}

@keyframes scanline {
  0% { top: 0; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
.animate-scanline {
  animation: scanline 3s linear infinite;
}

@keyframes sweep {
  0% { left: -100%; }
  100% { left: 200%; }
}
.animate-sweep {
  animation: sweep 1.5s ease-in-out infinite;
}

@keyframes ripple {
  0% { transform: scale(0.8); opacity: 1; border-width: 2px; }
  100% { transform: scale(1.5); opacity: 0; border-width: 0px; }
}
.animate-ripple-1 {
  animation: ripple 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
.animate-ripple-2 {
  animation: ripple 3s cubic-bezier(0.4, 0, 0.2, 1) infinite 1.5s;
}

@keyframes pulseCore {
  0%, 100% { transform: scale(0.9); opacity: 0.6; }
  50% { transform: scale(1.1); opacity: 1; }
}
.animate-pulse-core {
  animation: pulseCore 2s ease-in-out infinite;
}
</style>
