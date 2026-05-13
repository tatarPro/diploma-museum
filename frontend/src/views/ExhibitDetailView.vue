<template>
  <div>
    <TheNavbar />

    <div v-if="loading" class="loading-spinner">Загрузка...</div>

    <div v-else-if="exhibit" class="exhibit-detail container fade-up">
      <!-- Заголовок -->
      <header class="exhibit-detail__header">
        <h1>{{ exhibit.title }}</h1>
        <p class="exhibit-detail__desc">{{ exhibit.description }}</p>
      </header>

      <!-- 3D / AR Вьюер -->
      <section v-if="exhibit.model_url" class="viewer-section">
        <div class="viewer-tabs">
          <button
            :class="['viewer-tab', { active: activeTab === '3d' }]"
            @click="activeTab = '3d'"
          >3D-просмотр</button>
          <button
            :class="['viewer-tab', { active: activeTab === 'ar' }]"
            @click="switchToAR"
          >AR-просмотр</button>
        </div>

        <div class="viewer-container" ref="viewerContainer">
          <canvas ref="canvasEl" class="viewer-canvas"></canvas>

          <div v-if="modelLoading" class="viewer-overlay">
            <div class="viewer-loader">
              <div class="spinner"></div>
              <p>Загрузка 3D-модели...</p>
            </div>
          </div>

          <div ref="arButtonContainer" class="ar-button-container"></div>

          <p v-if="!arSupported && activeTab === 'ar'" class="viewer-notice">
            Ваше устройство или браузер не поддерживает WebXR AR.
            Попробуйте в Chrome на Android-устройстве с поддержкой ARCore.
          </p>
        </div>

        <p class="viewer-hint">Вращайте модель мышью или пальцем</p>
      </section>

      <!-- Фотография (если нет 3D) -->
      <div v-else-if="exhibit.photo_url" class="exhibit-detail__photo">
        <img :src="apiBase + exhibit.photo_url" :alt="exhibit.title" />
      </div>

      <!-- Галерея -->
      <section v-if="exhibit.images.length" class="exhibit-detail__gallery">
        <h2>Галерея</h2>
        <div class="gallery-grid">
          <a
            v-for="img in exhibit.images"
            :key="img.id"
            :href="apiBase + img.url"
            target="_blank"
          >
            <img :src="apiBase + img.url" :alt="`Фотография ${img.id}`" />
          </a>
        </div>
      </section>

      <router-link to="/" class="btn btn-ghost back-btn">← Назад</router-link>
    </div>

    <div v-else class="loading-spinner">Экспонат не найден</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import TheNavbar from '@/components/TheNavbar.vue'
import api from '@/api'

import * as THREE from 'three'
import { GLTFLoader }    from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { ARButton }      from 'three/examples/jsm/webxr/ARButton.js'

const route   = useRoute()
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const exhibit        = ref(null)
const loading        = ref(true)
const modelLoading   = ref(false)
const arSupported    = ref(true)
const activeTab      = ref('3d')

const canvasEl          = ref(null)
const viewerContainer   = ref(null)
const arButtonContainer = ref(null)

let renderer, scene, camera, controls, currentModel

