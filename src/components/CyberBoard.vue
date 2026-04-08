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
            <h1 class="relative text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-emerald-300 tracking-[0.2em] z-10 filter drop-shadow-[0_0_12px_rgba(52,211,153,0.8)]">
              智慧文旅数字导览
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
      <aside class="w-full lg:w-[28%] flex flex-col justify-between transform-style-3d rotate-y-[15deg] origin-left transition-transform duration-500 hover:rotate-y-[5deg] h-full relative z-20">
        <!-- 模块标题 (固定高度占位，确保两侧标题高度一致) -->
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
          <!-- 景区实景图背景 -->
          <div class="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=800&q=80')] bg-cover bg-center opacity-40 group-hover:opacity-60 transition-opacity duration-700 group-hover:scale-105"></div>
          <!-- 底部渐变遮罩，确保文字清晰 -->
          <div class="absolute inset-0 bg-gradient-to-t from-[#021815] via-[#021815]/70 to-transparent"></div>
          
          <div class="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-emerald-400 z-10"></div>
          <div class="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-emerald-400 z-10"></div>
          
          <div class="relative z-10 p-5 flex flex-col justify-between h-full">
            <div class="flex justify-end">
               <div class="flex items-center gap-2 text-amber-400 bg-black/40 px-3 py-1.5 rounded-full backdrop-blur-md border border-emerald-500/30">
                  <Sun class="w-4 h-4" />
                  <span class="text-sm font-bold">24°C</span>
                  <div class="w-px h-3 bg-emerald-500/50 mx-1"></div>
                  <span class="text-xs text-emerald-100/80">晴 | AQI 20</span>
               </div>
            </div>
            <div class="mt-auto pt-6">
              <h3 class="text-2xl font-black text-emerald-300 tracking-widest filter drop-shadow-[0_0_5px_#34d399]">云梦山国家森林公园</h3>
              <p class="text-[10px] text-emerald-400/80 font-mono tracking-widest mt-1">YUNMENG MOUNTAIN NAT'L PARK</p>
            </div>
          </div>
        </div>

        <!-- 卡片 2：详细介绍 (高度减小，支持滚动) -->
        <div class="tech-card flex-1 min-h-[150px] max-h-[250px] p-6 relative flex flex-col gap-3 border-emerald-500/20 bg-[#021815]/60 shrink-0">
          <div class="flex items-center gap-2 mb-2 shrink-0">
            <div class="w-2 h-4 bg-emerald-400"></div>
            <h3 class="text-lg font-bold text-white tracking-wider">景区简介</h3>
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
            >{{ introText }}</div>
          </div>
          <!-- 底部渐变遮罩，提示可滚动 -->
          <div class="absolute bottom-0 left-0 w-full h-[30px] bg-gradient-to-t from-[#021815] to-transparent pointer-events-none z-20"></div>
          <!-- 装饰扫光 -->
          <div class="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-50 z-20"></div>
        </div>

        <!-- 卡片 3：票务信息 (独立成块) -->
        <div class="flex gap-4 h-[100px] shrink-0">
          <!-- 门票卡片 -->
          <div class="flex-1 tech-card border-emerald-500/20 bg-[#021815]/60 hover:border-emerald-400/80 p-4 flex flex-col justify-center relative overflow-hidden group cursor-pointer transition-all">
            <div class="absolute inset-0 bg-emerald-500/5 group-hover:bg-emerald-500/10 transition-colors"></div>
            <span class="text-xs text-emerald-400/80 font-mono tracking-widest relative z-10 mb-1">成人票价 TICKET</span>
            <div class="flex items-baseline gap-1 relative z-10">
              <span class="text-2xl font-bold text-amber-400 drop-shadow-[0_0_5px_#fbbf24]">¥120</span>
              <span class="text-xs text-emerald-100/50">/人</span>
            </div>
            <!-- 装饰背景图标 -->
            <Ticket class="absolute right-[-10px] bottom-[-10px] w-16 h-16 text-emerald-500/10 group-hover:text-emerald-500/20 group-hover:scale-110 transition-all -rotate-12" />
          </div>
          
          <!-- 营业时间卡片 -->
          <div class="flex-1 tech-card border-teal-500/20 bg-[#021815]/60 hover:border-teal-400/80 p-4 flex flex-col justify-center relative overflow-hidden group cursor-pointer transition-all">
            <div class="absolute inset-0 bg-teal-500/5 group-hover:bg-teal-500/10 transition-colors"></div>
            <span class="text-xs text-teal-400/80 font-mono tracking-widest relative z-10 mb-1">营业时间 OPENING</span>
            <div class="text-lg font-bold text-emerald-100 relative z-10 drop-shadow-[0_0_5px_#10b981]">
              08:00 - 18:00
            </div>
            <!-- 装饰背景图标 -->
            <ClockIcon class="absolute right-[-10px] bottom-[-10px] w-16 h-16 text-teal-500/10 group-hover:text-teal-500/20 group-hover:scale-110 transition-all rotate-12" />
          </div>
        </div>

        <!-- 卡片 4：客流监控 (动态数据，填补底部) -->
        <div class="tech-card p-5 flex flex-col gap-4 relative border-emerald-500/20 bg-[#021815]/60 shrink-0 overflow-hidden">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-2 h-4 bg-emerald-400"></div>
              <h3 class="text-md font-bold text-white tracking-wider">实时客流监控</h3>
            </div>
            <div class="flex gap-1 items-center">
              <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></div>
              <span class="text-[10px] text-emerald-400 font-mono">LIVE</span>
            </div>
          </div>
          
          <div class="flex justify-between items-end mt-1">
            <div class="flex flex-col">
              <span class="text-xs text-emerald-100/60 mb-1">当前在园人数</span>
              <div class="flex items-baseline gap-2">
                 <span class="text-3xl font-black text-emerald-300 tracking-wider font-mono">4,520</span>
                 <span class="text-xs text-emerald-100/40">人</span>
              </div>
            </div>
            <div class="flex flex-col items-end">
              <span class="text-xs text-emerald-100/60 mb-1">舒适度指数</span>
              <span class="px-3 py-1 rounded border border-emerald-400/50 bg-emerald-400/10 text-emerald-300 text-sm font-bold shadow-[0_0_10px_rgba(52,211,153,0.2)]">
                🟢 良好畅通
              </span>
            </div>
          </div>
          
          <!-- 简单的动态波形条 -->
          <div class="h-6 w-full flex items-end gap-[2px] opacity-60 mt-1">
             <div v-for="i in 40" :key="`flow-${i}`" class="flex-1 bg-emerald-500/40 rounded-t-sm" :style="`height: ${20 + Math.random() * 80}%; animation: wave ${0.5 + Math.random()}s infinite alternate;`"></div>
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

      <!-- 【右侧面板】：功能与管理区 (向内翻转) -->
      <aside class="w-full lg:w-[28%] flex flex-col justify-between transform-style-3d rotate-y-[-15deg] origin-right transition-transform duration-500 hover:rotate-y-[-5deg] h-full relative z-20">
        <!-- 模块标题 (恢复大标题) -->
        <div class="flex items-center gap-3 justify-end h-[40px] shrink-0">
           <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">核心应用场景</h2>
           <div class="flex gap-1">
             <div class="w-1.5 h-6 bg-teal-800 skew-x-[15deg]"></div>
             <div class="w-1.5 h-6 bg-teal-500 skew-x-[15deg]"></div>
             <div class="w-1.5 h-6 bg-emerald-400 skew-x-[15deg] shadow-[0_0_8px_#34d399]"></div>
           </div>
        </div>

        <!-- 内部 Tab 切换区 -->
        <div class="flex gap-4 justify-end shrink-0 border-b border-emerald-500/20 pb-2 mt-4">
           <button @click="activeTab = 'spots'" :class="['text-sm font-bold tracking-widest transition-colors relative', activeTab === 'spots' ? 'text-emerald-400 text-shadow-glow' : 'text-emerald-100/40 hover:text-emerald-100']">
             景点列表
             <div v-if="activeTab === 'spots'" class="absolute -bottom-[9px] left-0 w-full h-[2px] bg-emerald-400 shadow-[0_0_8px_#34d399]"></div>
           </button>
           <button @click="activeTab = 'admin'" :class="['text-sm font-bold tracking-widest transition-colors relative', activeTab === 'admin' ? 'text-emerald-400 text-shadow-glow' : 'text-emerald-100/40 hover:text-emerald-100']">
             管理入口
             <div v-if="activeTab === 'admin'" class="absolute -bottom-[9px] left-0 w-full h-[2px] bg-emerald-400 shadow-[0_0_8px_#34d399]"></div>
           </button>
        </div>

        <!-- 内容区：景点列表 (滚动) -->
        <div v-if="activeTab === 'spots'" class="flex-1 flex flex-col gap-3 min-h-[300px] overflow-y-auto custom-scrollbar pr-2 my-4">
          <div v-for="(spot, index) in spotList" :key="index" class="tech-panel flex items-center gap-4 p-3 cursor-pointer group hover:bg-emerald-500/10 transition-all border border-emerald-500/20 bg-[#021815]/40 rounded-lg relative overflow-hidden shrink-0">
             <div class="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-400/5 to-transparent -translate-x-[100%] group-hover:translate-x-[100%] transition-transform duration-700 z-0"></div>
             <!-- 景点缩略图 -->
             <div class="w-16 h-16 rounded-md bg-emerald-900/50 border border-emerald-500/30 flex items-center justify-center shrink-0 z-10 group-hover:border-emerald-400 transition-colors overflow-hidden relative">
                <img :src="spot.image" alt="spot" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500" />
                <div class="absolute inset-0 bg-emerald-500/20 mix-blend-overlay"></div>
             </div>
             <div class="flex flex-col flex-1 z-10">
               <div class="flex justify-between items-start">
                  <span class="text-base font-bold text-emerald-50 tracking-wider group-hover:text-emerald-300 transition-colors">{{ spot.name }}</span>
                  <span :class="['text-[10px] px-2 py-0.5 rounded-sm border', spot.status === '畅通' ? 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10' : (spot.status === '拥挤' ? 'text-amber-400 border-amber-400/30 bg-amber-400/10' : 'text-teal-300 border-teal-300/30 bg-teal-300/10')]">{{ spot.status }}</span>
               </div>
               <span class="text-[10px] text-emerald-500/60 font-mono tracking-widest mt-0.5">{{ spot.en }}</span>
               <p class="text-xs text-emerald-100/60 mt-1 line-clamp-1">{{ spot.desc }}</p>
             </div>
          </div>
        </div>

        <!-- 内容区：管理入口 (六宫格) -->
        <div v-else class="flex-1 grid grid-cols-2 grid-rows-3 gap-4 min-h-[300px] my-4">
          <div 
            v-for="(item, index) in adminMenu" 
            :key="index" 
            @click="handleAdminAction(item.action)"
            class="tech-panel flex flex-col items-center justify-center gap-2 p-4 cursor-pointer group hover:bg-emerald-500/10 transition-all relative overflow-hidden h-full border border-emerald-500/20 bg-[#021815]/40 rounded-lg"
          >
             <div class="absolute inset-0 bg-gradient-to-b from-transparent via-emerald-400/10 to-transparent translate-y-[-100%] group-hover:translate-y-[100%] transition-transform duration-1000 z-0"></div>
             <!-- 针对启停按钮做特殊的颜色处理 -->
             <component 
               :is="item.icon" 
               class="w-8 h-8 transition-colors duration-300 z-10"
               :class="[
                 item.action === 'toggle-fay' 
                   ? (isFayRunning ? 'text-red-400 group-hover:text-red-300 group-hover:scale-110 shadow-[0_0_15px_#f87171] rounded-full' : 'text-emerald-400 group-hover:text-white group-hover:scale-110')
                   : 'text-emerald-400 group-hover:text-white group-hover:scale-110'
               ]"
             />
             <div class="flex flex-col items-center z-10 mt-1">
               <span class="text-sm font-bold text-white tracking-widest">
                 <!-- 如果是启停按钮，根据状态显示不同文字 -->
                 {{ item.action === 'toggle-fay' ? (isFayRunning ? '关闭 Fay 服务' : '开启 Fay 服务') : item.title }}
               </span>
               <span class="text-[10px] text-emerald-500/60 font-mono tracking-widest mt-0.5">{{ item.en }}</span>
             </div>
          </div>
        </div>

        <!-- 底部操作按钮 -->
        <button class="mt-auto shrink-0 h-14 w-full bg-gradient-to-r from-teal-600 to-emerald-500 rounded-lg font-bold text-white tracking-[0.2em] shadow-[0_0_20px_rgba(52,211,153,0.4)] hover:shadow-[0_0_30px_rgba(52,211,153,0.6)] hover:scale-[1.02] transition-all flex items-center justify-center gap-2 relative overflow-hidden group">
           <div class="absolute inset-0 bg-white/20 -translate-x-full group-hover:translate-x-full transition-transform duration-700 skew-x-[-20deg]"></div>
           <Navigation class="w-5 h-5" />
           <span>唤醒伴游向导</span>
        </button>
      </aside>
    </main>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { 
  Settings, 
  Activity,
  Clock as ClockIcon,
  Power as PowerIcon,
  MapPin,
  Sun,
  Navigation,
  Radio,
  ShieldAlert,
  Route,
  Ticket,
  User as UserIcon,
  Hexagon as HexagonIcon
} from 'lucide-vue-next'

