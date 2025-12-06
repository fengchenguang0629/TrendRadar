import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../components/Layout.vue'
import Dashboard from '../pages/Dashboard.vue'
import Crawler from '../pages/Crawler.vue'
import Config from '../pages/Config.vue'
import Keywords from '../pages/Keywords.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '新闻看板', icon: 'DataAnalysis' }
      },
      {
        path: 'crawler',
        name: 'Crawler',
        component: Crawler,
        meta: { title: '爬虫控制', icon: 'Rocket' }
      },
      {
        path: 'config',
        name: 'Config',
        component: Config,
        meta: { title: '配置管理', icon: 'Setting' }
      },
      {
        path: 'keywords',
        name: 'Keywords',
        component: Keywords,
        meta: { title: '关键词管理', icon: 'Collection' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
