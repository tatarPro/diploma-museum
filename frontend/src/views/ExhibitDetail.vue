<template>
  <div class="detail-container" v-if="item">
    <h1>{{ item.title }}</h1>

    <!-- Окно 3D просмотра -->
    <div ref="canvasContainer" class="canvas-container"></div>

    <div class="info">
      <h3>Описание</h3>
      <p>{{ item.description }}</p>
      <p class="date">Добавлено: {{ new Date(item.created_at).toLocaleDateString() }}</p>
    </div>
  </div>
  <div v-else>Загрузка...</div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const route = useRoute();
const item = ref(null);
const canvasContainer = ref(null);

// Three.js переменные
let scene, camera, renderer, controls, model;

const initThreeJS = (modelUrl) => {
  const width = canvasContainer.value.clientWidth;
  const height = 500; // Фиксированная высота

  // Сцена
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf0f0f0);

  // Камера
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 1, 3);

  // Рендерер
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  canvasContainer.value.appendChild(renderer.domElement);

  // Свет
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
  scene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffffff, 1);
  dirLight.position.set(5, 10, 7);
  scene.add(dirLight);

  // Управление (вращение)
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Загрузка модели
  const loader = new GLTFLoader();
  loader.load(`http://localhost:8000${modelUrl}`, (gltf) => {
    model = gltf.scene;
    // Центрирование модели (опционально, но полезно)
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);

    scene.add(model);
  }, undefined, (error) => {
    console.error('Ошибка загрузки модели:', error);
  });

  animate();
};

const animate = () => {
  requestAnimationFrame(animate);
  if (controls) controls.update();
  if (renderer && scene && camera) renderer.render(scene, camera);
};

onMounted(async () => {
  const id = route.params.id;
  try {
    const res = await axios.get(`http://localhost:8000/exhibits/${id}`);
    item.value = res.data;
    // Ждем пока DOM обновится, потом инициируем 3D
    setTimeout(() => {
        if (item.value.model_url) initThreeJS(item.value.model_url);
    }, 100);
  } catch (e) {
    console.error(e);
  }
});

onBeforeUnmount(() => {
    // Очистка ресурсов при уходе со страницы (упрощенно)
    if (renderer) {
        renderer.dispose();
    }
});
</script>

<style scoped>
.canvas-container {
  width: 100%;
  height: 500px;
  background: #eee;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}
</style>