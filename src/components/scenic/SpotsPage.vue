<template>
  <div class="page-frame">
    <PageHeader title="景区景点导览" subtitle="SCENIC SPOTS" />

    <div class="page-body">
      <div ref="spotListRef" class="spot-list" @mouseenter="pauseSpotScroll" @mouseleave="resumeSpotScroll">
        <div ref="spotScrollContent" class="spot-list-inner">
          <div
            v-for="(spot, index) in store.spotList"
            :key="index"
            class="spot-card"
            :class="{ active: activeSpotIndex === index }"
            @click="handleLocateSpot(spot, index)"
          >
            <div class="spot-shine"></div>
            <div class="spot-thumb">
              <img :src="spot.image_url" alt="spot" />
              <div class="spot-thumb-mask"></div>
            </div>
            <div class="spot-info">
              <div class="spot-title-row">
                <span class="spot-name">{{ spot.spot_name }}</span>
                <span class="spot-index">{{ String(index + 1).padStart(2, '0') }}</span>
              </div>
              <span class="spot-en">{{ spot.en_name }}</span>
              <p class="spot-desc">{{ spot.description }}</p>
            </div>
            <div class="spot-locate" :class="{ active: activeSpotIndex === index }" @click.stop="handleLocateSpot(spot, index)">
              <MapPin class="locate-icon" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { MapPin } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import { useAvatarStore } from '@/stores/avatar'
import PageHeader from '@/components/scenic/PageHeader.vue'

const store = useScenicStore()
const avatarStore = useAvatarStore()

const spotListRef = ref(null)
const spotScrollContent = ref(null)
let spotScrollAnimationId = null
let isSpotScrolling = true
let currentSpotScroll = 0

const activeSpotIndex = ref(-1)

const startSpotAutoScroll = () => {
  const scroll = () => {
    if (isSpotScrolling && spotListRef.value && spotScrollContent.value) {
      currentSpotScroll += 0.18
      spotListRef.value.scrollTop = currentSpotScroll
      const maxScroll = spotScrollContent.value.scrollHeight - spotListRef.value.clientHeight
      if (spotListRef.value.scrollTop >= maxScroll - 1) {
        currentSpotScroll = 0
        spotListRef.value.scrollTop = 0
      }
    }
    spotScrollAnimationId = requestAnimationFrame(scroll)
  }
  spotScrollAnimationId = requestAnimationFrame(scroll)
}

const pauseSpotScroll = () => { isSpotScrolling = false }
const resumeSpotScroll = () => {
  isSpotScrolling = true
  if (spotListRef.value) currentSpotScroll = spotListRef.value.scrollTop
}

// 点击景点：高亮 + 数字人讲解（FAY 逻辑）
const handleLocateSpot = (spot, index) => {
  activeSpotIndex.value = index
  if (spot.description && avatarStore.isReady) {
    avatarStore.speak(spot.description)
  }
}

onMounted(() => startSpotAutoScroll())
onUnmounted(() => {
  if (spotScrollAnimationId) cancelAnimationFrame(spotScrollAnimationId)
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
  position: relative;
}

.spot-list {
  position: absolute;
  inset: 0;
  overflow-y: auto;
  padding-right: 6px;
}

.spot-list::-webkit-scrollbar { width: 4px; }
.spot-list::-webkit-scrollbar-track { background: rgba(45, 212, 191, 0.05); border-radius: 2px; }
.spot-list::-webkit-scrollbar-thumb { background: rgba(45, 212, 191, 0.25); border-radius: 2px; }
.spot-list::-webkit-scrollbar-thumb:hover { background: rgba(45, 212, 191, 0.5); }

.spot-list-inner {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.spot-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  border: 1px solid rgba(45, 212, 191, 0.18);
  border-radius: 12px;
  background: rgba(2, 18, 24, 0.55);
  backdrop-filter: blur(6px);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.spot-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(45, 212, 191, 0.06) 0%, transparent 40%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.spot-card:hover,
.spot-card.active {
  border-color: rgba(45, 212, 191, 0.55);
  background: rgba(2, 28, 32, 0.72);
  box-shadow: 0 0 28px rgba(45, 212, 191, 0.12), inset 0 0 16px rgba(45, 212, 191, 0.06);
  transform: translateX(-4px);
}

.spot-card:hover::before,
.spot-card.active::before {
  opacity: 1;
}

.spot-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 60%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(45, 212, 191, 0.08), transparent);
  transition: left 0.6s ease;
}

.spot-card:hover .spot-shine {
  left: 120%;
}

.spot-thumb {
  position: relative;
  width: 76px;
  height: 76px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(45, 212, 191, 0.25);
  flex-shrink: 0;
  z-index: 1;
}

.spot-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.spot-card:hover .spot-thumb img {
  transform: scale(1.08);
}

.spot-thumb-mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(45, 212, 191, 0.1) 0%, transparent 60%);
  mix-blend-mode: overlay;
}

.spot-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 1;
}

.spot-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.spot-name {
  font-size: 16px;
  font-weight: 700;
  color: #f0fdfa;
  letter-spacing: 1px;
  text-shadow: 0 0 8px rgba(45, 212, 191, 0.25);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.spot-index {
  font-size: 12px;
  font-weight: 800;
  color: rgba(45, 212, 191, 0.35);
  font-family: ui-monospace, SFMono-Regular, monospace;
}

.spot-en {
  font-size: 10px;
  color: rgba(45, 212, 191, 0.55);
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.spot-desc {
  font-size: 12px;
  color: rgba(226, 232, 240, 0.6);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.spot-locate {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(45, 212, 191, 0.25);
  border-radius: 8px;
  background: rgba(45, 212, 191, 0.06);
  color: rgba(45, 212, 191, 0.7);
  flex-shrink: 0;
  z-index: 1;
  transition: all 0.25s ease;
}

.spot-locate:hover,
.spot-locate.active {
  border-color: rgba(45, 212, 191, 0.6);
  background: rgba(45, 212, 191, 0.18);
  color: #5eead4;
  box-shadow: 0 0 14px rgba(45, 212, 191, 0.25);
}

.locate-icon {
  width: 16px;
  height: 16px;
}
</style>
