<template>
  <div class="public-home">
    <div class="hero-banner">
      <h1>Виртуальный музей поискового отряда</h1>
      <p>Прикоснитесь к истории. Исследуйте найденные артефакты в 3D и дополненной реальности.</p>
    </div>

    <section class="museum-section">
      <h2>Экспозиция находок</h2>
      <div class="grid">
        <div v-for="item in exhibits" :key="item.id" class="museum-card" @click="goToExhibit(item.id)">
          <div class="card-image-wrapper">
            <img :src="`${apiBase}${item.photo_url}`" alt="Фото экспоната" />
            <div class="ar-badge" v-if="item.model_url">AR / 3D</div>
          </div>
          <div class="card-info">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description.substring(0, 80) }}...</p>
          </div>
        </div>
      </div>
      <p v-if="!exhibits.length" class="empty-state">Экспонаты загружаются...</p>
    </section>

    <section class="museum-section articles-section">
      <h2>История и экспедиции</h2>
      <div class="grid">
        <div v-for="art in articles" :key="art.id" class="article-card" @click="$router.push(`/article/${art.id}`)">
          <img :src="`${apiBase}${art.preview_image_url}`" alt="Превью" />
          <h3>{{ art.title }}</h3>
          <span class="date">{{ new Date(art.created_at).toLocaleDateString('ru-RU') }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const exhibits = ref([]);
const articles = ref([]);
const router = useRouter();
// Важно: apiBase должен указывать на твой бэкенд
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';

onMounted(async () => {
  try {
    const exRes = await axios.get(`${apiBase}/exhibits`);
    exhibits.value = exRes.data;
    const artRes = await axios.get(`${apiBase}/articles`);
    articles.value = artRes.data;
  } catch (error) {
    console.error("Ошибка загрузки данных", error);
  }
});

const goToExhibit = (id) => {
  router.push(`/exhibit/${id}`);
};
</script>

<style scoped>
.hero-banner {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #2c3e50, #4ca1af);
  color: white;
  border-radius: 12px;
  margin-bottom: 3rem;
}
.hero-banner h1 { font-size: 2.5rem; margin-bottom: 1rem; }
.museum-section { margin-bottom: 4rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 2rem; }
.museum-card, .article-card {
  background: var(--card-bg); border-radius: 12px; overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.3s ease;
}
.museum-card:hover, .article-card:hover { transform: translateY(-10px); }
.card-image-wrapper { position: relative; height: 220px; }
.card-image-wrapper img, .article-card img { width: 100%; height: 100%; object-fit: cover; }
.ar-badge {
  position: absolute; top: 10px; right: 10px; background: rgba(76, 175, 80, 0.9);
  color: white; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem;
}
.card-info { padding: 1.5rem; }
.card-info h3, .article-card h3 { margin: 0 0 0.5rem 0; font-size: 1.2rem; }
.empty-state { text-align: center; color: #7f8c8d; }
.article-card h3 { padding: 1rem 1rem 0; }
.article-card .date { display: block; padding: 0 1rem 1rem; color: #95a5a6; font-size: 0.9rem; }
</style>