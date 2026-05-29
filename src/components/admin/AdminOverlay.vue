<template>
  <div v-if="visible" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm transition-opacity duration-300 animate-fade-in">
    <!-- 弹窗主体 (科技感风格) -->
    <div class="relative w-[90%] max-w-[1200px] h-[85%] bg-[#021815]/90 border border-emerald-500/50 rounded-xl shadow-[0_0_50px_rgba(52,211,153,0.2)] flex flex-col overflow-hidden">
      
      <!-- 四角高亮边框 -->
      <div class="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-emerald-400 rounded-tl-xl pointer-events-none"></div>
      <div class="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-emerald-400 rounded-tr-xl pointer-events-none"></div>
      <div class="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-emerald-400 rounded-bl-xl pointer-events-none"></div>
      <div class="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-emerald-400 rounded-br-xl pointer-events-none"></div>

      <!-- 顶部标题栏 -->
      <header class="h-16 border-b border-emerald-500/30 flex items-center justify-between px-6 bg-gradient-to-r from-emerald-900/40 to-transparent shrink-0">
        <div class="flex items-center gap-3">
          <Database class="w-6 h-6 text-emerald-400 animate-pulse" />
          <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">系统数据管理核心</h2>
          <span class="text-xs text-emerald-500/60 font-mono tracking-widest ml-4 border border-emerald-500/30 px-2 py-0.5 rounded">ADMIN TERMINAL</span>
        </div>
        <button @click="close" class="text-emerald-400/60 hover:text-emerald-300 hover:rotate-90 transition-all duration-300">
          <X class="w-7 h-7" />
        </button>
      </header>

      <!-- 主体内容 -->
      <div class="flex-1 flex overflow-hidden">
        <!-- 左侧菜单 -->
        <aside class="w-56 lg:w-64 border-r border-emerald-500/20 bg-emerald-900/10 p-4 flex flex-col gap-3 shrink-0">
          <button 
            @click="activeMenu = 'scenic'" 
            :class="['w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm tracking-widest transition-all', activeMenu === 'scenic' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'text-emerald-100/60 hover:bg-emerald-500/10 hover:text-emerald-100 border border-transparent']"
          >
            <Map class="w-4 h-4" />
            景区基础信息
          </button>
          <button 
            @click="activeMenu = 'spots'" 
            :class="['w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm tracking-widest transition-all', activeMenu === 'spots' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'text-emerald-100/60 hover:bg-emerald-500/10 hover:text-emerald-100 border border-transparent']"
          >
            <MapPin class="w-4 h-4" />
            景点列表管理
          </button>
          <button 
            @click="activeMenu = 'control'" 
            :class="['w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm tracking-widest transition-all', activeMenu === 'control' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'text-emerald-100/60 hover:bg-emerald-500/10 hover:text-emerald-100 border border-transparent']"
          >
            <Settings class="w-4 h-4" />
            互动控制台
          </button>
        </aside>

        <!-- 右侧内容区 -->
        <main class="flex-1 flex flex-col relative bg-gradient-to-br from-[#020b14]/80 to-transparent overflow-hidden">
          
          <!-- ================== 景区信息管理 ================== -->
          <div v-if="activeMenu === 'scenic'" class="flex-1 flex flex-col overflow-hidden animate-fade-in">
             <!-- 固定的顶部操作栏 -->
             <div class="flex-shrink-0 flex justify-between items-center p-6 border-b border-emerald-500/10">
                <h3 class="text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3 tracking-wider">景区全局配置</h3>
                <button @click="handleSaveScenic" class="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_15px_rgba(52,211,153,0.4)] transition-all flex items-center gap-2">
                   <Save class="w-4 h-4" /> 保存修改
                </button>
             </div>
             
             <!-- 可滚动的表单主体 -->
             <div class="flex-1 overflow-y-auto p-6 custom-scrollbar">
                <div class="max-w-4xl mx-auto pb-12">

                   <div v-if="loadingScenic" class="text-emerald-400/60 flex items-center gap-2">
                      <Loader2 class="w-5 h-5 animate-spin" /> 数据加载中...
                   </div>
                   
                   <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div class="flex flex-col gap-2">
                         <label class="text-sm text-emerald-100/70">景区中文名称</label>
                         <input v-model="scenicForm.scenic_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                      </div>
                      <div class="flex flex-col gap-2">
                         <label class="text-sm text-emerald-100/70">景区英文名称</label>
                         <input v-model="scenicForm.scenic_en_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                      </div>
                      <div class="flex flex-col gap-2 md:col-span-2">
                         <label class="text-sm text-emerald-100/70">地理位置</label>
                         <input v-model="scenicForm.address" type="text" placeholder="例如：北京市。。。" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                      </div>
                      <div class="flex flex-col gap-2">
                         <label class="text-sm text-emerald-100/70">成人票价 (元)</label>
                         <input v-model="scenicForm.ticket_price" type="number" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                      </div>
                      <div class="flex flex-col gap-2">
                         <label class="text-sm text-emerald-100/70">营业时间</label>
                         <input v-model="scenicForm.opening_hours" type="text" placeholder="例如: 08:00 - 18:00" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                      </div>
                      <div class="flex flex-col gap-2 md:col-span-2">
                         <label class="text-sm text-emerald-100/70">封面图片</label>
                         <div 
                           class="relative w-full h-40 rounded-lg border-2 border-dashed border-emerald-500/30 bg-emerald-900/10 overflow-hidden flex flex-col items-center justify-center cursor-pointer group hover:border-emerald-400 hover:bg-emerald-900/20 transition-all duration-300"
                           @click="$refs.scenicFileInput.click()"
                         >
                           <img v-if="scenicForm.cover_image" :src="scenicForm.cover_image" class="absolute inset-0 w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" />
                           
                           <!-- 遮罩层与更换提示 (有图片时) -->
                           <div v-if="scenicForm.cover_image" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center gap-2 z-10 backdrop-blur-[2px]">
                              <Upload class="w-8 h-8 text-emerald-300 transform -translate-y-2 group-hover:translate-y-0 transition-transform duration-300" />
                              <span class="text-sm font-bold tracking-widest text-emerald-300">点击更换封面图片</span>
                           </div>

                           <!-- 初始无图片状态 -->
                           <div v-if="!scenicForm.cover_image" class="flex flex-col items-center justify-center gap-3 z-0">
                              <div class="p-3 rounded-full bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                                <Upload class="w-8 h-8 text-emerald-500/60 group-hover:text-emerald-400 transition-colors" />
                              </div>
                              <div class="flex flex-col items-center gap-1">
                                <span class="text-emerald-400 font-bold tracking-wide">点击上传景区封面图</span>
                                <span class="text-[10px] text-emerald-500/50 font-mono">支持 JPG / PNG / WEBP 格式，最大 16MB</span>
                              </div>
                           </div>
                           
                           <!-- 上传中状态 -->
                           <div v-if="uploadingScenicImg" class="absolute inset-0 bg-[#021815]/90 flex flex-col items-center justify-center gap-3 z-20 backdrop-blur-sm">
                             <Loader2 class="w-8 h-8 text-emerald-400 animate-spin" />
                             <span class="text-xs tracking-widest text-emerald-400 animate-pulse">UPLOADING...</span>
                           </div>
                           
                           <input type="file" ref="scenicFileInput" class="hidden" accept="image/*" @change="e => handleImageUpload(e, 'scenic')" />
                         </div>
                      </div>
                      <div class="flex flex-col gap-2 md:col-span-2">
                         <label class="text-sm text-emerald-100/70">景区详细介绍</label>
                         <textarea v-model="scenicForm.introduction" rows="8" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors resize-none custom-scrollbar"></textarea>
                      </div>
                   </div>
                </div>
             </div>
          </div>

          <!-- ================== 景点列表管理 ================== -->
          <div v-if="activeMenu === 'spots'" class="flex-1 flex flex-col overflow-hidden animate-fade-in">

             <div class="flex-shrink-0 flex justify-between items-center p-6 border-b border-emerald-500/10">
                <h3 class="text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3 tracking-wider">景点列表管理</h3>
                <button @click="openSpotModal()" class="px-4 py-2 bg-emerald-500/20 hover:bg-emerald-500/40 border border-emerald-400/50 rounded text-emerald-300 transition-all flex items-center gap-2 hover:shadow-[0_0_15px_rgba(52,211,153,0.4)]">
                   <Plus class="w-4 h-4" /> 添加新景点
                </button>
             </div>

             <!-- 可滚动的列表主体 -->
             <div class="flex-1 overflow-y-auto p-6 custom-scrollbar">
                <div class="max-w-4xl mx-auto pb-12">
                   <div v-if="loadingSpots" class="text-emerald-400/60 flex items-center gap-2">
                      <Loader2 class="w-5 h-5 animate-spin" /> 数据加载中...
                   </div>

                   <div v-else class="grid grid-cols-1 gap-4">
                       <div v-for="spot in spotList" :key="spot.id" class="group bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-4 hover:border-emerald-500/50 hover:bg-emerald-900/20 transition-all flex gap-4">
                          <!-- 左侧缩略图 -->
                          <div class="w-24 h-24 rounded bg-[#020b14] border border-emerald-500/30 overflow-hidden flex-shrink-0 relative group-hover:border-emerald-400">
                             <img v-if="spot.image_url" :src="spot.image_url" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
                             <div v-else class="w-full h-full flex items-center justify-center text-emerald-500/30">
                                <ImageIcon class="w-8 h-8" />
                             </div>
                          </div>

                          <!-- 中间信息 -->
                          <div class="flex-1 flex flex-col justify-center">
                             <div class="flex items-center gap-2 mb-1">
                                <h4 class="text-lg font-bold text-emerald-100">{{ spot.spot_name }}</h4>
                                <span class="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded">{{ spot.en_name || 'N/A' }}</span>
                             </div>
                             <p class="text-sm text-emerald-100/60 line-clamp-2 mb-2">{{ spot.description || '暂无简介' }}</p>
                             <div class="flex items-center gap-4 text-xs text-emerald-400/80">
                                <span class="flex items-center gap-1"><Users class="w-3.5 h-3.5" /> 最大承载: <b class="text-emerald-300">{{ spot.max_capacity }}</b></span>
                                <span>排序权重: {{ spot.sort_order }}</span>
                             </div>
                          </div>

                          <!-- 右侧操作 -->
                          <div class="flex flex-col gap-2 justify-center border-l border-emerald-500/10 pl-4">
                             <button @click="openSpotModal(spot)" class="p-2 text-emerald-400 hover:bg-emerald-500/20 rounded transition-colors" title="编辑">
                                <Edit class="w-4 h-4" />
                             </button>
                             <button @click="handleDeleteSpot(spot.id)" class="p-2 text-red-400 hover:bg-red-500/20 rounded transition-colors" title="删除">
                                <Trash2 class="w-4 h-4" />
                             </button>
                          </div>
                       </div>
                   </div>
                </div>
             </div>
          </div>
          <!-- ================== 互动控制台 ================== -->
          <div v-if="activeMenu === 'control'" class="flex-1 flex flex-col overflow-hidden animate-fade-in">
             <div class="flex-shrink-0 flex justify-between items-center p-6 border-b border-emerald-500/10">
                <h3 class="text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3 tracking-wider">互动控制台</h3>
             </div>
             
             <div class="flex-1 overflow-y-auto p-6 custom-scrollbar">
                <div class="max-w-4xl mx-auto pb-12 flex flex-col gap-8">
                   
                   <!-- 主题切换 -->
                   <section class="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-5">
                      <h4 class="text-emerald-100 font-bold flex items-center gap-2 mb-4"><Palette class="w-5 h-5 text-emerald-400" /> 全局主题切换</h4>
                      <div class="flex gap-4 flex-wrap">
                         <button @click="setTheme('default')" :class="['px-6 py-3 rounded-lg border flex flex-col items-center gap-2 transition-all', currentTheme === 'default' ? 'border-emerald-400 bg-emerald-500/20 shadow-[0_0_15px_rgba(52,211,153,0.3)] text-emerald-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
                            <Moon class="w-6 h-6" />
                            <span class="text-sm">极夜模式</span>
                         </button>
                         <button @click="setTheme('spring_season')" :class="['px-6 py-3 rounded-lg border flex flex-col items-center gap-2 transition-all', currentTheme === 'spring_season' ? 'border-lime-400 bg-lime-500/20 shadow-[0_0_15px_rgba(132,204,22,0.3)] text-lime-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
                            <Leaf class="w-6 h-6" />
                            <span class="text-sm">春季主题</span>
                         </button>
                         <button @click="setTheme('summer')" :class="['px-6 py-3 rounded-lg border flex flex-col items-center gap-2 transition-all', currentTheme === 'summer' ? 'border-sky-400 bg-sky-500/20 shadow-[0_0_15px_rgba(56,189,248,0.3)] text-sky-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
                            <Sun class="w-6 h-6" />
                            <span class="text-sm">夏季主题</span>
                         </button>
                         <button @click="setTheme('autumn')" :class="['px-6 py-3 rounded-lg border flex flex-col items-center gap-2 transition-all', currentTheme === 'autumn' ? 'border-orange-400 bg-orange-500/20 shadow-[0_0_15px_rgba(249,115,22,0.3)] text-orange-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
                            <Wind class="w-6 h-6" />
                            <span class="text-sm">秋季主题</span>
                         </button>
                         <button @click="setTheme('winter')" :class="['px-6 py-3 rounded-lg border flex flex-col items-center gap-2 transition-all', currentTheme === 'winter' ? 'border-slate-400 bg-slate-500/20 shadow-[0_0_15px_rgba(148,163,184,0.3)] text-slate-300' : 'border-emerald-500/30 hover:bg-emerald-900/40 text-emerald-100/60']">
                            <Snowflake class="w-6 h-6" />
                            <span class="text-sm">冬季主题</span>
                         </button>
                      </div>
                   </section>

                   <!-- 数字人广播 -->
                   <section class="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-5">
                      <h4 class="text-emerald-100 font-bold flex items-center gap-2 mb-4"><Mic class="w-5 h-5 text-emerald-400" /> 数字人主动广播</h4>
                      <div class="flex gap-2">
                         <input v-model="broadcastMsg" @keyup.enter="handleBroadcast" type="text" placeholder="输入要让 Fay 播报的紧急通知或导览词..." class="flex-1 bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40" />
                         <button @click="handleBroadcast" class="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_10px_rgba(52,211,153,0.3)] flex items-center gap-2 whitespace-nowrap">
                            <Send class="w-4 h-4" /> 立即播报
                         </button>
                      </div>
                   </section>

                   <!-- 客流模拟器 -->
                   <section class="bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-5">
                      <h4 class="text-emerald-100 font-bold flex items-center gap-2 mb-4"><Activity class="w-5 h-5 text-emerald-400" /> 客流压力模拟器</h4>
                      <p class="text-xs text-emerald-100/50 mb-4">调整以下景点人数并保存，以在右侧面板及地图上观察拥挤预警联动效果。</p>
                      <div class="flex flex-col gap-3">
                         <div v-for="spot in spotList" :key="spot.id" class="flex items-center gap-4 bg-[#020b14] border border-emerald-500/10 p-3 rounded">
                            <span class="w-32 text-sm text-emerald-100 truncate">{{ spot.spot_name }}</span>
                            <div class="flex-1 flex items-center gap-3">
                               <input type="range" v-model.number="spot.temp_visitors" :max="spot.max_capacity * 1.5" min="0" class="flex-1 accent-emerald-500" />
                               <input type="number" v-model.number="spot.temp_visitors" class="w-20 bg-emerald-900/30 border border-emerald-500/30 rounded px-2 py-1 text-sm text-emerald-100 text-center" />
                               <span class="text-xs text-emerald-500/60 w-24">/ {{ spot.max_capacity }} MAX</span>
                            </div>
                            <button @click="applyFlow(spot)" class="px-3 py-1 bg-emerald-500/20 hover:bg-emerald-500/40 border border-emerald-400/50 rounded text-emerald-300 text-xs transition-colors">
                               应用
                            </button>
                         </div>
                      </div>
                   </section>

                </div>
             </div>
          </div>
        </main>
      </div>
    </div>
  </div>

  <!-- 新增/编辑景点的内部子弹窗 -->
    <div v-if="spotModalVisible" class="absolute inset-0 z-[110] flex items-center justify-center bg-black/60 backdrop-blur-sm">
    <div class="w-[90%] max-w-[500px] bg-[#021815] border border-emerald-400/50 rounded-lg shadow-2xl p-6 relative">
          <button @click="spotModalVisible = false" class="absolute top-4 right-4 text-emerald-400/60 hover:text-emerald-300"><X class="w-5 h-5" /></button>
          <h3 class="text-lg font-bold text-emerald-300 mb-6">{{ isEditingSpot ? '编辑景点' : '新增景点' }}</h3>
          
          <div class="flex flex-col gap-4">
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70">景点名称</label>
                <input v-model="spotForm.spot_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" />
             </div>
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70">英文名称</label>
                <input v-model="spotForm.en_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" />
             </div>
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70">最大承载量 (人)</label>
                <input v-model="spotForm.max_capacity" type="number" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" />
             </div>
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70 mb-1">景点图片</label>
                <div 
                  class="relative w-full h-32 rounded-lg border-2 border-dashed border-emerald-500/30 bg-emerald-900/10 overflow-hidden flex flex-col items-center justify-center cursor-pointer group hover:border-emerald-400 hover:bg-emerald-900/20 transition-all duration-300"
                  @click="$refs.spotFileInput.click()"
                >
                  <img v-if="spotForm.image_url" :src="spotForm.image_url" class="absolute inset-0 w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" />
                  
                  <!-- 遮罩层与更换提示 (有图片时) -->
                  <div v-if="spotForm.image_url" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center gap-1 z-10 backdrop-blur-[2px]">
                     <Upload class="w-6 h-6 text-emerald-300 transform -translate-y-1 group-hover:translate-y-0 transition-transform duration-300" />
                     <span class="text-xs font-bold tracking-widest text-emerald-300">更换景点图片</span>
                  </div>

                  <!-- 初始无图片状态 -->
                  <div v-if="!spotForm.image_url" class="flex flex-col items-center justify-center gap-2 z-0">
                     <div class="p-2 rounded-full bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                       <Upload class="w-6 h-6 text-emerald-500/60 group-hover:text-emerald-400 transition-colors" />
                     </div>
                     <div class="flex flex-col items-center gap-1">
                       <span class="text-xs text-emerald-400 font-bold tracking-wide">点击上传景点图片</span>
                       <span class="text-[9px] text-emerald-500/50 font-mono">JPG / PNG / WEBP, &lt;16MB</span>
                     </div>
                  </div>
                  
                  <!-- 上传中状态 -->
                  <div v-if="uploadingSpotImg" class="absolute inset-0 bg-[#021815]/90 flex flex-col items-center justify-center gap-2 z-20 backdrop-blur-sm">
                    <Loader2 class="w-6 h-6 text-emerald-400 animate-spin" />
                    <span class="text-[10px] tracking-widest text-emerald-400 animate-pulse">UPLOADING...</span>
                  </div>
                  
                  <input type="file" ref="spotFileInput" class="hidden" accept="image/*" @change="e => handleImageUpload(e, 'spot')" />
                </div>
             </div>
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70">景点介绍</label>
                <textarea v-model="spotForm.description" rows="3" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none resize-none custom-scrollbar"></textarea>
             </div>
             
             <div class="flex justify-end gap-3 mt-4">
                <button @click="spotModalVisible = false" class="px-4 py-2 text-sm text-emerald-400/80 hover:text-emerald-300">取消</button>
                <button @click="handleSaveSpot" class="px-4 py-2 text-sm bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_10px_rgba(52,211,153,0.3)] flex items-center gap-2">
                   <Loader2 v-if="savingSpot" class="w-4 h-4 animate-spin" /> 保存
                </button>
             </div>
          </div>
       </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, Database, Map, MapPin, Save, Plus, Edit2, Trash2, Loader2, Upload, Image as ImageIcon, Users, Edit, Settings, Palette, Moon, Sun, Leaf, Wind, Snowflake, Mic, Send, Activity } from 'lucide-vue-next'