onMounted(async () => {
  try {
    const { data } = await api.get(`/exhibits/${route.params.id}`)
    exhibit.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

watch(
  () => exhibit.value,
  (val) => { if (val?.model_url) setTimeout(() => initThreeJS(), 50) },
)

function initThreeJS() {
  const container = viewerContainer.value
  const canvas    = canvasEl.value
  if (!container || !canvas) return

  const W = container.clientWidth
  const H = container.clientHeight || 480

  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.setSize(W, H)
  renderer.shadowMap.enabled = true
  renderer.xr.enabled = true

  scene = new THREE.Scene()
  set3DBackground()

  camera = new THREE.PerspectiveCamera(50, W / H, 0.01, 1000)
  camera.position.set(0, 1, 3)

  const ambient = new THREE.AmbientLight(0xffffff, 1.2)
  scene.add(ambient)

  const directional = new THREE.DirectionalLight(0xffffff, 2.0)
  directional.position.set(5, 10, 7)
  directional.castShadow = true
  scene.add(directional)

  const fill = new THREE.DirectionalLight(0xfff5e0, 0.6)
  fill.position.set(-5, -3, -5)
  scene.add(fill)

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping  = true
  controls.dampingFactor  = 0.08
  controls.minDistance    = 0.5
  controls.maxDistance    = 20
  controls.enablePan      = false

  setupARButton()
  loadModel(exhibit.value.model_url)

  window.addEventListener('resize', onResize)
  renderer.setAnimationLoop(renderLoop)
}

function set3DBackground() {
  if (scene) scene.background = new THREE.Color(0x1a1714)
}
function clearBackground() {
  if (scene) scene.background = null
}

function setupARButton() {
  if (!navigator.xr) { arSupported.value = false; return }
  navigator.xr.isSessionSupported('immersive-ar').then((supported) => {
    arSupported.value = supported
    if (!supported) return
    const btn = ARButton.createButton(renderer, {
      requiredFeatures: ['hit-test'],
      optionalFeatures: ['dom-overlay'],
    })
    btn.style.cssText = ''
    btn.classList.add('ar-start-btn')
    arButtonContainer.value?.appendChild(btn)
    renderer.xr.addEventListener('sessionstart', clearBackground)
    renderer.xr.addEventListener('sessionend',   set3DBackground)
  })
}

function loadModel(relativePath) {
  if (currentModel) { scene.remove(currentModel); currentModel = null }
  modelLoading.value = true
  const loader = new GLTFLoader()

  loader.load(
    apiBase + relativePath,
    (gltf) => {
      const model = gltf.scene
      scene.add(model)
      currentModel = model

      const box    = new THREE.Box3().setFromObject(model)
      const center = box.getCenter(new THREE.Vector3())
      const size   = box.getSize(new THREE.Vector3())
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale  = 2 / maxDim

      model.scale.setScalar(scale)
      model.position.set(-center.x * scale, -box.min.y * scale, -center.z * scale)

      const fittedSize = maxDim * scale
      camera.position.set(0, fittedSize * 0.6, fittedSize * 2.2)
      controls.target.set(0, fittedSize * 0.3, 0)
      controls.update()

      modelLoading.value = false
    },
    undefined,
    (err) => { console.error('Ошибка загрузки модели:', err); modelLoading.value = false },
  )
}

function renderLoop() {
  if (controls) controls.update()
  if (renderer && scene && camera) renderer.render(scene, camera)
}

function onResize() {
  const container = viewerContainer.value
  if (!container || !renderer || !camera) return
  const W = container.clientWidth
  const H = container.clientHeight || 480
  camera.aspect = W / H
  camera.updateProjectionMatrix()
  renderer.setSize(W, H)
}

function switchToAR() { activeTab.value = 'ar' }

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  if (renderer) { renderer.setAnimationLoop(null); renderer.dispose() }
  if (controls) controls.dispose()
})
</script>

<style scoped>
.exhibit-detail {
  padding-top: 56px;
  padding-bottom: 80px;
  max-width: 1000px;
}

.exhibit-detail__header { margin-bottom: 40px; }
.exhibit-detail__header h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); margin-bottom: 14px; }
.exhibit-detail__desc {
  font-size: 1.05rem;
  color: var(--color-text-muted);
  max-width: 680px;
  line-height: 1.7;
}

/* ─── Viewer ──────────────────────────────────────────────────────────────── */
.viewer-section { margin-bottom: 56px; }

.viewer-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 0;
}
.viewer-tab {
  padding: 10px 22px;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  background: var(--color-surface-2);
  color: var(--color-text-muted);
  font-weight: 600;
  font-size: 0.875rem;
  border: 1px solid var(--color-border);
  border-bottom: none;
  cursor: pointer;
  transition: all var(--transition);
}
.viewer-tab.active {
  background: var(--color-surface);
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.viewer-container {
  position: relative;
  width: 100%;
  height: 480px;
  background: #1a1714;
  border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
}
.viewer-canvas { width: 100% !important; height: 100% !important; display: block; }

.viewer-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(26,23,20,0.85);
  z-index: 10;
}
.viewer-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: #f0ede7;
  font-size: 0.9rem;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255,255,255,0.15);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.viewer-notice {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 14px 24px;
  background: rgba(192,57,43,0.88);
  color: #fff;
  font-size: 0.875rem;
  text-align: center;
  line-height: 1.5;
}

.ar-button-container {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 20;
}
:deep(.ar-start-btn) {
  background: var(--color-accent) !important;
  color: #fff !important;
  border: none !important;
  padding: 11px 26px !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(139,69,19,0.35) !important;
  transition: all 0.25s ease !important;
}
:deep(.ar-start-btn:hover) {
  background: var(--color-accent-2) !important;
  transform: translateY(-1px);
}

.viewer-hint {
  margin-top: 10px;
  font-size: 0.82rem;
  color: var(--color-text-muted);
  text-align: center;
}

/* ─── Photo fallback ──────────────────────────────────────────────────────── */
.exhibit-detail__photo {
  margin-bottom: 48px;
  border-radius: var(--radius-md);
  overflow: hidden;
  max-height: 480px;
}
.exhibit-detail__photo img { width: 100%; object-fit: cover; }

/* ─── Gallery ─────────────────────────────────────────────────────────────── */
.exhibit-detail__gallery { margin-bottom: 48px; }
.exhibit-detail__gallery h2 { font-size: 1.35rem; margin-bottom: 20px; }
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 10px;
}
.gallery-grid a img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: var(--radius-sm);
  transition: transform var(--transition);
}
.gallery-grid a:hover img { transform: scale(1.04); }

.back-btn { margin-top: 8px; }
</style>
