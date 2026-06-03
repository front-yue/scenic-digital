<template>
  <transition name="fade-overlay">
    <div v-if="store.isInteractMode" class="fixed inset-0 z-40 flex items-center justify-center overflow-hidden">
      
      <!-- 沉浸式背景 -->
      <div class="absolute inset-0 bg-black/80 backdrop-blur-xl tech-bg-photo"></div>
      
      <!-- 主内容区：单屏状态驱动 -->
      <div class="relative w-full h-full md:w-[90%] md:max-w-[700px] md:h-[90vh] flex flex-col tech-card transform-style-3d md:rounded-2xl overflow-hidden">
        
        <!-- 标题栏 (始终显示) -->
        <div class="absolute top-0 left-0 right-0 z-20 flex items-center justify-between p-3 md:p-5">
          <div class="flex items-center gap-2 md:gap-3">
            <div class="w-2 h-2 md:w-3 md:h-3 rounded-full animate-pulse" style="background-color: var(--color-cyan-400); box-shadow: 0 0 10px var(--color-cyan-400);"></div>
            <h2 class="text-base md:text-2xl font-black text-transparent bg-clip-text tracking-wider md:tracking-widest font-mono bg-gradient-to-r from-[var(--color-cyan-300)] to-[var(--color-cyan-500)]">
              AI 景区穿越照相馆
            </h2>
          </div>
          <button 
            @click="exitPhotoRoom"
            class="px-3 py-1.5 md:px-4 md:py-2 border border-red-500/50 text-red-400 rounded hover:bg-red-500/20 hover:text-red-300 transition-all flex items-center gap-1.5 md:gap-2 text-xs md:text-base"
          >
            <XCircleIcon class="w-4 h-4 md:w-5 md:h-5" />
            退出
          </button>
        </div>

        <!-- ========== 状态一：拍照区 ========= -->
        <transition name="fade-step" mode="out-in">
          <div v-if="!isProcessing && !resultImage" key="camera" class="flex-1 flex flex-col items-center justify-center p-4 md:p-6">
            
            <!-- 摄像头容器 -->
            <div class="relative w-full max-w-[300px] md:max-w-[420px] aspect-[3/4] border-2 rounded-lg overflow-hidden group" style="border-color: rgba(var(--color-cyan-500), 0.3); box-shadow: 0 0 30px rgba(var(--color-cyan-500), 0.1);">
              <!-- 取景框角标 -->
              <div class="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 z-10" style="border-color: var(--color-cyan-400);"></div>
              <div class="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 z-10" style="border-color: var(--color-cyan-400);"></div>
              <div class="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 z-10" style="border-color: var(--color-cyan-400);"></div>
              <div class="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 z-10" style="border-color: var(--color-cyan-400);"></div>

              <div class="absolute inset-0 w-full h-[10%] animate-scanline z-10 pointer-events-none scanline-gradient"></div>

              <video ref="videoElement" class="w-full h-full object-cover scale-x-[-1]" autoplay playsinline muted></video>

              <!-- 初始化中 -->
              <div v-if="!cameraReady && !cameraError" class="absolute inset-0 flex flex-col items-center justify-center bg-black/60 z-20">
                <Loader2Icon class="w-10 h-10 animate-spin mb-4" style="color: var(--color-cyan-400);" />
                <p class="font-mono tracking-widest text-sm" style="color: var(--color-cyan-300);">初始化光学传感器...</p>
              </div>
              
              <!-- 摄像头错误 -->
              <div v-if="cameraError" class="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-20">
                <AlertTriangleIcon class="w-12 h-12 text-red-500 mb-4" />
                <p class="text-red-400 text-sm">{{ cameraError }}</p>
                <button @click="initCamera" class="mt-4 px-4 py-2 border text-sm hover:bg-[var(--color-cyan-500)]/20 transition-colors" style="color: var(--color-cyan-400); border-color: var(--color-cyan-500);">
                  重试
                </button>
              </div>
              
              <!-- 倒计时 -->
              <div v-if="isCountingDown" class="absolute inset-0 flex items-center justify-center bg-black/40 z-30">
                <span class="text-9xl font-black text-white text-shadow-glow animate-ping-slow countdown-shadow">
                  {{ countdown }}
                </span>
              </div>

              <!-- 闪光 -->
              <div v-if="showFlash" class="absolute inset-0 bg-white z-40 animate-flash pointer-events-none"></div>
            </div>

            <!-- 拍照按钮 -->
            <div class="mt-6 md:mt-8 flex flex-col items-center gap-3">
              <button @click="takePhoto" :disabled="!cameraReady || isCountingDown" class="relative group">
                <div class="absolute -inset-1 rounded-full blur opacity-50 group-hover:opacity-100 transition duration-200 group-disabled:opacity-0 bg-gradient-to-r from-[var(--color-cyan-400)] to-[var(--color-cyan-600)]"></div>
                <div class="relative px-6 py-2.5 md:px-8 md:py-3 bg-black rounded-full border flex items-center gap-2 md:gap-3 group-disabled:border-gray-600 group-disabled:text-gray-500" style="border-color: var(--color-cyan-500);">
                  <CameraIcon class="w-5 h-5 md:w-6 md:h-6 group-disabled:text-gray-500" style="color: var(--color-cyan-400);" />
                  <span class="text-sm md:text-lg font-bold tracking-wider md:tracking-widest group-disabled:text-gray-500" style="color: var(--color-cyan-300);">生成穿越海报</span>
                </div>
              </button>
              <p class="text-xs md:text-sm font-mono opacity-60" style="color: var(--color-cyan-500);">请注视镜头并保持微笑</p>
            </div>
          </div>

          <!-- ========== 状态二：AI 处理中 ========= -->
          <div v-else-if="isProcessing && !resultImage" key="processing" class="flex-1 flex flex-col items-center justify-center p-6">
            <!-- 处理中的抓拍图（模糊背景） -->
            <div class="relative w-full max-w-[300px] md:max-w-[420px] aspect-[3/4] rounded-lg overflow-hidden border-2" style="border-color: rgba(var(--color-cyan-500), 0.3);">
              <img v-if="capturedPreview" :src="capturedPreview" class="w-full h-full object-cover scale-105 blur-sm" alt="抓拍预览" />
              <div class="absolute inset-0 bg-black/50 flex flex-col items-center justify-center">
                <div class="w-16 h-16 md:w-20 md:h-20 rounded-full border-4 border-t-transparent animate-spin mb-6" style="border-color: var(--color-cyan-400); border-top-color: transparent;"></div>
                <p class="text-lg md:text-xl font-bold font-mono tracking-widest mb-3" style="color: var(--color-cyan-300);">AI 风格迁移中</p>
                <div class="w-48 md:w-64 h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div class="h-full animate-progress bg-gradient-to-r from-[var(--color-cyan-500)] to-[var(--color-cyan-300)]"></div>
                </div>
                <p class="text-xs md:text-sm mt-3 animate-pulse opacity-70" style="color: var(--color-cyan-500);">正在进行融合渲染，请稍候...</p>
              </div>
            </div>
          </div>

          <!-- ========== 状态三：结果展示 ========= -->
          <div v-else-if="resultImage" key="result" class="flex-1 flex flex-col items-center justify-center p-4 md:p-6">
            <!-- 生成的图片 -->
            <div class="relative w-full max-w-[300px] md:max-w-[420px] aspect-[3/4] rounded-lg overflow-hidden border-2" style="border-color: rgba(var(--color-cyan-500), 0.5); box-shadow: 0 0 40px rgba(var(--color-cyan-500), 0.15);">
              <img :src="resultImage" class="w-full h-full object-cover" alt="合成结果" />
              <!-- 成功标识 -->
              <div class="absolute top-3 left-3 px-3 py-1 rounded-full bg-emerald-500/80 backdrop-blur-sm text-xs font-bold text-white flex items-center gap-1.5">
                <CheckCircleIcon class="w-3.5 h-3.5" /> 生成完成
              </div>
            </div>

            <!-- 操作区 -->
            <div class="mt-5 md:mt-6 flex flex-col items-center gap-4 w-full max-w-[420px]">
              <!-- 扫码区 -->
              <div class="w-full border rounded-lg p-3 md:p-4 flex items-center gap-3 md:gap-4 bg-black/30" style="border-color: rgba(var(--color-cyan-500), 0.3);">
                <div class="w-[56px] h-[56px] md:w-[70px] md:h-[70px] bg-white rounded p-1 flex-shrink-0">
                  <QrCodeIcon class="w-full h-full text-black" />
                </div>
                <div class="flex-1">
                  <h4 class="font-bold mb-0.5 text-sm md:text-base" style="color: var(--color-cyan-300);">扫描获取高清大图</h4>
                  <p class="text-[10px] md:text-xs leading-relaxed opacity-80" style="color: var(--color-cyan-500);">请使用微信或浏览器扫描二维码，将照片保存至手机。</p>
                </div>
              </div>

              <!-- 重新拍摄按钮 -->
              <button @click="retakePhoto" class="flex items-center gap-2 px-5 py-2.5 md:px-6 md:py-3 rounded-full border transition-all hover:bg-[var(--color-cyan-500)]/10" style="border-color: var(--color-cyan-500); color: var(--color-cyan-300);">
                <RotateCcwIcon class="w-4 h-4 md:w-5 md:h-5" />
                <span class="text-sm md:text-base font-bold tracking-wider">重新拍摄</span>
              </button>
            </div>
          </div>
        </transition>

      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onUnmounted, watch } from 'vue'
