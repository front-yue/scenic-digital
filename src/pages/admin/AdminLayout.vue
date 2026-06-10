<template>
  <!-- 密码验证遮罩 -->
  <div v-if="!isVerified" class="fixed inset-0 z-50 bg-[#020b14]/95 backdrop-blur-md flex items-center justify-center">
    <div class="w-[340px] bg-[#061226]/90 border border-emerald-500/40 rounded-xl p-8 shadow-[0_0_40px_rgba(52,211,153,0.1)]">
      <div class="flex flex-col items-center gap-5">
        <div class="w-14 h-14 rounded-full border border-emerald-400/40 bg-emerald-500/10 flex items-center justify-center">
          <Lock class="w-6 h-6 text-emerald-400" />
        </div>
        <div class="text-center">
          <h3 class="text-lg font-bold text-white tracking-wider mb-1">管理后台</h3>
          <p class="text-xs text-emerald-400/60 font-mono tracking-widest">ACCESS REQUIRED</p>
        </div>
        <div class="w-full">
          <input
            v-model="password"
            @keyup.enter="handleVerify"
            type="password"
            placeholder="请输入访问密码"
            class="w-full h-11 bg-white/5 border border-emerald-500/30 rounded-lg px-4 text-sm text-white/90 tracking-wider placeholder-emerald-100/25 focus:outline-none focus:border-emerald-400/60 focus:bg-white/8 transition-all"
            autofocus
          />
          <p v-if="errorMsg" class="mt-2 text-xs text-red-400/80 text-center">{{ errorMsg }}</p>
        </div>
        <button
          @click="handleVerify"
          :disabled="!password.trim() || verifying"
          class="w-full h-10 rounded-lg bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 text-sm font-bold tracking-widest hover:bg-emerald-500/30 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          {{ verifying ? '验证中...' : '进入管理' }}
        </button>
        <button @click="router.push('/')" class="text-xs text-emerald-500/40 hover:text-emerald-400/70 transition-colors">
          ← 返回首页
        </button>
      </div>
    </div>
  </div>

  <!-- 管理后台主体 -->
  <div v-else class="h-screen w-screen bg-[#021114] flex flex-col overflow-hidden">
    <!-- 顶部标题栏 -->
    <header class="h-12 md:h-16 border-b border-emerald-500/30 flex items-center justify-between px-3 md:px-6 bg-gradient-to-r from-emerald-900/40 to-transparent shrink-0">
      <div class="flex items-center gap-2 md:gap-3">
        <Database class="w-5 h-5 md:w-6 md:h-6 text-emerald-400 animate-pulse" />
        <h2 class="text-base md:text-xl font-bold text-white tracking-widest">管理核心</h2>
        <span class="hidden md:inline text-xs text-emerald-500/60 font-mono tracking-widest ml-4 border border-emerald-500/30 px-2 py-0.5 rounded">ADMIN TERMINAL</span>
      </div>
      <button @click="goBack" class="flex items-center gap-1 md:gap-2 px-2.5 md:px-4 py-1.5 md:py-2 rounded-lg border border-emerald-500/30 bg-emerald-900/20 text-emerald-300 hover:bg-emerald-500/20 transition-all">
        <ArrowLeft class="w-3.5 h-3.5 md:w-4 md:h-4" />
        <span class="text-xs md:text-sm tracking-wider">返回</span>
      </button>
    </header>

    <!-- 导航菜单：移动端水平Tab / 桌面端侧边栏 -->
    <nav class="md:hidden flex border-b border-emerald-500/20 bg-emerald-900/10 shrink-0 overflow-x-auto">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        custom
        v-slot="{ isActive, navigate }"
      >
        <button
          @click="navigate"
          :class="['flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 text-xs tracking-wider transition-all whitespace-nowrap border-b-2', isActive ? 'text-emerald-300 border-emerald-400 bg-emerald-500/10' : 'text-emerald-100/50 border-transparent hover:text-emerald-100']"
        >
          <component :is="item.icon" class="w-3.5 h-3.5" />
          {{ item.label }}
        </button>
      </router-link>
    </nav>

    <!-- 主体内容 -->
    <div class="flex-1 flex overflow-hidden">
      <!-- 桌面端侧边栏 -->
      <aside class="hidden md:flex w-56 lg:w-64 border-r border-emerald-500/20 bg-emerald-900/10 p-4 flex-col gap-3 shrink-0">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          custom
          v-slot="{ isActive, navigate }"
        >
          <button
            @click="navigate"
            :class="['w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm tracking-widest transition-all', isActive ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'text-emerald-100/60 hover:bg-emerald-500/10 hover:text-emerald-100 border border-transparent']"
          >
            <component :is="item.icon" class="w-4 h-4" />
            {{ item.label }}
          </button>
        </router-link>
      </aside>

      <!-- 内容区 -->
      <main class="flex-1 flex flex-col relative bg-gradient-to-br from-[#020b14]/80 to-transparent overflow-hidden">
        <router-view v-slot="{ Component }">
          <transition name="admin-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Database, Map, MapPin, Settings, ArrowLeft, Lock } from 'lucide-vue-next'
import { scenicRequest } from '@/utils/request'

const router = useRouter()

const menuItems = [
  { path: '/admin/scenic', label: '景区基础信息', icon: Map },
  { path: '/admin/spots', label: '景点列表管理', icon: MapPin },
  { path: '/admin/control', label: '互动控制台', icon: Settings }
]

const goBack = () => {
  router.push('/')
}

// ========== 密码验证 ==========
const isVerified = ref(false)
const password = ref('')
const verifying = ref(false)
const errorMsg = ref('')

const handleVerify = async () => {
  if (!password.value.trim() || verifying.value) return
  verifying.value = true
  errorMsg.value = ''
  try {
    const res = await scenicRequest.post('/api/admin/verify', { password: password.value })
    if (res && res.code === 200) {
      sessionStorage.setItem('admin_verified', 'true')
      isVerified.value = true
    } else {
      errorMsg.value = res?.message || '验证失败'
    }
  } catch (err) {
    errorMsg.value = err?.response?.data?.message || '密码错误'
  } finally {
    verifying.value = false
  }
}

onMounted(() => {
  if (sessionStorage.getItem('admin_verified') == 'true') {
    isVerified.value = true
  }
})
</script>

<style scoped>
.admin-fade-enter-active {
  transition: opacity 0.2s ease-out, transform 0.2s ease-out;
}
.admin-fade-leave-active {
  transition: opacity 0.15s ease-in;
}
.admin-fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
.admin-fade-leave-to {
  opacity: 0;
}
</style>
