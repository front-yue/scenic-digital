<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-500 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="visible" class="fixed inset-0 z-[200] flex items-center justify-center">
        <!-- 模糊背景遮罩 -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="close"></div>
        
        <!-- 弹窗主体 -->
        <div class="relative w-[500px] max-w-[90vw] bg-[#061226]/95 border border-cyan-500/50 rounded-xl shadow-[0_0_40px_rgba(0,240,255,0.2)] flex flex-col overflow-hidden">
          
          <!-- 装饰边角 -->
          <div class="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-cyan-400 pointer-events-none z-30"></div>
          <div class="absolute top-0 right-0 w-6 h-6 border-t-2 border-r-2 border-cyan-400 pointer-events-none z-30"></div>
          <div class="absolute bottom-0 left-0 w-6 h-6 border-b-2 border-l-2 border-cyan-400 pointer-events-none z-30"></div>
          <div class="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-cyan-400 pointer-events-none z-30"></div>
          
          <!-- 发光背景特效 -->
          <div class="absolute -top-20 -right-20 w-40 h-40 bg-cyan-500/20 rounded-full blur-[60px] pointer-events-none"></div>

          <!-- 头部 -->
          <div class="h-14 border-b border-cyan-500/30 flex items-center justify-between px-6 bg-gradient-to-r from-cyan-900/40 to-transparent relative z-10">
            <div class="flex items-center gap-3">
              <div class="p-1.5 bg-cyan-500/20 rounded-lg border border-cyan-400/30">
                <Info class="w-5 h-5 text-cyan-400" />
              </div>
              <h3 class="text-lg font-bold text-cyan-300 tracking-widest text-shadow-glow">系统版本信息</h3>
            </div>
            <button @click="close" class="text-cyan-500/70 hover:text-cyan-300 transition-colors p-1 hover:bg-cyan-500/10 rounded-lg">
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- 内容区 -->
          <div class="p-6 space-y-6 relative z-10">
            <!-- 版本号展示 -->
            <div class="flex items-center justify-between bg-cyan-950/30 p-4 rounded-lg border border-cyan-800/50">
              <div class="flex flex-col">
                <span class="text-sm text-cyan-500/80 mb-1">当前版本</span>
                <span class="text-2xl font-black text-white tracking-wider font-mono">v2.1.0<span class="text-cyan-400 text-sm ml-2 font-normal">智游版</span></span>
              </div>
              <div class="w-12 h-12 rounded-full border-2 border-dashed border-cyan-500/50 flex items-center justify-center animate-[spin_10s_linear_infinite]">
                <div class="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center">
                  <div class="w-3 h-3 bg-cyan-400 rounded-full shadow-[0_0_10px_#00f0ff]"></div>
                </div>
              </div>
            </div>

            <!-- 更新内容 -->
            <div class="space-y-3">
              <div class="flex items-center gap-2 text-cyan-300">
                <CheckCircle2 class="w-4 h-4" />
                <h4 class="font-bold tracking-wider">本次更新内容</h4>
              </div>
              <ul class="space-y-2 text-sm text-gray-300 ml-6">
                <li class="relative before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:bg-cyan-500 before:rounded-full before:-ml-4">
                  <strong class="text-cyan-100">MCP 引擎升级：</strong>实现动态场景地理位置感知，路线规划更智能。
                </li>
                <li class="relative before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:bg-cyan-500 before:rounded-full before:-ml-4">
                  <strong class="text-cyan-100">高德雷达系统：</strong>新增拖拽/缩放全息弹窗，接入步行导航与单点雷达双模式。
                </li>
                <li class="relative before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:bg-cyan-500 before:rounded-full before:-ml-4">
                  <strong class="text-cyan-100">赛博视觉重构：</strong>全站适配极夜蓝风格，重写 AdminOverlay 控制台与 Driver.js 引导。
                </li>
                <li class="relative before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:bg-cyan-500 before:rounded-full before:-ml-4">
                  <strong class="text-cyan-100">全新演示数据：</strong>内置杭州西湖风景名胜区高精度 Mock 数据。
                </li>
              </ul>
            </div>

            <!-- 注意事项 -->
            <div class="bg-amber-950/30 border border-amber-500/30 rounded-lg p-4 space-y-2">
              <div class="flex items-center gap-2 text-amber-400">
                <AlertTriangle class="w-4 h-4" />
                <h4 class="font-bold tracking-wider text-sm">运行注意事项</h4>
              </div>
              <ul class="text-xs text-amber-200/70 space-y-1.5 ml-6 list-disc">
                <li>由于浏览器安全策略，Fay 数字人语音收音需允许【麦克风】权限。</li>
                <li>地图模块依赖高德 JS API 及 Web 服务 API，请确保 <code>.env</code> 密钥有效。</li>
                <li>若 MCP 导航失败，请检查 Python 后端服务 (端口 8888) 是否正常运行。</li>
              </ul>
            </div>
          </div>

          <!-- 底部按钮 -->
          <div class="p-4 border-t border-cyan-500/20 bg-black/20 flex justify-end relative z-10">
            <button 
              @click="close" 
              class="px-6 py-2 bg-cyan-600/20 hover:bg-cyan-500/40 border border-cyan-500/50 rounded text-cyan-100 text-sm tracking-wider transition-all hover:shadow-[0_0_15px_rgba(0,240,255,0.4)]"
            >
              系统确认
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { X, Info, AlertTriangle, CheckCircle2 } from 'lucide-vue-next'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible'])

const close = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
/* 发光文字特效 */
.text-shadow-glow {
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
}
</style>
