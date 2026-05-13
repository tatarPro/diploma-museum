/**
 * api/index.js
 * Настроенный экземпляр Axios для работы с FastAPI.
 * Базовый URL задаётся через переменную окружения VITE_API_BASE_URL.
 */

import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
})

export default api
