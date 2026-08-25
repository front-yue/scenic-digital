<template>
  <div class="page-header" :class="`align-${align}`">
    <div class="header-deco">
      <div class="deco-bar"></div>
      <div class="deco-bar"></div>
      <div class="deco-bar"></div>
    </div>
    <div class="header-text">
      <h2 class="header-title">{{ title }}</h2>
      <span class="header-subtitle">{{ subtitle }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  align: { type: String, default: 'left' }
})
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 44px;
  flex-shrink: 0;
}

.page-header.align-left { flex-direction: row; }
.page-header.align-right { flex-direction: row-reverse; }

.header-deco {
  display: flex;
  gap: 4px;
  align-items: center;
}

.page-header.align-left .header-deco {
  transform: skewX(-15deg);
}

.page-header.align-right .header-deco {
  transform: skewX(15deg);
}

.deco-bar {
  width: 5px;
  height: 22px;
  border-radius: 1px;
}

.deco-bar:nth-child(1) { background: rgba(45, 212, 191, 0.25); }
.deco-bar:nth-child(2) { background: rgba(45, 212, 191, 0.6); height: 26px; }
.deco-bar:nth-child(3) { background: #2dd4bf; height: 30px; box-shadow: 0 0 10px rgba(45, 212, 191, 0.6); }

.header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.page-header.align-right .header-text {
  align-items: flex-end;
}

.header-title {
  font-size: 22px;
  font-weight: 800;
  color: #f0fdfa;
  letter-spacing: 2px;
  text-shadow: 0 0 14px rgba(45, 212, 191, 0.35);
}

.header-subtitle {
  font-size: 10px;
  color: rgba(45, 212, 191, 0.65);
  letter-spacing: 2px;
  font-weight: 600;
}
</style>
