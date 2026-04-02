<template>
  <div 
    class="relative p-4 rounded-2xl border transition-all duration-300 cursor-pointer overflow-hidden group"
    :class="[
      active 
        ? `${activeBg || 'bg-blue-50'} border-transparent shadow-md` 
        : 'bg-white border-gray-100 hover:border-gray-200 hover:shadow-sm'
    ]"
    @click="$emit('toggle')"
  >
    <!-- 激活时的背景光晕效果 -->
    <div 
      v-if="active" 
      class="absolute -top-10 -right-10 w-32 h-32 rounded-full blur-2xl opacity-50"
      :class="[activeGlow || 'bg-blue-400']"
    ></div>

    <div class="relative z-10">
      <div 
        class="w-10 h-10 rounded-full flex items-center justify-center mb-3 transition-colors"
        :class="[
          active 
            ? `${activeColor || 'text-blue-500'} bg-white shadow-sm` 
            : 'text-gray-400 bg-gray-50 group-hover:bg-gray-100'
        ]"
      >
        <component :is="lucideIcons[currentIcon]" class="w-5 h-5" />
      </div>
      
      <div class="font-medium text-gray-800">{{ title }}</div>
      <div class="text-xs mt-1 transition-colors" :class="[active ? (activeColor || 'text-blue-600') : 'text-gray-400']">
        {{ active ? '已开启' : '已关闭' }}
      </div>
    </div>
    
    <!-- 右上角状态指示灯 -->
    <div 
      class="absolute top-4 right-4 w-2 h-2 rounded-full transition-colors"
      :class="[active ? (activeDot || 'bg-blue-500') : 'bg-gray-200']"
    ></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import * as lucideIcons from 'lucide-vue-next'

const props = defineProps({
  title: String,
  active: Boolean,
  icon: String,
  inactiveIcon: String,
  activeColor: String,
  activeBg: String,
  activeGlow: String,
  activeDot: String
})

defineEmits(['toggle'])

const currentIcon = computed(() => {
  if (!props.active && props.inactiveIcon) {
    return props.inactiveIcon
  }
  return props.icon
})
</script>