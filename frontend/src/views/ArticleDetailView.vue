<template>
  <div>
    <TheNavbar />
    <div v-if="loading" class="loading-spinner">Загрузка...</div>
    <article v-else-if="article" class="article-detail container fade-up">

      <img
        v-if="article.main_image_url"
        :src="apiBase + article.main_image_url"
        :alt="article.title"
        class="article-detail__hero-img"
      />

      <header class="article-detail__header">
        <p class="article-detail__date">{{ formatDate(article.created_at) }}</p>
        <h1>{{ article.title }}</h1>
      </header>

      <div class="article-detail__content" v-html="renderContent(article.content)"></div>

      <section v-if="article.images.length" class="article-detail__gallery">
        <h2>Галерея</h2>
        <div class="gallery-grid">
          <a
            v-for="img in article.images"
            :key="img.id"
            :href="apiBase + img.url"
            target="_blank"
          >
            <img :src="apiBase + img.url" :alt="`Фотография ${img.id}`" />
          </a>
        </div>
      </section>

      <router-link to="/" class="btn btn-ghost" style="margin-top: 40px; display: inline-flex">
        ← Назад
      </router-link>
    </article>
    <div v-else class="loading-spinner">Статья не найдена</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import TheNavbar from '@/components/TheNavbar.vue'
import api from '@/api'

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const route   = useRoute()
const article = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get(`/articles/${route.params.id}`)
    article.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

function renderContent(text) {
  if (!text) return ''
  return text.split('\n\n').map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('')
}
</script>

<style scoped>
.article-detail {
  max-width: 860px;
  padding-top: 56px;
  padding-bottom: 80px;
}
.article-detail__hero-img {
  width: 100%;
  max-height: 480px;
  object-fit: cover;
  border-radius: var(--radius-md);
  margin-bottom: 40px;
}
.article-detail__header { margin-bottom: 32px; }
.article-detail__date { color: var(--color-text-muted); font-size: 0.82rem; margin-bottom: 10px; }
.article-detail__header h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); }
.article-detail__content {
  font-size: 1.05rem;
  line-height: 1.85;
  color: var(--color-text);
}
.article-detail__content :deep(p) { margin-bottom: 1.4em; }

.article-detail__gallery { margin-top: 56px; }
.article-detail__gallery h2 { font-size: 1.35rem; margin-bottom: 20px; }
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 10px;
}
.gallery-grid a img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: var(--radius-sm);
  transition: transform var(--transition);
}
.gallery-grid a:hover img { transform: scale(1.03); }
</style>
