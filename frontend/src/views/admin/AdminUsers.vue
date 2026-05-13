<template>
  <div class="admin-page">
    <div class="admin-page__header">
      <h1>Пользователи</h1>
      <button class="btn btn-primary" @click="showForm = true">+ Добавить модератора</button>
    </div>

    <div v-if="loading" class="loading-spinner">Загрузка…</div>
    <div v-else class="admin-table-wrap">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th><th>Логин</th><th>Роль</th><th>Дата создания</th><th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.login }}</td>
            <td>
              <span class="badge" :class="`badge-${user.role}`">{{ user.role }}</span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <button
                v-if="user.id !== currentUserId"
                class="btn btn-danger btn-sm"
                @click="confirmDelete(user)"
              >🗑️ Удалить</button>
              <span v-else class="badge badge-moderator">Вы</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Форма создания пользователя -->
    <Teleport to="body">
      <div v-if="showForm" class="modal-backdrop" @click.self="closeForm">
        <div class="modal-box">
          <div class="modal-header">
            <h2>Новый пользователь</h2>
            <button class="modal-close" @click="closeForm">✕</button>
          </div>
          <form class="modal-form" @submit.prevent="submitForm">
            <div class="form-group">
              <label>Логин *</label>
              <input v-model="form.login" required placeholder="moderator_ivanov" />
            </div>
            <div class="form-group">
              <label>Пароль *</label>
              <input v-model="form.password" type="password" required placeholder="Минимум 6 символов" minlength="6" />
            </div>
            <div class="form-group">
              <label>Роль</label>
              <select v-model="form.role">
                <option value="moderator">Модератор</option>
                <option value="admin">Администратор</option>
              </select>
            </div>
            <p v-if="formError" class="form-error">{{ formError }}</p>
            <div class="modal-footer">
              <button type="button" class="btn btn-ghost" @click="closeForm">Отмена</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? 'Создание…' : 'Создать' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Диалог удаления -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null">
        <div class="modal-box modal-box--sm">
          <h2>Удалить пользователя?</h2>
          <p>«{{ deleteTarget.login }}» будет удалён. Контент останется в системе.</p>
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
import { ref, onMounted, computed } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import { jwtDecode } from 'jwt-decode'

const auth    = useAuthStore()
const users   = ref([])
const loading = ref(true)
const showForm     = ref(false)
const submitting   = ref(false)
const formError    = ref('')
const deleteTarget = ref(null)

const form = ref({ login: '', password: '', role: 'moderator' })

// Получаем ID текущего пользователя из токена
const currentUserId = computed(() => {
  if (!auth.token) return null
  try { return parseInt(jwtDecode(auth.token).sub) }
  catch { return null }
})

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await api.get('/users', { headers: auth.authHeaders() })
    users.value = data
  } finally {
    loading.value = false
  }
}

function closeForm() {
  showForm.value  = false
  formError.value = ''
  form.value      = { login: '', password: '', role: 'moderator' }
}

async function submitForm() {
  formError.value = ''; submitting.value = true
  try {
    await api.post('/users', form.value, { headers: auth.authHeaders() })
    closeForm()
    await fetchUsers()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Ошибка создания пользователя'
  } finally {
    submitting.value = false
  }
}

function confirmDelete(user) { deleteTarget.value = user }

async function performDelete() {
  submitting.value = true
  try {
    await api.delete(`/users/${deleteTarget.value.id}`, { headers: auth.authHeaders() })
    deleteTarget.value = null
    await fetchUsers()
  } catch (e) {
    alert(e.response?.data?.detail || 'Ошибка удаления')
  } finally {
    submitting.value = false
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

onMounted(fetchUsers)
</script>

<style scoped>
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
  padding: 14px 16px;
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
.btn-sm { padding: 6px 14px; font-size: 0.85rem; }

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
  max-width: 480px;
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
.form-error {
  color: var(--color-danger);
  font-size: 0.88rem;
  margin-bottom: 12px;
  padding: 8px 12px;
  background: rgba(192,57,43,0.1);
  border-radius: var(--radius-sm);
}
</style>
