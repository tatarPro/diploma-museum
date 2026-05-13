import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // ─── Публичные ──────────────────────────────────────────────────────────
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/exhibits/:id',
    name: 'ExhibitDetail',
    component: () => import('@/views/ExhibitDetailView.vue'),
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: () => import('@/views/ArticleDetailView.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutView.vue'),
  },
  {
    path: '/join',
    name: 'Join',
    component: () => import('@/views/JoinView.vue'),
  },

  // ─── Защищённые (adminPanel) ────────────────────────────────────────────
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/admin/exhibits',
      },
      {
        path: 'exhibits',
        name: 'AdminExhibits',
        component: () => import('@/views/admin/AdminExhibits.vue'),
      },
      {
        path: 'articles',
        name: 'AdminArticles',
        component: () => import('@/views/admin/AdminArticles.vue'),
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/AdminUsers.vue'),
        meta: { requiresAdmin: true }, // Только для admin
      },
    ],
  },

  // ─── Fallback ────────────────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// ─── Navigation Guard ────────────────────────────────────────────────────────
router.beforeEach((to) => {
  const auth = useAuthStore()

  // Требует авторизации
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  // Требует роль admin
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'AdminExhibits' }
  }
})

export default router
