<template>
  <div class="admin-page">
    <div class="admin-page__header">
      <h1>Экспонаты</h1>
      <button class="btn btn-primary" @click="openForm()">+ Добавить</button>
    </div>

    <!-- Список -->
    <div v-if="loading" class="loading-spinner">Загрузка…</div>
    <div v-else class="admin-table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th><th>Название</th><th>Фото</th><th>3D модель</th><th>Дата</th><th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="exhibit in exhibits" :key="exhibit.id">
            <td>{{ exhibit.id }}</td>
            <td>{{ exhibit.title }}</td>
            <td>
              <img v-if="exhibit.photo_url" :src="apiBase + exhibit.photo_url" class="thumb" :alt="exhibit.title" />
              <span v-else>—</span>
            </td>
            <td>{{ exhibit.model_url ? '✅' : '—' }}</td>
            <td>{{ formatDate(exhibit.created_at) }}</td>
            <td class="table-actions">
              <button class="btn btn-ghost btn-sm" @click="openForm(exhibit)">✏️</button>
              <button class="btn btn-danger btn-sm" @click="confirmDelete(exhibit)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальная форма -->
    <Teleport to="body">
      <div v-if="showForm" class="modal-backdrop" @click.self="closeForm">
        <div class="modal-box">
          <div class="modal-header">
            <h2>{{ editingId ? 'Редактировать экспонат' : 'Новый экспонат' }}</h2>
            <button class="modal-close" @click="closeForm">✕</button>
          </div>

          <form class="modal-form" @submit.prevent="submitForm">
            <div class="form-group">
              <label>Название *</label>
              <input v-model="form.title" required placeholder="Название экспоната" />
            </div>
            <div class="form-group">
              <label>Описание *</label>
              <textarea v-model="form.description" required placeholder="Подробное описание…"></textarea>
            </div>
            <div class="form-group">
              <label>Главное фото (jpg/png)</label>
              <input type="file" accept="image/*" @change="e => form.photo = e.target.files[0]" />
            </div>
            <div class="form-group">
              <label>3D-модель (.glb)</label>
              <input type="file" accept=".glb,.gltf" @change="e => form.model = e.target.files[0]" />
            </div>
            <div class="form-group">
              <label>Галерея (несколько фото)</label>
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

    <!-- Диалог подтверждения удаления -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null">
        <div class="modal-box modal-box--sm">
          <h2>Подтверждение удаления</h2>
          <p>Вы уверены, что хотите удалить «{{ deleteTarget.title }}»? Это действие необратимо.</p>
          <div class="modal-footer">
            <button class="btn btn-ghost" @click="deleteTarget = null">Отмена</button>
            <button class="btn btn-danger" @click="performDelete" :disabled="submitting">
              {{ submitting ? 'Удаление…' : 'Удалить' }}
            </button>
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

const exhibits    = ref([])
const loading     = ref(true)
const showForm    = ref(false)
const submitting  = ref(false)
const formError   = ref('')
const deleteTarget= ref(null)
const editingId   = ref(null)

const form = ref({
  title: '', description: '', photo: null, model: null, gallery: [],
})

// ─── CRUD ─────────────────────────────────────────────────────────────────

async function fetchExhibits() {
  loading.value = true
  try {
    const { data } = await api.get('/exhibits')
    exhibits.value = data
  } finally {
    loading.value = false
  }
}

function openForm(exhibit = null) {
  editingId.value   = exhibit?.id || null
  form.value        = {
    title:       exhibit?.title       || '',
    description: exhibit?.description || '',
    photo: null, model: null, gallery: [],
  }
  formError.value = ''
  showForm.value  = true
}

function closeForm() {
  showForm.value = false
  editingId.value = null
}

async function submitForm() {
  formError.value  = ''
  submitting.value = true

  try {
    // Формируем FormData вручную — FastAPI принимает multipart/form-data
    const fd = new FormData()
    fd.append('title',       form.value.title)
    fd.append('description', form.value.description)
    if (form.value.photo) fd.append('photo', form.value.photo)
    if (form.value.model) fd.append('model', form.value.model)
    form.value.gallery.forEach(f => fd.append('gallery', f))

    // Важно: явно передаём оба заголовка для multipart + Bearer
    const headers = auth.authHeaders(true)

    if (editingId.value) {
      await api.put(`/exhibits/${editingId.value}`, fd, { headers })
    } else {
      await api.post('/exhibits', fd, { headers })
    }

    closeForm()
    await fetchExhibits()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Ошибка сохранения'
  } finally {
    submitting.value = false
  }
}

function confirmDelete(exhibit) {
  deleteTarget.value = exhibit
}

async function performDelete() {
  submitting.value = true
  try {
    await api.delete(`/exhibits/${deleteTarget.value.id}`, {
      headers: auth.authHeaders(),
    })
    deleteTarget.value = null
    await fetchExhibits()
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка удаления')
  } finally {
    submitting.value = false
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU')
}

onMounted(fetchExhibits)
</script>

<style scoped>
/* Стили используют общие классы из global.css */
.admin-page__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}
.admin-page__header h1 {
  font-size: 1.6rem;
}

.admin-table-wrap {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: auto;
  box-shadow: var(--shadow-sm);
}
.admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}
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

.thumb {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: var(--radius-sm);
}

.table-actions { display: flex; gap: 8px; }
.btn-sm { padding: 6px 12px; font-size: 0.85rem; }

/* ─── Modal ───────────────────────────────────────────────────────────────── */
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
.modal-box--sm { max-width: 420px; padding: 32px; display: flex; flex-direction: column; gap: 16px; }
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px 0;
}
.modal-header h2 { font-size: 1.3rem; }
.modal-close {
  background: none;
  border: none;
  font-size: 1.1rem;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}
.modal-close:hover { background: var(--color-surface-2); }
.modal-form {
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.form-error {
  color: var(--color-danger);
  font-size: 0.88rem;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: rgba(192,57,43,0.1);
  border-radius: var(--radius-sm);
}
</style>
