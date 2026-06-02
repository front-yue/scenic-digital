<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="visible" class="fixed inset-0 z-[200] flex items-end sm:items-center justify-center">
        <!-- 遮罩 -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="close"></div>

        <!-- 弹窗主体 -->
        <Transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="translate-y-full"
          enter-to-class="translate-y-0"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="translate-y-0"
          leave-to-class="translate-y-full"
        >
          <div
            v-if="visible"
            class="relative w-full max-w-lg max-h-[85vh] bg-[#021815]/95 backdrop-blur-xl border border-emerald-500/30 rounded-t-2xl sm:rounded-2xl flex flex-col overflow-hidden shadow-[0_0_40px_rgba(52,211,153,0.1)]"
          >
            <!-- 顶部标题栏 -->
            <div class="flex items-center justify-between px-5 py-4 border-b border-emerald-500/20 shrink-0 bg-gradient-to-r from-emerald-900/40 to-transparent">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                  <SettingsIcon class="w-4 h-4 text-emerald-400" />
                </div>
                <div>
                  <h2 class="text-base font-bold text-white tracking-wider">系统配置</h2>
                  <p class="text-[10px] text-emerald-500/50 font-mono tracking-widest mt-0.5">SYSTEM CONFIGURATION</p>
                </div>
              </div>
              <button @click="close" class="w-8 h-8 rounded-lg flex items-center justify-center border border-emerald-500/20 bg-emerald-900/20 text-emerald-400/60 hover:text-emerald-300 hover:bg-emerald-500/20 transition-all">
                <XIcon class="w-4 h-4" />
              </button>
            </div>

            <!-- 配置内容（滚动） -->
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-5">
              <div v-for="group in CONFIG_SCHEMA" :key="group.key">
                <!-- 分组标题 -->
                <div class="flex items-center gap-2 mb-3">
                  <div class="w-1 h-4 bg-emerald-400 rounded-full"></div>
                  <h3 class="text-sm font-bold text-white tracking-wider">{{ group.group }}</h3>
                </div>
                <p class="text-[11px] text-emerald-100/40 mb-3 ml-3">{{ group.description }}</p>

                <!-- 字段列表 -->
                <div class="space-y-3">
                  <div v-for="field in group.fields" :key="field.key" class="space-y-1.5">
                    <div class="flex items-center justify-between">
                      <label class="text-xs text-emerald-100/70 font-medium">{{ field.label }}</label>
                      <span
                        class="text-[9px] px-1.5 py-0.5 rounded font-mono tracking-wider"
                        :class="{
                          'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30': configSources[field.key] === 'user',
                          'bg-blue-500/15 text-blue-400 border border-blue-500/30': configSources[field.key] === 'env',
                          'bg-red-500/15 text-red-400 border border-red-500/30': configSources[field.key] === 'empty'
                        }"
                      >
                        {{ configSources[field.key] === 'user' ? '自定义' : configSources[field.key] === 'env' ? '默认值' : '未配置' }}
                      </span>
                    </div>
                    <div class="relative">
                      <input
                        v-model="formData[field.key]"
                        :type="field.type === 'password' && !showSecrets[field.key] ? 'password' : 'text'"
                        :placeholder="field.placeholder"
                        class="w-full h-10 bg-emerald-900/20 border border-emerald-500/30 rounded-lg px-3 pr-10 text-sm text-emerald-100 placeholder-emerald-100/30 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-all font-mono text-xs"
                        @input="onFieldChange(field.key)"
                      />
                      <button
                        v-if="field.type === 'password'"
                        @click="showSecrets[field.key] = !showSecrets[field.key]"
                        class="absolute right-2 top-1/2 -translate-y-1/2 w-6 h-6 flex items-center justify-center text-emerald-400/40 hover:text-emerald-300 transition-colors"
                      >
                        <EyeIcon v-if="!showSecrets[field.key]" class="w-3.5 h-3.5" />
                        <EyeOffIcon v-else class="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 底部操作栏 -->
            <div class="shrink-0 px-5 py-4 border-t border-emerald-500/20 flex items-center justify-between gap-3">
              <button
                @click="handleReset"
                class="px-4 py-2 rounded-lg border border-emerald-500/20 bg-emerald-900/10 text-xs text-emerald-100/50 hover:text-emerald-100/80 hover:bg-emerald-900/30 transition-all"
              >
                恢复默认
              </button>
              <div class="flex gap-2">
                <button
                  @click="close"
                  class="px-4 py-2 rounded-lg border border-emerald-500/20 bg-emerald-900/10 text-xs text-emerald-100/60 hover:text-emerald-100 hover:bg-emerald-900/30 transition-all"
                >
                  取消
                </button>
                <button
                  @click="handleSave"
                  class="px-5 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-xs text-[#021114] font-bold shadow-[0_0_15px_rgba(52,211,153,0.4)] transition-all active:scale-95"
                >
                  保存配置
                </button>
              </div>
            </div>

            <!-- 保存成功提示 -->
            <Transition
              enter-active-class="transition duration-300"
              enter-from-class="opacity-0 translate-y-2"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition duration-200"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <div v-if="showSaved" class="absolute top-16 left-1/2 -translate-x-1/2 px-4 py-2 rounded-lg bg-emerald-500/20 border border-emerald-400/40 text-xs text-emerald-300 font-medium backdrop-blur-md">
                ✓ 配置已保存，刷新页面后生效
              </div>
            </Transition>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, reactive } from 'vue'
import { Settings as SettingsIcon, X as XIcon, Eye as EyeIcon, EyeOff as EyeOffIcon } from 'lucide-vue-next'
import { CONFIG_SCHEMA, getAllConfigValues, saveConfigValues, clearUserConfig } from '@/utils/config-store'

const props = defineProps({
  visible: { type: Boolean, default: false }
})

const emit = defineEmits(['update:visible', 'saved'])

const formData = reactive({})
const configSources = reactive({})
const showSecrets = reactive({})
const showSaved = ref(false)

// 打开弹窗时加载当前配置
watch(() => props.visible, (val) => {
  if (val) {
    const allValues = getAllConfigValues()
    for (const [key, info] of Object.entries(allValues)) {
      formData[key] = info.value
      configSources[key] = info.source
    }
    showSaved.value = false
  }
})

const onFieldChange = (key) => {
  // 标记为用户自定义
  configSources[key] = formData[key] ? 'user' : 'empty'
}

const handleSave = () => {
  saveConfigValues({ ...formData })
  showSaved.value = true
  setTimeout(() => {
    showSaved.value = false
    emit('saved')
    close()
  }, 1500)
}

const handleReset = () => {
  clearUserConfig()
  // 重新加载默认值
  const allValues = getAllConfigValues()
  for (const [key, info] of Object.entries(allValues)) {
    formData[key] = info.value
    configSources[key] = info.source
  }
}

const close = () => {
  emit('update:visible', false)
}
</script>
