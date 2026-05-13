<template>
  <header class="navbar">
    <div class="container navbar__inner">

      <!-- Логотип -->
      <router-link to="/" class="navbar__logo">
          <img src="./pics/nord_logo.jpg">
      </router-link>

      <!-- Навигация (десктоп) -->
      <nav class="navbar__nav">
        <router-link to="/">Главная</router-link>
        <router-link to="/about">О нас</router-link>
        <router-link to="/join">Вступить в отряд</router-link>
        <a href="https://surpk.ru/" target="_blank" rel="noopener noreferrer" class="navbar__external">
          Учебное заведение
          <svg class="external-icon" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 10L10 2M10 2H5M10 2V7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="https://rf-poisk.ru/" target="_blank" rel="noopener noreferrer" class="navbar__external">
          Поисковое движение России
          <svg class="external-icon" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 10L10 2M10 2H5M10 2V7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <router-link v-if="auth.isAuthenticated" to="/admin">Панель управления</router-link>
      </nav>

      <!-- Правая часть -->
      <div class="navbar__actions">
        <button class="theme-toggle" @click="toggleTheme" :aria-label="isDark ? 'Светлая тема' : 'Тёмная тема'">
          <span v-if="isDark">☀️</span>
          <span v-else>🌙</span>
        </button>
        <button v-if="auth.isAuthenticated" class="btn btn-ghost btn-sm" @click="handleLogout">Выйти</button>
        <router-link v-else to="/login" class="btn btn-primary btn-sm">Войти</router-link>
      </div>

      <!-- Бургер (мобильный) -->
      <button class="burger" @click="menuOpen = !menuOpen" :aria-label="menuOpen ? 'Закрыть меню' : 'Открыть меню'">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>
    </div>

    <!-- Мобильное меню -->
    <nav class="mobile-menu" :class="{ 'mobile-menu--open': menuOpen }">
      <router-link to="/" @click="menuOpen = false">Главная</router-link>
      <router-link to="/about" @click="menuOpen = false">О нас</router-link>
      <router-link to="/join" @click="menuOpen = false">Вступить в отряд</router-link>
      <a href="https://surpk.ru/" target="_blank" rel="noopener noreferrer">СПК</a>
      <a href="https://rf-poisk.ru/" target="_blank" rel="noopener noreferrer">Поисковое движение России</a>
      <router-link v-if="auth.isAuthenticated" to="/admin" @click="menuOpen = false">Панель управления</router-link>
      <button v-if="auth.isAuthenticated" class="mobile-menu__btn" @click="handleLogout">Выйти</button>
      <router-link v-else to="/login" class="mobile-menu__btn-link" @click="menuOpen = false">Войти</router-link>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth     = useAuthStore()
const router   = useRouter()
const isDark   = ref(false)
const menuOpen = ref(false)

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
  menuOpen.value = false
  router.push('/')
}
</script>

<style scoped>
.navbar {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.navbar__inner {
  display: flex;
  align-items: center;
  height: 64px;
  gap: 20px;
}

.navbar__logo {
  font-family: var(--font-display);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-text);
  text-decoration: none;
  white-space: nowrap;
  flex-shrink: 0;
  letter-spacing: 0.01em;
}
.navbar__logo:hover { color: var(--color-accent); }

.navbar__nav {
  display: flex;
  align-items: center;
  gap: 18px;
  flex: 1;
}

.navbar__nav a,
.navbar__external {
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 0.875rem;
  transition: color var(--transition);
  text-decoration: none;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
.navbar__nav a.router-link-active,
.navbar__nav a:hover,
.navbar__external:hover {
  color: var(--color-accent);
}

.external-icon {
  width: 10px;
  height: 10px;
  opacity: 0.55;
  flex-shrink: 0;
  margin-top: 1px;
}

.navbar__actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.btn-sm { padding: 7px 16px; font-size: 0.85rem; }

.theme-toggle {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  cursor: pointer;
  transition: background var(--transition);
  flex-shrink: 0;
}
.theme-toggle:hover { background: var(--color-border); }

/* ─── Бургер ──────────────────────────────────────────────────────────────── */
.burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  padding: 6px;
  cursor: pointer;
  margin-left: auto;
  flex-shrink: 0;
}
.burger span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--color-text);
  border-radius: 2px;
  transition: transform 0.25s ease, opacity 0.25s ease;
  transform-origin: center;
}
.burger span.open:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.burger span.open:nth-child(2) { opacity: 0; }
.burger span.open:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

/* ─── Мобильное меню ─────────────────────────────────────────────────────── */
.mobile-menu {
  display: none;
  flex-direction: column;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.32s ease;
}
.mobile-menu--open {
  max-height: 600px;
}
.mobile-menu a,
.mobile-menu__btn,
.mobile-menu__btn-link {
  display: block;
  padding: 13px 24px;
  color: var(--color-text-muted);
  font-size: 0.95rem;
  font-weight: 500;
  border: none;
  border-bottom: 1px solid var(--color-border);
  background: none;
  text-align: left;
  cursor: pointer;
  text-decoration: none;
  font-family: var(--font-body);
  width: 100%;
  transition: background var(--transition), color var(--transition);
}
.mobile-menu a:last-child,
.mobile-menu__btn { border-bottom: none; }
.mobile-menu a.router-link-active { color: var(--color-accent); }
.mobile-menu a:hover,
.mobile-menu__btn:hover,
.mobile-menu__btn-link:hover {
  background: var(--color-surface-2);
  color: var(--color-text);
}

/* ─── Адаптив ─────────────────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .navbar__nav,
  .navbar__actions { display: none; }
  .burger { display: flex; }
  .mobile-menu { display: flex; }
}
</style>
