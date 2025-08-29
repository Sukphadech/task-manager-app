import { createRouter, createWebHistory } from 'vue-router'

// import views
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Board from '../views/Board.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/board/:id', name: 'Board', component: Board, props: true },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
