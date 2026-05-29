<template>
  <transition name="fade-overlay">
    <div v-if="store.isInteractMode" class="fixed inset-0 z-40 flex items-center justify-center overflow-hidden">
      
      <!-- 沉浸式背景：深色毛玻璃 + 动态网格 -->
      <div class="absolute inset-0 bg-black/80 backdrop-blur-xl tech-bg-photo"></div>
      
      <!-- 主内容区：AI 照相馆悬浮舱 -->
      <div class="relative w-[90%] max-w-[1200px] h-[80vh] flex tech-card transform-style-3d">
        
        <!-- 左侧：实时摄像头画面 -->
        <div class="flex-1 relative border-r border-[var(--app-glow-1)] flex flex-col items-center justify-center p-6">
          
          <!-- 标题栏 -->
          <div class="absolute top-6 left-6 flex items-center gap-3 z-10">
            <div class="w-3 h-3 rounded-full animate-pulse" style="background-color: var(--color-cyan-400); box-shadow: 0 0 10px var(--color-cyan-400);"></div>
            <h2 class="text-2xl font-black text-transparent bg-clip-text tracking-widest font-mono bg-gradient-to-r from-[var(--color-cyan-300)] to-[var(--color-cyan-500)]">
              AI 景区穿越照相馆
            </h2>
          </div>
          
          <!-- 退出按钮 -->
          <button 
            @click="exitPhotoRoom"
            class="absolute top-6 right-6 px-4 py-2 border border-red-500/50 text-red-400 rounded hover:bg-red-500/20 hover:text-red-300 transition-all z-10 flex items-center gap-2"
          >
            <XCircleIcon class="w-5 h-5" />
            退出
          </button>

          <!-- 摄像头容器 (带科幻边框) -->
          <div class="relative w-full max-w-[450px] aspect-[3/4] border-2 rounded-lg overflow-hidden mt-10 group" style="border-color: rgba(var(--color-cyan-500), 0.3); box-shadow: 0 0 30px rgba(var(--color-cyan-500), 0.1);">
            
            <!-- 取景框角标 -->
            <div class="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 z-10" style="border-color: var(--color-cyan-400);"></div>
            <div class="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 z-10" style="border-color: var(--color-cyan-400);"></div>
            <div class="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 z-10" style="border-color: var(--color-cyan-400);"></div>
            <div class="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 z-10" style="border-color: var(--color-cyan-400);"></div>

            <!-- 扫描线动画 -->
            <div class="absolute inset-0 w-full h-[10%] animate-scanline z-10 pointer-events-none scanline-gradient"></div>

            <!-- 摄像头 Video 元素 -->
            <video 
              ref="videoElement" 
              class="w-full h-full object-cover scale-x-[-1]" 
              autoplay 
              playsinline
              muted
            ></video>

            <!-- 状态提示覆盖层 -->
            <div v-if="!cameraReady && !cameraError" class="absolute inset-0 flex flex-col items-center justify-center bg-black/60 z-20">
              <Loader2Icon class="w-10 h-10 animate-spin mb-4" style="color: var(--color-cyan-400);" />
              <p class="font-mono tracking-widest" style="color: var(--color-cyan-300);">初始化光学传感器...</p>
            </div>
            
            <div v-if="cameraError" class="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-20">
              <AlertTriangleIcon class="w-12 h-12 text-red-500 mb-4" />
              <p class="text-red-400">{{ cameraError }}</p>
              <button @click="initCamera" class="mt-4 px-4 py-2 border hover:bg-[var(--color-cyan-500)]/20 transition-colors" style="color: var(--color-cyan-400); border-color: var(--color-cyan-500);">
                重试
              </button>
            </div>
            
            <!-- 倒计时覆盖层 -->
            <div v-if="isCountingDown" class="absolute inset-0 flex items-center justify-center bg-black/40 z-30">
              <span class="text-9xl font-black text-white text-shadow-glow animate-ping-slow countdown-shadow">
                {{ countdown }}
              </span>
            </div>

            <!-- 拍照闪光层 -->
            <div v-if="showFlash" class="absolute inset-0 bg-white z-40 animate-flash pointer-events-none"></div>
          </div>

          <!-- 控制台区 -->
          <div class="mt-8 flex flex-col items-center gap-4">
             <button 
              @click="takePhoto"
              :disabled="!cameraReady || isCountingDown || isProcessing"
              class="relative group"
            >
              <div class="absolute -inset-1 rounded-full blur opacity-50 group-hover:opacity-100 transition duration-200 group-disabled:opacity-0 bg-gradient-to-r from-[var(--color-cyan-400)] to-[var(--color-cyan-600)]"></div>
              <div class="relative px-8 py-3 bg-black rounded-full border flex items-center gap-3 group-disabled:border-gray-600 group-disabled:text-gray-500" style="border-color: var(--color-cyan-500);">
                <CameraIcon class="w-6 h-6 group-disabled:text-gray-500" style="color: var(--color-cyan-400);" />
                <span class="text-lg font-bold tracking-widest group-disabled:text-gray-500" style="color: var(--color-cyan-300);">
                  {{ isProcessing ? 'AI 融合中...' : '生成穿越海报' }}
                </span>
              </div>
            </button>
            <p class="text-sm font-mono opacity-60" style="color: var(--color-cyan-500);">请注视镜头并保持微笑</p>
          </div>
        </div>

        <!-- 右侧：生成结果展示区 -->
        <div class="w-[400px] bg-black/20 p-6 flex flex-col relative overflow-hidden">
          <!-- 装饰背景 -->
          <div class="absolute -top-20 -right-20 w-64 h-64 rounded-full blur-3xl opacity-10" style="background-color: var(--color-cyan-500);"></div>
          
          <h3 class="text-xl font-bold mb-6 flex items-center gap-2" style="color: var(--color-cyan-300);">
            <ImageIcon class="w-5 h-5" />
            合成影像结果
          </h3>

          <!-- 图片占位/展示区 -->
          <div class="flex-1 w-full border border-dashed rounded-lg flex flex-col items-center justify-center relative overflow-hidden group bg-black/30" style="border-color: rgba(var(--color-cyan-500), 0.3);">
            <template v-if="!resultImage && !isProcessing">
              <UserFocusIcon class="w-16 h-16 mb-4 opacity-50" style="color: var(--color-cyan-900);" />
              <p class="font-mono text-center opacity-70" style="color: var(--color-cyan-700);">等待拍摄...<br>照片将显示在此处</p>
            </template>
            
            <template v-if="isProcessing">
               <div class="flex flex-col items-center w-3/4">
                 <div class="w-full h-2 bg-gray-800 rounded-full overflow-hidden mb-4">
                   <div class="h-full animate-progress bg-gradient-to-r from-[var(--color-cyan-500)] to-[var(--color-cyan-300)]"></div>
                 </div>
                 <p class="text-sm animate-pulse" style="color: var(--color-cyan-400);">AI 正在进行风格迁移与融合渲染...</p>
               </div>
            </template>

            <img 
              v-if="resultImage" 
              :src="resultImage" 
              class="w-full h-full object-contain z-10"
              alt="合成结果" 
            />
          </div>

          <!-- 扫码区 -->
          <div class="mt-6 h-[120px] border rounded-lg p-4 flex items-center gap-4 bg-black/20" :class="{ 'opacity-30': !resultImage }" style="border-color: rgba(var(--color-cyan-500), 0.3);">
            <div class="w-[80px] h-[80px] bg-white rounded p-1">
              <!-- 这里可以用真实二维码组件替换，目前用占位图 -->
              <QrCodeIcon class="w-full h-full text-black" />
            </div>
            <div class="flex-1">
              <h4 class="font-bold mb-1" style="color: var(--color-cyan-300);">扫描获取高清大图</h4>
              <p class="text-xs leading-relaxed opacity-80" style="color: var(--color-cyan-500);">请使用微信或浏览器扫描左侧二维码，将照片保存至手机。</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { 
  XCircle as XCircleIcon, 
  Camera as CameraIcon,
  Loader2 as Loader2Icon,
  AlertTriangle as AlertTriangleIcon,
  Image as ImageIcon,
  User as UserFocusIcon,
  QrCode as QrCodeIcon
} from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'