import { getScenicInfo, updateScenicInfo, getScenicSpots, addScenicSpot, updateScenicSpot, deleteScenicSpot, uploadImage, updateSpotFlow } from '../../api/scenic'
import { sendFayMessage } from '../../api/fay'
import { getConfig, updateConfig } from '../../api/config'
import { Message } from '../../utils/message'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'data-updated', 'theme-changed'])

const close = () => {
  emit('update:visible', false)
}

// 菜单状态
const activeMenu = ref('scenic') // 'scenic' | 'spots' | 'control'

// ================== 控制台逻辑 ==================
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
      emit('theme-changed')
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
  emit('theme-changed')
  
  // 保存到数据库
  try {
    await updateConfig('theme', theme)
    Message.success('主题已保存')
  } catch (error) {
    Message.error('主题配置保存失败')
  }
}

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

const applyFlow = async (spot) => {
  try {
    const res = await updateSpotFlow(spot.id, spot.temp_visitors)
    if (res && res.status === 'success') {
      Message.success(`${spot.spot_name} 客流更新成功`)
      emit('data-updated')
    } else {
      Message.error('客流更新失败')
    }
  } catch (error) {
    Message.error('网络异常，客流更新失败')
  }
}

// ================== 景区信息管理逻辑 ==================
const loadingScenic = ref(false)
const scenicForm = ref({
  id: null,
  scenic_name: '',
  scenic_en_name: '',
  address: '',
  cover_image: '',
  ticket_price: '',
  opening_hours: '',
  introduction: ''
})

