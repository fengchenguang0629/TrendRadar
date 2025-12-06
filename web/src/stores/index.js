import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const config = ref(null)
  const keywords = ref([])
  const crawlerStatus = ref({
    running: false,
    last_run: null,
    last_status: null,
    log_count: 0
  })
  const crawlerLogs = ref([])

  const isLoading = ref(false)
  const message = ref('')
  const messageType = ref('success')

  const loadConfig = async () => {
    try {
      isLoading.value = true
      const response = await fetch('/api/config')
      config.value = await response.json()
    } catch (error) {
      showMessage('加载配置失败', 'error')
    } finally {
      isLoading.value = false
    }
  }

  const saveConfig = async (newConfig) => {
    try {
      isLoading.value = true
      const response = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig)
      })
      const result = await response.json()
      if (result.success) {
        config.value = newConfig
        showMessage('配置保存成功', 'success')
      } else {
        showMessage(result.message || '保存失败', 'error')
      }
    } catch (error) {
      showMessage('保存配置失败', 'error')
    } finally {
      isLoading.value = false
    }
  }

  const loadKeywords = async () => {
    try {
      const response = await fetch('/api/keywords')
      const data = await response.json()
      keywords.value = data.groups || []
    } catch (error) {
      showMessage('加载关键词失败', 'error')
    }
  }

  const saveKeywords = async (newKeywords) => {
    try {
      isLoading.value = true
      const response = await fetch('/api/keywords', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ groups: newKeywords })
      })
      const result = await response.json()
      if (result.success) {
        keywords.value = newKeywords
        showMessage('关键词保存成功', 'success')
      } else {
        showMessage(result.message || '保存失败', 'error')
      }
    } catch (error) {
      showMessage('保存关键词失败', 'error')
    } finally {
      isLoading.value = false
    }
  }

  const updateCrawlerStatus = async () => {
    try {
      const response = await fetch('/api/crawler/status')
      crawlerStatus.value = await response.json()
    } catch (error) {
      console.error('更新爬虫状态失败:', error)
    }
  }

  const loadCrawlerLogs = async () => {
    try {
      const response = await fetch('/api/crawler/logs?limit=100')
      const data = await response.json()
      crawlerLogs.value = data.logs || []
    } catch (error) {
      console.error('加载日志失败:', error)
    }
  }

  const showMessage = (msg, type = 'success') => {
    message.value = msg
    messageType.value = type
  }

  return {
    config,
    keywords,
    crawlerStatus,
    crawlerLogs,
    isLoading,
    message,
    messageType,
    loadConfig,
    saveConfig,
    loadKeywords,
    saveKeywords,
    updateCrawlerStatus,
    loadCrawlerLogs,
    showMessage
  }
})
