<template>
  <div v-if="visible" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm transition-opacity duration-300 animate-fade-in">
    <!-- 弹窗主体 (科技感风格) -->
    <div class="relative w-[90%] max-w-[1200px] h-[85%] bg-[#021815]/90 border border-emerald-500/50 rounded-xl shadow-[0_0_50px_rgba(52,211,153,0.2)] flex flex-col overflow-hidden">
      
      <!-- 四角高亮边框 -->
      <div class="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-emerald-400 rounded-tl-xl pointer-events-none"></div>
      <div class="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-emerald-400 rounded-tr-xl pointer-events-none"></div>
      <div class="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-emerald-400 rounded-bl-xl pointer-events-none"></div>
      <div class="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-emerald-400 rounded-br-xl pointer-events-none"></div>

      <!-- 顶部标题栏 -->
      <header class="h-16 border-b border-emerald-500/30 flex items-center justify-between px-6 bg-gradient-to-r from-emerald-900/40 to-transparent shrink-0">
        <div class="flex items-center gap-3">
          <Database class="w-6 h-6 text-emerald-400 animate-pulse" />
          <h2 class="text-xl font-bold text-white tracking-widest text-shadow-glow">系统数据管理核心</h2>
          <span class="text-xs text-emerald-500/60 font-mono tracking-widest ml-4 border border-emerald-500/30 px-2 py-0.5 rounded">ADMIN TERMINAL</span>
        </div>
        <button @click="close" class="text-emerald-400/60 hover:text-emerald-300 hover:rotate-90 transition-all duration-300">
          <X class="w-7 h-7" />
        </button>
      </header>

      <!-- 主体内容 -->
      <div class="flex-1 flex overflow-hidden">
        <!-- 左侧菜单 -->
        <aside class="w-56 lg:w-64 border-r border-emerald-500/20 bg-emerald-900/10 p-4 flex flex-col gap-3 shrink-0">
          <button 
            @click="activeMenu = 'scenic'" 
            :class="['w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm tracking-widest transition-all', activeMenu === 'scenic' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'text-emerald-100/60 hover:bg-emerald-500/10 hover:text-emerald-100 border border-transparent']"
          >
            <Map class="w-4 h-4" />
            景区基础信息
          </button>
          <button 
            @click="activeMenu = 'spots'" 
            :class="['w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm tracking-widest transition-all', activeMenu === 'spots' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'text-emerald-100/60 hover:bg-emerald-500/10 hover:text-emerald-100 border border-transparent']"
          >
            <MapPin class="w-4 h-4" />
            景点列表管理
          </button>
        </aside>

        <!-- 右侧内容区 -->
        <main class="flex-1 p-6 overflow-y-auto custom-scrollbar relative bg-[#021114]/50">
          
          <!-- ================== 景区信息管理 ================== -->
          <div v-if="activeMenu === 'scenic'" class="max-w-4xl animate-fade-in">
             <div class="flex justify-between items-center mb-6">
                <h3 class="text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3">景区全局配置</h3>
                <button @click="handleSaveScenic" class="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_15px_rgba(52,211,153,0.4)] transition-all flex items-center gap-2">
                   <Save class="w-4 h-4" /> 保存修改
                </button>
             </div>

             <div v-if="loadingScenic" class="text-emerald-400/60 flex items-center gap-2">
                <Loader2 class="w-5 h-5 animate-spin" /> 数据加载中...
             </div>
             
             <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="flex flex-col gap-2">
                   <label class="text-sm text-emerald-100/70">景区中文名称</label>
                   <input v-model="scenicForm.scenic_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                </div>
                <div class="flex flex-col gap-2">
                   <label class="text-sm text-emerald-100/70">景区英文名称</label>
                   <input v-model="scenicForm.scenic_en_name" type="text" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                </div>
                <div class="flex flex-col gap-2">
                   <label class="text-sm text-emerald-100/70">成人票价 (元)</label>
                   <input v-model="scenicForm.ticket_price" type="number" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                </div>
                <div class="flex flex-col gap-2">
                   <label class="text-sm text-emerald-100/70">营业时间</label>
                   <input v-model="scenicForm.opening_hours" type="text" placeholder="例如: 08:00 - 18:00" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors" />
                </div>
                <div class="flex flex-col gap-2 md:col-span-2">
                   <label class="text-sm text-emerald-100/70">封面图片</label>
                   <div 
                     class="relative w-full h-40 rounded-lg border-2 border-dashed border-emerald-500/30 bg-emerald-900/10 overflow-hidden flex flex-col items-center justify-center cursor-pointer group hover:border-emerald-400 hover:bg-emerald-900/20 transition-all duration-300"
                     @click="$refs.scenicFileInput.click()"
                   >
                     <img v-if="scenicForm.cover_image" :src="scenicForm.cover_image" class="absolute inset-0 w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" />
                     
                     <!-- 遮罩层与更换提示 (有图片时) -->
                     <div v-if="scenicForm.cover_image" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center gap-2 z-10 backdrop-blur-[2px]">
                        <Upload class="w-8 h-8 text-emerald-300 transform -translate-y-2 group-hover:translate-y-0 transition-transform duration-300" />
                        <span class="text-sm font-bold tracking-widest text-emerald-300">点击更换封面图片</span>
                     </div>

                     <!-- 初始无图片状态 -->
                     <div v-if="!scenicForm.cover_image" class="flex flex-col items-center justify-center gap-3 z-0">
                        <div class="p-3 rounded-full bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                          <Upload class="w-8 h-8 text-emerald-500/60 group-hover:text-emerald-400 transition-colors" />
                        </div>
                        <div class="flex flex-col items-center gap-1">
                          <span class="text-emerald-400 font-bold tracking-wide">点击上传景区封面图</span>
                          <span class="text-[10px] text-emerald-500/50 font-mono">支持 JPG / PNG / WEBP 格式，最大 16MB</span>
                        </div>
                     </div>
                     
                     <!-- 上传中状态 -->
                     <div v-if="uploadingScenicImg" class="absolute inset-0 bg-[#021815]/90 flex flex-col items-center justify-center gap-3 z-20 backdrop-blur-sm">
                       <Loader2 class="w-8 h-8 text-emerald-400 animate-spin" />
                       <span class="text-xs tracking-widest text-emerald-400 animate-pulse">UPLOADING...</span>
                     </div>
                     
                     <input type="file" ref="scenicFileInput" class="hidden" accept="image/*" @change="e => handleImageUpload(e, 'scenic')" />
                   </div>
                </div>
                <div class="flex flex-col gap-2 md:col-span-2">
                   <label class="text-sm text-emerald-100/70">景区详细介绍</label>
                   <textarea v-model="scenicForm.introduction" rows="8" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-4 py-2 text-emerald-100 focus:outline-none focus:border-emerald-400 focus:bg-emerald-900/40 transition-colors resize-none custom-scrollbar"></textarea>
                </div>
             </div>
          </div>

          <!-- ================== 景点列表管理 ================== -->
          <div v-if="activeMenu === 'spots'" class="animate-fade-in flex flex-col h-full">
             <div class="flex justify-between items-center mb-6">
                <h3 class="text-lg font-bold text-emerald-300 border-l-4 border-emerald-400 pl-3">景点与客流管理</h3>
                <button @click="openSpotModal()" class="px-4 py-2 bg-emerald-500/20 border border-emerald-500/50 text-emerald-300 font-bold rounded hover:bg-emerald-500/40 transition-all flex items-center gap-2">
                   <Plus class="w-4 h-4" /> 新增景点
                </button>
             </div>

             <div v-if="loadingSpots" class="text-emerald-400/60 flex items-center gap-2">
                <Loader2 class="w-5 h-5 animate-spin" /> 数据加载中...
             </div>

             <div v-else class="flex-1 overflow-auto custom-scrollbar pr-2">
                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                   <!-- 景点卡片 -->
                   <div v-for="spot in spotList" :key="spot.id" class="border border-emerald-500/30 bg-emerald-900/20 rounded-lg p-4 relative group hover:border-emerald-400/60 transition-colors">
                      <div class="flex gap-4">
                         <img :src="spot.image_url" class="w-20 h-20 rounded object-cover border border-emerald-500/30 shrink-0" alt="spot image" />
                         <div class="flex flex-col flex-1 overflow-hidden">
                            <div class="flex justify-between items-start">
                               <h4 class="text-emerald-100 font-bold truncate">{{ spot.spot_name }}</h4>
                               <span :class="['text-[10px] px-1.5 py-0.5 rounded border whitespace-nowrap', getStatusColor(spot.status)]">{{ spot.status || '未知' }}</span>
                            </div>
                            <span class="text-xs text-emerald-500/60 font-mono truncate">{{ spot.en_name }}</span>
                            <div class="mt-auto flex justify-between items-center">
                               <span class="text-xs text-emerald-100/50">承载: {{ spot.max_capacity }} 人</span>
                               <div class="flex gap-2">
                                  <button @click="openSpotModal(spot)" class="text-emerald-400 hover:text-emerald-300 bg-emerald-900/50 p-1.5 rounded transition-colors"><Edit2 class="w-3.5 h-3.5" /></button>
                                  <button @click="handleDeleteSpot(spot.id)" class="text-red-400 hover:text-red-300 bg-red-900/30 p-1.5 rounded transition-colors"><Trash2 class="w-3.5 h-3.5" /></button>
                               </div>
                            </div>
                         </div>
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </main>
      </div>
    </div>

    <!-- 新增/编辑景点的内部子弹窗 -->
    <div v-if="spotModalVisible" class="absolute inset-0 z-[110] flex items-center justify-center bg-black/60 backdrop-blur-sm">
       <div class="w-[90%] max-w-[500px] bg-[#021815] border border-emerald-400/50 rounded-lg shadow-2xl p-6 relative">
          <button @click="spotModalVisible = false" class="absolute top-4 right-4 text-emerald-400/60 hover:text-emerald-300"><X class="w-5 h-5" /></button>
          <h3 class="text-lg font-bold text-emerald-300 mb-6">{{ isEditingSpot ? '编辑景点' : '新增景点' }}</h3>
          
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
                <label class="text-xs text-emerald-100/70">最大承载量 (人)</label>
                <input v-model="spotForm.max_capacity" type="number" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none" />
             </div>
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70 mb-1">景点图片</label>
                <div 
                  class="relative w-full h-32 rounded-lg border-2 border-dashed border-emerald-500/30 bg-emerald-900/10 overflow-hidden flex flex-col items-center justify-center cursor-pointer group hover:border-emerald-400 hover:bg-emerald-900/20 transition-all duration-300"
                  @click="$refs.spotFileInput.click()"
                >
                  <img v-if="spotForm.image_url" :src="spotForm.image_url" class="absolute inset-0 w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" />
                  
                  <!-- 遮罩层与更换提示 (有图片时) -->
                  <div v-if="spotForm.image_url" class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col items-center justify-center gap-1 z-10 backdrop-blur-[2px]">
                     <Upload class="w-6 h-6 text-emerald-300 transform -translate-y-1 group-hover:translate-y-0 transition-transform duration-300" />
                     <span class="text-xs font-bold tracking-widest text-emerald-300">更换景点图片</span>
                  </div>

                  <!-- 初始无图片状态 -->
                  <div v-if="!spotForm.image_url" class="flex flex-col items-center justify-center gap-2 z-0">
                     <div class="p-2 rounded-full bg-emerald-500/10 group-hover:bg-emerald-500/20 transition-colors">
                       <Upload class="w-6 h-6 text-emerald-500/60 group-hover:text-emerald-400 transition-colors" />
                     </div>
                     <div class="flex flex-col items-center gap-1">
                       <span class="text-xs text-emerald-400 font-bold tracking-wide">点击上传景点图片</span>
                       <span class="text-[9px] text-emerald-500/50 font-mono">JPG / PNG / WEBP, &lt;16MB</span>
                     </div>
                  </div>
                  
                  <!-- 上传中状态 -->
                  <div v-if="uploadingSpotImg" class="absolute inset-0 bg-[#021815]/90 flex flex-col items-center justify-center gap-2 z-20 backdrop-blur-sm">
                    <Loader2 class="w-6 h-6 text-emerald-400 animate-spin" />
                    <span class="text-[10px] tracking-widest text-emerald-400 animate-pulse">UPLOADING...</span>
                  </div>
                  
                  <input type="file" ref="spotFileInput" class="hidden" accept="image/*" @change="e => handleImageUpload(e, 'spot')" />
                </div>
             </div>
             <div class="flex flex-col gap-1">
                <label class="text-xs text-emerald-100/70">景点介绍</label>
                <textarea v-model="spotForm.description" rows="3" class="bg-emerald-900/20 border border-emerald-500/30 rounded px-3 py-2 text-sm text-emerald-100 focus:border-emerald-400 outline-none resize-none custom-scrollbar"></textarea>
             </div>
             
             <div class="flex justify-end gap-3 mt-4">
                <button @click="spotModalVisible = false" class="px-4 py-2 text-sm text-emerald-400/80 hover:text-emerald-300">取消</button>
                <button @click="handleSaveSpot" class="px-4 py-2 text-sm bg-emerald-500 hover:bg-emerald-400 text-[#021114] font-bold rounded shadow-[0_0_10px_rgba(52,211,153,0.3)] flex items-center gap-2">
                   <Loader2 v-if="savingSpot" class="w-4 h-4 animate-spin" /> 保存
                </button>
             </div>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, Database, Map, MapPin, Save, Plus, Edit2, Trash2, Loader2, Upload } from 'lucide-vue-next'