const fetchScenicInfo = async () => {
  loadingScenic.value = true
  try {
    const res = await getScenicInfo()
    if (res && res.status === 'success' && res.data) {
      scenicForm.value = { ...res.data }
    }
  } catch (error) {
    console.error('获取景区信息失败:', error)
  } finally {
    loadingScenic.value = false
  }
}

const handleSaveScenic = async () => {
  if (!scenicForm.value.id) return Message.warning('景区信息不存在，无法更新');
  try {
    const res = await updateScenicInfo(scenicForm.value.id, scenicForm.value);
    if (res && res.status === 'success') {
      Message.success('景区全局配置保存成功！');
      emit('data-updated'); // 通知父组件刷新数据
    } else {
      Message.error('保存失败: ' + res.message);
    }
  } catch (error) {
    console.error('保存景区信息失败:', error);
    Message.error('保存失败，请检查网络或后端服务');
  }
}

// ================== 景点列表管理逻辑 ==================
const loadingSpots = ref(false)
const spotList = ref([])

const fetchSpotList = async () => {
  loadingSpots.value = true
  try {
    const res = await getScenicSpots()
    if (res && res.status === 'success') {
      // 为控制台添加 temp_visitors 用于绑定滑动条
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

// 获取状态颜色标签
const getStatusColor = (status) => {
  if (status === '畅通') return 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10'
  if (status === '拥挤') return 'text-red-400 border-red-400/30 bg-red-400/10'
  return 'text-amber-400 border-amber-400/30 bg-amber-400/10'
}

// 景点弹窗逻辑
const spotModalVisible = ref(false)
const isEditingSpot = ref(false)
const savingSpot = ref(false)
const spotForm = ref({
  id: null,
  spot_name: '',
  en_name: '',
  max_capacity: 1000,
  image_url: '',
  description: ''
})

const openSpotModal = (spot = null) => {
  if (spot) {
    isEditingSpot.value = true
    spotForm.value = { ...spot }
  } else {
    isEditingSpot.value = false
    spotForm.value = {
      id: null,
      spot_name: '',
      en_name: '',
      max_capacity: 1000,
      image_url: '',
      description: ''
    }
  }
  spotModalVisible.value = true
}

const handleSaveSpot = async () => {
  if (!spotForm.value.spot_name || !spotForm.value.max_capacity) {
    return Message.warning('请填写景点名称和最大承载量');
  }
  
  savingSpot.value = true
  try {
    let res;
    // 后端外键要求有 scenic_id，当前我们默认为 1（云梦山）
    const payload = { ...spotForm.value, scenic_id: 1 }; 
    
    if (isEditingSpot.value) {
      res = await updateScenicSpot(spotForm.value.id, payload)
    } else {
      res = await addScenicSpot(payload)
    }
    
    if (res && res.status === 'success') {
      spotModalVisible.value = false
      fetchSpotList() // 刷新列表
      emit('data-updated') // 通知大屏刷新
      Message.success('保存景点成功！')
    } else {
      Message.error('保存景点失败: ' + res.message)
    }
  } catch (error) {
    console.error('保存景点失败:', error)
    Message.error('保存失败，请检查网络或后端服务')
  } finally {
    savingSpot.value = false
  }
}

const handleDeleteSpot = async (id) => {
  if (!confirm('确定要删除此景点吗？删除后不可恢复。')) return;
  try {
    const res = await deleteScenicSpot(id)
    if (res && res.status === 'success') {
      fetchSpotList() // 刷新列表
      emit('data-updated')
      Message.success('删除成功')
    } else {
      Message.error('删除失败: ' + res.message)
    }
  } catch (error) {
    console.error('删除景点失败:', error)
    Message.error('删除失败，请检查网络')
  }
}

// ================== 图片上传通用逻辑 ==================
const uploadingScenicImg = ref(false)
const uploadingSpotImg = ref(false)
const scenicFileInput = ref(null)
const spotFileInput = ref(null)

const handleImageUpload = async (event, type) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 校验文件类型和大小 (前端先拦截一次)
  if (!file.type.startsWith('image/')) {
    Message.warning('请选择有效的图片文件')
    return
  }
  if (file.size > 16 * 1024 * 1024) {
    Message.warning('图片大小不能超过 16MB')
    return
  }

  const isScenic = type === 'scenic'
  if (isScenic) uploadingScenicImg.value = true
  else uploadingSpotImg.value = true

  try {
    const res = await uploadImage(file)
    if (res && res.status === 'success' && res.data?.url) {
      if (isScenic) {
        scenicForm.value.cover_image = res.data.url
      } else {
        spotForm.value.image_url = res.data.url
      }
      Message.success('图片上传成功')
    } else {
      Message.error('上传失败: ' + (res?.message || '未知错误'))
    }
  } catch (error) {
    console.error('图片上传异常:', error)
    Message.error('网络或服务器异常，图片上传失败')
  } finally {
    if (isScenic) uploadingScenicImg.value = false
    else uploadingSpotImg.value = false
    // 清空 input value 确保同名文件可再次触发 change 事件
    event.target.value = ''
  }
}

// 监听弹窗显示，自动加载数据
watch(() => props.visible, (newVal) => {
  if (newVal) {
    fetchScenicInfo()
    fetchSpotList()
    fetchThemeConfig()
  }
})
</script>

<style scoped>
/* 简单的淡入动画 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}
</style>
