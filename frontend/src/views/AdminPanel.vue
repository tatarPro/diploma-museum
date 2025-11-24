<template>
  <div class="admin-layout">
    <!-- SIDEBAR -->
    <aside class="sidebar">
      <h3>Меню</h3>
      <ul>
        <li @click="currentTab = 'users'" v-if="authStore.role === 'admin'" :class="{active: currentTab==='users'}">Пользователи</li>
        <li @click="currentTab = 'exhibits'" :class="{active: currentTab==='exhibits'}">Экспонаты</li>
        <li @click="currentTab = 'articles'" :class="{active: currentTab==='articles'}">Статьи</li>
      </ul>
    </aside>

    <!-- CONTENT -->
    <section class="content-area">

      <!-- USERS TAB -->
      <div v-if="currentTab === 'users' && authStore.role === 'admin'">
        <h2>Добавить пользователя</h2>
        <form @submit.prevent="addUser">
          <input v-model="newUser.login" placeholder="Логин" required />
          <input v-model="newUser.password" type="password" placeholder="Пароль" required />
          <select v-model="newUser.role">
            <option value="moderator">Модератор</option>
            <option value="admin">Администратор</option>
          </select>
          <button class="btn" type="submit">Создать</button>
        </form>
      </div>

      <!-- EXHIBITS TAB -->
      <div v-if="currentTab === 'exhibits'">
        <h2>Управление экспонатами</h2>

        <!-- Form -->
        <div class="card form-card">
          <h3>{{ isEditing ? 'Редактировать' : 'Добавить' }} экспонат</h3>
          <form @submit.prevent="submitExhibit">
            <input v-model="exhibitForm.title" placeholder="Название" required />
            <textarea v-model="exhibitForm.description" placeholder="Описание" required></textarea>

            <div v-if="!isEditing">
              <label>Фото превью:</label>
              <input type="file" @change="e => exFiles.photo = e.target.files[0]" accept="image/*" required />
              <label>3D Модель (.glb):</label>
              <input type="file" @change="e => exFiles.model = e.target.files[0]" accept=".glb" required />
              <label>Галерея (доп. фото):</label>
              <input type="file" @change="e => exFiles.gallery = e.target.files" accept="image/*" multiple />
            </div>

            <button class="btn" type="submit">{{ isEditing ? 'Сохранить изменения' : 'Создать' }}</button>
            <button v-if="isEditing" type="button" class="btn btn-danger" @click="cancelEdit">Отмена</button>
          </form>
        </div>

        <!-- List -->
        <h3>Список экспонатов</h3>
        <div v-for="ex in exhibitsList" :key="ex.id" class="item-row">
          <span>{{ ex.title }} (ID: {{ ex.id }})</span>
          <div>
            <button class="btn" @click="startEditExhibit(ex)">Ред.</button>
            <button class="btn btn-danger" @click="deleteItem('exhibits', ex.id)">Удал.</button>
          </div>
        </div>
      </div>

      <!-- ARTICLES TAB -->
      <div v-if="currentTab === 'articles'">
        <h2>Управление статьями</h2>

        <!-- Form -->
        <div class="card form-card">
          <h3>{{ isEditingArt ? 'Редактировать' : 'Добавить' }} статью</h3>
          <form @submit.prevent="submitArticle">
            <input v-model="artForm.title" placeholder="Заголовок" required />
            <textarea v-model="artForm.content" placeholder="Текст статьи" required rows="5"></textarea>

            <div v-if="!isEditingArt">
              <label>Превью (карточка):</label>
              <input type="file" @change="e => artFiles.preview = e.target.files[0]" accept="image/*" required />
              <label>Главное фото (начало):</label>
              <input type="file" @change="e => artFiles.main = e.target.files[0]" accept="image/*" required />
              <label>Фото в конце (галерея):</label>
              <input type="file" @change="e => artFiles.gallery = e.target.files" accept="image/*" multiple />
            </div>

            <button class="btn" type="submit">{{ isEditingArt ? 'Сохранить' : 'Опубликовать' }}</button>
            <button v-if="isEditingArt" type="button" class="btn btn-danger" @click="cancelEditArt">Отмена</button>
          </form>
        </div>

        <!-- List -->
        <h3>Список статей</h3>
        <div v-for="art in articlesList" :key="art.id" class="item-row">
          <span>{{ art.title }}</span>
          <div>
            <button class="btn" @click="startEditArt(art)">Ред.</button>
            <button class="btn btn-danger" @click="deleteItem('articles', art.id)">Удал.</button>
          </div>
        </div>
      </div>

    </section>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const currentTab = ref('exhibits');
const api = 'http://localhost:8000';

// Вспомогательная функция для получения заголовков (чтобы токен всегда был свежим)
const getAuthHeader = () => {
  return { Authorization: `Bearer ${authStore.token}` };
};

// Вспомогательная функция для заголовков с файлами
const getFileConfig = () => {
  return {
    headers: {
      Authorization: `Bearer ${authStore.token}`,
      'Content-Type': 'multipart/form-data'
    }
  };
};

// Data Lists
const exhibitsList = ref([]);
const articlesList = ref([]);

// --- USERS ---
const newUser = reactive({ login: '', password: '', role: 'moderator' });
const addUser = async () => {
  try {
    // Здесь передаем headers правильно
    await axios.post(`${api}/users/`, newUser, { headers: getAuthHeader() });
    alert('Пользователь создан!');
    newUser.login = ''; newUser.password = '';
  } catch (e) {
    console.error(e);
    alert('Ошибка создания пользователя: ' + (e.response?.data?.detail || e.message));
  }
};

