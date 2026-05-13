<template>
  <div class="login-page">
    <div class="login-card card fade-up">
      <div class="login-card__header">
        <div class="login-card__icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
        </div>
        <h1>Вход в систему</h1>
        <p>Панель управления музеем</p>
      </div>

      <form class="login-card__form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="login">Логин</label>
          <input id="login" v-model="form.login" type="text" placeholder="admin" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input id="password" v-model="form.password" type="password" placeholder="••••••••" required autocomplete="current-password" />
        </div>

        <p v-if="error" class="login-error">{{ error }}</p>

        <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <router-link to="/" class="login-back">← На главную</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth   = useAuthStore()
const router = useRouter()
const route  = useRoute()

const form    = ref({ login: '', password: '' })
const error   = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value   = ''
  loading.value = true
  try {
    await auth.login(form.value.login, form.value.password)
    const redirect = route.query.redirect || '/admin'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка входа. Проверьте логин и пароль.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.login-card__header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.login-card__icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(139,69,19,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  margin-bottom: 4px;
}
.login-card__icon-wrap svg {
  width: 26px;
  height: 26px;
}

.login-card__header h1 {
  font-size: 1.55rem;
  color: var(--color-text);
}
.login-card__header p {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.login-card__form { display: flex; flex-direction: column; }

.login-error {
  color: var(--color-danger);
  font-size: 0.875rem;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: rgba(192, 57, 43, 0.1);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(192, 57, 43, 0.25);
}

.login-btn {
  width: 100%;
  justify-content: center;
  padding: 12px;
  font-size: 1rem;
}
.login-btn:disabled { opacity: 0.65; cursor: not-allowed; }

.login-back {
  text-align: center;
  font-size: 0.85rem;
  color: var(--color-text-muted);
}
.login-back:hover { color: var(--color-accent); }
</style>
