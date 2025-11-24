import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AdminPanel from '../views/AdminPanel.vue'
import ExhibitDetail from '../views/ExhibitDetail.vue'
import { useAuthStore } from '../stores/auth'
import ArticleDetail from '../views/ArticleDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/article/:id',
      name: 'article',
      component: ArticleDetail
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPanel,
      meta: { requiresAuth: true }
    },
    {
      path: '/exhibit/:id',
      name: 'exhibit',
      component: ExhibitDetail
    }
  ]
})

// Защита админки (если нет токена — перекидываем на логин)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login')
  } else {
    next()
  }
})

export default router