<template>
  <div class="home">
    <h1>Экспонаты музея</h1>
    <div class="grid">
      <div v-for="item in exhibits" :key="item.id" class="card" @click="goToDetail(item.id)">
        <img :src="`http://localhost:8000${item.photo_url}`" alt="Exibit photo" class="preview-img" />
        <div class="content">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description.substring(0, 100) }}...</p>
        </div>
      </div>
    </div>
    <div v-if="exhibits.length === 0">Экспонатов пока нет.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const exhibits = ref([]);
const router = useRouter();

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/exhibits');
    exhibits.value = res.data;
  } catch (e) {
    console.error("Ошибка загрузки:", e);
  }
});

const goToDetail = (id) => {
  router.push(`/exhibit/${id}`);
};
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.preview-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
.content {
  padding: 15px;
}
</style>