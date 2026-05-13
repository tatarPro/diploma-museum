/**
 * main.js — Точка входа Vue-приложения.
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/styles/theme.css'   // CSS-переменные и темы
import './assets/styles/global.css'  // Базовые стили

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
