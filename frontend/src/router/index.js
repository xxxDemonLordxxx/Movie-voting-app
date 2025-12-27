import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import SubmissionForm from '@/views/SubmissionForm.vue'
import SubmissionDetail from '@/views/SubmissionDetail.vue'
import Calendar from '@/views/Calendar.vue'
import AboutUs from '@/views/AboutUs.vue'
import VotingForm from '@/views/VotingForm.vue'
import Polls from '@/views/Polls.vue'
import SubmissionsList from '@/views/SubmissionsList.vue'
import AdminLogin from '@/views/AdminLogin.vue'

const routes = [
  { path: '/', name: 'home', component: HomePage },
  { path: '/submissions/new/:id', name: 'submit', component: SubmissionForm },
  { path: '/submissions/:id', name: 'submission', component: SubmissionDetail },
  { path: '/calendar', name: 'calendar', component: Calendar},
  { path: '/about_us', name: 'about-us', component: AboutUs},
  { path: '/voting/:id', name: 'voting', component: VotingForm},
  { path: '/polls', name: 'polls', component: Polls},
  { path: '/polls/:id', name: 'submissions-list', component: SubmissionsList},
  { path: '/login', name: 'admin-login', component: AdminLogin} 
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router