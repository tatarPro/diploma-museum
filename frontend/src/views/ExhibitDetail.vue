<template>
  <div v-if="item" class="exhibit-detail">
    <button @click="$router.back()" class="btn-back">← В каталог</button>
    <h1 class="title">{{ item.title }}</h1>

    <div class="ar-notice">
      Для просмотра в AR (дополненной реальности) откройте эту страницу со смартфона (Android/Chrome или iOS/WebXR Viewer).
    </div>

    <!-- Контейнер для 3D -->
    <div ref="canvasContainer" class="canvas-container"></div>

    <div class="description-card">
      <h3>Историческая справка</h3>
      <p>{{ item.description }}</p>
    </div>

    <div v-if="item.images && item.images.length" class="gallery">
      <h3>Фотографии находки</h3>
      <div class="gallery-grid">
        <img v-for="img in item.images" :key="img.url" :src="`${apiBase}${img.url}`" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
// ИМПОРТ AR КНОПКИ
import { ARButton } from 'three/examples/jsm/webxr/ARButton.js';

const route = useRoute();
const item = ref(null);
const canvasContainer = ref(null);
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000';

let scene, camera, renderer, controls, arButtonElement;

const initThreeJS = (url) => {
  const width = canvasContainer.value.clientWidth;
  const height = 500;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xe0e0e0);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.01, 100);
  camera.position.set(0, 0.5, 2);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(width, height);
  // ВАЖНО: Включаем поддержку WebXR
  renderer.xr.enabled = true;
  canvasContainer.value.appendChild(renderer.domElement);

  // Добавляем кнопку "START AR" поверх интерфейса
  arButtonElement = ARButton.createButton(renderer);
  document.body.appendChild(arButtonElement);

  // Освещение
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
  scene.add(ambientLight);
  const dirLight = new THREE.DirectionalLight(0xffffff, 1);
  dirLight.position.set(1, 2, 1);
  scene.add(dirLight);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Загрузка модели
  new GLTFLoader().load(`${apiBase}${url}`, (gltf) => {
    const model = gltf.scene;

    // Центруем и масштабируем модель
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());

    // Подгоняем размер, чтобы в AR он не был огромным (приводим к ~30-50 см)
    const maxDim = Math.max(size.x, size.y, size.z);
    if (maxDim > 1) {
      const scale = 0.5 / maxDim;
      model.scale.set(scale, scale, scale);
    }

    model.position.sub(center.multiplyScalar(model.scale.x));

    // Для AR: сдвигаем модель немного вперед от камеры
    model.position.z = -1;

    scene.add(model);
  }, undefined, (error) => {
    console.error('Ошибка загрузки 3D модели:', error);
  });

  // ВАЖНО: Для AR используем setAnimationLoop вместо requestAnimationFrame
  renderer.setAnimationLoop(() => {
    controls.update();
    renderer.render(scene, camera);
  });
};

onMounted(async () => {
  try {
    const res = await axios.get(`${apiBase}/exhibits/${route.params.id}`);
    item.value = res.data;
    setTimeout(() => {
      if(item.value.model_url) initThreeJS(item.value.model_url);
    }, 100);
  } catch (e) {
    console.error("Ошибка:", e);
  }
});

onBeforeUnmount(() => {
  // Убираем AR кнопку при уходе со страницы
  if (arButtonElement && arButtonElement.parentNode) {
    arButtonElement.parentNode.removeChild(arButtonElement);
  }
  if (renderer) renderer.dispose();
});
</script>

<style scoped>
.btn-back { background: transparent; border: 1px solid var(--primary); color: var(--primary); padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-bottom: 1rem; }
.btn-back:hover { background: var(--primary); color: white; }
.title { font-size: 2rem; margin-bottom: 0.5rem; }
.ar-notice { background: #fff3cd; color: #856404; padding: 10px; border-radius: 8px; margin-bottom: 1rem; font-size: 0.9rem; }
.canvas-container { width: 100%; height: 500px; border-radius: 12px; overflow: hidden; margin-bottom: 2rem; position: relative; }
.description-card { background: var(--card-bg); padding: 2rem; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 2rem; line-height: 1.6; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
.gallery-grid img { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 1px solid var(--border); }
</style>