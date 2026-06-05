<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-500 ease-out"
      enter-from-class="opacity-0 translate-y-8 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-8 scale-95"
    >
      <div v-if="visible" class="fixed inset-0 z-[100] flex pointer-events-none">
        <!-- 弹窗主体，改为绝对定位并支持拖拽与缩放 -->
        <div 
          ref="modalRef"
          class="absolute pointer-events-auto bg-[#061226]/90 backdrop-blur-2xl border border-cyan-500/50 rounded-xl shadow-[0_0_30px_rgba(0,240,255,0.3)] flex flex-col touch-none"
          :style="{
            left: `${position.x}px`,
            top: `${position.y}px`,
            width: `${size.width}px`,
            height: `${size.height}px`
          }"
        >
          
          <!-- 顶部标题栏 (作为拖拽把手) -->
          <div 
            class="h-10 bg-cyan-900/40 border-b border-cyan-500/30 flex items-center justify-between px-4 z-20 relative rounded-t-xl cursor-move select-none"
            @mousedown="startDrag"
            @touchstart="startDrag"
          >
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_5px_#00f0ff]"></div>
              <span class="text-sm text-cyan-300 font-bold tracking-wider text-shadow-glow">
                {{ destCoord ? '智能导航雷达' : '当前位置雷达' }}
              </span>
            </div>
            <button @click="closeMap" class="text-cyan-400 hover:text-white transition-colors hover:scale-110">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>

          <!-- 使用 Vue-AMap 渲染地图 -->
          <div class="flex-1 w-full relative overflow-hidden rounded-b-xl">
            <!-- 极夜蓝样式地图底图 -->
            <el-amap 
              :center="center" 
              :zoom="zoom" 
              map-style="amap://styles/darkblue" 
              class="w-full h-full z-0"
              @init="initMap"
            >
              <!-- 可以在这里添加各种覆盖物、标记等 -->
            </el-amap>
            
            <!-- 地图内部边缘的暗角遮罩，增加科幻屏幕的纵深感 -->
            <div class="absolute inset-0 pointer-events-none shadow-[inset_0_0_40px_rgba(0,0,0,0.8)] z-10"></div>
            <!-- 地图上方的一层极淡的发光遮罩 -->
            <div class="absolute inset-0 pointer-events-none bg-cyan-400/5 mix-blend-screen z-10"></div>
          </div>

          <!-- 装饰边角 (4个角，更具雷达感) -->
          <div class="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-cyan-400 pointer-events-none z-30 rounded-tl-xl"></div>
          <div class="absolute top-0 right-0 w-6 h-6 border-t-2 border-r-2 border-cyan-400 pointer-events-none z-30 rounded-tr-xl"></div>
          <div class="absolute bottom-0 left-0 w-6 h-6 border-b-2 border-l-2 border-cyan-400 pointer-events-none z-30 rounded-bl-xl"></div>
          
          <!-- 右下角增加一个拖拽缩放的把手，同时兼具装饰角功能 -->
          <div 
            class="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-cyan-400 z-30 rounded-br-xl cursor-nwse-resize"
            @mousedown.stop="startResize"
            @touchstart.stop="startResize"
          >
            <!-- 添加三条防滑纹理提示这是可拖拽区域 -->
            <div class="absolute bottom-1 right-1 w-3 h-3 flex flex-col items-end justify-end gap-[2px] opacity-70 pointer-events-none">
              <div class="w-1 h-[1px] bg-cyan-400"></div>
              <div class="w-2 h-[1px] bg-cyan-400"></div>
              <div class="w-3 h-[1px] bg-cyan-400"></div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  originCoord: {
    type: String,
    default: ''
  },
  destCoord: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:visible'])

// ================== 弹窗拖拽与缩放逻辑 ==================
const modalRef = ref(null)

// 初始位置和尺寸（相对于屏幕）
const isMobile = window.innerWidth < 640
const position = ref({
  x: isMobile ? 16 : window.innerWidth / 2 + 50,
  y: isMobile ? 80 : 150
})
const size = ref({
  width: isMobile ? window.innerWidth - 32 : 450,
  height: isMobile ? window.innerHeight * 0.5 : 350
})

// 拖拽状态
let isDragging = false
let startDragPos = { x: 0, y: 0 }
let startModalPos = { x: 0, y: 0 }

// 缩放状态
let isResizing = false
let startResizePos = { x: 0, y: 0 }
let startModalSize = { w: 0, h: 0 }

// 开始拖拽
const startDrag = (e) => {
  if (e.target.closest('button')) return
  isDragging = true
  const point = e.touches ? e.touches[0] : e
  startDragPos = { x: point.clientX, y: point.clientY }
  startModalPos = { x: position.value.x, y: position.value.y }
  document.body.style.userSelect = 'none'
}

// 开始缩放
const startResize = (e) => {
  isResizing = true
  const point = e.touches ? e.touches[0] : e
  startResizePos = { x: point.clientX, y: point.clientY }
  startModalSize = { w: size.value.width, h: size.value.height }
  document.body.style.userSelect = 'none'
}

