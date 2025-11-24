<template>
  <div class="login-container">
    <div class="card">
      <h2>Вход в систему</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Логин</label>
          <input v-model="username" type="text" required placeholder="Введите логин" />
        </div>
        <div class="form-group">
          <label>Пароль</label>
          <input v-model="password" type="password" required placeholder="Введите пароль" />
        </div>
        <button type="submit" class="btn">Войти</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const error = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  const success = await authStore.login(username.value, password.value);
  if (success) {
    router.push('/admin'); // После входа кидаем в админку
  } else {
    error.value = 'Неверный логин или пароль';
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}
.card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.form-group {
  margin-bottom: 15px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>