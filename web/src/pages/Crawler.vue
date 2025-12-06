<template>
  <div class="crawler">
    <!-- 状态卡片 -->
    <el-row :gutter="20" class="status-row">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="status-card" :class="{ running: crawlerStatus.running }">
          <div class="status-icon">{{ crawlerStatus.running ? '🔄' : '⏸️' }}</div>
          <div class="status-content">
            <div class="status-label">运行状态</div>
            <div class="status-value">{{ crawlerStatus.running ? '运行中' : '未运行' }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="status-card">
          <div class="status-icon">🕐</div>
          <div class="status-content">
            <div class="status-label">上次运行</div>
            <div class="status-value">{{ crawlerStatus.last_run || '-' }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="status-card">
          <div class="status-icon">📋</div>
          <div class="status-content">
            <div class="status-label">运行结果</div>
            <div class="status-value" :class="statusClass">{{ statusText }}</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="status-card">
          <div class="status-icon">📝</div>
          <div class="status-content">
            <div class="status-label">日志条数</div>
            <div class="status-value">{{ crawlerStatus.log_count }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 控制面板 -->
    <el-card class="control-panel">
      <template #header>
        <div class="card-header">
          <span>⚡ 手动控制</span>
        </div>
      </template>

      <el-space>
        <el-button
          type="primary"
          size="large"
          @click="startCrawler"
          :disabled="crawlerStatus.running"
          :loading="crawlerStatus.running"
          :icon="VideoPlay"
        >
          立即运行爬虫
        </el-button>
        <el-button
          type="danger"
          size="large"
          @click="stopCrawler"
          :disabled="!crawlerStatus.running"
          :icon="VideoPause"
        >
          停止爬虫
        </el-button>
      </el-space>

      <el-alert
        title="💡 提示"
        type="info"
        description="点击'立即运行爬虫'将执行一次完整的新闻爬取任务"
        :closable="false"
        style="margin-top: 15px"
      />
    </el-card>

    <!-- 定时任务信息 -->
    <el-card class="cron-panel">
      <template #header>
        <div class="card-header">
          <span>⏰ 定时任务信息</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="运行模式">
          <el-tag :type="cronInfo.run_mode === 'cron' ? 'success' : 'info'">
            {{ modeText }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="环境">
          <el-tag :type="cronInfo.is_docker ? 'warning' : 'info'">
            {{ cronInfo.is_docker ? 'Docker容器' : '本地环境' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="cronInfo.run_mode === 'cron'" label="Cron表达式">
          <code>{{ cronInfo.cron_schedule }}</code>
        </el-descriptions-item>
        <el-descriptions-item v-if="cronInfo.run_mode === 'cron'" label="启动时立即执行">
          <el-tag :type="cronInfo.immediate_run ? 'success' : 'info'">
            {{ cronInfo.immediate_run ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 实时日志 -->
    <el-card class="log-panel">
      <template #header>
        <div class="card-header">
          <span>📝 运行日志</span>
          <el-space>
            <el-button size="small" @click="clearLogs" :icon="Delete">清空</el-button>
            <el-button size="small" @click="loadLogs" :icon="Refresh">刷新</el-button>
          </el-space>
        </div>
      </template>

      <div class="log-container" ref="logContainer">
        <div v-if="crawlerLogs.length === 0" class="log-empty">暂无日志</div>
        <div v-for="(log, index) in crawlerLogs" :key="index" class="log-entry">
          <span class="log-time">[{{ log.time }}]</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAppStore } from '../stores'
import { 
  VideoPlay, 
  VideoPause, 
  Delete, 
  Refresh 
} from '@element-plus/icons-vue'

const appStore = useAppStore()
const logContainer = ref(null)

const crawlerStatus = ref({
  running: false,
  last_run: null,
  last_status: null,
  log_count: 0
})

const crawlerLogs = ref([])

const cronInfo = ref({
  cron_schedule: '*/30 * * * *',
  run_mode: 'manual',
  immediate_run: false,
  is_docker: false
})

const statusText = computed(() => {
  const status = crawlerStatus.value.last_status
  if (status === 'success') return '✅ 成功'
  if (status === 'failed') return '❌ 失败'
  if (status === 'stopped') return '⏹️ 已停止'
  if (status === 'error') return '⚠️ 错误'
  return '-'
})

const statusClass = computed(() => {
  const status = crawlerStatus.value.last_status
  if (status === 'success') return 'success'
  if (status === 'failed' || status === 'error') return 'error'
  return ''
})

const modeText = computed(() => {
  const modes = {
    'cron': '定时任务模式',
    'once': '单次执行模式',
    'web': '仅Web服务模式',
    'manual': '手动模式'
  }
  return modes[cronInfo.value.run_mode] || cronInfo.value.run_mode
})

const startCrawler = async () => {
  try {
    const response = await fetch('/api/crawler/start', { method: 'POST' })
    const result = await response.json()
    if (result.success) {
      appStore.showMessage('爬虫已启动', 'success')
      crawlerLogs.value = []
      startLogStreaming()
      updateStatus()
    } else {
      appStore.showMessage(result.message || '启动失败', 'error')
    }
  } catch (error) {
    appStore.showMessage('启动失败', 'error')
  }
}

const stopCrawler = async () => {
  if (!confirm('确定要停止正在运行的爬虫吗？')) return

  try {
    const response = await fetch('/api/crawler/stop', { method: 'POST' })
    const result = await response.json()
    if (result.success) {
      appStore.showMessage('爬虫已停止', 'success')
      stopLogStreaming()
      updateStatus()
    } else {
      appStore.showMessage(result.message || '停止失败', 'error')
    }
  } catch (error) {
    appStore.showMessage('停止失败', 'error')
  }
}

const updateStatus = async () => {
  try {
    const response = await fetch('/api/crawler/status')
    crawlerStatus.value = await response.json()
  } catch (error) {
    console.error('更新状态失败:', error)
  }
}

const loadLogs = async () => {
  try {
    const response = await fetch('/api/crawler/logs?limit=100')
    const data = await response.json()
    crawlerLogs.value = data.logs || []
    scrollToBottom()
  } catch (error) {
    console.error('加载日志失败:', error)
  }
}

const clearLogs = () => {
  crawlerLogs.value = []
}

const startLogStreaming = () => {
  const eventSource = new EventSource('/api/crawler/logs/stream')
  eventSource.onmessage = (event) => {
    const log = JSON.parse(event.data)
    crawlerLogs.value.push(log)
    scrollToBottom()
  }
  eventSource.onerror = () => {
    eventSource.close()
  }
}

const stopLogStreaming = () => {
  // EventSource会自动关闭
}

const scrollToBottom = () => {
  setTimeout(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  }, 0)
}

const loadCronInfo = async () => {
  try {
    const response = await fetch('/api/cron/info')
    cronInfo.value = await response.json()
  } catch (error) {
    console.error('加载定时任务信息失败:', error)
  }
}

onMounted(() => {
  updateStatus()
  loadLogs()
  loadCronInfo()
  setInterval(updateStatus, 3000)
})
</script>

<style scoped>
.crawler {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-row {
  margin-bottom: 20px;
}

.status-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.status-card.running {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 1px solid #3b82f6;
}

.status-icon {
  font-size: 32px;
}

.status-content {
  flex: 1;
}

.status-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.status-value {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.status-value.success {
  color: #67c23a;
}

.status-value.error {
  color: #f56c6c;
}

.control-panel,
.cron-panel,
.log-panel {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.log-container {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 6px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.6;
  max-height: 400px;
  overflow-y: auto;
}

.log-empty {
  text-align: center;
  color: #666;
  padding: 20px;
}

.log-entry {
  margin-bottom: 4px;
  padding: 4px 8px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.05);
}

.log-time {
  color: #569cd6;
  margin-right: 8px;
}

.log-message {
  color: #d4d4d4;
}

code {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  font-size: 12px;
}

@media (max-width: 768px) {
  .status-card {
    padding: 15px;
  }

  .status-icon {
    font-size: 24px;
  }

  .status-value {
    font-size: 16px;
  }
}
</style>