// --- EXHIBITS LOGIC ---
const exhibitForm = reactive({ id: null, title: '', description: '' });
const exFiles = reactive({ photo: null, model: null, gallery: null });
const isEditing = ref(false);

const loadExhibits = async () => {
  try {
    exhibitsList.value = (await axios.get(`${api}/exhibits`)).data;
  } catch (e) { console.error(e); }
};

const submitExhibit = async () => {
  const formData = new FormData();
  formData.append('title', exhibitForm.title);
  formData.append('description', exhibitForm.description);

  try {
    if (isEditing.value) {
      // Редактирование (PUT)
      // Примечание: FastAPI Form(...) ожидает данные формы, поэтому отправляем formData
      // Заголовки для FormData нужны правильные
      await axios.put(`${api}/exhibits/${exhibitForm.id}`, formData, {
         headers: getAuthHeader() // Axios сам поставит multipart boundary для formData
      });
      alert('Экспонат обновлен!');
    } else {
      // Создание (POST) с файлами
      if (exFiles.photo) formData.append('photo', exFiles.photo);
      if (exFiles.model) formData.append('model', exFiles.model);
      if (exFiles.gallery) {
        for(let i=0; i<exFiles.gallery.length; i++) formData.append('gallery', exFiles.gallery[i]);
      }

      // ИСПРАВЛЕННАЯ ЧАСТЬ:
      await axios.post(`${api}/exhibits/`, formData, getFileConfig());
      alert('Экспонат создан!');
    }
    resetExForm();
    loadExhibits();
  } catch (e) {
    console.error(e);
    alert('Ошибка: ' + (e.response?.data?.detail || e.message));
  }
};

const startEditExhibit = (item) => {
  isEditing.value = true;
  exhibitForm.id = item.id;
  exhibitForm.title = item.title;
  exhibitForm.description = item.description;
  // Файлы при редактировании пока не трогаем, чтобы не усложнять курсовую
};

const resetExForm = () => {
  isEditing.value = false;
  exhibitForm.title = '';
  exhibitForm.description = '';
  exFiles.photo = null;
  exFiles.model = null;
  exFiles.gallery = null;
  // Сброс input type=file (костыль через поиск элемента, но рабочий)
  document.querySelectorAll('input[type="file"]').forEach(el => el.value = '');
};

// --- ARTICLES LOGIC ---
const artForm = reactive({ id: null, title: '', content: '' });
const artFiles = reactive({ preview: null, main: null, gallery: null });
const isEditingArt = ref(false);

const loadArticles = async () => {
  try {
    articlesList.value = (await axios.get(`${api}/articles`)).data;
  } catch (e) { console.error(e); }
};

const submitArticle = async () => {
  const formData = new FormData();
  formData.append('title', artForm.title);
  formData.append('content', artForm.content);

  try {
    if (isEditingArt.value) {
      // Редактирование
      await axios.put(`${api}/articles/${artForm.id}`, formData, { headers: getAuthHeader() });
      alert('Статья обновлена!');
    } else {
      // Создание
      if (artFiles.preview) formData.append('preview', artFiles.preview);
      if (artFiles.main) formData.append('main_img', artFiles.main);
      if (artFiles.gallery) {
        for(let i=0; i<artFiles.gallery.length; i++) formData.append('gallery', artFiles.gallery[i]);
      }

      // ИСПРАВЛЕННАЯ ЧАСТЬ:
      await axios.post(`${api}/articles/`, formData, getFileConfig());
      alert('Статья опубликована!');
    }
    resetArtForm();
    loadArticles();
  } catch (e) {
    console.error(e);
    alert('Ошибка: ' + (e.response?.data?.detail || e.message));
  }
};

const startEditArt = (item) => {
  isEditingArt.value = true;
  artForm.id = item.id;
  artForm.title = item.title;
  artForm.content = item.content;
};

const resetArtForm = () => {
  isEditingArt.value = false;
  artForm.title = '';
  artForm.content = '';
  artFiles.preview = null;
  artFiles.main = null;
  artFiles.gallery = null;
  document.querySelectorAll('input[type="file"]').forEach(el => el.value = '');
};

// --- COMMON ---
const deleteItem = async (type, id) => {
  if(!confirm('Удалить эту запись?')) return;
  try {
    await axios.delete(`${api}/${type}/${id}`, { headers: getAuthHeader() });
    if (type === 'exhibits') loadExhibits();
    if (type === 'articles') loadArticles();
  } catch (e) {
    alert('Ошибка удаления');
  }
};

const cancelEdit = resetExForm;
const cancelEditArt = resetArtForm;

watch(currentTab, (val) => {
  if (val === 'exhibits') loadExhibits();
  if (val === 'articles') loadArticles();
}, { immediate: true });
</script>

<style scoped>
.admin-layout { display: flex; gap: 20px; }
.sidebar { width: 250px; background: var(--card-bg); padding: 20px; border-right: 1px solid var(--border); height: 80vh; }
.sidebar ul { list-style: none; padding: 0; }
.sidebar li { padding: 10px; cursor: pointer; border-radius: 4px; margin-bottom: 5px; }
.sidebar li:hover, .sidebar li.active { background: var(--primary); color: white; }
.content-area { flex-grow: 1; }
.item-row { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid var(--border); align-items: center; }
.form-card { background: var(--card-bg); padding: 20px; border: 1px solid var(--border); margin-bottom: 20px; }
</style>