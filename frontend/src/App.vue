<template>
  <div :class="['app-container', theme]">
    <header>
      <nav>
        <div class="logo">Поисковый отряд </div>
        <div class="links">
          <router-link to="/">Главная</router-link>
          <router-link v-if="authStore.token" to="/admin">Админка</router-link>
          <button @click="toggleTheme" class="theme-btn">{{ theme === 'light' ? '🌙' : '☀️' }}</button>
          <a v-if="!authStore.token" href="/login">Вход</a>
          <a v-else href="#" @click.prevent="logout">Выход</a>
        </div>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const theme = ref(localStorage.getItem('theme') || 'light');

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  localStorage.setItem('theme', theme.value);
};

const logout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style>
/* CSS VARIABLES */
:root {
  --bg-color: #ffffff;
  --text-color: #000000;
  --primary: #4CAF50;
  --card-bg: #f9f9f9;
  --border: #ddd;
}

.dark {
  --bg-color: #1a1a1a;
  --text-color: #f0f0f0;
  --card-bg: #2d2d2d;
  --border: #444;
}

body { margin: 0; font-family: sans-serif; }
.app-container { background-color: var(--bg-color); color: var(--text-color); min-height: 100vh; transition: 0.3s; }

nav { display: flex; justify-content: space-between; padding: 1rem 2rem; border-bottom: 1px solid var(--border); align-items: center; }
.links a, .theme-btn { margin-left: 15px; color: var(--text-color); text-decoration: none; cursor: pointer; background: none; border: none; font-size: 1.2rem; }
.links a.router-link-active { color: var(--primary); }

main { padding: 2rem; max-width: 1200px; margin: 0 auto; }

.btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
.btn-danger { background: #e74c3c; margin-left: 5px; }
input, textarea, select { width: 100%; padding: 8px; margin-bottom: 10px; background: var(--card-bg); color: var(--text-color); border: 1px solid var(--border); box-sizing: border-box; }
</style>