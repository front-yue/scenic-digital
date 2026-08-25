<template>
  <div class="scenic-screen">
    <!-- 景区实景背景 -->
    <div
      class="scenic-bg"
      :style="{ backgroundImage: scenicBgUrl ? `url(${scenicBgUrl})` : '' }"
    ></div>
    <div class="scenic-overlay"></div>

    <!-- 粒子层 -->
    <ParticleLayer class="particle-layer" />

    <!-- 顶部装饰 -->
    <div class="top-decor">
      <div class="scan-line primary"></div>
      <div class="scan-line secondary"></div>
    </div>

    <!-- 顶部导航 -->
    <TopNavBar
      title="智慧文旅 · 数字人"
      subtitle="SCENIC DIGITAL"
      :logo="logoUrl"
      :menu-items="menuItems"
      :active-key="activeMenu"
      :weather="weatherInfo"
      @menu-click="activeMenu = $event"
      @open-config="openConfig"
      @go-admin="goAdmin"
    />

    <!-- 主内容区 -->
    <main class="main-layout">
      <!-- 左侧：数字人 -->
      <section class="avatar-section" :class="{ 'chat-active': activeMenu === 'chat' }">
        <AvatarPanel />
      </section>

      <!-- 右侧：内容面板 -->
      <section class="content-section">
        <Transition name="panel" mode="out-in">
          <component :is="currentPage" :key="activeMenu" />
        </Transition>
      </section>
    </main>

    <!-- 配置弹窗 -->
    <ConfigPanel v-model:visible="showConfig" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useScenicStore } from '@/stores/scenic'
import { useAvatarStore } from '@/stores/avatar'
import { useFaySocket } from '@/composables/useFaySocket'
import { getConfig } from '@/api/config'
import TopNavBar from '@/components/scenic/TopNavBar.vue'
import AvatarPanel from '@/components/scenic/AvatarPanel.vue'
import OverviewPage from '@/components/scenic/OverviewPage.vue'
import SpotsPage from '@/components/scenic/SpotsPage.vue'
import RoutesPage from '@/components/scenic/RoutesPage.vue'
import MapPage from '@/components/scenic/MapPage.vue'
import ChatPage from '@/components/scenic/ChatPage.vue'
import AnnouncementPage from '@/components/scenic/AnnouncementPage.vue'
import ConfigPanel from '@/components/common/ConfigPanel.vue'
import ParticleLayer from '@/components/common/ParticleLayer.vue'
import {
  LayoutDashboard,
  Landmark,
  Route,
  Map,
  MessageSquare,
  Megaphone
} from 'lucide-vue-next'

const router = useRouter()
const scenicStore = useScenicStore()
const avatarStore = useAvatarStore()
useFaySocket()

const activeMenu = ref('overview')
const showConfig = ref(false)

const logoUrl = '/logo.png'

// 天气：映射到 FAY 后端字段
const weatherInfo = computed(() => {
  const info = scenicStore.scenicInfo || {}
  if (info.weather_desc && info.weather_temp) {
    return {
      temp: info.weather_temp,
      text: info.weather_desc
    }
  }
  // 默认天气
  return { temp: 26, text: '多云' }
})

const scenicBgUrl = computed(() => {
  const info = scenicStore.scenicInfo || {}
  // 优先使用景区封面图，其次取第一个景点图
  if (info.cover_image) return info.cover_image
  const firstSpot = scenicStore.spotList?.[0]
  if (firstSpot?.image_url) return firstSpot.image_url
  return ''
})

const menuItems = [
  { key: 'overview', label: '景区概览', icon: LayoutDashboard },
  { key: 'spots', label: '景点导览', icon: Landmark },
  { key: 'routes', label: '游览路线', icon: Route },
  { key: 'map', label: '景区地图', icon: Map },
  { key: 'chat', label: '智能问答', icon: MessageSquare },
  { key: 'announcement', label: '系统公告', icon: Megaphone }
]

const pageMap = {
  overview: OverviewPage,
  spots: SpotsPage,
  routes: RoutesPage,
  map: MapPage,
  chat: ChatPage,
  announcement: AnnouncementPage
}

const currentPage = computed(() => pageMap[activeMenu.value] || OverviewPage)

