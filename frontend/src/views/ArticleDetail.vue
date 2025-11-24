<template>
  <div v-if="art" class="article-page">
    <button @click="$router.back()" class="btn">← Назад</button>

    <!-- Header Image -->
    <div class="article-header">
      <img :src="`http://localhost:8000${art.main_image_url}`" class="main-img" />
      <div class="title-overlay">
        <h1>{{ art.title }}</h1>
      </div>
    </div>

    <!-- Metadata -->
    <div class="meta">
      <span>Автор ID: {{ art.author_id }}</span>
      <br>
      <span>{{ new Date(art.created_at).toLocaleDateString() }}</span>
    </div>

    <!-- Content -->
    <div class="content">
      {{ art.content }}
    </div>

    <!-- Bottom Gallery -->
    <div v-if="art.images && art.images.length > 0" class="gallery">
      <h3>Галерея</h3>
      <div class="gallery-grid">
        <img v-for="img in art.images" :key="img.url" :src="`http://localhost:8000${img.url}`" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const art = ref(null);

onMounted(async () => {
  art.value = (await axios.get(`http://localhost:8000/articles/${route.params.id}`)).data;
});
</script>

<style scoped>
.main-img { width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; }
.meta { color: #777; margin: 10px 0; font-size: 0.9rem; }
.content { white-space: pre-wrap; line-height: 1.6; margin-bottom: 30px; }
.gallery-grid img { height: 150px; margin-right: 10px; border-radius: 4px; }
</style>