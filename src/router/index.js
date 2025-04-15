import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import { requireAuth } from '../store/requireAuth';
import Confirm from '../views/Confirm.vue';
import { requireNoAuth } from '@/store/requireNoAuth';

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    beforeEnter: requireAuth
  },
  { 
    path: '/confirm',
    name: 'Confirm',
    component: Confirm
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
