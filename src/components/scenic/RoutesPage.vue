<template>
  <div class="page-frame">
    <PageHeader title="推荐游览路线" subtitle="RECOMMENDED ROUTES" />

    <div class="page-body">
      <div v-if="routes.length" class="routes-list">
        <div v-for="(route, ri) in routes" :key="ri" class="route-card">
          <div class="route-header">
            <div class="route-badge" :class="`tone-${ri % 3}`">
              <RouteIcon class="badge-icon" />
              <span>{{ route.label }}</span>
            </div>
            <div class="route-meta">
              <Clock class="meta-icon" />
              <span>{{ route.duration }}</span>
            </div>
          </div>

          <div class="route-timeline">
            <div
              v-for="(spot, si) in route.spots"
              :key="si"
              class="timeline-node"
            >
              <div class="node-dot" :class="`tone-${ri % 3}`"></div>
              <span class="node-name">{{ spot }}</span>
              <div v-if="si < route.spots.length - 1" class="node-arrow">
                <ChevronRight class="arrow-icon" />
              </div>
            </div>
          </div>

          <div class="route-wave">
            <div v-for="i in 30" :key="`wave-${ri}-${i}`" class="wave-bar" :style="`height: ${20 + Math.random() * 80}%; animation-delay: ${i * 0.05}s;`"></div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <Compass class="empty-icon" />
        <span>暂无推荐路线</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Route as RouteIcon, Clock, ChevronRight, Compass } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import PageHeader from '@/components/scenic/PageHeader.vue'

const store = useScenicStore()

const routes = computed(() => {
  const r = store.scenicInfo?.recommended_routes
  return Array.isArray(r) ? r : []
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
  overflow-y: auto;
  padding-right: 6px;
}

.page-body::-webkit-scrollbar { width: 4px; }
.page-body::-webkit-scrollbar-track { background: rgba(45, 212, 191, 0.05); border-radius: 2px; }
.page-body::-webkit-scrollbar-thumb { background: rgba(45, 212, 191, 0.25); border-radius: 2px; }
.page-body::-webkit-scrollbar-thumb:hover { background: rgba(45, 212, 191, 0.5); }

.routes-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.route-card {
  position: relative;
  padding: 20px;
  border: 1px solid rgba(45, 212, 191, 0.18);
  border-radius: 16px;
  background: rgba(2, 18, 24, 0.55);
  backdrop-filter: blur(6px);
  overflow: hidden;
  transition: all 0.3s ease;
}

.route-card:hover {
  border-color: rgba(45, 212, 191, 0.45);
  background: rgba(2, 28, 32, 0.68);
  box-shadow: 0 0 28px rgba(45, 212, 191, 0.1);
  transform: translateY(-2px);
}

.route-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 40px;
  height: 40px;
  border-top: 2px solid rgba(45, 212, 191, 0.4);
  border-left: 2px solid rgba(45, 212, 191, 0.4);
  border-top-left-radius: 16px;
  pointer-events: none;
}

.route-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.route-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.route-badge.tone-0 {
  border: 1px solid rgba(45, 212, 191, 0.45);
  background: rgba(45, 212, 191, 0.12);
  color: #5eead4;
}

.route-badge.tone-1 {
  border: 1px solid rgba(56, 189, 248, 0.45);
  background: rgba(56, 189, 248, 0.12);
  color: #7dd3fc;
}

.route-badge.tone-2 {
  border: 1px solid rgba(129, 140, 248, 0.45);
  background: rgba(129, 140, 248, 0.12);
  color: #a5b4fc;
}

.badge-icon {
  width: 15px;
  height: 15px;
}

.route-meta {
  display: flex;
  align-items: center;
  gap: 5px;
  color: rgba(226, 232, 240, 0.55);
  font-size: 12px;
}

.meta-icon {
  width: 13px;
  height: 13px;
}

.route-timeline {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 4px;
  margin-bottom: 16px;
}

.timeline-node {
  display: flex;
  align-items: center;
  gap: 8px;
}

.node-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  box-shadow: 0 0 8px currentColor;
}

.node-dot.tone-0 { background: #2dd4bf; color: #2dd4bf; }
.node-dot.tone-1 { background: #38bdf8; color: #38bdf8; }
.node-dot.tone-2 { background: #818cf8; color: #818cf8; }

.node-name {
  font-size: 14px;
  color: #e2e8f0;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.node-arrow {
  color: rgba(45, 212, 191, 0.35);
  margin: 0 2px;
}

.arrow-icon {
  width: 14px;
  height: 14px;
}

.route-wave {
  display: flex;
  align-items: end;
  gap: 3px;
  height: 28px;
  opacity: 0.45;
}

.wave-bar {
  flex: 1;
  background: linear-gradient(180deg, rgba(45, 212, 191, 0.6) 0%, rgba(45, 212, 191, 0.1) 100%);
  border-radius: 2px 2px 0 0;
  animation: wave 1.2s infinite alternate ease-in-out;
}

@keyframes wave {
  from { transform: scaleY(0.5); }
  to { transform: scaleY(1); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
  color: rgba(226, 232, 240, 0.45);
  font-size: 14px;
}

.empty-icon {
  width: 48px;
  height: 48px;
  opacity: 0.5;
}
</style>