import { startFayLive, stopFayLive, getFayStatus } from '../api/fay'

// 动态时间
const currentTime = ref('');
const currentDate = ref('');
const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false });
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
};
let timeInterval;

// 景区列表与管理入口状态
const activeTab = ref('spots');

const spotList = [
  { name: '云海观景台', en: 'SEA OF CLOUDS', desc: '海拔1200米，观赏日出云海的最佳位置', status: '畅通', image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=200&q=80' },
  { name: '千年古刹', en: 'ANCIENT TEMPLE', desc: '始建于唐代，历史悠久，香火鼎盛', status: '拥挤', image: 'https://images.unsplash.com/photo-1540201505303-349079213bc0?auto=format&fit=crop&w=200&q=80' },
  { name: '翡翠飞瀑', en: 'EMERALD FALLS', desc: '落差80米，水质清澈，负氧离子极高', status: '畅通', image: 'https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&w=200&q=80' },
  { name: '幽光溶洞', en: 'GLOWING CAVE', desc: '天然喀斯特地貌，钟乳石千姿百态', status: '适中', image: 'https://images.unsplash.com/photo-1518557984649-7b161c230cfa?auto=format&fit=crop&w=200&q=80' },
  { name: '高山草甸', en: 'ALPINE MEADOW', desc: '天然高山牧场，适合露营与拍照', status: '畅通', image: 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=200&q=80' }
];

const adminMenu = [
  { title: '全区广播', en: 'BROADCAST', icon: Radio, action: 'broadcast' },
  { title: '应急调度', en: 'EMERGENCY', icon: ShieldAlert, action: 'emergency' },
  { title: '设备监控', en: 'MONITORING', icon: Activity, action: 'monitoring' },
  { title: '路线编辑', en: 'ROUTE EDIT', icon: Route, action: 'route' },
  { title: '票务管理', en: 'TICKETING', icon: Ticket, action: 'ticketing' },
  { title: '启停 Fay 服务', en: 'FAY POWER', icon: PowerIcon, action: 'toggle-fay' }
];

// =========== 管理入口操作逻辑 ===========
const isFayRunning = ref(false);

const handleAdminAction = async (action) => {
  if (action === 'toggle-fay') {
    try {
      if (isFayRunning.value) {
        // 执行关闭
        const res = await stopFayLive();
        if (res && res.result === 'successful') {
          isFayRunning.value = false;
          alert('已成功关闭 Fay 数字人');
        } else {
          alert('关闭失败，请检查 Fay 服务端状态');
        }
      } else {
        // 执行开启
        const res = await startFayLive();
        if (res && res.result === 'successful') {
          isFayRunning.value = true;
          alert('已成功开启 Fay 数字人');
        } else {
          alert('开启失败，请检查 Fay 服务端状态');
        }
      }
    } catch (error) {
      console.error('调用启停接口失败:', error);
      alert('请求 Fay 服务端接口失败，请检查网络连接');
    }
  } else {
    // 其他功能的占位处理
    console.log(`点击了管理功能: ${action}`);
  }
};

// =========== Canvas 背景粒子特效 ===========
const particleCanvas = ref(null)
let animationFrameId = null

// =========== 景区简介文本与自动滚动逻辑 ===========
// 景区简介文本（未来可直接由数据库请求赋值）
const introText = ref('云梦山国家森林公园位于城市北部，占地面积约8500公顷。这里群峰叠翠，飞瀑流泉，森林覆盖率高达95%，被誉为“城市绿肺”。作为国家AAAAA级旅游景区，云梦山不仅是自然生态的宝库，更是文化传承的圣地。\n\n景区融合了自然生态与历史人文，拥有千年古刹、高山草甸、幽光溶洞等多样化景观。漫步于林间小道，您可以聆听百鸟齐鸣，感受微风拂面的清爽。数字导览系统将为您提供沉浸式的游览体验，开启智慧生态之旅。\n\n此外，公园内还设有全长12公里的环山步道和多处观景平台，是登山爱好者和摄影师的绝佳去处。每年秋季，漫山红叶更是吸引数十万游客前来观赏。这里的日出云海、璀璨星空更是不可多得的视觉盛宴。\n\n为了提升游客体验，景区引进了最先进的物联网技术与全息投影设备。在游客中心，您可以与我们的AI数字人导游进行实时互动，获取最佳游览路线推荐、实时天气状况以及各景点的客流拥挤度信息。\n\n餐饮与住宿方面，景区内设有多家特色主题餐厅和隐匿于山林间的生态木屋酒店，确保您在亲近自然的同时，也能享受到现代化的舒适服务。无论是家庭出游、朋友聚会还是企业团建，云梦山国家森林公园都将是您的不二之选。\n\n在环保方面，我们坚持“绿水青山就是金山银山”的发展理念，全面推行零碳排放游览模式。景区内所有接驳车均为纯电动车辆，并设置了智能垃圾分类回收系统。我们诚挚地邀请每一位游客共同参与到生态保护中来。');

const introScrollContainer = ref(null);
const introScrollContent = ref(null);
let introScrollAnimationId = null;
let isIntroScrolling = true;
let currentScrollTop = 0; // 用于精确记录浮点数滚动位置

const startIntroAutoScroll = () => {
  const scroll = () => {
    if (isIntroScrolling && introScrollContainer.value && introScrollContent.value) {
      // 修复1：将递增值由 0.5 降至 0.2，减慢滚动速度
      currentScrollTop += 0.2; 
      introScrollContainer.value.scrollTop = currentScrollTop;
      
      // 修复2：计算触底条件时增加 1px 的容差。
      // 因为浏览器在不同分辨率缩放或子像素渲染下，scrollTop 的值可能永远达不到绝对精确的最大值
      const maxScrollTop = introScrollContainer.value.scrollHeight - introScrollContainer.value.clientHeight;
      if (introScrollContainer.value.scrollTop >= maxScrollTop - 1) {
        // 到达底部后回到顶部重新滚动
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
  // 当鼠标移开或触屏松开恢复滚动时，同步真实的 scrollTop 值，防止用户手动滚动过内容后位置突跳
  if (introScrollContainer.value) {
    currentScrollTop = introScrollContainer.value.scrollTop;
  }
};

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
      this.color = Math.random() > 0.5 ? '#10b981' : '#34d399'
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

  // 启动时间更新
  updateTime();
  timeInterval = setInterval(updateTime, 1000);

  // 启动景区简介自动滚动
  startIntroAutoScroll();

  // 获取 Fay 初始状态
  initFayStatus();
})

// 初始化获取 Fay 服务状态
const initFayStatus = async () => {
  try {
    const res = await getFayStatus();
    if (res && res.status !== undefined) {
      isFayRunning.value = res.status;
    }
  } catch (error) {
    console.error('获取 Fay 服务初始状态失败:', error);
  }
};

onUnmounted(() => {
  window.removeEventListener('resize', () => {})
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  if (introScrollAnimationId) cancelAnimationFrame(introScrollAnimationId)
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

<style>
/* 隐藏原生滚动条并自定义细滚动条 */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(16, 185, 129, 0.05);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.3);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(16, 185, 129, 0.6);
}
</style>
