<template>
  <header>
    <nav>
      <div class="logo">Museum SPO</div>
      <div class="links">
        <router-link to="/">Главная</router-link>
        <router-link v-if="!authStore.token" to="/login">Вход</router-link>
        <router-link v-if="authStore.token" to="/admin">Админка</router-link>
        <a v-if="authStore.token" href="#" @click.prevent="logout">Выход</a>
      </div>
    </nav>
  </header>

  <main>
    <router-view />
  </main>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style>
:root {
  --primary-color: #4CAF50; /* Зеленый */
  --text-color: #000;
  --bg-color: #fff;
}

body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  background-color: var(--bg-color);
  color: var(--text-color);
}

nav {
  display: flex;
  justify-content: space-between;
  padding: 1rem 2rem;
  border-bottom: 1px solid #eee;
}

.logo {
  font-weight: bold;
  font-size: 1.2rem;
  color: var(--primary-color);
}

.links a {
  margin-left: 15px;
  text-decoration: none;
  color: var(--text-color);
}

.links a.router-link-active {
  color: var(--primary-color);
}

main {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
}

input, textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
}
</style>