<template>
  <div class="keywords">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <h3>🔑 关键词管理</h3>
        <el-tag type="info">{{ keywords.length }} 个分组</el-tag>
      </div>
      <div class="toolbar-right">
        <el-button @click="addGroup" :icon="Plus">添加分组</el-button>
        <el-button type="primary" @click="saveKeywords" :icon="DocumentCopy">保存</el-button>
      </div>
    </div>

    <!-- 使用说明 -->
    <div class="tips">
      <span>💡 每个分组可包含多个关键词</span>
      <span>•</span>
      <span>同组关键词视为同一主题</span>
      <span>•</span>
      <span>使用 <code>!</code> 前缀排除关键词</span>
      <span>•</span>
      <span>每行一个关键词</span>
    </div>

    <!-- 关键词分组网格布局 -->
    <div class="keywords-grid">
      <div
        v-for="(group, index) in keywords"
        :key="index"
        :class="['keyword-card', `color-${(index % 4) + 1}`]"
      >
        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="card-number">{{ index + 1 }}</div>
          <el-input
            v-model="groupTitles[index]"
            placeholder="分组名称"
            size="small"
            class="card-title-input"
          />
          <el-button
            type="danger"
            size="small"
            text
            @click="deleteGroup(index)"
            :icon="Delete"
          />
        </div>

        <!-- 关键词列表 -->
        <div class="keywords-list">
          <el-input
            v-model="keywords[index]"
            type="textarea"
            :rows="8"
            placeholder="输入关键词，每行一个"
            class="keywords-textarea"
            resize="vertical"
          />
        </div>

        <!-- 卡片底部统计 -->
        <div class="card-footer">
          <span class="keyword-count">{{ getKeywordCount(keywords[index]) }} 个关键词</span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <el-empty v-if="keywords.length === 0" description="暂无关键词分组，点击添加分组开始">
      <el-button type="primary" @click="addGroup" :icon="Plus">添加第一个分组</el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAppStore } from '../stores'
import { 
  Plus, 
  Delete, 
  DocumentCopy 
} from '@element-plus/icons-vue'

const appStore = useAppStore()

const keywords = ref([])
const groupTitles = ref([])

const loadKeywords = async () => {
  try {
    const response = await fetch('/api/keywords')
    const data = await response.json()
    
    // 处理分组数据
    if (data.groups && Array.isArray(data.groups)) {
      keywords.value = data.groups.map(group => {
        if (Array.isArray(group)) {
          // 如果是数组，直接join
          return group.join('\n')
        } else if (typeof group === 'object' && group !== null) {
          // 如果是对象（包含required、normal、filter_words），合并所有关键词
          const allWords = []
          if (group.required && Array.isArray(group.required)) {
            allWords.push(...group.required.map(w => w + '+'))
          }
          if (group.normal && Array.isArray(group.normal)) {
            allWords.push(...group.normal)
          }
          if (group.filter_words && Array.isArray(group.filter_words)) {
            allWords.push(...group.filter_words.map(w => w + '!'))
          }
          return allWords.join('\n')
        } else if (typeof group === 'string') {
          return group
        }
        return ''
      })
    } else {
      keywords.value = []
    }
    
    // 处理分组标题 - 生成默认标题
    groupTitles.value = keywords.value.map((_, i) => `分组 ${i + 1}`)
    
    console.log('加载关键词成功:', keywords.value.length, '个分组')
  } catch (error) {
    console.error('加载关键词失败:', error)
    appStore.showMessage('加载关键词失败', 'error')
  }
}

const saveKeywords = async () => {
  try {
    const groups = keywords.value
      .map(text => text.split('\n').map(line => line.trim()).filter(line => line.length > 0))
      .filter(group => group.length > 0)

    if (groups.length === 0) {
      appStore.showMessage('至少需要一个关键词分组', 'warning')
      return
    }

    // 获取对应的分组标题
    const titles = groupTitles.value.slice(0, groups.length)

    const response = await fetch('/api/keywords', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ groups, titles })
    })
    const result = await response.json()
    if (result.success) {
      appStore.showMessage('关键词保存成功', 'success')
    } else {
      appStore.showMessage(result.message || '保存失败', 'error')
    }
  } catch (error) {
    console.error('保存失败:', error)
    appStore.showMessage('保存失败', 'error')
  }
}

