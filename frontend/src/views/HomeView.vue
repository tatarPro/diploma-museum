<template>
  <div class="home">

    <!-- SECTION: EXHIBITS -->
    <section class="section">
      <h2>🏛 Экспонаты</h2>
      <div class="grid">
        <div v-for="item in exhibits" :key="item.id" class="card" @click="$router.push(`/exhibit/${item.id}`)">
          <img :src="host + item.photo_url" class="card-img" />
          <div class="card-body">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description.substring(0, 60) }}...</p>
          </div>
        </div>
      </div>
      <p v-if="exhibits.length === 0">Нет экспонатов.</p>
    </section>

    <!-- SECTION: ARTICLES -->
    <section class="section">
      <h2>📜 История отряда (Статьи)</h2>
      <div class="grid">
        <div v-for="art in articles" :key="art.id" class="card" @click="$router.push(`/article/${art.id}`)">
          <img :src="host + art.preview_image_url" class="card-img" />
          <div class="card-body">
            <h3>{{ art.title }}</h3>
            <small>{{ new Date(art.created_at).toLocaleDateString() }} | ID Автора: {{ art.author_id }}</small>
          </div>
        </div>
      </div>
      <p v-if="articles.length === 0">Нет статей.</p>
    </section>

    <!-- SECTION: ABOUT US -->
    <section class="section about">
      <h2>ℹ️ О нас</h2>
      <div class="about-content">
        <div class="placeholder-img-large">Главное фото отряда (Placeholder)</div>
        <div class="about-text-block">
          <div class="placeholder-img-small">Фото (Placeholder)</div>
          <p>
            Здесь будет текст истории отряда. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </p>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const exhibits = ref([]);
const articles = ref([]);
const host = 'http://localhost:8000';

onMounted(async () => {
  exhibits.value = (await axios.get(`${host}/exhibits`)).data;
  articles.value = (await axios.get(`${host}/articles`)).data;
});
</script>

<style scoped>
.section { margin-bottom: 60px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; cursor: pointer; transition: 0.2s; }
.card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
.card-img { width: 100%; height: 180px; object-fit: cover; }
.card-body { padding: 15px; }

/* Placeholders */
.placeholder-img-large { width: 100%; height: 300px; background: #ccc; display: flex; align-items: center; justify-content: center; color: #555; margin-bottom: 20px; }
.about-text-block { display: flex; gap: 20px; align-items: flex-start; }
.placeholder-img-small { width: 150px; height: 150px; background: #ddd; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
</style>