const openConfig = () => {
  showConfig.value = true
}

const goAdmin = () => {
  router.push('/admin')
}

// 主题加载（原 loadSystemConfig 逻辑，使用 FAY 的 getConfig 接口）
const loadSystemConfig = async () => {
  try {
    const res = await getConfig('theme')
    if (res?.status === 'success' && res.data?.value) {
      const theme = res.data.value
      if (theme === 'default') document.documentElement.removeAttribute('data-theme')
      else document.documentElement.setAttribute('data-theme', theme)
    }
  } catch (e) {
    console.error('获取系统配置失败:', e)
  }
}

onMounted(async () => {
  await loadSystemConfig()
  await scenicStore.refreshAllData()
})

onUnmounted(() => {
  avatarStore.destroySDK()
})
</script>

<style lang="scss" scoped>
.scenic-screen {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  color: #e2e8f0;
}

/* 景区背景 */
.scenic-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
  filter: brightness(0.92) saturate(1.1);
}

.particle-layer {
  position: absolute;
  inset: 0;
  z-index: 2;
}

.top-decor {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 72px;
  z-index: 5;
  pointer-events: none;
}

.scan-line {
  position: absolute;
  left: 0;
  right: 0;
  pointer-events: none;
}

.scan-line.primary {
  top: 64px;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(45, 212, 191, 0.25) 8%,
    rgba(45, 212, 191, 0.85) 50%,
    rgba(45, 212, 191, 0.25) 92%,
    transparent 100%
  );
  box-shadow: 0 0 14px rgba(45, 212, 191, 0.45), 0 0 28px rgba(45, 212, 191, 0.2);
}

.scan-line.primary::after {
  content: '';
  position: absolute;
  left: 0;
  top: -1px;
  height: 4px;
  width: 90px;
  background: linear-gradient(90deg, transparent, #5eead4, transparent);
  border-radius: 2px;
  filter: blur(3px);
  animation: scan-sweep 5s linear infinite;
}

.scan-line.secondary {
  top: 68px;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(45, 212, 191, 0.08) 20%,
    rgba(45, 212, 191, 0.18) 50%,
    rgba(45, 212, 191, 0.08) 80%,
    transparent 100%
  );
}

@keyframes scan-sweep {
  from { left: -90px; }
  to { left: calc(100% + 90px); }
}

.scenic-overlay {
  position: absolute;
  inset: 0;
  background:
    /* 顶部：仅顶部窄带暗色，确保导航栏可读 */
    linear-gradient(180deg, rgba(2, 12, 18, 0.55) 0%, rgba(2, 12, 18, 0) 22%),
    /* 底部：稍暗托起控件 */
    linear-gradient(0deg, rgba(2, 12, 18, 0.4) 0%, rgba(2, 12, 18, 0) 28%),
    /* 左侧中央：数字人区聚光 */
    radial-gradient(ellipse 55% 70% at 32% 50%, transparent 0%, rgba(2, 12, 18, 0.18) 80%),
    /* 右侧：内容区压暗，保证右侧卡片文字清晰 */
    radial-gradient(ellipse 50% 90% at 100% 50%, rgba(2, 12, 18, 0.35) 0%, transparent 70%);
  z-index: 1;
}

/* 主布局 */
.main-layout {
  position: relative;
  z-index: 10;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  height: calc(100vh - 72px);
  padding: 24px 32px 32px;
  box-sizing: border-box;
}

.avatar-section {
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  min-height: 0;
  padding-bottom: 20px;
}

.content-section {
  position: relative;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 4px;
}

.content-section::-webkit-scrollbar {
  width: 4px;
}

.content-section::-webkit-scrollbar-thumb {
  background: rgba(45, 212, 191, 0.25);
  border-radius: 2px;
}

/* 面板切换动画 */
.panel-enter-active,
.panel-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.panel-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.panel-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 响应式 */
@media (max-width: 1280px) {
  .main-layout {
    grid-template-columns: 1fr 420px;
    gap: 24px;
    padding: 20px 24px 28px;
  }
}

@media (max-width: 1024px) {
  .main-layout {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;
  }

  .avatar-section {
    display: none;
  }
}
</style>
