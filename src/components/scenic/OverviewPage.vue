<template>
  <div class="page-frame">
    <PageHeader title="景区全景概况" subtitle="SCENIC OVERVIEW" />

    <div class="page-body">
      <!-- 景区名片卡 -->
      <div class="hero-card">
        <div class="hero-glow"></div>
        <div class="hero-content">
          <div class="hero-meta">
            <span class="meta-tag">SCENIC</span>
            <span class="meta-divider"></span>
            <span class="meta-en">{{ store.scenicInfo.scenic_en_name || '—' }}</span>
          </div>
          <h3 class="hero-title">{{ store.scenicInfo.scenic_name || '未命名景区' }}</h3>
          <div class="hero-row">
            <div v-if="store.scenicInfo.address" class="hero-address">
              <MapPin class="addr-icon" />
              <span>{{ store.scenicInfo.address }}</span>
            </div>
          </div>
        </div>
        <div class="hero-corner tl"></div>
        <div class="hero-corner br"></div>
      </div>

      <!-- 简介 -->
      <div class="intro-card">
        <div class="card-header">
          <div class="header-dot"></div>
          <h3 class="card-title">景区简介</h3>
          <span class="card-sub">INTRODUCTION</span>
        </div>
        <div
          ref="introScrollContainer"
          class="intro-scroll"
          @mouseenter="pauseIntroScroll"
          @mouseleave="resumeIntroScroll"
          @touchstart="pauseIntroScroll"
          @touchend="resumeIntroScroll"
        >
          <div ref="introScrollContent" class="intro-text">{{ store.scenicInfo.introduction || '暂无简介' }}</div>
        </div>
        <div class="intro-fade"></div>
      </div>

      <!-- 票务 / 时间 -->
      <div class="stats-row">
        <div class="stat-card ticket">
          <div class="stat-bg-icon"><Ticket class="bg-icon" /></div>
          <span class="stat-caption">成人票价</span>
          <div class="stat-value-row">
            <span class="stat-price">¥{{ store.scenicInfo.ticket_price }}</span>
            <span class="stat-unit">/人</span>
          </div>
          <span class="stat-en">TICKET PRICE</span>
        </div>

        <div class="stat-card hours">
          <div class="stat-bg-icon"><ClockIcon class="bg-icon" /></div>
          <span class="stat-caption">营业时间</span>
          <div class="stat-value-row">
            <span class="stat-hours">{{ store.scenicInfo.opening_hours }}</span>
          </div>
          <span class="stat-en">OPENING HOURS</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Ticket, Clock as ClockIcon, MapPin } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import PageHeader from '@/components/scenic/PageHeader.vue'

const store = useScenicStore()

const introScrollContainer = ref(null)
const introScrollContent = ref(null)
let introScrollAnimationId = null
let isIntroScrolling = true
let currentScrollTop = 0

const startIntroAutoScroll = () => {
  const scroll = () => {
    if (isIntroScrolling && introScrollContainer.value && introScrollContent.value) {
      currentScrollTop += 0.2
      introScrollContainer.value.scrollTop = currentScrollTop
      const maxScrollTop = introScrollContainer.value.scrollHeight - introScrollContainer.value.clientHeight
      if (introScrollContainer.value.scrollTop >= maxScrollTop - 1) {
        currentScrollTop = 0
        introScrollContainer.value.scrollTop = 0
      }
    }
    introScrollAnimationId = requestAnimationFrame(scroll)
  }
  introScrollAnimationId = requestAnimationFrame(scroll)
}

const pauseIntroScroll = () => { isIntroScrolling = false }
const resumeIntroScroll = () => {
  isIntroScrolling = true
  if (introScrollContainer.value) currentScrollTop = introScrollContainer.value.scrollTop
}

onMounted(() => startIntroAutoScroll())
onUnmounted(() => {
  if (introScrollAnimationId) cancelAnimationFrame(introScrollAnimationId)
})
</script>

<style scoped>
.page-frame {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  gap: 16px;
}

.page-body {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow-y: auto;
  padding-right: 6px;
}

.page-body::-webkit-scrollbar { width: 4px; }
.page-body::-webkit-scrollbar-track { background: rgba(45, 212, 191, 0.05); border-radius: 2px; }
.page-body::-webkit-scrollbar-thumb { background: rgba(45, 212, 191, 0.25); border-radius: 2px; }
.page-body::-webkit-scrollbar-thumb:hover { background: rgba(45, 212, 191, 0.5); }

/* 景区名片 */
.hero-card {
  position: relative;
  padding: 24px 22px;
  border: 1px solid rgba(45, 212, 191, 0.28);
  border-radius: 16px;
  background: rgba(2, 18, 24, 0.55);
  backdrop-filter: blur(8px);
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: inset 0 0 24px rgba(45, 212, 191, 0.04);
}

.hero-glow {
  position: absolute;
  top: -60%;
  left: -10%;
  width: 80%;
  height: 200%;
  background: radial-gradient(ellipse at center, rgba(45, 212, 191, 0.16) 0%, transparent 60%);
  pointer-events: none;
  animation: hero-drift 8s ease-in-out infinite;
}

