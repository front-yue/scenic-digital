<template>
  <div class="page-frame">
    <PageHeader title="系统公告" subtitle="SYSTEM ANNOUNCEMENT" />

    <div class="page-body announce-body">
      <!-- 版本号卡片 -->
      <div class="version-card">
        <div class="version-info">
          <span class="version-label">当前版本</span>
          <span class="version-num">
            v{{ appVersion }}
            <span class="version-tag">智游版</span>
          </span>
        </div>
        <div class="version-orbit">
          <div class="orbit-ring"></div>
          <div class="orbit-core"></div>
        </div>
      </div>

      <!-- 更新内容 -->
      <section class="announce-section">
        <div class="section-title">
          <CheckCircle2 class="section-icon" />
          <span>本次更新内容</span>
        </div>
        <ul class="announce-list">
          <li v-for="(item, i) in updates" :key="i">
            <strong class="item-title">{{ item.title }}：</strong>
            <span class="item-desc">{{ item.desc }}</span>
          </li>
        </ul>
      </section>

      <!-- 注意事项 -->
      <section class="announce-section notice">
        <div class="section-title">
          <AlertTriangle class="section-icon" />
          <span>运行注意事项</span>
        </div>
        <ul class="notice-list">
          <li v-for="(item, i) in notices" :key="i">{{ item }}</li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
import { CheckCircle2, AlertTriangle } from 'lucide-vue-next'
import PageHeader from '@/components/scenic/PageHeader.vue'

const appVersion = '2.0.0'

const updates = [
  { title: '智能播报系统', desc: '支持后端配置多时段定时播报，可指定日期、时间范围与播报内容，数字人自动播报接待。' },
  { title: '数字人启动问候', desc: '开启数字人后自动拉取系统问候语并播报，初次使用体验更友好。' },
  { title: '路线推荐与管理', desc: '推荐游览路线从数据库动态读取，管理后台支持路线景点可视化编辑与 AI 智能生成。' },
  { title: '多主题适配优化', desc: '春夏秋冬四套主题颜色规范统一，表单控件、下拉选项随主题自动切换，视觉风格一致。' }
]

const notices = [
  '首次升级需执行 SQL 迁移：创建 broadcast_schedule 表，并确保 system_config 包含 broadcast_greeting 记录。',
  '数字人功能需在项目根目录 .env 中正确配置 VITE_XMOV_APP_ID 与 VITE_XMOV_APP_SECRET。',
  '管理后台已启用密码验证，默认密码配置在 backend/.env 的 ADMIN_PASSWORD 字段。'
]
</script>

<style scoped>
.page-frame {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  gap: 16px;
}

.page-body {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 版本号卡片 */
.version-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border: 1px solid rgba(45, 212, 191, 0.35);
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(45, 212, 191, 0.1) 0%, rgba(2, 18, 24, 0.5) 60%);
  backdrop-filter: blur(6px);
  position: relative;
  overflow: hidden;
}

.version-label {
  display: block;
  font-size: 13px;
  color: rgba(45, 212, 191, 0.85);
  margin-bottom: 6px;
  letter-spacing: 1px;
}

.version-num {
  font-size: 30px;
  font-weight: 900;
  color: #f0fdfa;
  letter-spacing: 1px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  text-shadow: 0 0 16px rgba(45, 212, 191, 0.35);
}

.version-tag {
  font-size: 13px;
  font-weight: 500;
  color: #2dd4bf;
  margin-left: 8px;
  letter-spacing: 0;
}

.version-orbit {
  position: relative;
  width: 56px;
  height: 56px;
  flex-shrink: 0;
}

.orbit-ring {
  position: absolute;
  inset: 0;
  border: 2px dashed rgba(45, 212, 191, 0.5);
  border-radius: 50%;
  animation: spin 10s linear infinite;
}

.orbit-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(45, 212, 191, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}

.orbit-core::after {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #2dd4bf;
  box-shadow: 0 0 10px #2dd4bf;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 区块 */
.announce-section {
  border: 1px solid rgba(45, 212, 191, 0.18);
  border-radius: 16px;
  background: rgba(2, 18, 24, 0.55);
  backdrop-filter: blur(6px);
  padding: 18px 20px;
}

.announce-section.notice {
  border-color: rgba(251, 191, 36, 0.3);
  background: rgba(69, 45, 4, 0.35);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #5eead4;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 14px;
}

.notice .section-title {
  color: #fbbf24;
}

.section-icon {
  width: 18px;
  height: 18px;
}

.announce-list,
.notice-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.announce-list li {
  position: relative;
  padding-left: 18px;
  font-size: 14px;
  line-height: 1.7;
  color: rgba(226, 232, 240, 0.85);
}

.announce-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 10px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #2dd4bf;
  box-shadow: 0 0 8px rgba(45, 212, 191, 0.6);
}

.item-title {
  color: #ccfbf1;
  font-weight: 600;
}

.item-desc {
  color: rgba(226, 232, 240, 0.8);
}

.notice-list {
  padding-left: 18px;
  list-style: disc;
}

.notice-list li {
  font-size: 13px;
  line-height: 1.7;
  color: rgba(251, 191, 36, 0.75);
}
</style>
