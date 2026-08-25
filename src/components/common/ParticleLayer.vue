<template>
  <canvas ref="canvasRef" class="particle-layer"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  // 粒子最大数量（实际会根据屏幕宽度自适应）
  maxCount: { type: Number, default: 140 },
  // 粒子最小数量下限
  minCount: { type: Number, default: 60 },
  // 连线最大距离
  linkDistance: { type: Number, default: 110 },
  // 连线颜色（rgba 字符串中的 RGB）
  linkColor: { type: String, default: '45, 212, 191' }
})

const canvasRef = ref(null)
let ctx = null
let particles = []
let animId = null

const palette = [
  '45, 212, 191',     // 青绿
  '94, 234, 212',     // 浅青
  '251, 191, 36',     // 暖黄
  '253, 224, 71',     // 浅黄
  '255, 255, 255',    // 纯白
  '226, 232, 240'     // 冷白
]

const computeCount = () => {
  const width = window.innerWidth
  const byWidth = Math.floor(width / 11)
  return Math.min(props.maxCount, Math.max(props.minCount, byWidth))
}

const init = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const dpr = window.devicePixelRatio || 1
  canvas.width = window.innerWidth * dpr
  canvas.height = window.innerHeight * dpr
  canvas.style.width = window.innerWidth + 'px'
  canvas.style.height = window.innerHeight + 'px'
  ctx = canvas.getContext('2d')
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  const count = computeCount()
  particles = []
  for (let i = 0; i < count; i++) {
    // 50% 概率用青绿系（呼应科技主题），其余从全部调色板随机
    const colorIdx = Math.random() < 0.5
      ? (Math.random() < 0.5 ? 0 : 1)
      : Math.floor(Math.random() * palette.length)
    particles.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3 - 0.08,
      r: Math.random() * 2.2 + 0.8,
      color: palette[colorIdx],
      alpha: Math.random() * 0.5 + 0.4,
      phase: Math.random() * Math.PI * 2,
      pulseSpeed: Math.random() * 0.015 + 0.005
    })
  }
}

const draw = () => {
  if (!ctx) return
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)

  // 粒子
  for (const p of particles) {
    p.x += p.vx
    p.y += p.vy
    p.phase += p.pulseSpeed
    const twinkle = Math.sin(p.phase) * 0.4 + 0.6

    // 屏幕回环
    if (p.x < -10) p.x = window.innerWidth + 10
    if (p.x > window.innerWidth + 10) p.x = -10
    if (p.y < -10) p.y = window.innerHeight + 10
    if (p.y > window.innerHeight + 10) p.y = -10

    const alpha = p.alpha * twinkle
    const glow = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4)
    glow.addColorStop(0, `rgba(${p.color}, ${alpha})`)
    glow.addColorStop(1, `rgba(${p.color}, 0)`)
    ctx.fillStyle = glow
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2)
    ctx.fill()
  }

  // 连线（科技感）
  ctx.lineWidth = 0.5
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x
      const dy = particles[i].y - particles[j].y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < props.linkDistance) {
        const lineAlpha = (1 - dist / props.linkDistance) * 0.18
        ctx.strokeStyle = `rgba(${props.linkColor}, ${lineAlpha})`
        ctx.beginPath()
        ctx.moveTo(particles[i].x, particles[i].y)
        ctx.lineTo(particles[j].x, particles[j].y)
        ctx.stroke()
      }
    }
  }

  animId = requestAnimationFrame(draw)
}

const handleResize = () => {
  init()
}

onMounted(() => {
  init()
  draw()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.particle-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
</style>