@keyframes hero-drift {
  0%, 100% { opacity: 0.5; transform: translateX(0); }
  50% { opacity: 1; transform: translateX(20%); }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.meta-tag {
  font-size: 10px;
  font-weight: 800;
  color: #2dd4bf;
  letter-spacing: 3px;
  padding: 3px 8px;
  border: 1px solid rgba(45, 212, 191, 0.4);
  border-radius: 4px;
  background: rgba(45, 212, 191, 0.1);
}

.meta-divider {
  width: 16px;
  height: 1px;
  background: rgba(45, 212, 191, 0.3);
}

.meta-en {
  font-size: 11px;
  color: rgba(45, 212, 191, 0.7);
  letter-spacing: 2px;
  font-family: ui-monospace, SFMono-Regular, monospace;
}

.hero-title {
  font-size: 30px;
  font-weight: 900;
  color: #f0fdfa;
  letter-spacing: 3px;
  text-shadow: 0 0 18px rgba(45, 212, 191, 0.45);
  margin-bottom: 14px;
}

.hero-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.hero-address {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(226, 232, 240, 0.7);
  min-width: 0;
  flex: 1;
}

.hero-address span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.addr-icon {
  width: 14px;
  height: 14px;
  color: #2dd4bf;
  flex-shrink: 0;
}

.hero-corner {
  position: absolute;
  width: 38px;
  height: 38px;
  pointer-events: none;
}

.hero-corner.tl {
  top: 0;
  left: 0;
  border-top: 2px solid rgba(45, 212, 191, 0.6);
  border-left: 2px solid rgba(45, 212, 191, 0.6);
  border-top-left-radius: 16px;
}

.hero-corner.br {
  bottom: 0;
  right: 0;
  border-bottom: 2px solid rgba(45, 212, 191, 0.6);
  border-right: 2px solid rgba(45, 212, 191, 0.6);
  border-bottom-right-radius: 16px;
}

/* 简介 */
.intro-card {
  position: relative;
  flex: 1;
  min-height: 120px;
  border: 1px solid rgba(45, 212, 191, 0.18);
  border-radius: 16px;
  background: rgba(2, 18, 24, 0.55);
  backdrop-filter: blur(6px);
  padding: 18px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.header-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #2dd4bf;
  box-shadow: 0 0 10px #2dd4bf;
}

.card-title {
  font-size: 16px;
  font-weight: 800;
  color: #f0fdfa;
  letter-spacing: 1.5px;
}

.card-sub {
  font-size: 10px;
  color: rgba(45, 212, 191, 0.5);
  letter-spacing: 1.5px;
  margin-left: auto;
  font-family: ui-monospace, SFMono-Regular, monospace;
}

.intro-scroll {
  flex: 1;
  overflow-y: auto;
  padding-right: 6px;
}

.intro-scroll::-webkit-scrollbar { width: 3px; }
.intro-scroll::-webkit-scrollbar-thumb { background: rgba(45, 212, 191, 0.25); border-radius: 2px; }

.intro-text {
  font-size: 14px;
  line-height: 1.9;
  color: rgba(226, 232, 240, 0.78);
  text-align: justify;
  white-space: pre-wrap;
}

.intro-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 36px;
  background: linear-gradient(180deg, transparent 0%, rgba(2, 18, 24, 0.85) 70%);
  pointer-events: none;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
}

/* 统计卡 */
.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  height: 120px;
  flex-shrink: 0;
}

.stat-card {
  position: relative;
  border-radius: 16px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(45, 212, 191, 0.18);
  background: rgba(2, 18, 24, 0.55);
}

.stat-card:hover {
  border-color: rgba(45, 212, 191, 0.45);
  transform: translateY(-2px);
  box-shadow: 0 0 24px rgba(45, 212, 191, 0.1);
}

.stat-card.ticket:hover { border-color: rgba(251, 191, 36, 0.45); box-shadow: 0 0 24px rgba(251, 191, 36, 0.1); }

.stat-bg-icon {
  position: absolute;
  right: -8px;
  bottom: -10px;
  color: rgba(45, 212, 191, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover .stat-bg-icon {
  color: rgba(45, 212, 191, 0.14);
  transform: scale(1.1) rotate(-5deg);
}

.stat-card.ticket .stat-bg-icon { color: rgba(251, 191, 36, 0.08); }
.stat-card.ticket:hover .stat-bg-icon { color: rgba(251, 191, 36, 0.14); }

.bg-icon {
  width: 64px;
  height: 64px;
}

.stat-caption {
  font-size: 12px;
  color: rgba(226, 232, 240, 0.55);
  letter-spacing: 1px;
  z-index: 1;
}

.stat-card.ticket .stat-caption { color: rgba(251, 191, 36, 0.65); }

.stat-value-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
  z-index: 1;
}

.stat-price {
  font-size: 28px;
  font-weight: 900;
  color: #fbbf24;
  text-shadow: 0 0 12px rgba(251, 191, 36, 0.3);
}

.stat-unit {
  font-size: 12px;
  color: rgba(226, 232, 240, 0.5);
}

.stat-hours {
  font-size: 20px;
  font-weight: 800;
  color: #f0fdfa;
  text-shadow: 0 0 10px rgba(45, 212, 191, 0.25);
}

.stat-en {
  font-size: 10px;
  color: rgba(45, 212, 191, 0.45);
  letter-spacing: 1.5px;
  margin-top: 2px;
  font-family: ui-monospace, SFMono-Regular, monospace;
  z-index: 1;
}

.stat-card.ticket .stat-en { color: rgba(251, 191, 36, 0.45); }
</style>
