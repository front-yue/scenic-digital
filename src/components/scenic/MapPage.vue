<template>
  <div class="page-frame">
    <PageHeader title="景区地图导览" subtitle="SCENIC MAP">
      <template #actions>
        <span class="map-hint"><Map :size="13" /> 实时定位 · 景点标注</span>
      </template>
    </PageHeader>

    <div class="map-body">
      <el-amap :center="mapCenter" :zoom="mapZoom" map-style="amap://styles/darkblue" class="map-canvas" @init="onMapInit" />
      <div class="map-mask"></div>
      <div v-if="!store.scenicInfo" class="map-loading">地图加载中…</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Map } from 'lucide-vue-next'
import { useScenicStore } from '@/stores/scenic'
import { getGeocode } from '@/api/map'
import PageHeader from '@/components/scenic/PageHeader.vue'

const store = useScenicStore()
const mapCenter = ref([120.148, 30.253])
const mapZoom = ref(14)
let amapInstance = null
let spotMarkers = []

const markerContent = (name) => `
  <div style="display:flex;flex-direction:column;align-items:center;transform:translateY(-4px);">
    <div style="width:12px;height:12px;border-radius:50%;background:#2dd4bf;box-shadow:0 0 10px #2dd4bf;border:2px solid #04121a;"></div>
    <div style="margin-top:4px;padding:2px 8px;border-radius:10px;background:rgba(4,18,26,0.85);color:#eafffb;font-size:12px;white-space:nowrap;border:1px solid rgba(45,212,191,0.4);">${name}</div>
  </div>`

const onMapInit = (map) => {
  amapInstance = map
  addSpotMarkers()
}

const addSpotMarkers = () => {
  if (!amapInstance || !window.AMap) return
  spotMarkers.forEach((m) => amapInstance.remove(m))
  spotMarkers = []
  store.spotList.forEach((spot) => {
    const lat = Number(spot.latitude)
    const lng = Number(spot.longitude)
    if (!lat || !lng) return
    const marker = new window.AMap.Marker({
      position: [lng, lat],
      content: markerContent(spot.spot_name),
      offset: new window.AMap.Pixel(-20, -20),
      title: spot.spot_name,
    })
    amapInstance.add(marker)
    spotMarkers.push(marker)
  })
}

const centerOnScenic = async () => {
  if (!store.scenicInfo?.address) return
  try {
    const res = await getGeocode(store.scenicInfo.address)
    if (res?.code === 200) {
      const [lng, lat] = res.data.location.split(',').map(Number)
      mapCenter.value = [lng, lat]
      await nextTick()
      if (amapInstance) amapInstance.setZoomAndCenter(mapZoom.value, [lng, lat])
    }
  } catch (e) {
    console.error('地理编码失败', e)
  }
}

onMounted(centerOnScenic)
watch(() => store.spotList, () => nextTick(addSpotMarkers), { deep: true })
</script>

<style scoped>
.page-frame { display: flex; flex-direction: column; height: 100%; min-height: 0; }
.map-hint { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; color: #5fd9c8; padding: 6px 12px; border-radius: 20px; background: rgba(45, 212, 191, 0.1); border: 1px solid rgba(45, 212, 191, 0.22); }
.map-body { position: relative; flex: 1; min-height: 0; border-radius: 16px; overflow: hidden; border: 1px solid rgba(45, 212, 191, 0. 2); }
.map-canvas { width: 100%; height: 100%; }
.map-mask { position: absolute; inset: 0; pointer-events: none; box-shadow: inset 0 0 60px rgba(4, 12, 20, 0.7); }
.map-loading { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #5fd9c8; font-size: 14px; }
</style>