import { getScenicInfo, updateScenicInfo, getScenicSpots, addScenicSpot, updateScenicSpot, deleteScenicSpot, uploadImage } from '../../api/scenic'
import { Message } from '../../utils/message'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'data-updated'])

const close = () => {
  emit('update:visible', false)
}

// 菜单状态
const activeMenu = ref('scenic') // 'scenic' | 'spots'

// ================== 景区信息管理逻辑 ==================
const loadingScenic = ref(false)
const scenicForm = ref({
  id: null,
  scenic_name: '',
  scenic_en_name: '',
  cover_image: '',
  ticket_price: '',
  opening_hours: '',
  introduction: ''
})

const fetchScenicInfo = async () => {
  loadingScenic.value = true
  try {
    const res = await getScenicInfo()
    if (res && res.status === 'success' && res.data) {
      scenicForm.value = { ...res.data }
    }
  } catch (error) {
    console.error('获取景区信息失败:', error)
  } finally {
    loadingScenic.value = false
  }
}

const handleSaveScenic = async () => {
  if (!scenicForm.value.id) return Message.warning('景区信息不存在，无法更新');
  try {
    const res = await updateScenicInfo(scenicForm.value.id, scenicForm.value);
    if (res && res.status === 'success') {
      Message.success('景区全局配置保存成功！');
      emit('data-updated'); // 通知父组件刷新数据
    } else {
      Message.error('保存失败: ' + res.message);
    }
  } catch (error) {
    console.error('保存景区信息失败:', error);
    Message.error('保存失败，请检查网络或后端服务');
  }
}

