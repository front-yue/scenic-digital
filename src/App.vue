<template>
  <div>
    <!-- 路由视图出口 -->
    <router-view></router-view>
  </div>
</template>

<script setup>
// App.vue 现在只负责渲染当前路由对应的组件
</script>

<style>
/* 确保背景色在路由切换时过渡平滑 */
body {
  margin: 0;
  padding: 0;
}
</style>
