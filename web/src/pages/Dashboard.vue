<template>
  <div class="dashboard">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-select
          v-model="selectedDate"
          placeholder="请选择日期"
          size="large"
          @change="handleDateChange"
          style="width: 250px"
        >
          <el-option
            v-for="date in dates"
            :key="date"
            :label="date"
            :value="date"
          >
            <span>📅 {{ date }}</span>
          </el-option>
        </el-select>
        <div v-if="selectedDate" class="stats-info">
          <span class="stat-item">📄 {{ files.length }} 个文件</span>
        </div>
      </div>
      <div class="toolbar-right">
        <el-button 
          v-if="selectedFile" 
          type="primary" 
          @click="openInNewTab"
          :icon="DocumentCopy"
        >
          在新标签页打开
        </el-button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div v-if="!selectedDate" class="empty-state">
      <el-empty description="请选择日期查看新闻" />
    </div>

    <div v-else class="news-container">
      <!-- 文件列表侧边栏 -->
      <div class="file-sidebar">
        <el-scrollbar>
          <div class="file-list">
            <div
              v-for="file in files"
              :key="file"
              :class="['file-item', { active: selectedFile === file }]"
              @click="selectFile(file)"
            >
              <div class="file-icon">📄</div>
              <div class="file-info">
                <div class="file-name">{{ file }}</div>
                <div class="file-time">{{ formatFileName(file) }}</div>
              </div>
            </div>
            <el-empty v-if="files.length === 0" description="暂无新闻文件" />
          </div>
        </el-scrollbar>
      </div>

      <!-- 新闻内容主区域 -->
      <div class="news-main">
        <div v-if="!selectedFile" class="empty-state">
          <el-empty description="请选择文件查看新闻内容" />
        </div>
        <div v-else class="news-content">
          <iframe
            :src="`/news/${selectedDate}/${selectedFile}`"
            frameborder="0"
            class="news-iframe"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { DocumentCopy } from '@element-plus/icons-vue'

const dates = ref([])
const files = ref([])
const selectedDate = ref(null)
const selectedFile = ref(null)

const loadDates = async () => {
  try {
    const response = await fetch('/api/news/dates')
    const data = await response.json()
    dates.value = data.dates || []
    
    // 自动选择最新的日期
    if (dates.value.length > 0) {
      selectedDate.value = dates.value[0]
      await loadFiles(dates.value[0])
    }
  } catch (error) {
    console.error('加载日期列表失败:', error)
  }
}

const handleDateChange = async () => {
  selectedFile.value = null
  if (selectedDate.value) {
    await loadFiles(selectedDate.value)
  }
}

const loadFiles = async (date) => {
  try {
    const response = await fetch(`/api/news/files/${date}`)
    const data = await response.json()
    files.value = data.files || []
    // 自动选择第一个文件
    if (files.value.length > 0) {
      selectedFile.value = files.value[0]
    }
  } catch (error) {
    console.error('加载文件列表失败:', error)
  }
}

const selectFile = (file) => {
  selectedFile.value = file
}

const formatFileName = (filename) => {
  // 提取文件名中的时间信息
  const match = filename.match(/(\d+时\d+分)/)
  if (match) {
    return match[1]
  }
  return filename.replace('.html', '')
}

const openInNewTab = () => {
  if (selectedDate.value && selectedFile.value) {
    window.open(`/news/${selectedDate.value}/${selectedFile.value}`, '_blank')
  }
}

onMounted(() => {
  loadDates()
})
</script>

<style scoped>
.dashboard {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e4e7eb;
  flex-shrink: 0;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stats-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-item {
  font-size: 14px;
  color: #606266;
  padding: 6px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.news-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.file-sidebar {
  width: 260px;
  background: #f9fafb;
  border-right: 1px solid #e4e7eb;
  user-select: none;
  flex-shrink: 0;
}

.file-list {
  padding: 8px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  margin-bottom: 6px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e4e7eb;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.file-item:hover {
  border-color: #667eea;
  background: #f0f4ff;
  transform: translateX(3px);
}

.file-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: white;
}

.file-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.file-info {
  flex: 1;
  min-width: 0;
}

.file-name {
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-item.active .file-name {
  color: white;
}

.file-time {
  font-size: 11px;
  color: #909399;
  margin-top: 2px;
}

.file-item.active .file-time {
  color: rgba(255, 255, 255, 0.8);
}

.news-main {
  flex: 1;
  background: white;
  overflow: hidden;
}

.news-content {
  width: 100%;
  height: 100%;
}

.news-iframe {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .toolbar-left,
  .toolbar-right {
    justify-content: space-between;
  }

  .news-container {
    flex-direction: column;
  }

  .file-sidebar {
    width: 100%;
    height: 200px;
    border-right: none;
    border-bottom: 1px solid #e4e7eb;
  }
}
</style>
