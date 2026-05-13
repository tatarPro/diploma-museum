/**
 * stores/auth.js
 * Pinia-хранилище для управления аутентификацией.
 * Токен и роль сохраняются в localStorage для сохранения сессии.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  // ─── Состояние ────────────────────────────────────────────────────────────
  const token = ref(localStorage.getItem('museum_token') || null)
  const role  = ref(localStorage.getItem('museum_role')  || null)

  // ─── Геттеры ──────────────────────────────────────────────────────────────
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin         = computed(() => role.value === 'admin')

  // ─── Действия ─────────────────────────────────────────────────────────────

  /**
   * Вход в систему.
   * @param {string} login
   * @param {string} password
   */
  async function login(login, password) {
    const { data } = await axios.post('/api/auth/login', { login, password })
    token.value = data.access_token
    role.value  = data.role
    localStorage.setItem('museum_token', token.value)
    localStorage.setItem('museum_role',  role.value)
  }

  /** Выход из системы — очищает состояние и localStorage. */
  function logout() {
    token.value = null
    role.value  = null
    localStorage.removeItem('museum_token')
    localStorage.removeItem('museum_role')
  }

  /**
   * Возвращает заголовки для защищённых запросов.
   * Используется при отправке multipart/form-data с файлами.
   */
  function authHeaders(multipart = false) {
    const headers = { Authorization: `Bearer ${token.value}` }
    if (multipart) headers['Content-Type'] = 'multipart/form-data'
    return headers
  }

  return { token, role, isAuthenticated, isAdmin, login, logout, authHeaders }
})
