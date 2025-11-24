<template>
  <div class="admin-panel">
    <h1>Панель управления</h1>
    <p>Ваша роль: <strong>{{ authStore.role }}</strong></p>

    <!-- Секция добавления модераторов (Только админ) -->
    <div v-if="authStore.role === 'admin'" class="card">
      <h3>Добавить пользователя</h3>
      <form @submit.prevent="addUser">
        <input v-model="newUser.login" placeholder="Логин" required />
        <input v-model="newUser.password" placeholder="Пароль" type="password" required />
        <select v-model="newUser.role">
            <option value="moderator">Модератор</option>
            <option value="admin">Администратор</option>
        </select>
        <button class="btn" type="submit">Создать</button>
      </form>
    </div>

    <!-- Секция добавления экспоната -->
    <div class="card">
      <h3>Добавить экспонат</h3>
      <form @submit.prevent="addExhibit">
        <input v-model="exhibit.title" placeholder="Название" required />
        <textarea v-model="exhibit.description" placeholder="Описание" required></textarea>

        <label>Фото (Превью):</label>
        <input type="file" @change="handleFileUpload($event, 'photo')" accept="image/*" required />

        <label>3D Модель (.glb):</label>
        <input type="file" @change="handleFileUpload($event, 'model')" accept=".glb,.gltf" required />

        <button class="btn" type="submit">Загрузить экспонат</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();

// Пользователи
const newUser = reactive({ login: '', password: '', role: 'moderator' });

const addUser = async () => {
  try {
    await axios.post('http://localhost:8000/users/', newUser, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    });
    alert('Пользователь создан!');
    newUser.login = ''; newUser.password = '';
  } catch (e) {
    alert('Ошибка: ' + e.response?.data?.detail || e.message);
  }
};

// Экспонаты
const exhibit = reactive({ title: '', description: '' });
let photoFile = null;
let modelFile = null;

const handleFileUpload = (event, type) => {
  if (type === 'photo') photoFile = event.target.files[0];
  if (type === 'model') modelFile = event.target.files[0];
};

const addExhibit = async () => {
  const formData = new FormData();
  formData.append('title', exhibit.title);
  formData.append('description', exhibit.description);
  formData.append('photo', photoFile);
  formData.append('model', modelFile);

  try {
    await axios.post('http://localhost:8000/exhibits/', formData, {
      headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'multipart/form-data'
      }
    });
    alert('Экспонат добавлен!');
    exhibit.title = ''; exhibit.description = '';
  } catch (e) {
    alert('Ошибка загрузки');
  }
};
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
}
select {
    width: 100%; padding: 8px; margin-bottom: 10px;
}
</style>