// ================== 景点列表管理逻辑 ==================
const loadingSpots = ref(false)
const spotList = ref([])

const fetchSpotList = async () => {
  loadingSpots.value = true
  try {
    const res = await getScenicSpots()
    if (res && res.status === 'success') {
      spotList.value = res.data || []
    }
  } catch (error) {
    console.error('获取景点列表失败:', error)
  } finally {
    loadingSpots.value = false
  }
}

// 获取状态颜色标签
const getStatusColor = (status) => {
  if (status === '畅通') return 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10'
  if (status === '拥挤') return 'text-red-400 border-red-400/30 bg-red-400/10'
  return 'text-amber-400 border-amber-400/30 bg-amber-400/10'
}

// 景点弹窗逻辑
const spotModalVisible = ref(false)
const isEditingSpot = ref(false)
const savingSpot = ref(false)
const spotForm = ref({
  id: null,
  spot_name: '',
  en_name: '',
  max_capacity: 1000,
  image_url: '',
  description: ''
})

const openSpotModal = (spot = null) => {
  if (spot) {
    isEditingSpot.value = true
    spotForm.value = { ...spot }
  } else {
    isEditingSpot.value = false
    spotForm.value = {
      id: null,
      spot_name: '',
      en_name: '',
      max_capacity: 1000,
      image_url: '',
      description: ''
    }
  }
  spotModalVisible.value = true
}

