<template>
  <div class="admin-layout">
    <!-- Боковое меню -->
    <aside class="sidebar">
      <div class="sidebar__brand">
        <router-link to="/" class="sidebar__brand-link">Поисковый отряд</router-link>
      </div>
      <nav class="sidebar__nav">
        <router-link to="/admin/exhibits" class="sidebar__link">
          <svg class="sidebar__icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6">
            <rect x="2" y="3" width="16" height="13" rx="2"/>
            <path d="M2 8h16"/>
          </svg>
          Экспонаты
        </router-link>
        <router-link to="/admin/articles" class="sidebar__link">
          <svg class="sidebar__icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6">
            <path d="M4 4h12M4 8h12M4 12h8"/>
            <rect x="2" y="2" width="16" height="16" rx="2"/>
          </svg>
          Статьи
        </router-link>
        <router-link v-if="auth.isAdmin" to="/admin/users" class="sidebar__link">
          <svg class="sidebar__icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6">
            <circle cx="8" cy="7" r="3"/>
            <path d="M2 17c0-3.314 2.686-6 6-6s6 2.686 6 6"/>
            <path d="M15 7c1.657 0 3 1.343 3 3M17 17c0-2.209-1.343-4-3-4"/>
          </svg>
          Пользователи
        </router-link>
      </nav>
      <div class="sidebar__footer">
        <div class="sidebar__user">
          <span class="badge" :class="`badge-${auth.role}`">{{ auth.role }}</span>
        </div>
        <button class="btn btn-ghost sidebar__logout" @click="handleLogout">Выйти</button>
      </div>
    </aside>

    <!-- Основная область -->
    <main class="admin-main">
      <header class="admin-topbar">
        <router-link to="/" class="admin-topbar__home">← На сайт</router-link>
        <button class="theme-toggle" @click="toggleTheme" :aria-label="isDark ? 'Светлая тема' : 'Тёмная тема'">
          <span v-if="isDark">☀️</span>
          <span v-else>🌙</span>
        </button>
      </header>
      <div class="admin-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth   = useAuthStore()
const router = useRouter()
const isDark = ref(false)

onMounted(() => {
  isDark.value = document.documentElement.getAttribute('data-theme') === 'dark'
})

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.setAttribute('data-theme', 'dark')
    localStorage.setItem('museum_theme', 'dark')
  } else {
    document.documentElement.removeAttribute('data-theme')
    localStorage.setItem('museum_theme', 'light')
  }
}

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg);
}

/* ─── Sidebar ─────────────────────────────────────────────────────────────── */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar__brand {
  padding: 22px 20px;
  border-bottom: 1px solid var(--color-border);
}
.sidebar__brand-link {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text);
  text-decoration: none;
  display: block;
}
.sidebar__brand-link:hover { color: var(--color-accent); }

.sidebar__nav {
  flex: 1;
  padding: 14px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar__link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 0.9rem;
  transition: all var(--transition);
  text-decoration: none;
}
.sidebar__link:hover {
  background: var(--color-surface-2);
  color: var(--color-text);
}
.sidebar__link.router-link-active {
  background: rgba(139,69,19,0.1);
  color: var(--color-accent);
  font-weight: 600;
}

.sidebar__icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.sidebar__footer {
  padding: 16px 20px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sidebar__user { display: flex; align-items: center; }
.sidebar__logout { width: 100%; justify-content: center; font-size: 0.875rem; }

/* ─── Main ────────────────────────────────────────────────────────────────── */
.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.admin-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 32px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 10;
}
.admin-topbar__home {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  font-weight: 500;
  text-decoration: none;
}
.admin-topbar__home:hover { color: var(--color-accent); }

.theme-toggle {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: 50%;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background var(--transition);
}
.theme-toggle:hover { background: var(--color-border); }

.admin-content { padding: 32px; }
</style>
