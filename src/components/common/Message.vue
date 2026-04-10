<template>
  <div class="fixed top-10 left-1/2 -translate-x-1/2 z-[9999] flex flex-col gap-2 pointer-events-none">
    <transition-group name="msg-fade">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg border bg-[#021815]/90 backdrop-blur-md min-w-[280px]"
        :class="{
          'border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]': msg.type === 'success',
          'border-red-500/50 shadow-[0_0_15px_rgba(248,113,113,0.2)]': msg.type === 'error',
          'border-amber-500/50 shadow-[0_0_15px_rgba(251,191,36,0.2)]': msg.type === 'warning',
          'border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]': msg.type === 'info'
        }"
      >
        <!-- 图标 -->
        <CheckCircle2 v-if="msg.type === 'success'" class="w-5 h-5 text-emerald-400" />
        <XCircle v-if="msg.type === 'error'" class="w-5 h-5 text-red-400" />
        <AlertCircle v-if="msg.type === 'warning'" class="w-5 h-5 text-amber-400" />
        <Info v-if="msg.type === 'info'" class="w-5 h-5 text-blue-400" />

        <span class="text-sm font-medium tracking-wide" :class="{
          'text-emerald-100': msg.type === 'success',
          'text-red-100': msg.type === 'error',
          'text-amber-100': msg.type === 'warning',
          'text-blue-100': msg.type === 'info'
        }">
          {{ msg.content }}
        </span>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { CheckCircle2, XCircle, AlertCircle, Info } from 'lucide-vue-next'

const messages = ref([])
let seed = 0

const addMessage = (options) => {
  const id = seed++
  const msg = {
    id,
    type: options.type || 'info',
    content: options.content,
    duration: options.duration || 3000
  }
  messages.value.push(msg)

  if (msg.duration > 0) {
    setTimeout(() => {
      removeMessage(id)
    }, msg.duration)
  }
}

const removeMessage = (id) => {
  const idx = messages.value.findIndex(m => m.id === id)
  if (idx !== -1) {
    messages.value.splice(idx, 1)
  }
}

defineExpose({
  addMessage
})
</script>

<style scoped>
.msg-fade-enter-active,
.msg-fade-leave-active {
  transition: all 0.3s ease;
}
.msg-fade-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}
.msg-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