const store = useScenicStore()

// 摄像头相关
const videoElement = ref(null)
const mediaStream = ref(null)
const cameraReady = ref(false)
const cameraError = ref('')

// 拍照流程状态
const isCountingDown = ref(false)
const countdown = ref(3)
const showFlash = ref(false)
const isProcessing = ref(false)
const resultImage = ref(null)

// 初始化摄像头
const initCamera = async () => {
  cameraError.value = ''
  cameraReady.value = false
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1080 },
        height: { ideal: 1920 },
        facingMode: 'user' // 优先前置摄像头
      }
    })
    mediaStream.value = stream
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      // 等待视频元数据加载完成
      videoElement.value.onloadedmetadata = () => {
        cameraReady.value = true
      }
    }
  } catch (err) {
    console.error('无法访问摄像头:', err)
    cameraError.value = '无法访问摄像头，请检查权限设置。'
  }
}

// 停止摄像头
const stopCamera = () => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
    mediaStream.value = null
  }
  cameraReady.value = false
}

// 退出互动模式
const exitPhotoRoom = () => {
  store.isInteractMode = false
}

// 监听模式切换
watch(() => store.isInteractMode, (newVal) => {
  if (newVal) {
    // 延迟一点初始化摄像头，等弹窗动画差不多完成
    setTimeout(() => {
      initCamera()
    }, 300)
    resultImage.value = null
  } else {
    stopCamera()
  }
})

