import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import SuggestionForm from '@/views/SuggestionForm.vue'
import SuggestionDetail from '@/views/SuggestionDetail.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/suggest', name: 'suggest', component: SuggestionForm },
  { path: '/suggestion/:id', name: 'suggestion-detail', component: SuggestionDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router