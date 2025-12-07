import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import SuggestionForm from '@/views/SuggestionForm.vue'
import SuggestionDetail from '@/views/SuggestionDetail.vue'
import Calendar from '@/views/Calendar.vue'
import AboutUs from '@/views/AboutUs.vue'
import VotingForm from '@/views/VotingForm.vue'
import Polls from '@/views/Polls.vue'
import SubmissionsList from '@/views/SubmissionsList.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/submissions/new', name: 'submit', component: SuggestionForm },
  { path: '/suggestion/:id', name: 'suggestion-detail', component: SuggestionDetail },
  { path: '/calendar', name: 'calendar', component: Calendar},
  { path: '/about_us', name: 'about-us', component: AboutUs},
  { path: '/voting', name: 'voting', component: VotingForm},
  { path: '/polls', name: 'polls', component: Polls},
  { path: '/polls/:poll_id', name: 'SubmissionsList', component: SubmissionsList},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router