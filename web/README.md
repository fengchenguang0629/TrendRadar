# TrendRadar Web 管理界面

使用 Vue 3 + Element Plus + Vite 构建的现代化Web管理界面。

## 🚀 快速开始

### 开发模式

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:5173
```

### 生产构建

```bash
# 构建项目
npm run build

# 输出到 dist/ 目录
```

## 📁 项目结构

```
web/
├── src/
│   ├── main.js              # 入口文件
│   ├── App.vue              # 根组件
│   ├── components/
│   │   └── Layout.vue       # 布局组件（侧边菜单）
│   ├── pages/
│   │   ├── Dashboard.vue    # 新闻看板
│   │   ├── Crawler.vue      # 爬虫控制
│   │   ├── Config.vue       # 配置管理
│   │   └── Keywords.vue     # 关键词管理
│   ├── router/
│   │   └── index.js         # 路由配置
│   ├── stores/
│   │   └── index.js         # Pinia状态管理
│   └── assets/
├── public/
│   └── index.html           # HTML模板
├── dist/                    # 构建输出
├── package.json
├── vite.config.js
└── build.sh
```

## 🎨 主要特性

### 1. 侧边菜单导航
- 固定侧边栏，菜单项清晰
- 当前页面高亮显示
- 响应式设计

### 2. 新闻看板
- 统计卡片展示关键数据
- 日期树形选择
- 仅显示HTML文件（不显示TXT）
- 在线预览新闻内容
- 支持在新标签页打开

### 3. 爬虫控制
- 实时状态监控
- 手动启动/停止爬虫
- 实时日志流式显示
- 定时任务信息展示

### 4. 配置管理
- 标签页式组织配置
- 爬虫、报告、通知、权重配置
- 实时保存和重置

### 5. 关键词管理
- 分组管理关键词
- 支持添加/删除分组
- 批量编辑关键词

## 🔧 后端API

Flask后端提供以下API接口：

```
GET  /api/config                    # 获取配置
POST /api/config                    # 保存配置
GET  /api/keywords                  # 获取关键词
POST /api/keywords                  # 保存关键词
GET  /api/news/dates                # 获取日期列表
GET  /api/news/files/<date>         # 获取文件列表（仅HTML）
GET  /api/news/content/<date>/<file> # 获取文件内容
GET  /api/stats                     # 获取统计信息
POST /api/crawler/start             # 启动爬虫
POST /api/crawler/stop              # 停止爬虫
GET  /api/crawler/status            # 获取爬虫状态
GET  /api/crawler/logs              # 获取日志
GET  /api/crawler/logs/stream       # 实时日志流
GET  /api/cron/info                 # 获取定时任务信息
```

## 🎯 UI/UX改进

### 相比旧版本的改进：

1. **侧边菜单导航**
   - 更清晰的导航结构
   - 固定菜单，内容区域可滚动
   - 更好的空间利用

2. **新闻看板优化**
   - 只显示HTML文件，隐藏TXT文件
   - 树形日期选择器
   - 更大的预览区域
   - 支持在新标签页打开

3. **现代化设计**
   - Element Plus组件库
   - 统一的配色方案
   - 响应式布局
   - 平滑的过渡动画

4. **更好的交互**
   - 实时状态更新
   - 流式日志显示
   - 表单验证
   - 操作反馈提示

## 📦 依赖

- Vue 3.3+
- Vue Router 4.2+
- Pinia 2.1+
- Element Plus 2.4+
- Vite 4.4+

## 🚀 部署

### Docker部署

```bash
# 构建镜像
docker build -t trendradar-web .

# 运行容器
docker run -p 5000:5000 trendradar-web
```

### 本地部署

```bash
# 构建前端
npm run build

# 启动Flask后端
python3 app.py
```

## 📝 开发指南

### 添加新页面

1. 在 `src/pages/` 创建新的 `.vue` 文件
2. 在 `src/router/index.js` 中添加路由
3. 在 `src/components/Layout.vue` 中添加菜单项

### 修改样式

- 全局样式在 `src/App.vue` 中
- 组件样式使用 `<style scoped>`
- 使用CSS变量保持一致性

### 状态管理

使用Pinia进行状态管理，在 `src/stores/index.js` 中定义。

## 🐛 故障排查

### 前端无法加载

1. 检查Node.js版本：`node --version`
2. 重新安装依赖：`rm -rf node_modules && npm install`
3. 清除缓存：`npm cache clean --force`

### API请求失败

1. 检查Flask后端是否运行
2. 检查CORS配置
3. 查看浏览器控制台错误信息

## 📄 许可证

GPL-3.0
