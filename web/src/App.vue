<template>
  <div id="app">
    <router-view />
    <el-message
      v-if="appStore.message"
      :type="appStore.messageType"
      :duration="3000"
      @close="appStore.message = ''"
    >
      {{ appStore.message }}
    </el-message>
  </div>
</template>

<script setup>
import { useAppStore } from './stores'

const appStore = useAppStore()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  width: 100%;
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
  background-color: #f5f7fa;
}
</style>