import { 
  XCircle as XCircleIcon, 
  Camera as CameraIcon,
  Loader2 as Loader2Icon,
  AlertTriangle as AlertTriangleIcon,
  QrCode as QrCodeIcon,
  CheckCircle as CheckCircleIcon,
  RotateCcw as RotateCcwIcon
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
const capturedPreview = ref(null) // 抓拍后的预览图（处理中显示）

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
    setTimeout(() => { initCamera() }, 300)
    resultImage.value = null
    capturedPreview.value = null
    isProcessing.value = false
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
  capturedPreview.value = null
  
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      isCountingDown.value = false
      executeCapture()
    }
  }, 1000)
}

// 重新拍摄
const retakePhoto = () => {
  resultImage.value = null
  capturedPreview.value = null
  isProcessing.value = false
  // 摄像头保持开启，直接回到拍照状态
}

// 执行抓拍和模拟 AI 处理
const executeCapture = () => {
  // 1. 闪光灯特效
  showFlash.value = true
  setTimeout(() => { showFlash.value = false }, 150)

  // 2. 截取画面到 Canvas
  const canvas = document.createElement('canvas')
  const targetRatio = 3 / 4;
  const vW = videoElement.value.videoWidth
  const vH = videoElement.value.videoHeight
  const videoRatio = vW / vH;

  let sourceX = 0, sourceY = 0, sourceWidth = vW, sourceHeight = vH;

  if (videoRatio > targetRatio) {
    sourceWidth = vH * targetRatio;
    sourceX = (vW - sourceWidth) / 2;
  } else {
    sourceHeight = vW / targetRatio;
    sourceY = (vH - sourceHeight) / 2;
  }

  canvas.width = 900
  canvas.height = 1200
  const ctx = canvas.getContext('2d')
  ctx.translate(canvas.width, 0)
  ctx.scale(-1, 1)
  ctx.drawImage(videoElement.value, sourceX, sourceY, sourceWidth, sourceHeight, 0, 0, canvas.width, canvas.height)
  
  const base64Image = canvas.toDataURL('image/jpeg', 0.8)
  
  // 3. 保存抓拍预览并进入处理状态
  capturedPreview.value = base64Image
  isProcessing.value = true
  
  // TODO: 后续将 base64Image 发送给后端 AI 生图接口
  
  // 模拟 AI 生成时间
  setTimeout(() => {
    isProcessing.value = false
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

/* 步骤切换过渡 */
.fade-step-enter-active { transition: opacity 0.5s ease, transform 0.5s ease; }
.fade-step-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-step-enter-from { opacity: 0; transform: translateY(20px); }
.fade-step-leave-to { opacity: 0; transform: translateY(-20px); }
</style>