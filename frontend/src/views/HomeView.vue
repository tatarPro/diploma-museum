<template>
  <div class="home-page">
    <TheNavbar />

    <!-- Hero -->
    <section class="hero">
      <div class="hero__bg"></div>
      <div class="container hero__content">
        <p class="hero__eyebrow fade-up">Поисковый отряд "НОРД"</p>
        <h1 class="hero__title fade-up" style="animation-delay:0.1s">Музей памяти и истории</h1>
        <p class="hero__subtitle fade-up" style="animation-delay:0.22s">
          Сохраняем память. Исследуем историю. Чтим героев.
        </p>
        <div class="hero__links fade-up" style="animation-delay:0.34s">
          <router-link to="/about" class="btn btn-primary">О нас</router-link>
          <router-link to="/join" class="btn btn-ghost hero__btn-ghost">Вступить в отряд</router-link>
        </div>
      </div>
    </section>

    <!-- Экспонаты -->
    <section class="section container">
      <h2 class="section__title">Экспонаты</h2>
      <div v-if="loadingExhibits" class="loading-spinner">Загрузка...</div>
      <div v-else-if="exhibits.length === 0" class="empty-state">Экспонаты пока не добавлены</div>
      <div v-else class="grid-cards">
        <router-link
          v-for="exhibit in exhibits"
          :key="exhibit.id"
          :to="`/exhibits/${exhibit.id}`"
          class="card exhibit-card"
        >
          <div class="card__image-wrap">
            <img
              v-if="exhibit.photo_url"
              :src="apiBase + exhibit.photo_url"
              :alt="exhibit.title"
              class="card__image"
            />
            <div v-else class="card__image-placeholder">
              <span class="placeholder-icon"></span>
            </div>
          </div>
          <div class="card__body">
            <h3 class="card__title">{{ exhibit.title }}</h3>
            <p class="card__desc">{{ truncate(exhibit.description, 100) }}</p>
            <span v-if="exhibit.model_url" class="card__ar-badge">AR-просмотр доступен</span>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Статьи -->
    <section class="section section--alt">
      <div class="container">
        <h2 class="section__title">Истории экспедиций</h2>
        <div v-if="loadingArticles" class="loading-spinner">Загрузка...</div>
        <div v-else-if="articles.length === 0" class="empty-state">Статьи пока не добавлены</div>
        <div v-else class="grid-cards">
          <router-link
            v-for="article in articles"
            :key="article.id"
            :to="`/articles/${article.id}`"
            class="card article-card"
          >
            <div class="card__image-wrap">
              <img
                v-if="article.preview_image_url"
                :src="apiBase + article.preview_image_url"
                :alt="article.title"
                class="card__image"
              />
              <div v-else class="card__image-placeholder">
                <span class="placeholder-icon placeholder-icon--article"></span>
              </div>
            </div>
            <div class="card__body">
              <p class="card__date">{{ formatDate(article.created_at) }}</p>
              <h3 class="card__title">{{ article.title }}</h3>
              <p class="card__desc">{{ truncate(article.content, 110) }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container footer__inner">
        <span>© {{ new Date().getFullYear() }} Музей поискового отряда "НОРД"</span>
        <div class="footer__links">
          <router-link to="/about">О нас</router-link>
          <router-link to="/join">Вступить</router-link>
          <a href="https://rf-poisk.ru/" target="_blank" rel="noopener noreferrer">Поисковое движение России</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TheNavbar from '@/components/TheNavbar.vue'
import api from '@/api'

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const exhibits       = ref([])
const articles       = ref([])
const loadingExhibits = ref(true)
const loadingArticles = ref(true)

onMounted(async () => {
  try {
    const [exRes, arRes] = await Promise.all([
      api.get('/exhibits'),
      api.get('/articles'),
    ])
    exhibits.value = exRes.data
    articles.value = arRes.data
  } catch (e) {
    console.error('Ошибка загрузки:', e)
  } finally {
    loadingExhibits.value = false
    loadingArticles.value = false
  }
})

function truncate(text, len) {
  if (!text) return ''
  return text.length > len ? text.slice(0, len) + '…' : text
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}
</script>

<style scoped>
.home-page { min-height: 100vh; display: flex; flex-direction: column; }

/* ─── Hero ────────────────────────────────────────────────────────────────── */
.hero {
  position: relative;
  min-height: 420px;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.hero__bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(100,45,10,0.92) 0%, rgba(180,100,50,0.78) 100%);
  background-color: #3a1f08;
}
.hero__content {
  position: relative;
  z-index: 1;
  color: #fff;
  padding: 88px 24px;
  max-width: 640px;
}
.hero__eyebrow {
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.75;
  margin-bottom: 14px;
}
.hero__title {
  font-size: clamp(2rem, 5vw, 3.4rem);
  margin-bottom: 16px;
  line-height: 1.15;
}
.hero__subtitle {
  font-size: 1.1rem;
  opacity: 0.85;
  margin-bottom: 32px;
  line-height: 1.6;
}
.hero__links { display: flex; gap: 14px; flex-wrap: wrap; }
.hero__btn-ghost {
  border-color: rgba(255,255,255,0.45);
  color: #fff;
}
.hero__btn-ghost:hover {
  background: rgba(255,255,255,0.12);
  color: #fff;
  border-color: rgba(255,255,255,0.7);
}

/* ─── Sections ────────────────────────────────────────────────────────────── */
.section { padding: 72px 24px; flex: 1; }
.section--alt { background: var(--color-surface-2); padding: 72px 0; }
.section__title {
  font-size: 1.7rem;
  margin-bottom: 36px;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--color-accent);
  display: inline-block;
}

/* ─── Cards ──────────────────────────────────────────────────────────────── */
.card__image-wrap {
  aspect-ratio: 16/9;
  overflow: hidden;
  background: var(--color-surface-2);
}
.card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.card:hover .card__image { transform: scale(1.04); }

.card__image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface-2);
}
.placeholder-icon {
  width: 40px;
  height: 40px;
  border: 2px solid var(--color-border);
  border-radius: 6px;
  opacity: 0.4;
}
.placeholder-icon--article {
  border-radius: 2px;
  width: 32px;
  height: 40px;
}

.card__body {
  padding: 18px 20px 22px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.card__date { font-size: 0.78rem; color: var(--color-text-muted); }
.card__title { font-size: 1.05rem; color: var(--color-text); line-height: 1.35; }
.card__desc { font-size: 0.875rem; color: var(--color-text-muted); line-height: 1.55; }
.card__ar-badge {
  display: inline-block;
  background: var(--color-accent);
  color: #fff;
  font-size: 0.72rem;
  padding: 3px 10px;
  border-radius: 99px;
  font-weight: 600;
  width: fit-content;
  letter-spacing: 0.02em;
}

/* ─── Empty / loading ─────────────────────────────────────────────────────── */
.empty-state {
  color: var(--color-text-muted);
  font-size: 0.95rem;
  padding: 40px 0;
}

/* ─── Footer ─────────────────────────────────────────────────────────────── */
.footer {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: 24px;
  margin-top: auto;
}
.footer__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  color: var(--color-text-muted);
  font-size: 0.85rem;
}
.footer__links { display: flex; gap: 20px; }
.footer__links a { color: var(--color-text-muted); font-size: 0.85rem; }
.footer__links a:hover { color: var(--color-accent); }
</style>
