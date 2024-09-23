import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NameAnalysis from '../views/NameAnalysis.vue';
import GlobalStat from '../views/GlobalStat.vue';
import StatsDiversity from '../views/StatsDiversity.vue';
import ContactPage from '../views/ContactPage.vue';
import LoginPage from '../views/LoginPage.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/name-analysis', name: 'NameAnalysis', component: NameAnalysis },
  { path: '/global-stat', name: 'GlobalStat', component: GlobalStat },
  { path: '/stats-diversity', name: 'StatsDiversity', component: StatsDiversity },
  { path: '/contact', name: 'ContactPage', component: ContactPage },
  { path: '/login', name: 'LoginPage', component: LoginPage },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Guard pour vérifier si l'utilisateur est authentifié
router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const loggedIn = localStorage.getItem('user');

  // Empêcher les utilisateurs connectés d'accéder à la page de connexion
  if (to.path === '/login' && loggedIn) {
    return next('/');
  }

  // Si la route nécessite une authentification et que l'utilisateur n'est pas connecté
  const authRequired = !publicPages.includes(to.path);
  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
});

export default router;
