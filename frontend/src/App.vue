<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'

// Восстанавливаем тему из localStorage при загрузке приложения
onMounted(() => {
  const saved = localStorage.getItem('museum_theme')
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark')
  }
})
</script>