// 拍照核心逻辑
const takePhoto = () => {
  if (!cameraReady.value) return
  
  isCountingDown.value = true
  countdown.value = 3
  resultImage.value = null
  
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      isCountingDown.value = false
      executeCapture()
    }
  }, 1000)
}

// 执行抓拍和模拟 AI 处理
const executeCapture = () => {
  // 1. 闪光灯特效
  showFlash.value = true
  setTimeout(() => { showFlash.value = false }, 150)

  // 2. 截取画面到 Canvas (获取纯净的人物原图)
  const canvas = document.createElement('canvas')
  // 强制生成竖屏比例 (3:4) 的图片，以匹配取景框
  const targetRatio = 3 / 4;
  const vW = videoElement.value.videoWidth
  const vH = videoElement.value.videoHeight
  const videoRatio = vW / vH;

  let sourceX = 0, sourceY = 0, sourceWidth = vW, sourceHeight = vH;

  if (videoRatio > targetRatio) {
    // 视频太宽了，需要裁切掉左右两边
    sourceWidth = vH * targetRatio;
    sourceX = (vW - sourceWidth) / 2;
  } else {
    // 视频太高了，需要裁切掉上下两边
    sourceHeight = vW / targetRatio;
    sourceY = (vH - sourceHeight) / 2;
  }

  canvas.width = 900 // 固定输出宽度
  canvas.height = 1200 // 固定输出高度，保持 3:4
  const ctx = canvas.getContext('2d')
  
  // 处理镜像翻转
  ctx.translate(canvas.width, 0)
  ctx.scale(-1, 1)
  
  // 将计算好的居中裁切区域绘制到 Canvas 上
  ctx.drawImage(videoElement.value, sourceX, sourceY, sourceWidth, sourceHeight, 0, 0, canvas.width, canvas.height)
  
  const base64Image = canvas.toDataURL('image/jpeg', 0.8)
  
  // 3. 进入处理状态
  isProcessing.value = true
  
  // TODO: 后续在这里将 base64Image 发送给后端的 AI 生图接口
  // 请求体示例: { "image": base64Image, "prompt": "人物与赛博朋克风景融合..." }
  
  // 目前用 setTimeout 模拟网络请求和 AI 生成时间
  setTimeout(() => {
    isProcessing.value = false
    // 模拟后端返回了生成好的带有风景的 AI 图像
    // 这里暂且展示游客的原图截屏
    resultImage.value = base64Image
  }, 3000)
}

onUnmounted(() => {
  stopCamera()
})

</script>

<style scoped>
.tech-bg-photo {
  background-image: 
    radial-gradient(circle at 50% 50%, rgba(var(--color-cyan-500), 0.05) 0%, transparent 50%),
    linear-gradient(rgba(var(--color-cyan-500), 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(var(--color-cyan-500), 0.02) 1px, transparent 1px);
  background-size: 100% 100%, 30px 30px, 30px 30px;
  background-position: center center;
}

.scanline-gradient {
  background-image: linear-gradient(to bottom, transparent, rgba(var(--color-cyan-400), 0.2), transparent);
}

.countdown-shadow {
  filter: drop-shadow(0 0 20px var(--color-cyan-500));
}

/* 渐显弹窗动画 */
.fade-overlay-enter-active,
.fade-overlay-leave-active {
  transition: opacity 0.5s ease;
}
.fade-overlay-enter-from,
.fade-overlay-leave-to {
  opacity: 0;
}

/* 扫描线动画 (复用/覆盖) */
@keyframes scanline {
  0% { top: -10%; opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
.animate-scanline { animation: scanline 3s linear infinite; }

/* 倒计时心跳放大 */
@keyframes ping-slow {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}
.animate-ping-slow { animation: ping-slow 1s ease-in-out infinite; }

/* 闪光灯 */
@keyframes flash {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}
.animate-flash { animation: flash 0.15s ease-out; }

/* 进度条动画 */
@keyframes progress {
  0% { width: 0%; }
  50% { width: 70%; }
  100% { width: 100%; }
}
.animate-progress { animation: progress 3s ease-in-out forwards; }
</style>