import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NameAnalysis from '../views/NameAnalysis.vue'
import GlobalStat from '../views/GlobalStat.vue'
import StatsDiversity from '../views/StatsDiversity.vue'
import ContactPage from '../views/ContactPage.vue'
import LoginPage from '../views/LoginPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/name-analysis', name: 'NameAnalysis', component: NameAnalysis },
  { path: '/global-stat', name: 'GlobalStat', component: GlobalStat },
  { path: '/stats-diversity', name: 'StatsDiversity', component: StatsDiversity },
  { path: '/contact', name: 'ContactPage', component: ContactPage },
  { path: '/login', name: 'LoginPage', component: LoginPage },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
