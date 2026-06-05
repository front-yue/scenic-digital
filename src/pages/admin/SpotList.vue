<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <div class="flex-shrink-0 flex justify-between items-center p-4 md:p-6 border-b border-emerald-500/10">
      <h3 class="text-base md:text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3 tracking-wider">景点列表管理</h3>
      <button @click="openModal()" class="px-3 md:px-4 py-1.5 md:py-2 text-xs md:text-sm bg-emerald-500/20 hover:bg-emerald-500/40 border border-emerald-400/50 rounded text-emerald-300 transition-all flex items-center gap-1.5 md:gap-2 hover:shadow-[0_0_15px_rgba(52,211,153,0.4)]">
        <Plus class="w-3.5 h-3.5 md:w-4 md:h-4" /> <span class="hidden sm:inline">添加新景点</span><span class="sm:hidden">新增</span>
      </button>
    </div>

    <!-- 可滚动的列表主体 -->
    <div class="flex-1 overflow-y-auto p-4 md:p-6 custom-scrollbar">
      <div class="max-w-4xl mx-auto pb-12">
        <div v-if="loading" class="text-emerald-400/60 flex items-center gap-2">
          <Loader2 class="w-5 h-5 animate-spin" /> 数据加载中...
        </div>

        <div v-else class="grid grid-cols-1 gap-4">
          <div v-for="spot in spotList" :key="spot.id" class="group bg-emerald-900/10 border border-emerald-500/20 rounded-lg p-3 md:p-4 hover:border-emerald-500/50 hover:bg-emerald-900/20 transition-all flex flex-col sm:flex-row gap-3 md:gap-4">
            <!-- 左侧缩略图 -->
            <div class="w-full sm:w-24 h-32 sm:h-24 rounded bg-[#020b14] border border-emerald-500/30 overflow-hidden flex-shrink-0 relative group-hover:border-emerald-400">
              <img v-if="spot.image_url" :src="spot.image_url" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />
              <div v-else class="w-full h-full flex items-center justify-center text-emerald-500/30">
                <ImageIcon class="w-8 h-8" />
              </div>
            </div>

            <!-- 中间信息 -->
            <div class="flex-1 flex flex-col justify-center">
              <div class="flex items-center gap-2 mb-1">
                <h4 class="text-base md:text-lg font-bold text-emerald-100">{{ spot.spot_name }}</h4>
                <span class="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded">{{ spot.en_name || 'N/A' }}</span>
              </div>
              <p class="text-sm text-emerald-100/60 line-clamp-2 mb-2">{{ spot.description || '暂无简介' }}</p>
              <div class="flex items-center gap-4 text-xs text-emerald-400/80">
                <span class="flex items-center gap-1"><MapPin class="w-3.5 h-3.5" /> 经纬度: <b class="text-emerald-300">{{ spot.latitude || '-' }}, {{ spot.longitude || '-' }}</b></span>
                <span>排序权重: {{ spot.sort_order }}</span>
              </div>
            </div>

            <!-- 右侧操作 -->
            <div class="flex sm:flex-col gap-2 justify-center border-t sm:border-t-0 sm:border-l border-emerald-500/10 pt-2 sm:pt-0 sm:pl-4">
              <button @click="openModal(spot)" class="p-2 text-emerald-400 hover:bg-emerald-500/20 rounded transition-colors" title="编辑">
                <Edit class="w-4 h-4" />
              </button>
              <button @click="handleDelete(spot.id)" class="p-2 text-red-400 hover:bg-red-500/20 rounded transition-colors" title="删除">
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑景点弹窗 -->
    <Teleport to="body">
      <div v-if="modalVisible" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div class="w-[90%] max-w-[500px] bg-[#021815] border border-emerald-400/50 rounded-lg shadow-2xl p-6 relative">
          <button @click="modalVisible = false" class="absolute top-4 right-4 text-emerald-400/60 hover:text-emerald-300"><X class="w-5 h-5" /></button>
          <h3 class="text-lg font-bold text-emerald-300 mb-6">{{ isEditing ? '编辑景点' : '新增景点' }}</h3>

          <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-xs text-emerald-100/70">景点名称</label>
              <input v-model="spotForm.spot_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-xs text-emerald-100/70">英文名称</label>
              <input v-model="spotForm.en_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-xs text-emerald-100/70">景点经纬度</label>
              <div class="flex gap-3">
                <div class="flex-1 flex flex-col gap-1">
                  <span class="text-[10px] text-emerald-400/60">纬度 latitude</span>
                  <input v-model="spotForm.latitude" type="number" step="0.000001" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" placeholder="30.2368" />
                </div>
                <div class="flex-1 flex flex-col gap-1">
                  <span class="text-[10px] text-emerald-400/60">经度 longitude</span>
                  <input v-model="spotForm.longitude" type="number" step="0.000001" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" placeholder="120.1475" />
                </div>
              </div>
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-xs text-emerald-100/70 mb-1">景点图片</label>
              <div
                class="relative w-full h-32 rounded-lg border-2 border-dashed border-emerald-500/30 bg-emerald-900/10 overflow-hidden flex flex-col items-center justify-center cursor-pointer group hover:border-emerald-400 hover:bg-emerald-900/20 transition-all duration-300"
                @click="$refs.spotFileInput.click()"
              >
                <img v-if="spotForm.image_url" :src="spotForm.image_url" class="absolute inset-0 w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" />

                <div v-if="spotForm.image_url" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center gap-1 z-10 backdrop-blur-[2px]">
                  <Upload class="w-6 h-6 text-emerald-300 transform -translate-y-1 group-hover:translate-y-0 transition-transform duration-300" />
                  <span class="text-xs font-bold tracking-widest text-emerald-300">更换景点图片</span>
                </div>

                <div v-if="!spotForm.image_url" class="flex flex-col items-center justify-center gap-2 z-0">
                  <div class="p-2 rounded-full bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                    <Upload class="w-6 h-6 text-emerald-500/60 group-hover:text-emerald-400 transition-colors" />
                  </div>
                  <div class="flex flex-col items-center gap-1">
                    <span class="text-xs text-emerald-400 font-bold tracking-wide">点击上传景点图片</span>
                    <span class="text-[9px] text-emerald-500/50 font-mono">JPG / PNG / WEBP, &lt;16MB</span>
                  </div>
                </div>

                <div v-if="uploading" class="absolute inset-0 bg-[#021815]/90 flex flex-col items-center justify-center gap-2 z-20 backdrop-blur-sm">
                  <Loader2 class="w-6 h-6 text-emerald-400 animate-spin" />
                  <span class="text-[10px] tracking-widest text-emerald-400 animate-pulse">UPLOADING...</span>
                </div>

                <input type="file" ref="spotFileInput" class="hidden" accept="image/*" @change="handleImageUpload" />
              </div>
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-xs text-emerald-100/70">景点介绍</label>
              <textarea v-model="spotForm.description" rows="3" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none resize-none custom-scrollbar"></textarea>
            </div>

            <div class="flex justify-end gap-3 mt-4">
              <button @click="modalVisible = false" class="px-4 py-2 text-sm text-emerald-400/80 hover:text-emerald-300">取消</button>
              <button @click="handleSave" class="px-4 py-2 text-sm bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_10px_rgba(52,211,153,0.3)] flex items-center gap-2">
                <Loader2 v-if="saving" class="w-4 h-4 animate-spin" /> 保存
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Edit, Trash2, X, Loader2, Upload, Image as ImageIcon, MapPin } from 'lucide-vue-next'
import { getScenicSpots, addScenicSpot, updateScenicSpot, deleteScenicSpot, uploadImage } from '@/api/scenic'
import { Message } from '@/utils/message'