// 移动
const onMove = (e) => {
  const point = e.touches ? e.touches[0] : e
  if (isDragging) {
    const dx = point.clientX - startDragPos.x
    const dy = point.clientY - startDragPos.y
    position.value.x = Math.max(0, Math.min(window.innerWidth - 100, startModalPos.x + dx))
    position.value.y = Math.max(0, Math.min(window.innerHeight - 60, startModalPos.y + dy))
  }
  if (isResizing) {
    const dx = point.clientX - startResizePos.x
    const dy = point.clientY - startResizePos.y
    size.value.width = Math.max(280, startModalSize.w + dx)
    size.value.height = Math.max(200, startModalSize.h + dy)
  }
}

// 松开
const onEnd = () => {
  isDragging = false
  isResizing = false
  document.body.style.userSelect = ''
}

// 监听全局鼠标事件
onMounted(() => {
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', onEnd)
  window.addEventListener('touchmove', onMove, { passive: false })
  window.addEventListener('touchend', onEnd)

  window.addEventListener('resize', () => {
    if (!props.visible) {
      const mobile = window.innerWidth < 640
      position.value = { x: mobile ? 16 : window.innerWidth / 2 + 50, y: mobile ? 80 : 150 }
      size.value = { width: mobile ? window.innerWidth - 32 : 450, height: mobile ? window.innerHeight * 0.5 : 350 }
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMove)
  window.removeEventListener('mouseup', onEnd)
  window.removeEventListener('touchmove', onMove)
  window.removeEventListener('touchend', onEnd)
})
// ================== 地图核心逻辑 ==================

// 默认中心点：浙大科技园湖州基地
const center = ref([120.088993, 30.865912])
const zoom = ref(12)
let mapInstance = null
let walkingRoute = null
let locationMarker = null

// 地图初始化完成时的回调
const initMap = (map) => {
  mapInstance = map
  drawRoute()
}

// 绘制路径或单点的函数
const drawRoute = () => {
  if (!mapInstance || !props.originCoord) return

  const [lng1, lat1] = props.originCoord.split(',').map(Number)
  
  // 更新中心点
  center.value = [lng1, lat1]

  // 清除旧路线和标记
  if (walkingRoute) {
    walkingRoute.clear()
  }
  if (locationMarker) {
    mapInstance.remove(locationMarker)
    locationMarker = null
  }

  if (props.destCoord) {
    // 【模式一】导航模式：有起点和终点
    const [lng2, lat2] = props.destCoord.split(',').map(Number)
    
    AMap.plugin('AMap.Walking', function() {
      walkingRoute = new AMap.Walking({
        map: mapInstance,
        panel: '', 
        outlineColor: '#00f0ff',
        isOutline: true,
        autoFitView: true
      })

      walkingRoute.search([lng1, lat1], [lng2, lat2], function(status, result) {
        if (status === 'complete') {
          console.log('绘制路线成功')
        } else {
          console.error('绘制路线失败：', result)
        }
      })
    })
  } else {
    // 使用自定义的 HTML 内容来渲染一个极具科幻感的雷达波纹标记
    const markerContent = `
      <div class="relative flex items-center justify-center w-12 h-12">
        <div class="absolute w-full h-full rounded-full bg-cyan-400/20 animate-ping"></div>
        <div class="absolute w-8 h-8 rounded-full border border-cyan-400/50 animate-pulse"></div>
        <div class="absolute w-4 h-4 rounded-full bg-cyan-400 shadow-[0_0_15px_#00f0ff]"></div>
      </div>
    `
    locationMarker = new AMap.Marker({
      position: [lng1, lat1],
      content: markerContent,
      offset: new AMap.Pixel(-24, -24), // 偏移量，使其中心点对准坐标
      title: '当前位置',
      animation: 'AMAP_ANIMATION_DROP' // 增加一个炫酷的掉落动画
    })
    mapInstance.add(locationMarker)
    
    // 定位到中心并放大地图层级（拉近视角）
    mapInstance.setZoomAndCenter(12, [lng1, lat1])
  }
}

// 监听坐标或显示状态变化，重新绘制
watch(() => [props.visible, props.originCoord, props.destCoord], ([isVisible, origin, dest]) => {
  if (isVisible && origin) {
    nextTick(() => {
      drawRoute()
    })
  } else if (!isVisible) {
    if (walkingRoute) walkingRoute.clear()
    if (locationMarker && mapInstance) {
      mapInstance.remove(locationMarker)
      locationMarker = null
    }
  }
})

const closeMap = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
:deep(.amap-copyright) {
  display: none !important;
}
:deep(.amap-logo) {
  opacity: 0.8 !important;
}

/* 路线规划控制面板隐藏 */
:deep(.amap-call) {
  display: none !important;
}

/* 核心优化：给默认的起点和终点 Marker 增加科幻感
   红色（终点）通过 hue-rotate(180deg) 会变成 青色
   绿色（起点）通过 hue-rotate(180deg) 会变成 紫色
   这完美契合了赛博朋克/全息投影的主题色彩！ */
:deep(.amap-marker .amap-icon img) {
  filter: hue-rotate(180deg) brightness(1.2) drop-shadow(0 0 5px rgba(0,240,255,0.5));
}
</style>
