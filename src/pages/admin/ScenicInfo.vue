<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- 固定的顶部操作栏 -->
    <div class="flex-shrink-0 flex justify-between items-center p-4 md:p-6 border-b border-emerald-500/10">
      <h3 class="text-base md:text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3 tracking-wider">景区全局配置</h3>
      <button @click="handleSave" class="px-3 md:px-6 py-1.5 md:py-2 text-xs md:text-sm bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_15px_rgba(52,211,153,0.4)] transition-all flex items-center gap-1.5 md:gap-2">
        <Save class="w-3.5 h-3.5 md:w-4 md:h-4" /> 保存
      </button>
    </div>

    <!-- 可滚动的表单主体 -->
    <div class="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar">
      <div class="max-w-4xl mx-auto pb-12">

        <div v-if="loading" class="text-emerald-400/60 flex items-center gap-2">
          <Loader2 class="w-5 h-5 animate-spin" /> 数据加载中...
        </div>

        <div v-else class="grid grid-cols-1 gap-4 md:gap-6">
          <div class="flex flex-col gap-2">
            <label class="text-sm text-emerald-100/70">景区中文名称</label>
            <input v-model="form.scenic_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-sm text-emerald-100/70">景区英文名称</label>
            <input v-model="form.scenic_en_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-sm text-emerald-100/70">地理位置</label>
            <input v-model="form.address" type="text" placeholder="例如：北京市。。。" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 md:gap-6">
            <div class="flex flex-col gap-2">
              <label class="text-sm text-emerald-100/70">成人票价 (元)</label>
              <input v-model="form.ticket_price" type="number" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-sm text-emerald-100/70">营业时间</label>
              <input v-model="form.opening_hours" type="text" placeholder="例如: 08:00 - 18:00" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
            </div>
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-sm text-emerald-100/70">封面图片</label>
            <div
              class="relative w-full h-40 rounded-lg border-2 border-dashed border-emerald-500/30 bg-emerald-900/10 overflow-hidden flex flex-col items-center justify-center cursor-pointer group hover:border-emerald-400 hover:bg-emerald-900/20 transition-all duration-300"
              @click="$refs.fileInput.click()"
            >
              <img v-if="form.cover_image" :src="form.cover_image" class="absolute inset-0 w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" />

              <!-- 遮罩层与更换提示 (有图片时) -->
              <div v-if="form.cover_image" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center gap-2 z-10 backdrop-blur-[2px]">
                <Upload class="w-8 h-8 text-emerald-300 transform -translate-y-2 group-hover:translate-y-0 transition-transform duration-300" />
                <span class="text-sm font-bold tracking-widest text-emerald-300">点击更换封面图片</span>
              </div>

              <!-- 初始无图片状态 -->
              <div v-if="!form.cover_image" class="flex flex-col items-center justify-center gap-3 z-0">
                <div class="p-3 rounded-full bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                  <Upload class="w-8 h-8 text-emerald-500/60 group-hover:text-emerald-400 transition-colors" />
                </div>
                <div class="flex flex-col items-center gap-1">
                  <span class="text-emerald-400 font-bold tracking-wide">点击上传景区封面图</span>
                  <span class="text-[10px] text-emerald-500/50 font-mono">支持 JPG / PNG / WEBP 格式，最大 16MB</span>
                </div>
              </div>

              <!-- 上传中状态 -->
              <div v-if="uploading" class="absolute inset-0 bg-[#021815]/90 flex flex-col items-center justify-center gap-3 z-20 backdrop-blur-sm">
                <Loader2 class="w-8 h-8 text-emerald-400 animate-spin" />
                <span class="text-xs tracking-widest text-emerald-400 animate-pulse">UPLOADING...</span>
              </div>

              <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleImageUpload" />
            </div>
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-sm text-emerald-100/70">景区详细介绍</label>
            <textarea v-model="form.introduction" rows="8" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors resize-none custom-scrollbar"></textarea>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Save, Loader2, Upload } from 'lucide-vue-next'
import { getScenicInfo, updateScenicInfo, uploadImage } from '@/api/scenic'
import { Message } from '@/utils/message'

const loading = ref(false)
const uploading = ref(false)
const form = ref({
  id: null,
  scenic_name: '',
  scenic_en_name: '',
  address: '',
  cover_image: '',
  ticket_price: '',
  opening_hours: '',
  introduction: ''
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getScenicInfo()
    if (res && res.status === 'success' && res.data) {
      form.value = { ...res.data }
    }
  } catch (error) {
    console.error('获取景区信息失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  if (!form.value.id) return Message.warning('景区信息不存在，无法更新')
  try {
    const res = await updateScenicInfo(form.value.id, form.value)
    if (res && res.status === 'success') {
      Message.success('景区全局配置保存成功！')
    } else {
      Message.error('保存失败: ' + res.message)
    }
  } catch (error) {
    console.error('保存景区信息失败:', error)
    Message.error('保存失败，请检查网络或后端服务')
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    Message.warning('请选择有效的图片文件')
    return
  }
  if (file.size > 16 * 1024 * 1024) {
    Message.warning('图片大小不能超过 16MB')
    return
  }

  uploading.value = true
  try {
    const res = await uploadImage(file)
    if (res && res.status === 'success' && res.data?.url) {
      form.value.cover_image = res.data.url
      Message.success('图片上传成功')
    } else {
      Message.error('上传失败: ' + (res?.message || '未知错误'))
    }
  } catch (error) {
    console.error('图片上传异常:', error)
    Message.error('网络或服务器异常，图片上传失败')
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

onMounted(fetchData)
</script>