const loading = ref(false)
const spotList = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getScenicSpots()
    if (res && res.status === 'success') {
      spotList.value = res.data || []
    }
  } catch (error) {
    console.error('获取景点列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 弹窗逻辑
const modalVisible = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const uploading = ref(false)
const spotForm = ref({
  id: null,
  spot_name: '',
  en_name: '',
  latitude: '',
  longitude: '',
  image_url: '',
  description: ''
})

const openModal = (spot = null) => {
  if (spot) {
    isEditing.value = true
    spotForm.value = { ...spot }
  } else {
    isEditing.value = false
    spotForm.value = {
      id: null,
      spot_name: '',
      en_name: '',
      latitude: '',
      longitude: '',
      image_url: '',
      description: ''
    }
  }
  modalVisible.value = true
}

const handleSave = async () => {
  if (!spotForm.value.spot_name || !spotForm.value.latitude || !spotForm.value.longitude) {
    return Message.warning('请填写景点名称和经纬度')
  }

  saving.value = true
  try {
    let res
    const payload = { ...spotForm.value, scenic_id: 1 }

    if (isEditing.value) {
      res = await updateScenicSpot(spotForm.value.id, payload)
    } else {
      res = await addScenicSpot(payload)
    }

    if (res && res.status === 'success') {
      modalVisible.value = false
      fetchData()
      Message.success('保存景点成功！')
    } else {
      Message.error('保存景点失败: ' + res.message)
    }
  } catch (error) {
    console.error('保存景点失败:', error)
    Message.error('保存失败，请检查网络或后端服务')
  } finally {
    saving.value = false
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除此景点吗？删除后不可恢复。')) return
  try {
    const res = await deleteScenicSpot(id)
    if (res && res.status === 'success') {
      fetchData()
      Message.success('删除成功')
    } else {
      Message.error('删除失败: ' + res.message)
    }
  } catch (error) {
    console.error('删除景点失败:', error)
    Message.error('删除失败，请检查网络')
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
      spotForm.value.image_url = res.data.url
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