const handleSaveSpot = async () => {
  if (!spotForm.value.spot_name || !spotForm.value.max_capacity) {
    return Message.warning('请填写景点名称和最大承载量');
  }
  
  savingSpot.value = true
  try {
    let res;
    // 后端外键要求有 scenic_id，当前我们默认为 1（云梦山）
    const payload = { ...spotForm.value, scenic_id: 1 }; 
    
    if (isEditingSpot.value) {
      res = await updateScenicSpot(spotForm.value.id, payload)
    } else {
      res = await addScenicSpot(payload)
    }
    
    if (res && res.status === 'success') {
      spotModalVisible.value = false
      fetchSpotList() // 刷新列表
      emit('data-updated') // 通知大屏刷新
      Message.success('保存景点成功！')
    } else {
      Message.error('保存景点失败: ' + res.message)
    }
  } catch (error) {
    console.error('保存景点失败:', error)
    Message.error('保存失败，请检查网络或后端服务')
  } finally {
    savingSpot.value = false
  }
}

const handleDeleteSpot = async (id) => {
  if (!confirm('确定要删除此景点吗？删除后不可恢复。')) return;
  try {
    const res = await deleteScenicSpot(id)
    if (res && res.status === 'success') {
      fetchSpotList() // 刷新列表
      emit('data-updated')
      Message.success('删除成功')
    } else {
      Message.error('删除失败: ' + res.message)
    }
  } catch (error) {
    console.error('删除景点失败:', error)
    Message.error('删除失败，请检查网络')
  }
}

