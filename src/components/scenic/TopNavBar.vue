<template>
  <header class="top-nav">
    <!-- 左侧：Logo + 标题 + 菜单 -->
    <div class="nav-left">
      <div class="brand">
        <div class="brand-icon">
          <img v-if="logo" :src="logo" alt="logo" />
          <Mountain v-else />
        </div>
        <div class="brand-text">
          <div class="brand-title">{{ title }}</div>
          <div class="brand-subtitle">{{ subtitle }}</div>
        </div>
      </div>

      <nav class="nav-menu">
        <button
          v-for="item in menuItems"
          :key="item.key"
          class="menu-item"
          :class="{ active: activeKey === item.key }"
          @click="$emit('menuClick', item.key)"
        >
          <component :is="item.icon" class="menu-icon" />
          <span>{{ item.label }}</span>
        </button>
      </nav>
    </div>

    <!-- 右侧：工具 + 天气 + 时间 -->
    <div class="nav-right">
      <div class="tool-group">
        <button class="tool-btn" title="配置" @click="$emit('openConfig')">
          <Settings class="tool-icon" />
        </button>
        <button class="tool-btn" title="管理后台" @click="$emit('goAdmin')">
          <LayoutDashboard class="tool-icon" />
        </button>
      </div>

      <div class="weather" v-if="weather">
        <CloudSun class="weather-icon" />
        <span class="weather-temp">{{ weather.temp }}°C</span>
        <span class="weather-text">{{ weather.text }}</span>
      </div>

      <div class="datetime">
        <div class="time">{{ timeText }}</div>
        <div class="date">{{ dateText }}</div>
      </div>
    </div>

    <!-- 底部装饰线 -->
    <div class="nav-bottom-line">
      <div class="line-glow"></div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  Mountain,
  Settings,
  LayoutDashboard,
  CloudSun
} from 'lucide-vue-next'

defineProps({
  title: { type: String, default: '智慧文旅数字人体验平台' },
  subtitle: { type: String, default: 'SCENIC DIGITAL' },
  logo: { type: String, default: '' },
  menuItems: { type: Array, default: () => [] },
  activeKey: { type: String, default: '' },
  weather: { type: Object, default: null }
})

defineEmits(['menuClick', 'openConfig', 'goAdmin'])

const timeText = ref('--:--:--')
const dateText = ref('----/--/--')
let timer = null

const pad = (n) => String(n).padStart(2, '0')

const updateTime = () => {
  const now = new Date()
  timeText.value = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
  dateText.value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} 星期${['日','一','二','三','四','五','六'][now.getDay()]}`
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.top-nav {
  position: relative;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
  padding: 0 24px;
  background:
    linear-gradient(180deg, rgba(2, 12, 18, 0.92) 0%, rgba(4, 22, 32, 0.78) 70%, rgba(4, 22, 32, 0) 100%);
  border-bottom: 1px solid rgba(45, 212, 191, 0.18);
  backdrop-filter: blur(4px);
}

/* 底部发光装饰线 */
.nav-bottom-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(45, 212, 191, 0.25) 15%,
    rgba(45, 212, 191, 0.8) 50%,
    rgba(45, 212, 191, 0.25) 85%,
    transparent 100%
  );
}

.line-glow {
  position: absolute;
  left: 50%;
  bottom: -2px;
  transform: translateX(-50%);
  width: 280px;
  height: 4px;
  background: radial-gradient(ellipse at center, rgba(45, 212, 191, 0.55) 0%, transparent 70%);
  pointer-events: none;
}

/* 左侧 */
.nav-left {
  display: flex;
  align-items: center;
  gap: 22px;
  flex-shrink: 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.brand-icon {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2dd4bf;
  border: 1px solid rgba(45, 212, 191, 0.35);
  border-radius: 9px;
  background: rgba(45, 212, 191, 0.08);
  box-shadow: 0 0 20px rgba(45, 212, 191, 0.15);
}

.brand-icon img {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.brand-icon svg {
  width: 20px;
  height: 20px;
}

.brand-title {
  font-size: 18px;
  font-weight: 700;
  color: #f0fdfa;
  letter-spacing: 1.5px;
  text-shadow: 0 0 16px rgba(45, 212, 191, 0.4);
  white-space: nowrap;
}

.brand-subtitle {
  font-size: 10px;
  color: rgba(45, 212, 191, 0.7);
  letter-spacing: 2px;
  margin-top: 2px;
}

/* 菜单 */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid transparent;
  background: transparent;
  color: rgba(226, 232, 240, 0.75);
  font-size: 13px;
  cursor: pointer;
  border-radius: 6px;
  position: relative;
  white-space: nowrap;
}

.menu-item:hover {
  color: #f0fdfa;
  background: rgba(45, 212, 191, 0.1);
}

.menu-item.active {
  color: #f0fdfa;
  background: linear-gradient(180deg, rgba(45, 212, 191, 0.18) 0%, rgba(20, 184, 166, 0.06) 100%);
  border: 1px solid rgba(45, 212, 191, 0.45);
  box-shadow:
    inset 0 0 12px rgba(45, 212, 191, 0.12),
    0 0 18px rgba(45, 212, 191, 0.15);
}

.menu-item.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 40%;
  height: 2px;
  background: #2dd4bf;
  border-radius: 2px;
  box-shadow: 0 0 8px #2dd4bf;
}

.menu-icon {
  width: 16px;
  height: 16px;
}

/* 右侧 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.tool-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tool-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(45, 212, 191, 0.25);
  border-radius: 8px;
  background: rgba(45, 212, 191, 0.06);
  color: rgba(226, 232, 240, 0.8);
  cursor: pointer;
  transition: all 0.25s ease;
}

.tool-btn:hover {
  background: rgba(45, 212, 191, 0.14);
  border-color: rgba(45, 212, 191, 0.5);
  color: #f0fdfa;
  box-shadow: 0 0 14px rgba(45, 212, 191, 0.2);
}

.tool-icon {
  width: 17px;
  height: 17px;
}

.weather {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border: 1px solid rgba(45, 212, 191, 0.2);
  border-radius: 8px;
  background: rgba(15, 23, 42, 0.35);
  color: #e2e8f0;
  font-size: 13px;
}

.weather-icon {
  width: 20px;
  height: 20px;
  color: #fbbf24;
}

.weather-temp {
  font-weight: 600;
  color: #2dd4bf;
}

.datetime {
  text-align: right;
  min-width: 120px;
}

.time {
  font-size: 22px;
  font-weight: 700;
  color: #f0fdfa;
  font-variant-numeric: tabular-nums;
  letter-spacing: 1px;
  text-shadow: 0 0 12px rgba(45, 212, 191, 0.35);
}

.date {
  font-size: 11px;
  color: rgba(226, 232, 240, 0.65);
  margin-top: 2px;
  letter-spacing: 0.5px;
}
</style>
