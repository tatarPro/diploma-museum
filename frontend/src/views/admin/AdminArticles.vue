<template>
  <div class="admin-page">
    <div class="admin-page__header">
      <h1>Статьи / Истории экспедиций</h1>
      <button class="btn btn-primary" @click="openForm()">+ Добавить</button>
    </div>

    <div v-if="loading" class="loading-spinner">Загрузка…</div>
    <div v-else class="admin-table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th><th>Заголовок</th><th>Превью</th><th>Дата</th><th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articles" :key="article.id">
            <td>{{ article.id }}</td>
            <td>{{ article.title }}</td>
            <td>
              <img v-if="article.preview_image_url" :src="apiBase + article.preview_image_url" class="thumb" :alt="article.title" />
              <span v-else>—</span>
            </td>
            <td>{{ formatDate(article.created_at) }}</td>
            <td class="table-actions">
              <button class="btn btn-ghost btn-sm" @click="openForm(article)">✏️</button>
              <button class="btn btn-danger btn-sm" @click="confirmDelete(article)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Форма -->
    <Teleport to="body">
      <div v-if="showForm" class="modal-backdrop" @click.self="closeForm">
        <div class="modal-box modal-box--wide">
          <div class="modal-header">
            <h2>{{ editingId ? 'Редактировать статью' : 'Новая статья' }}</h2>
            <button class="modal-close" @click="closeForm">✕</button>
          </div>
          <form class="modal-form" @submit.prevent="submitForm">
            <div class="form-group">
              <label>Заголовок *</label>
              <input v-model="form.title" required placeholder="Название экспедиции…" />
            </div>
            <div class="form-group">
              <label>Содержание *</label>
              <textarea v-model="form.content" required style="min-height: 200px" placeholder="Текст статьи…"></textarea>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Фото-превью</label>
                <input type="file" accept="image/*" @change="e => form.previewImage = e.target.files[0]" />
              </div>
              <div class="form-group">
                <label>Главное фото</label>
                <input type="file" accept="image/*" @change="e => form.mainImage = e.target.files[0]" />
              </div>
            </div>
            <div class="form-group">
              <label>Галерея</label>
              <input type="file" accept="image/*" multiple @change="e => form.gallery = Array.from(e.target.files)" />
            </div>
            <p v-if="formError" class="form-error">{{ formError }}</p>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="closeForm">Отмена</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Сохранение…' : 'Сохранить' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Подтверждение удаления -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null">
        <div class="modal-box modal-box--sm">
          <h2>Удалить статью?</h2>
          <p>«{{ deleteTarget.title }}» будет удалена без возможности восстановления.</p>
          <div class="modal-footer">
            <button class="btn btn-ghost" @click="deleteTarget = null">Отмена</button>
            <button class="btn btn-danger" @click="performDelete" :disabled="submitting">Удалить</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

const auth    = useAuthStore()
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const articles     = ref([])
const loading      = ref(true)
const showForm     = ref(false)
const submitting   = ref(false)
const formError    = ref('')
const deleteTarget = ref(null)
const editingId    = ref(null)

const form = ref({
  title: '', content: '', previewImage: null, mainImage: null, gallery: [],
})

async function fetchArticles() {
  loading.value = true
  try {
    const { data } = await api.get('/articles')
    articles.value = data
  } finally {
    loading.value = false
  }
}

function openForm(article = null) {
  editingId.value = article?.id || null
  form.value = {
    title:        article?.title   || '',
    content:      article?.content || '',
    previewImage: null, mainImage: null, gallery: [],
  }
  formError.value = ''
  showForm.value  = true
}

function closeForm() { showForm.value = false; editingId.value = null }

async function submitForm() {
  formError.value = ''; submitting.value = true
  try {
    const fd = new FormData()
    fd.append('title',   form.value.title)
    fd.append('content', form.value.content)
    if (form.value.previewImage) fd.append('preview_image', form.value.previewImage)
    if (form.value.mainImage)    fd.append('main_image',    form.value.mainImage)
    form.value.gallery.forEach(f => fd.append('gallery', f))

    const headers = auth.authHeaders(true)
    if (editingId.value) {
      await api.put(`/articles/${editingId.value}`, fd, { headers })
    } else {
      await api.post('/articles', fd, { headers })
    }
    closeForm()
    await fetchArticles()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Ошибка сохранения'
  } finally {
    submitting.value = false
  }
}

function confirmDelete(article) { deleteTarget.value = article }

async function performDelete() {
  submitting.value = true
  try {
    await api.delete(`/articles/${deleteTarget.value.id}`, { headers: auth.authHeaders() })
    deleteTarget.value = null
    await fetchArticles()
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка удаления')
  } finally {
    submitting.value = false
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU')
}

onMounted(fetchArticles)
</script>

<style scoped>
/* Переиспользуем стили из AdminExhibits через global.css */
.admin-page__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}
.admin-page__header h1 { font-size: 1.6rem; }

.admin-table-wrap {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: auto;
  box-shadow: var(--shadow-sm);
}
.admin-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.admin-table th, .admin-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}
.admin-table th {
  font-weight: 600;
  color: var(--color-text-muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--color-surface-2);
}
.admin-table tbody tr:hover { background: var(--color-surface-2); }
.admin-table tbody tr:last-child td { border-bottom: none; }
.thumb { width: 48px; height: 48px; object-fit: cover; border-radius: var(--radius-sm); }
.table-actions { display: flex; gap: 8px; }
.btn-sm { padding: 6px 12px; font-size: 0.85rem; }

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
  backdrop-filter: blur(3px);
}
.modal-box {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}
.modal-box--wide { max-width: 720px; }
.modal-box--sm { max-width: 420px; padding: 32px; display: flex; flex-direction: column; gap: 16px; }
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px 0;
}
.modal-header h2 { font-size: 1.3rem; }
.modal-close {
  background: none; border: none; font-size: 1.1rem;
  color: var(--color-text-muted); cursor: pointer; padding: 4px 8px; border-radius: 4px;
}
.modal-close:hover { background: var(--color-surface-2); }
.modal-form { padding: 24px 28px; display: flex; flex-direction: column; }
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-error {
  color: var(--color-danger);
  font-size: 0.88rem;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: rgba(192,57,43,0.1);
  border-radius: var(--radius-sm);
}
</style>
