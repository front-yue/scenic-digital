<template>
  <div class="avatar-panel">
    <!-- 数字人渲染容器 -->
    <div class="avatar-stage">
      <div id="sdk" class="sdk-container"></div>

      <!-- 加载/未就绪提示 -->
      <div v-if="!isReady" class="avatar-placeholder">
        <div class="pulse-ring"></div>
        <User class="placeholder-icon" />
        <p class="placeholder-text">数字人准备中...</p>
      </div>
    </div>

    <!-- 底部控制按钮 -->
    <div class="avatar-controls">
      <button
        class="ctrl-btn"
        :class="{ active: micEnabled }"
        title="麦克风"
        @click="handleToggleMic"
      >
        <Mic class="ctrl-icon" :class="{ pulsing: micEnabled }" />
        <span class="ctrl-label">麦克</span>
      </button>
      <button
        class="ctrl-btn"
        :class="{ active: wakeupEnabled }"
        title="唤醒词"
        @click="handleToggleWakeup"
      >
        <Zap class="ctrl-icon" />
        <span class="ctrl-label">唤醒</span>
      </button>
      <button
        class="ctrl-btn"
        :class="{ active: isXmovRunning }"
        title="数字人开关"
        @click="handleToggleXmov"
      >
        <Power class="ctrl-icon" :class="{ pulsing: isXmovRunning }" />
        <span class="ctrl-label">数字人</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAvatarStore } from '@/stores/avatar'
import { toggleMicrophone, startFayLive, stopFayLive } from '@/api/fay'
import { Message } from '@/utils/message'
import { User, Mic, Zap, Power } from 'lucide-vue-next'

const avatarStore = useAvatarStore()
const { isReady, isXmovRunning } = storeToRefs(avatarStore)

// FAY 实时通道状态（本地记录）
const micEnabled = ref(false)
const wakeupEnabled = ref(false)

// ========== 控制按钮（严格沿用原 FAY 逻辑） ==========
const handleToggleMic = async () => {
  try {
    await toggleMicrophone()
    micEnabled.value = !micEnabled.value
    Message.success(micEnabled.value ? '麦克风已开启' : '麦克风已关闭')
  } catch (error) {
    console.error('切换麦克风状态失败:', error)
    Message.error('切换麦克风状态失败')
  }
}

const handleToggleWakeup = async () => {
  try {
    if (wakeupEnabled.value) {
      await stopFayLive()
      wakeupEnabled.value = false
      Message.info('已关闭 FAY 实时对讲')
    } else {
      await startFayLive()
      wakeupEnabled.value = true
      Message.success('已开启 FAY 实时对讲')
    }
  } catch (error) {
    console.error('切换 FAY 实时对讲失败:', error)
    Message.error('切换 FAY 实时对讲失败')
  }
}

const handleToggleXmov = async () => {
  if (avatarStore.isXmovRunning) {
    avatarStore.destroySDK()
    Message.info('已关闭前端 Xmov 数字人渲染')
  } else {
    avatarStore.initSDK()
    Message.success('已启动前端 Xmov 数字人渲染，请稍候...')
  }
}
</script>

<style scoped>
.avatar-panel {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

    /* 数字人舞台 */
.avatar-stage {
  position: relative;
  width: 100%;
  max-width: 520px;
  height: 100%;
  max-height: 720px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

/* 底部接地阴影，替代原来的全息圆环 */
.avatar-stage::after {
  content: '';
  position: absolute;
  bottom: 6%;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 24px;
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.45) 0%, transparent 70%);
  border-radius: 50%;
  z-index: 1;
  pointer-events: none;
  filter: blur(4px);
}

.sdk-container {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 2;
}

.sdk-container :deep(canvas) {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain;
  object-position: bottom center;
}

/* 占位提示 */
.avatar-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.pulse-ring {
  position: absolute;
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 1px solid rgba(45, 212, 191, 0.25);
  animation: pulse-ring 2s ease-out infinite;
}

.pulse-ring::before {
  content: '';
  position: absolute;
  inset: 20px;
  border-radius: 50%;
  border: 1px solid rgba(45, 212, 191, 0.15);
}

@keyframes pulse-ring {
  0% {
    transform: scale(0.85);
    opacity: 1;
  }
  100% {
    transform: scale(1.25);
    opacity: 0;
  }
}

.placeholder-icon {
  width: 64px;
  height: 64px;
  color: rgba(45, 212, 191, 0.5);
  margin-bottom: 16px;
}

.placeholder-text {
  color: rgba(226, 232, 240, 0.6);
  font-size: 14px;
  letter-spacing: 1px;
}

/* 语音提示已删除 */

/* 唤醒提示已删除 */

/* 底部控制按钮 */
.avatar-controls {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 0 0;
  z-index: 20;
}

.ctrl-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 16px;
  border: 1px solid rgba(45, 212, 191, 0.2);
  border-radius: 12px;
  background: rgba(2, 12, 18, 0.45);
  color: rgba(226, 232, 240, 0.6);
  cursor: pointer;
  transition: all 0.25s ease;
  min-width: 56px;
  backdrop-filter: blur(4px);
}

.ctrl-btn:hover {
  border-color: rgba(45, 212, 191, 0.45);
  color: #e2e8f0;
  background: rgba(45, 212, 191, 0.1);
  box-shadow: 0 0 16px rgba(45, 212, 191, 0.12);
}

.ctrl-btn.active {
  border-color: rgba(45, 212, 191, 0.6);
  color: #2dd4bf;
  background: rgba(45, 212, 191, 0.14);
  box-shadow:
    inset 0 0 8px rgba(45, 212, 191, 0.08),
    0 0 14px rgba(45, 212, 191, 0.18);
}

.ctrl-icon {
  width: 18px;
  height: 18px;
}

.ctrl-icon.pulsing {
  animation: mic-pulse 1.4s ease-in-out infinite;
}

@keyframes mic-pulse {
  0%, 100% { color: #2dd4bf; opacity: 0.7; }
  50% { color: #5eead4; opacity: 1; }
}

.ctrl-label {
  font-size: 11px;
  letter-spacing: 0.5px;
}
</style>
