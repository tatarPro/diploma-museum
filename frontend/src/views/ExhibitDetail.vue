<template>
  <div v-if="item" class="detail-page">
    <button @click="$router.back()" class="btn" style="margin-bottom: 1rem;">← Назад</button>
    <h1>{{ item.title }}</h1>

    <div ref="canvasContainer" class="canvas-container"></div>

    <div class="info-block">
      <p><strong>Описание:</strong> {{ item.description }}</p>
    </div>

    <!-- Gallery -->
    <div v-if="item.images && item.images.length > 0" class="gallery-section">
      <h3>Фотографии находки</h3>
      <div class="gallery-grid">
        <img v-for="img in item.images" :key="img.url" :src="`http://localhost:8000${img.url}`" class="gallery-img" />
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

const route = useRoute();
const item = ref(null);
const canvasContainer = ref(null);
let scene, camera, renderer, controls;

const initThreeJS = (url) => {
  const width = canvasContainer.value.clientWidth;
  const height = 400;
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xeeeeee);

  camera = new THREE.PerspectiveCamera(45, width/height, 0.1, 100);
  camera.position.set(0, 1, 3);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  canvasContainer.value.appendChild(renderer.domElement);

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5,10,7);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0xffffff, 0.5));

  controls = new OrbitControls(camera, renderer.domElement);

  new GLTFLoader().load(`http://localhost:8000${url}`, (gltf) => {
    const model = gltf.scene;
    // Auto center
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    model.position.sub(center);
    scene.add(model);
  });

  const animate = () => { requestAnimationFrame(animate); renderer.render(scene, camera); controls.update(); };
  animate();
};

onMounted(async () => {
  const res = await axios.get(`http://localhost:8000/exhibits/${route.params.id}`);
  item.value = res.data;
  setTimeout(() => { if(item.value.model_url) initThreeJS(item.value.model_url); }, 100);
});
</script>

<style scoped>
.canvas-container { height: 400px; background: #eee; border-radius: 8px; overflow: hidden; margin-bottom: 20px; }
.gallery-grid { display: flex; flex-wrap: wrap; gap: 10px; }
.gallery-img { height: 150px; border-radius: 4px; border: 1px solid #ddd; }
</style>