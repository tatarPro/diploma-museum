# 🔍 Музей Поискового Отряда
### Единая информационная система с элементами дополненной реальности

---

## Структура проекта

```
museum_project/
├── backend/
│   ├── main.py          # FastAPI приложение (все эндпоинты)
│   ├── models.py        # SQLAlchemy ORM модели
│   ├── schemas.py       # Pydantic схемы
│   ├── auth.py          # JWT + bcrypt утилиты
│   ├── database.py      # Подключение к MySQL
│   ├── requirements.txt
│   └── static/          # Загруженные файлы (создаётся автоматически)
│       ├── images/
│       └── models/
└── frontend/
    ├── src/
    │   ├── views/
    │   │   ├── HomeView.vue           # Главная страница
    │   │   ├── LoginView.vue          # Страница входа
    │   │   ├── ExhibitDetailView.vue  # Детальная страница + Three.js AR
    │   │   ├── ArticleDetailView.vue  # Детальная страница статьи
    │   │   └── admin/
    │   │       ├── AdminLayout.vue    # Макет admin-панели
    │   │       ├── AdminExhibits.vue  # CRUD экспонатов
    │   │       ├── AdminArticles.vue  # CRUD статей
    │   │       └── AdminUsers.vue     # CRUD пользователей (admin only)
    │   ├── stores/auth.js             # Pinia хранилище
    │   ├── router/index.js            # Vue Router
    │   ├── api/index.js               # Axios instance
    │   ├── components/TheNavbar.vue   # Навигация + тема
    │   └── assets/styles/
    │       ├── theme.css              # CSS переменные (светлая/тёмная тема)
    │       └── global.css             # Базовые стили
    ├── vite.config.js
    ├── package.json
    └── .env
```

---

## 🚀 Запуск бэкенда

### 1. Создать БД MySQL
```sql
CREATE DATABASE museum_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Настроить подключение
Отредактировать `database.py`:
```python
DATABASE_URL = "mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/museum_db"
```

### 3. Установить зависимости и запустить
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Создать первого администратора
```bash
curl -X POST http://localhost:8000/init-admin
# Логин: admin  |  Пароль: admin123
```

Документация API доступна на: `http://localhost:8000/docs`

---

## 🚀 Запуск фронтенда

```bash
cd frontend
npm install
npm run dev
# Открыть: http://localhost:5173
```

---

## 🥽 Дополненная реальность (AR)

- Страница экспоната (`/exhibits/:id`) автоматически загружает `.glb` модель в Three.js сцену.
- Вращение мышью/пальцем через OrbitControls.
- Кнопка **AR-просмотр** появляется только на совместимых устройствах (Android + Chrome + ARCore).
- Требуется HTTPS для WebXR в продакшне.

---

## 🔐 Роли и права

| Действие                  | admin | moderator |
|---------------------------|:-----:|:---------:|
| Просмотр контента         | ✅    | ✅         |
| Создать/редактировать контент | ✅ | ✅       |
| Удалить контент           | ✅    | ✅         |
| Управление пользователями | ✅    | ❌         |

---

## 📦 Технологический стек

**Бэкенд:** Python 3.11+, FastAPI, SQLAlchemy 2.0, MySQL, JWT, bcrypt  
**Фронтенд:** Vue 3 (Composition API), Vite, Pinia, Vue Router, Axios  
**3D / AR:** Three.js r165, GLTFLoader, OrbitControls, WebXR ARButton





python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

