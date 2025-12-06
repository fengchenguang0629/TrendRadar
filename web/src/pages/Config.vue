<template>
  <div class="config">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>⚙️ 配置管理</span>
          <el-space>
            <el-button @click="resetConfig" :icon="Refresh">重置</el-button>
            <el-button type="primary" @click="saveConfig" :icon="DocumentCopy">保存</el-button>
          </el-space>
        </div>
      </template>

      <el-tabs>
        <!-- 爬虫配置 -->
        <el-tab-pane label="🔧 爬虫配置">
          <el-form :model="formData" label-width="150px">
            <el-form-item label="启用爬虫">
              <el-switch v-model="formData.crawler.enable_crawler" />
            </el-form-item>
            <el-form-item label="请求间隔(ms)">
              <el-input-number v-model="formData.crawler.request_interval" :min="100" :step="100" />
            </el-form-item>
            <el-form-item label="使用代理">
              <el-switch v-model="formData.crawler.use_proxy" />
            </el-form-item>
            <el-form-item label="代理地址">
              <el-input v-model="formData.crawler.default_proxy" placeholder="http://127.0.0.1:10086" />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 报告配置 -->
        <el-tab-pane label="📊 报告配置">
          <el-form :model="formData" label-width="150px">
            <el-form-item label="推送模式">
              <el-select v-model="formData.report.mode">
                <el-option label="当日汇总" value="daily" />
                <el-option label="当前榜单" value="current" />
                <el-option label="增量监控" value="incremental" />
              </el-select>
            </el-form-item>
            <el-form-item label="排名高亮阈值">
              <el-input-number v-model="formData.report.rank_threshold" :min="1" :max="50" />
            </el-form-item>
            <el-form-item label="优先按位置排序">
              <el-switch v-model="formData.report.sort_by_position_first" />
            </el-form-item>
            <el-form-item label="每个关键词最大数量">
              <el-input-number v-model="formData.report.max_news_per_keyword" :min="0" />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 通知配置 -->
        <el-tab-pane label="🔔 通知配置">
          <el-form :model="formData" label-width="150px">
            <el-form-item label="启用通知">
              <el-switch v-model="formData.notification.enable_notification" />
            </el-form-item>
            <el-form-item label="飞书URL">
              <el-input v-model="formData.notification.webhooks.feishu_url" type="password" show-password />
            </el-form-item>
            <el-form-item label="钉钉URL">
              <el-input v-model="formData.notification.webhooks.dingtalk_url" type="password" show-password />
            </el-form-item>
            <el-form-item label="企业微信URL">
              <el-input v-model="formData.notification.webhooks.wework_url" type="password" show-password />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 权重配置 -->
        <el-tab-pane label="⚖️ 权重配置">
          <el-form :model="formData" label-width="150px">
            <el-form-item label="排名权重">
              <el-slider v-model="formData.weight.rank_weight" :min="0" :max="1" :step="0.1" />
            </el-form-item>
            <el-form-item label="频次权重">
              <el-slider v-model="formData.weight.frequency_weight" :min="0" :max="1" :step="0.1" />
            </el-form-item>
            <el-form-item label="热度权重">
              <el-slider v-model="formData.weight.hotness_weight" :min="0" :max="1" :step="0.1" />
            </el-form-item>
            <el-alert
              :title="`权重总和: ${(formData.weight.rank_weight + formData.weight.frequency_weight + formData.weight.hotness_weight).toFixed(1)}`"
              type="info"
              :closable="false"
            />
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '../stores'
import { 
  Refresh, 
  DocumentCopy 
} from '@element-plus/icons-vue'

const appStore = useAppStore()

const formData = ref({
  crawler: {},
  report: {},
  notification: { webhooks: {} },
  weight: {}
})

const originalData = ref(null)

const loadConfig = async () => {
  try {
    const response = await fetch('/api/config')
    const data = await response.json()
    formData.value = JSON.parse(JSON.stringify(data))
    originalData.value = JSON.parse(JSON.stringify(data))
  } catch (error) {
    appStore.showMessage('加载配置失败', 'error')
  }
}

const saveConfig = async () => {
  try {
    const response = await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    const result = await response.json()
    if (result.success) {
      appStore.showMessage('配置保存成功', 'success')
      originalData.value = JSON.parse(JSON.stringify(formData.value))
    } else {
      appStore.showMessage(result.message || '保存失败', 'error')
    }
  } catch (error) {
    appStore.showMessage('保存失败', 'error')
  }
}

const resetConfig = () => {
  if (confirm('确定要重置所有修改吗？')) {
    formData.value = JSON.parse(JSON.stringify(originalData.value))
    appStore.showMessage('已重置', 'success')
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.config {
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
</style>
