<template>
  <el-container class="layout-container">
    <!-- 顶部栏 -->
    <el-header class="layout-header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">🎯</span>
          <span class="logo-text">TrendRadar</span>
        </div>
        <div class="header-title">热点新闻管理系统</div>
      </div>
    </el-header>

    <el-container class="layout-body">
      <!-- 侧边菜单 -->
      <el-aside class="layout-aside">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
          router
        >
          <el-menu-item index="/" route="/">
            <el-icon><DataAnalysis /></el-icon>
            <span>新闻看板</span>
          </el-menu-item>
          <el-menu-item index="/crawler" route="/crawler">
            <el-icon><Rocket /></el-icon>
            <span>爬虫控制</span>
          </el-menu-item>
          <el-menu-item index="/config" route="/config">
            <el-icon><Setting /></el-icon>
            <span>配置管理</span>
          </el-menu-item>
          <el-menu-item index="/keywords" route="/keywords">
            <el-icon><Collection /></el-icon>
            <span>关键词管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  DataAnalysis, 
  Promotion as Rocket, 
  Setting, 
  Collection 
} from '@element-plus/icons-vue'

const route = useRoute()

const activeMenu = computed(() => {
  return route.path || '/'
})

const handleMenuSelect = (key) => {
  // 路由已通过router属性自动处理
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  letter-spacing: 1px;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  opacity: 0.9;
}

.layout-body {
  flex: 1;
  overflow: hidden;
}

.layout-aside {
  width: 200px;
  background: #fff;
  border-right: 1px solid #e4e7eb;
  overflow-y: auto;
  user-select: none;
}

.sidebar-menu {
  border: none;
  background: #fff;
  user-select: none;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  padding: 0 20px;
  color: #606266;
  font-size: 14px;
  transition: all 0.3s;
  cursor: pointer;
  user-select: none;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background-color: #f5f7fa !important;
  color: #667eea;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: #f0f4ff !important;
  color: #667eea !important;
  border-right: 3px solid #667eea;
}

.sidebar-menu :deep(.el-icon) {
  margin-right: 10px;
  font-size: 16px;
}

.layout-main {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f7fa;
}

/* 滚动条美化 */
.layout-aside::-webkit-scrollbar,
.layout-main::-webkit-scrollbar {
  width: 6px;
}

.layout-aside::-webkit-scrollbar-track,
.layout-main::-webkit-scrollbar-track {
  background: transparent;
}

.layout-aside::-webkit-scrollbar-thumb,
.layout-main::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.layout-aside::-webkit-scrollbar-thumb:hover,
.layout-main::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style>