const addGroup = async () => {
  keywords.value.push('')
  groupTitles.value.push(`分组 ${keywords.value.length}`)
  
  // 立即保存到文件
  await saveKeywords()
}

const deleteGroup = async (index) => {
  if (confirm('确定要删除这个分组吗？')) {
    keywords.value.splice(index, 1)
    groupTitles.value.splice(index, 1)
    
    // 立即保存到文件
    await saveKeywords()
  }
}

const getKeywordCount = (text) => {
  if (!text) return 0
  return text.split('\n').filter(line => line.trim().length > 0).length
}

onMounted(() => {
  loadKeywords()
})
</script>

<style scoped>
.keywords {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
  gap: 15px;
}

.toolbar-left h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tips {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: #f0f4ff;
  border-bottom: 1px solid #e4e7eb;
  font-size: 13px;
  color: #606266;
  flex-shrink: 0;
  overflow-x: auto;
}

.tips code {
  background: #e4e7eb;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  font-family: monospace;
}

.keywords-grid {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 32px;
  align-content: start;
  grid-auto-flow: row;
  row-gap: 32px;
}

.keyword-card {
  background: white;
  border: 2px solid #e4e7eb;
  border-radius: 12px;
  overflow: visible;
  display: flex;
  flex-direction: column;
  height: fit-content;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
  min-width: 0;
  word-break: break-word;
  position: relative;
  z-index: 1;
}

.keyword-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
  z-index: 10;
}

/* 颜色方案 - 左边框 */
.keyword-card.color-1 {
  border-left: 5px solid #667eea;
}

.keyword-card.color-2 {
  border-left: 5px solid #f56c6c;
}

.keyword-card.color-3 {
  border-left: 5px solid #67c23a;
}

.keyword-card.color-4 {
  border-left: 5px solid #e6a23c;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #f9fafb;
  border-bottom: 1px solid #e4e7eb;
}

.card-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.keyword-card.color-1 .card-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.keyword-card.color-2 .card-number {
  background: linear-gradient(135deg, #f56c6c 0%, #c0392b 100%);
}

.keyword-card.color-3 .card-number {
  background: linear-gradient(135deg, #67c23a 0%, #27ae60 100%);
}

.keyword-card.color-4 .card-number {
  background: linear-gradient(135deg, #e6a23c 0%, #d68910 100%);
}

.card-title-input {
  flex: 1;
}

.card-title-input :deep(.el-input__wrapper) {
  background: white;
  box-shadow: 0 0 0 1px #e4e7eb inset;
}

.keywords-list {
  padding: 0;
}

.keywords-textarea {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.6;
}

.keywords-textarea :deep(.el-textarea__inner) {
  border: none;
  border-radius: 0;
  padding: 12px 16px;
  resize: vertical;
  min-height: 100px;
  width: 100%;
  box-sizing: border-box;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.card-footer {
  padding: 10px 16px;
  background: #f9fafb;
  border-top: 1px solid #e4e7eb;
  font-size: 12px;
  color: #909399;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.keyword-card.color-1 .card-footer {
  background: linear-gradient(to right, rgba(102, 126, 234, 0.05) 0%, #f9fafb 100%);
}

.keyword-card.color-2 .card-footer {
  background: linear-gradient(to right, rgba(245, 108, 108, 0.05) 0%, #f9fafb 100%);
}

.keyword-card.color-3 .card-footer {
  background: linear-gradient(to right, rgba(103, 194, 58, 0.05) 0%, #f9fafb 100%);
}

.keyword-card.color-4 .card-footer {
  background: linear-gradient(to right, rgba(230, 162, 60, 0.05) 0%, #f9fafb 100%);
}

.keyword-count {
  font-weight: 500;
  color: #606266;
}

@media (max-width: 768px) {
  .keywords-grid {
    grid-template-columns: 1fr;
    padding: 16px;
    gap: 16px;
  }
  
  .keyword-card {
    margin-bottom: 0;
  }


  .toolbar {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  .toolbar-left,
  .toolbar-right {
    justify-content: space-between;
  }

  .tips {
    flex-wrap: wrap;
    font-size: 12px;
  }
}
</style>
