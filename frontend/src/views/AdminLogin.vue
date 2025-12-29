<template>
  <div class="login-page">
    <h2>Admin Login</h2>
    <form @submit.prevent="handleLogin">
      <input 
        v-model="password" 
        type="password" 
        placeholder="Enter 'meow' password"
      >
      <button type="submit">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    const response = await fetch(`http://localhost:8000/admin/${password.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    const data = await response.json()
    
    if (data.isadmin) {
      localStorage.setItem('isAdmin', 'true')

      // Redirect to main page
      router.push('/')
    } else {
      error.value = 'Access denied'
    }
  } catch (err) {
    error.value = 'Login failed'
  }
}
</script>