// ================== 图片上传通用逻辑 ==================
const uploadingScenicImg = ref(false)
const uploadingSpotImg = ref(false)
const scenicFileInput = ref(null)
const spotFileInput = ref(null)

const handleImageUpload = async (event, type) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 校验文件类型和大小 (前端先拦截一次)
  if (!file.type.startsWith('image/')) {
    Message.warning('请选择有效的图片文件')
    return
  }
  if (file.size > 16 * 1024 * 1024) {
    Message.warning('图片大小不能超过 16MB')
    return
  }

  const isScenic = type === 'scenic'
  if (isScenic) uploadingScenicImg.value = true
  else uploadingSpotImg.value = true

  try {
    const res = await uploadImage(file)
    if (res && res.status === 'success' && res.data?.url) {
      if (isScenic) {
        scenicForm.value.cover_image = res.data.url
      } else {
        spotForm.value.image_url = res.data.url
      }
      Message.success('图片上传成功')
    } else {
      Message.error('上传失败: ' + (res?.message || '未知错误'))
    }
  } catch (error) {
    console.error('图片上传异常:', error)
    Message.error('网络或服务器异常，图片上传失败')
  } finally {
    if (isScenic) uploadingScenicImg.value = false
    else uploadingSpotImg.value = false
    // 清空 input value 确保同名文件可再次触发 change 事件
    event.target.value = ''
  }
}

// 监听弹窗显示，自动加载数据
watch(() => props.visible, (newVal) => {
  if (newVal) {
    fetchScenicInfo()
    fetchSpotList()
  }
})
</script>

<style scoped>
/* 简单的淡入动画 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.98); }
  to { opacity: 1; transform: scale(1); }
}
</style>
